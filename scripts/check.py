#!/usr/bin/env python3
"""writing-craft checker: mechanical checks by genre and language.

The markers, thresholds, settings, and claim-ladder words are read from the
skill's reference files (references/patterns.md, genre-*.md, lang-*.md), so
each pattern stays defined in one place. Standard library only; no network,
no model calls.

Subcommands:
  scan FILE     catalog markers, built-in counters, placeholders, [NEED: ...]
                markers, and (with --source) numbers, dates, phone numbers,
                URLs, codes, and ladder words that are not in the source.
  compare A B   preservation check of B against original A (uses
                aiw_validate.py when present) plus the same fact comparison.

Script hits are candidates. The skill's guards still decide what is a finding.
"""

import argparse
import datetime
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
REFS = os.path.join(SKILL, "references")

LEVELS = {"off": 0, "relaxed": 1, "on": 2, "extra": 3}
DEFAULT_COLUMN = {"cv": "default", "science": "discussion", "prose": "blog"}
TIER_ORDER = {"F": 0, "P0": 1, "P1": 2, "P2": 3}


# ---------------------------------------------------------------------------
# Reading the reference files

class Entry:
    def __init__(self, eid, name):
        self.id = eid
        self.name = name
        self.tier = "P2"
        self.weak = False
        self.checks = {"en": [], "de": []}
        self.thresholds = {}  # lang or "*" -> (count, unit, size)


def parse_catalog(path=os.path.join(REFS, "patterns.md")):
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    entries = {}
    current = None
    for line in text.splitlines():
        m = re.match(r"^### ([A-Z]\d+) · (.+)$", line)
        if m:
            current = Entry(m.group(1), m.group(2).strip())
            entries[current.id] = current
            continue
        m = re.match(r"^\| \d+ \| ([A-Z]\d+) \| [^|]+\| ([^|]+)\| ([^|]*)\|", line)
        if m:
            eid = m.group(1)
            entry = entries.setdefault(eid, Entry(eid, ""))
            entry.tier = m.group(2).strip().split()[0]
            entry.weak = m.group(3).strip() == "yes"
            continue
        if current is None:
            continue
        m = re.match(r"^Check \((en|de)\): (.+)$", line)
        if m:
            current.checks[m.group(1)] = compile_items(m.group(2))
            continue
        m = re.match(r"^Threshold(?: \((en|de)\))?: (\d+) per (text|paragraph|([\d,]+) words)\s*$", line)
        if m:
            size = int(m.group(4).replace(",", "")) if m.group(4) else None
            unit = "words" if size else m.group(3)
            current.thresholds[m.group(1) or "*"] = (int(m.group(2)), unit, size)
    # Index rows come before the entries; re-read tiers for entries created later.
    for line in text.splitlines():
        m = re.match(r"^\| \d+ \| ([A-Z]\d+) \| [^|]+\| ([^|]+)\| ([^|]*)\|", line)
        if m and m.group(1) in entries:
            entries[m.group(1)].tier = m.group(2).strip().split()[0]
            entries[m.group(1)].weak = m.group(3).strip() == "yes"
    return entries


SENTENCE_START = (r"(?:^|(?<=[.!?:])[ \t]+|(?<=[.!?:][\"'”“»«])[ \t]+)"
                  r"[ \t]*(?:[-*•+][ \t]+|\d+[.)][ \t]+|>[ \t]*)?")


def compile_items(spec):
    items = []
    for raw in spec.split(" | "):
        raw = raw.strip()
        if not raw:
            continue
        density = False
        if raw.startswith("~~"):
            density, raw = "only", raw[2:]
        elif raw.startswith("~"):
            density, raw = True, raw[1:]
        if raw.startswith("re:"):
            source = raw[3:]
            if source.startswith("^"):
                source = SENTENCE_START + source[1:]
        else:
            start = raw.startswith("^")
            if start:
                raw = raw[1:]
            parts = [p.strip() for p in raw.split("…")]
            pieces = []
            for part in parts:
                stem = part.endswith("*")
                if stem:
                    part = part[:-1]
                piece = re.escape(part)
                if part and re.match(r"\w", part[0]):
                    piece = r"\b" + piece
                if stem:
                    piece += r"\w*"
                elif part and re.match(r"\w", part[-1]):
                    piece += r"\b"
                pieces.append(piece)
            source = r"[^.!?\n]{0,100}?".join(pieces)
            if start:
                source = SENTENCE_START + source
        try:
            items.append((re.compile(source, re.IGNORECASE | re.MULTILINE), density, raw))
        except re.error as err:
            sys.stderr.write("check.py: bad marker %r in catalog: %s\n" % (raw, err))
    return items


def parse_settings(path):
    """Return {column: {id: level}} from the settings table of a genre or language file."""
    table = {}
    if not os.path.exists(path):
        return table
    columns = None
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()
    for line in lines:
        if line.startswith("| ID |"):
            columns = [c.strip() for c in line.strip("|").split("|")]
            continue
        if columns and line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if not re.match(r"^[A-Z]\d+[a-z]?$", cells[0]):
                continue
            for col, cell in zip(columns[1:], cells[1:]):
                word = cell.split()[0].lower() if cell else ""
                if word == "partial":
                    word = "on"
                if word in LEVELS:
                    table.setdefault(col.lower(), {})[cells[0]] = word
        elif columns and not line.startswith("|"):
            columns = None
    return table


def parse_upgrade_words(genre):
    words = {"en": [], "de": []}
    names = [genre] if genre else ["cv", "science", "prose"]
    for name in names:
        path = os.path.join(REFS, "genre-%s.md" % name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().splitlines()
        for line in lines:
            m = re.match(r"^Upgrade words \((en|de)\): (.+)$", line.strip())
            if m:
                words[m.group(1)] += [w.strip() for w in m.group(2).split("|") if w.strip()]
    return words


class Settings:
    def __init__(self, genre, column, lang, strict=False, gentle=False, entries=None):
        self.genre_table = {}
        if genre:
            table = parse_settings(os.path.join(REFS, "genre-%s.md" % genre))
            if column not in table and table:
                raise SystemExit("check.py: unknown section or type %r for genre %s; choose one of: %s"
                                 % (column, genre, ", ".join(table)))
            self.genre_table = table.get(column, {})
        lang_table = parse_settings(os.path.join(REFS, "lang-%s.md" % lang))
        self.lang_table = lang_table.get("setting", {})
        self.strict = strict
        self.gentle = gentle
        self.entries = entries or {}

    def _lookup(self, table, eid):
        if eid in table:
            return table[eid]
        base = re.sub(r"[a-z]$", "", eid)
        if base in table:
            return table[base]
        subs = [v for k, v in table.items() if re.sub(r"[a-z]$", "", k) == eid and k != eid]
        if subs:
            return max(subs, key=lambda v: LEVELS[v])
        return None

    def level(self, eid):
        base = re.sub(r"[a-z]$", "", eid)
        if base.startswith("F"):
            return "on"
        value = self._lookup(self.genre_table, eid) or "on"
        lang = self._lookup(self.lang_table, eid)
        if lang == "off":
            value = "off"
        elif lang == "relaxed" and LEVELS[value] > LEVELS["relaxed"]:
            value = "relaxed"
        entry = self.entries.get(base)
        if self.gentle and entry and entry.tier == "P2" and value in ("on", "extra"):
            value = "relaxed"
        if self.strict and value == "relaxed":
            value = "on"
        return value


# ---------------------------------------------------------------------------
# Text helpers

GERMAN_WORDS = set("der die das und nicht ist mit für dass ein eine ich wir sie auch auf den dem des zu im von bei wird werden sind".split())
ENGLISH_WORDS = set("the and of to is with for that a an i we you it this on in are be was were by".split())


def detect_language(text):
    words = re.findall(r"[A-Za-zÄÖÜäöüß]+", text.lower())
    de = sum(1 for w in words if w in GERMAN_WORDS) + 2 * len(re.findall(r"[äöüß]", text.lower()))
    en = sum(1 for w in words if w in ENGLISH_WORDS)
    return "de" if de > en else "en"


def blank(text, start, end):
    return text[:start] + re.sub(r"[^\n]", " ", text[start:end]) + text[end:]


FENCE = r"^[ \t]{0,3}(`{3,}|~{3,})[^\n]*\n.*?(?:^[ \t]{0,3}\1[ \t]*$|\Z)"


def mask_code(text):
    """Blank fenced code and inline code, keeping offsets."""
    out = text
    for m in re.finditer(FENCE, out, re.MULTILINE | re.DOTALL):
        out = blank(out, m.start(), m.end())
    for m in re.finditer(r"`[^`\n]+`", out):
        out = blank(out, m.start(), m.end())
    return out


def mask_protected(text):
    """Blank code, URLs, blockquotes, and quoted spans, keeping offsets."""
    out = text
    for pattern in [r"^[ \t]{0,3}(`{3,}|~{3,})[^\n]*\n.*?(?:^[ \t]{0,3}\1[ \t]*$|\Z)",
                    r"`[^`\n]+`",
                    r"https?://\S+|www\.\S+",
                    r"<!--.*?-->",
                    r"^[ \t]*>[^\n]*(?:\n[ \t]*>[^\n]*)+",
                    r"\"[^\"\n]{1,300}\"", r"“[^”\n]{1,300}”", r"„[^“\n]{1,300}“",
                    r"»[^«\n]{1,300}«", r"«[^»\n]{1,300}»"]:
        flags = re.MULTILINE | re.DOTALL if pattern.startswith("^[ \\t]{0,3}(`") else re.MULTILINE
        for m in re.finditer(pattern, out, flags):
            out = blank(out, m.start(), m.end())
    return out


def line_col(text, offset):
    line = text.count("\n", 0, offset) + 1
    col = offset - (text.rfind("\n", 0, offset) + 1) + 1
    return line, col


def paragraphs(text):
    spans = []
    for m in re.finditer(r"(?:[^\n]|\n(?![ \t]*\n))+", text):
        if m.group(0).strip():
            spans.append((m.start(), m.end()))
    return spans


def paragraph_index(paras, offset):
    for i, (a, b) in enumerate(paras):
        if a <= offset < b:
            return i
    return len(paras) - 1 if paras else 0


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+|\n\s*\n", text) if len(s.strip()) > 5]


def word_count(text):
    return len(re.findall(r"\S+", text))


# ---------------------------------------------------------------------------
# Facts: numbers, dates, phones, URLs, codes

MONTHS = {
    "jan": 1, "january": 1, "januar": 1, "jänner": 1, "feb": 2, "february": 2, "februar": 2,
    "mar": 3, "march": 3, "mär": 3, "märz": 3, "mrz": 3, "apr": 4, "april": 4, "may": 5, "mai": 5,
    "jun": 6, "june": 6, "juni": 6, "jul": 7, "july": 7, "juli": 7, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9, "oct": 10, "october": 10, "okt": 10, "oktober": 10,
    "nov": 11, "november": 11, "dec": 12, "december": 12, "dez": 12, "dezember": 12,
}
MONTH_RE = "|".join(sorted((re.escape(k) for k in MONTHS), key=len, reverse=True))
SPELLED = {
    "en": {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
           "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
           "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
           "forty": 40, "fifty": 50, "hundred": 100, "thousand": 1000, "million": 1000000},
    "de": {"zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9,
           "zehn": 10, "elf": 11, "zwölf": 12, "zwanzig": 20, "dreißig": 30, "vierzig": 40,
           "fünfzig": 50, "hundert": 100, "tausend": 1000},
}
SCALES = {"k": 1e3, "tsd": 1e3, "tsd.": 1e3, "thousand": 1e3, "tausend": 1e3, "m": 1e6, "mio": 1e6,
          "mio.": 1e6, "million": 1e6, "millionen": 1e6, "mn": 1e6, "bn": 1e9, "b": 1e9, "mrd": 1e9,
          "mrd.": 1e9, "billion": 1e9, "milliarden": 1e9}
REFERENCE_WORDS = r"(?:figure|fig\.|table|tab\.|section|sec\.|chapter|eq\.|equation|appendix|page|pp?\.|abbildung|abb\.|tabelle|kapitel|abschnitt|gleichung|gl\.|seite|s\.|anhang)"
AI_PARAM = re.compile(r"[?&](?:utm_source=(?:chatgpt|openai|copilot|claude|grok|gemini|perplexity)[^&#]*|referrer=[a-z]+\.(?:com|ai))", re.I)


def number_values(raw):
    """All plausible values of a numeral written in English or German style."""
    raw = raw.replace(" ", "").replace(" ", "").replace(" ", "")
    values = set()
    if re.fullmatch(r"\d{1,3}([.,])\d{3}(?:\1\d{3})*", raw):
        values.add(float(re.sub(r"[.,]", "", raw)))          # thousands separator
    if re.fullmatch(r"\d+[.,]\d+", raw):
        values.add(float(raw.replace(",", ".")))              # decimal
    if re.fullmatch(r"\d{1,3}(?:,\d{3})+\.\d+", raw):
        values.add(float(raw.replace(",", "")))
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+,\d+", raw):
        values.add(float(raw.replace(".", "").replace(",", ".")))
    if re.fullmatch(r"\d+", raw):
        values.add(float(raw))
    return values


class FactSet:
    def __init__(self):
        self.numbers = set()
        self.dates = set()      # (y, m, d)
        self.months = set()     # (y, m)
        self.years = set()
        self.phones = []
        self.urls = set()
        self.codes = set()
        self.words = set()


def extract_facts(text, lang, collect=None):
    """Return a list of (kind, value, raw, offset) and fill `collect` (a FactSet) if given."""
    facts = []
    work = text
    for m in re.finditer(r"^[ \t]{0,3}(`{3,}|~{3,})[^\n]*\n.*?(?:^[ \t]{0,3}\1[ \t]*$|\Z)", work, re.M | re.S):
        work = blank(work, m.start(), m.end())

    def take(pattern, kind, handler, flags=re.I):
        nonlocal work
        for m in list(re.finditer(pattern, work, flags)):
            value = handler(m)
            if value is None:
                continue
            facts.append((kind, value, m.group(0), m.start()))
            work = blank(work, m.start(), m.end())

    def url(m):
        u = m.group(0).rstrip(".,;:!?)»“”\"'")
        return AI_PARAM.sub("", u).rstrip("/?").lower()
    take(r"https?://\S+|www\.\S+", "url", url)
    take(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", "url", lambda m: m.group(0).lower())
    take(r"\[NEED:[^\]]*\]", "need", lambda m: m.group(0), 0)

    def ymd(y, mo, d):
        y = int(y); y = y + 2000 if y < 100 else y
        mo, d = int(mo), int(d)
        if 1 <= mo <= 12 and 1 <= d <= 31:
            return ("date", y, mo, d)
        return None
    take(r"\b(\d{4})-(\d{2})-(\d{2})\b", "date", lambda m: ymd(m.group(1), m.group(2), m.group(3)))
    take(r"\b(\d{1,2})\.(\d{1,2})\.(\d{4}|\d{2})\b", "date", lambda m: ymd(m.group(3), m.group(2), m.group(1)))
    take(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", "date",
         lambda m: ("dateamb", int(m.group(3)), int(m.group(1)), int(m.group(2))))
    take(r"\b(\d{1,2})\.?\s+(%s)\.?\s+(\d{4})\b" % MONTH_RE, "date",
         lambda m: ymd(m.group(3), MONTHS[m.group(2).lower()], m.group(1)))
    take(r"\b(%s)\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b" % MONTH_RE, "date",
         lambda m: ymd(m.group(3), MONTHS[m.group(1).lower()], m.group(2)))
    take(r"\b(%s)\.?\s+(\d{4})\b" % MONTH_RE, "month",
         lambda m: ("month", int(m.group(2)), MONTHS[m.group(1).lower()]))
    take(r"\b(0?[1-9]|1[0-2])[./](\d{4})\b", "month", lambda m: ("month", int(m.group(2)), int(m.group(1))))

    def phone(m):
        digits = re.sub(r"\D", "", m.group(0))
        return digits if len(digits) >= 7 else None
    take(r"(?:\+|\b00)\d{1,3}[\s./-]?\(?\d{1,5}\)?(?:[\s./-]?\d{2,}){1,4}\b|\b0\d{2,5}[\s/-]?\d{3,}(?:[\s-]\d{2,})*\b",
         "phone", phone, 0)

    def ref(m):
        return m.group(0)
    take(r"%s\s*\d+(?:[.\-–]\d+)*[a-z]?" % REFERENCE_WORDS, "reference", ref)
    take(r"^[ \t]*(?:#{1,6}[ \t]*)?\d+(?:\.\d+)*[.)]?[ \t]+(?=\S)", "listmarker", ref, re.M)

    def scaled(m):
        base = number_values(m.group(1))
        scale = SCALES.get(m.group(2).lower().rstrip("."), SCALES.get(m.group(2).lower()))
        return ("number", frozenset(base | {v * scale for v in base}))
    take(r"(\d+(?:[.,]\d+)?)\s?(k|tsd\.?|thousand|tausend|mio\.?|million(?:en)?|mn|bn|mrd\.?|billion|milliarden|m|b)\b",
         "number", scaled)
    take(r"\b(\d+)(?:st|nd|rd|th|x)\b", "number", lambda m: ("number", frozenset(number_values(m.group(1)))))
    take(r"\b(?=[\w-]*\d)(?=[\w-]*[A-Za-z])[A-Za-z][\w-]*\d[\w-]*\b|\b\d+[A-Za-z]{1,3}\d[\w-]*\b",
         "code", lambda m: m.group(0).lower().replace("-", ""))

    def num(m):
        values = number_values(m.group(0))
        return ("number", frozenset(values)) if values else None
    take(r"(?<![\w.,])\d{1,3}(?:[.,  ]\d{3})+(?:[.,]\d+)?(?![\w])|(?<![\w.,])\d+(?:[.,]\d+)?(?![\w])",
         "number", num, 0)
    spelled = SPELLED.get(lang, {})
    take(r"\b(%s)\b" % "|".join(spelled), "spelled",
         lambda m: ("number", frozenset([float(spelled[m.group(1).lower()])])))

    if collect is not None:
        for kind, value, raw, _ in facts:
            if kind == "url":
                collect.urls.add(value)
            elif kind == "phone":
                collect.phones.append(value)
            elif kind == "code":
                collect.codes.add(value)
            elif kind in ("number", "spelled"):
                collect.numbers |= set(value[1])
            elif kind == "date":
                if value[0] == "dateamb":
                    for mo, d in ((value[2], value[3]), (value[3], value[2])):
                        collect.dates.add((value[1], mo, d)); collect.months.add((value[1], mo))
                else:
                    collect.dates.add(value[1:]); collect.months.add(value[1:3])
                collect.years.add(value[1])
            elif kind == "month":
                collect.months.add(value[1:]); collect.years.add(value[1])
        collect.words |= set(re.findall(r"\w+", text.lower()))
        collect.numbers |= {float(y) for y in collect.years}
        collect.years |= {int(v) for v in collect.numbers if v.is_integer() and 1900 <= v <= 2100}
    return facts


def fact_findings(output, source, lang, allow=()):
    """F1 candidates: facts in `output` that are not in `source`."""
    known = FactSet()
    extract_facts(source, lang, known)
    for value in allow:
        extract_facts(value, lang, known)
    today = datetime.date.today()
    known.dates.add((today.year, today.month, today.day))
    known.months.add((today.year, today.month))
    findings = []
    for kind, value, raw, offset in extract_facts(output, lang):
        missing = False
        note = ""
        if kind == "url":
            missing, note = value not in known.urls, "URL or email not in source"
        elif kind == "phone":
            missing = not any(value.endswith(p[-7:]) or p.endswith(value[-7:]) for p in known.phones if len(p) >= 7)
            note = "phone number not in source"
        elif kind == "code":
            parts = [p for p in re.split(r"[-_]", raw.lower()) if re.search(r"\d", p)]
            missing = (value not in known.codes and value not in known.words
                       and not all(p in known.words or p in known.codes for p in parts))
            note = "code or name with digits not in source"
        elif kind in ("number", "spelled"):
            values = value[1]
            if kind == "spelled" and raw.lower() in known.words:
                continue
            missing = not (values & known.numbers)
            if missing and all(v.is_integer() and 1900 <= v <= 2100 for v in values):
                missing = not any(int(v) in known.years for v in values)
            note = "spelled-out number not in source (check)" if kind == "spelled" else "number not in source"
        elif kind == "date":
            if value[0] == "dateamb":
                missing = not any(d in known.dates for d in [(value[1], value[2], value[3]), (value[1], value[3], value[2])])
            else:
                missing = tuple(value[1:]) not in known.dates
            note = "date not in source"
        elif kind == "month":
            missing, note = tuple(value[1:]) not in known.months, "month and year not in source"
        if missing:
            findings.append({"id": "F1", "offset": offset, "text": raw.strip(), "note": note})
    return findings


QUALIFIERS = {
    "en": r"up to|about|around|approximately|approx\.|roughly|nearly|almost|over|more than|at least|at most|under|less than|~",
    "de": r"bis zu|rund|etwa|ungefähr|ca\.|circa|knapp|fast|über|mehr als|mindestens|höchstens|unter|weniger als|~",
}


def qualifier_findings(output, source, lang):
    """F2 candidates: a qualifier on a number added, dropped, or changed."""
    pattern = re.compile(r"(?:(%s)\s*)?(\d+(?:[.,]\d+)?)" % QUALIFIERS.get(lang, QUALIFIERS["en"]), re.I)

    def pairs(text):
        found = {}
        for m in pattern.finditer(mask_code(text)):
            for value in number_values(m.group(2)):
                found.setdefault(value, set()).add((m.group(1) or "").lower())
        return found

    src = pairs(source)
    findings = []
    for m in pattern.finditer(mask_code(output)):
        qualifier = (m.group(1) or "").lower()
        values = number_values(m.group(2))
        known = [src[v] for v in values if v in src]
        if not known or any(qualifier in k for k in known):
            continue
        before = sorted(q for k in known for q in k)
        note = ("qualifier '%s' added to a number" % qualifier if qualifier else
                "qualifier '%s' dropped from a number" % before[0] if before and before[0] else "qualifier changed")
        if qualifier and before and before[0]:
            note = "qualifier changed from '%s' to '%s'" % (before[0], qualifier)
        findings.append({"id": "F2", "offset": m.start(), "text": m.group(0), "note": note})
    return findings


HEDGES = {
    "en": ["may", "might", "could", "possibly", "probably", "likely", "suggests", "suggest", "appears", "seems",
           "perhaps", "potentially", "approximately", "not"],
    "de": ["kann", "könnte", "könnten", "möglicherweise", "vermutlich", "wahrscheinlich", "dürfte", "scheint",
           "legt nahe", "deutet darauf hin", "etwa", "nicht", "kein", "keine"],
}


def hedge_findings(output, source, lang):
    """F2 candidates: hedges and negations that the revision has fewer of than the source."""
    findings = []
    for word in HEDGES.get(lang, HEDGES["en"]):
        pattern = r"(?<!\w)%s(?!\w)" % re.escape(word)
        before = len(re.findall(pattern, mask_code(source), re.I))
        after = len(re.findall(pattern, mask_code(output), re.I))
        if before > after:
            findings.append({"id": "F2", "offset": 0, "text": word,
                             "note": "'%s' appears %d time(s) in the source and %d in the revision: check for a removed hedge or negation" % (word, before, after)})
    return findings


def ladder_findings(output, source, lang, genre):
    words = parse_upgrade_words(genre).get(lang, [])
    src = source.lower()
    findings = []
    for word in words:
        pattern = r"(?<!\w)%s(?!\w)" % re.escape(word)
        if re.search(pattern, src, re.I):
            continue
        for m in re.finditer(pattern, output, re.I):
            findings.append({"id": "F2", "offset": m.start(), "text": m.group(0),
                             "note": "ladder word not in source (possible claim upgrade)"})
    return findings


# ---------------------------------------------------------------------------
# Built-in counters (the model applies the same rules by reading)

VERB_RE = re.compile(r"\b(?:is|are|was|were|has|have|had|will|would|should|must|do|does|did|can|could|may|might|am|been|being|"
                     r"ist|sind|war|waren|hat|haben|hatte|wird|werden|wurde|wurden|kann|können|muss|soll)\b", re.I)


def builtin_findings(text, masked, lang, genre, column):
    out = []
    words = word_count(masked)

    bold = re.findall(r"\*\*[^*\n]+\*\*", text)
    if len(bold) > 3:
        out.append(("M1", 0, "%d bold phrases" % len(bold), "more than three bold phrases"))

    tags = [m for m in re.finditer(r"(?:^|(?<=\s))#([A-Za-zÄÖÜäöüß_][\w-]*)", masked)
            if not re.fullmatch(r"(?=[0-9a-f]*\d)(?:[0-9a-f]{6}|[0-9a-f]{8})", m.group(1), re.I)
            and m.group(1) not in ("include", "define", "undef", "if", "ifdef", "ifndef", "elif", "else", "endif", "pragma")]
    if len(tags) >= 6:
        out.append(("M4", tags[0].start(), "%d hashtags" % len(tags), "hashtag block"))

    headings = re.findall(r"^#{1,6}\s+\S", text, re.M)
    if len(headings) > 3 and words < 300:
        out.append(("M3", 0, "%d headings in %d words" % (len(headings), words), "too many headings for the length (M3d)"))

    run = []
    lines = masked.split("\n") + [""]
    for i, line in enumerate(lines):
        m = re.match(r"^\s*[-*•+]\s+(.*\S)", line)
        if m:
            run.append((i, m.group(1)))
            continue
        if len(run) >= 5:
            bare = [t for _, t in run if 1 <= word_count(t) <= 6 and not VERB_RE.search(t)]
            if len(bare) >= 5 and len(bare) / len(run) >= 0.75:
                offset = sum(len(l) + 1 for l in lines[:run[0][0]])
                out.append(("M3", offset, "%d-item list of bare noun phrases" % len(run), "bare noun-phrase bullets (M3c)"))
        if len(run) >= 3:
            firsts = [t.split()[0].lower() for _, t in run if t.split()]
            for j in range(len(firsts) - 2):
                if firsts[j] == firsts[j + 1] == firsts[j + 2]:
                    offset = sum(len(l) + 1 for l in lines[:run[j][0]])
                    out.append(("R7", offset, "bullets starting '%s' ×3" % firsts[j], "cloned bullet openings"))
                    break
            tails = [t for _, t in run if re.search(r"\b(?:resulting in|which (?:led|resulted) to|leading to|was zu|wodurch|führte zu)\b", t, re.I)]
            if len(tails) >= 3:
                offset = sum(len(l) + 1 for l in lines[:run[0][0]])
                out.append(("R7", offset, "%d bullets end on a result clause" % len(tails), "cloned bullet skeleton"))
        run = []

    sents = sentences(masked)
    lengths = [word_count(s) for s in sents]
    if len(lengths) >= 5:
        avg = sum(lengths) / len(lengths)
        sd = (sum((l - avg) ** 2 for l in lengths) / len(lengths)) ** 0.5
        if avg > 10 and sd / avg < 0.25:
            out.append(("R8", 0, "sentence lengths cluster around %d words" % round(avg), "uniform sentence length (R8a)"))
    paras = [masked[a:b] for a, b in paragraphs(masked)]
    if len(paras) >= 4:
        counts = [len(sentences(p)) for p in paras]
        avg = sum(counts) / len(counts)
        if avg >= 3 and all(abs(c - avg) <= 1 for c in counts):
            out.append(("R8", 0, "all paragraphs are about %d sentences" % round(avg), "uniform paragraph length (R8b)"))
    starts = [re.findall(r"[\wÄÖÜäöüß']+", s.strip().lower())[:1] for s in sents]
    for j in range(len(starts) - 2):
        if starts[j] and starts[j] == starts[j + 1] == starts[j + 2] and starts[j][0] not in ("the", "der", "die", "das"):
            out.append(("R7", masked.find(sents[j].strip()), "three sentences start with '%s'" % starts[j][0], "repeated openings"))
            break

    tokens = re.findall(r"[\wÄÖÜäöüß'-]+", masked.lower())
    if len(tokens) >= 200 and len(set(tokens)) / len(tokens) < 0.40:
        out.append(("R9", 0, "type-token ratio %.2f" % (len(set(tokens)) / len(tokens)), "narrow vocabulary"))

    if genre == "prose" and column in ("email", "casual", "investor"):
        body = text.strip()
        if word_count(body) < 150 and len(sentences(body)) >= 4 and "\n" not in body:
            out.append(("R15", 0, "reply without line breaks", "wall of text"))

    if lang == "de":
        kann = re.findall(r"\b(?:kann|können)\b", masked, re.I)
        if len(kann) >= 4 and len(kann) / max(words, 1) >= 0.04:
            out.append(("R2", 0, "%d × kann/können in %d words" % (len(kann), words), "modal hedging density (R2a)"))
        for m in re.finditer(r"[^,;.:!?\n]+", masked):
            nouns = re.findall(r"\b[A-ZÄÖÜ][a-zäöüß]+(?:ung|heit|keit|ion|ität)(?:en)?\b", m.group(0))
            if len(nouns) >= 3:
                out.append(("R18", m.start(), m.group(0).strip()[:80], "%d nominalizations in one clause" % len(nouns)))
        formal = re.findall(r"(?<![.!?:]\s)(?<!^)(?<!\n)\b(?:Sie|Ihnen|Ihr|Ihre|Ihren|Ihrem|Ihrer)\b", masked)
        informal = re.findall(r"\b(?:du|dich|dir|dein|deine|deinen|deinem|deiner)\b", masked, re.I)
        if formal and informal:
            out.append(("G4", 0, "Sie ×%d and du ×%d" % (len(formal), len(informal)), "mixed forms of address"))
        if "”" in text:
            out.append(("M5", text.index("”"), "”", "English closing quotation mark in German text"))
    if '"' in masked and re.search(r"[“”„]", text):
        out.append(("M5", 0, "straight and curly double quotes", "mixed quotation-mark styles"))
    return out


# ---------------------------------------------------------------------------
# Scanning

def scan(text, genre=None, column=None, lang=None, source=None, allow=(), strict=False, gentle=False):
    entries = parse_catalog()
    lang = lang if lang in ("en", "de") else detect_language(text)
    if genre and not column:
        column = DEFAULT_COLUMN[genre]
    settings = Settings(genre, column, lang, strict, gentle, entries)
    masked = mask_protected(text)
    code_masked = mask_code(text)
    paras = paragraphs(masked)
    words = word_count(masked)
    raw_hits = []   # (eid, offset, text, note, density)

    for entry in entries.values():
        if settings.level(entry.id) == "off":
            continue
        haystack = code_masked if entry.id == "C5" else masked
        for regex, density, label in entry.checks.get(lang, []):
            for m in regex.finditer(haystack):
                if not m.group(0).strip():
                    continue
                start = m.start() + (len(m.group(0)) - len(m.group(0).lstrip()))
                raw_hits.append((entry.id, start, m.group(0).strip(), entry.name, density))

    for eid, offset, snippet, note in builtin_findings(text, masked, lang, genre, column):
        if settings.level(eid) != "off":
            raw_hits.append((re.sub(r"[a-z]$", "", eid), offset, snippet, note, False))

    findings, suppressed = [], 0
    by_entry = defaultdict(list)
    for hit in raw_hits:
        by_entry[hit[0]].append(hit)

    # Density items: keep where the entry's threshold is met; below it they
    # behave like weak-alone hits and count only inside a cluster.
    kept = []      # (eid, offset, snippet, note, weak)
    for eid, hits in by_entry.items():
        entry = entries.get(eid)
        level = settings.level(eid)
        weak_entry = (entry.weak if entry else False) or level == "relaxed"
        normal = [h for h in hits if not h[4]]
        dense = [h for h in hits if h[4]]
        passed, below = [], []
        if dense:
            rule = (entry.thresholds.get(lang) or entry.thresholds.get("*")) if entry else None
            if level == "extra" or not rule:
                passed = dense
            else:
                count, unit, size = rule
                if unit == "text":
                    passed, below = (dense, []) if len(dense) >= count else ([], dense)
                elif unit == "paragraph":
                    per = defaultdict(list)
                    for h in dense:
                        per[paragraph_index(paras, h[1])].append(h)
                    for group in per.values():
                        (passed if len(group) >= count else below).extend(group)
                else:
                    offsets = sorted(h[1] for h in dense)
                    window = any(i + count - 1 < len(offsets)
                                 and word_count(masked[offsets[i]:offsets[i + count - 1]]) <= size
                                 for i in range(len(offsets)))
                    passed, below = (dense, []) if window or (words < size and len(dense) >= count) else ([], dense)
        for h in normal:
            kept.append(h[:4] + (weak_entry and level != "extra",))
        for h in passed:
            kept.append(h[:3] + (h[3] + " (at threshold)",) + (False,))
        for h in below:
            if h[4] == "only":
                suppressed += 1
            else:
                kept.append(h[:4] + (True,))

    # Cluster rule for weak-alone hits.
    para_entries = defaultdict(set)
    for h in kept:
        if not h[4]:
            para_entries[paragraph_index(paras, h[1])].add(h[0])
    weak_entries = defaultdict(set)
    for h in kept:
        if h[4]:
            weak_entries[paragraph_index(paras, h[1])].add(h[0])
    for eid, offset, snippet, note, weak in kept:
        entry = entries.get(eid)
        if weak:
            index = paragraph_index(paras, offset)
            others = (para_entries[index] | weak_entries[index]) - {eid}
            if len(others) < 2:
                suppressed += 1
                continue
            note += " (in a cluster)"
        line, col = line_col(text, offset)
        tier = entry.tier if entry else "P2"
        findings.append({"id": eid, "tier": tier, "line": line, "col": col, "offset": offset,
                         "text": snippet[:100], "note": note})

    needs = []
    for m in re.finditer(r"\[NEED:[^\]]*\]", text):
        line, col = line_col(text, m.start())
        needs.append({"line": line, "col": col, "text": m.group(0)})

    if source is not None:
        facts = (fact_findings(text, source, lang, allow) + ladder_findings(text, source, lang, genre)
                 + qualifier_findings(text, source, lang) + hedge_findings(text, source, lang))
        for f in facts:
            line, col = line_col(text, f["offset"])
            findings.append({"id": f["id"], "tier": "F", "line": line, "col": col, "offset": f["offset"],
                             "text": f["text"][:100], "note": f["note"]})
        # F entries whose markers also occur in the source are the source's own words.
        src_lower = source.lower()
        findings = [f for f in findings if not (f["tier"] == "F" and f["id"] != "F1" and f["id"] != "F2"
                                                and f["text"].lower() in src_lower)]

    unique = []
    for f in sorted(findings, key=lambda f: (TIER_ORDER.get(f["tier"], 9), f["offset"])):
        if any(u["id"] == f["id"] and abs(u["offset"] - f["offset"]) < 20 and u["tier"] != "F" for u in unique):
            continue
        unique.append(f)
    unique.sort(key=lambda f: (TIER_ORDER.get(f["tier"], 9), f["line"], f["col"]))
    for f in unique:
        f.pop("offset", None)
    return {"genre": genre, "section": column, "lang": lang, "words": words,
            "findings": unique, "needs": needs, "suppressed": suppressed}


def format_report(result, name, source_name=None):
    head = "check.py scan · %s · genre=%s%s · lang=%s" % (
        name, result["genre"] or "none", " section=%s" % result["section"] if result["section"] else "", result["lang"])
    if source_name:
        head += " · source=%s" % source_name
    lines = [head]
    groups = [("Facts (F)", "F"), ("P0", "P0"), ("P1", "P1"), ("P2", "P2")]
    for title, tier in groups:
        items = [f for f in result["findings"] if f["tier"] == tier]
        if items:
            lines.append(title)
            for f in items:
                lines.append("  %-4s L%d:%d  \"%s\"  %s" % (f["id"], f["line"], f["col"], f["text"], f["note"]))
    if result["needs"]:
        lines.append("Open items")
        for n in result["needs"]:
            lines.append("  L%d  %s" % (n["line"], n["text"]))
    facts = sum(1 for f in result["findings"] if f["tier"] == "F")
    style = len(result["findings"]) - facts
    lines.append("Summary: %d fact finding(s), %d open item(s), %d style finding(s); %d weak-alone or below-threshold hit(s) not shown."
                 % (facts, len(result["needs"]), style, result["suppressed"]))
    lines.append("Script hits are candidates; the skill's guards decide what is a finding.")
    return "\n".join(lines)


def read(path):
    with open(path, encoding="utf-8-sig") as handle:
        return handle.read().replace("\r\n", "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="check.py", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command")
    for name in ("scan", "compare"):
        p = sub.add_parser(name)
        if name == "scan":
            p.add_argument("file")
            p.add_argument("--source", help="source material the text must not go beyond")
        else:
            p.add_argument("original")
            p.add_argument("revised")
        p.add_argument("--genre", choices=["cv", "science", "prose"])
        p.add_argument("--section", help="settings column: a CV part, a paper section, or a prose type")
        p.add_argument("--lang", choices=["en", "de", "auto"], default="auto")
        p.add_argument("--allow", action="append", default=[], help="extra text whose facts count as known (repeatable)")
        p.add_argument("--strict", action="store_true", help="stop-slop at full strength (relaxed becomes on)")
        p.add_argument("--gentle", action="store_true", help="polish-level entries only at thresholds")
        p.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 2
    try:
        if args.command == "scan":
            text = read(args.file)
            source = read(args.source) if args.source else None
            result = scan(text, args.genre, args.section and args.section.lower(), args.lang, source,
                          args.allow, args.strict, args.gentle)
            print(json.dumps(result, ensure_ascii=False, indent=2) if args.json
                  else format_report(result, args.file, args.source))
            return 1 if any(f["tier"] == "F" for f in result["findings"]) else 0
        original, revised = read(args.original), read(args.revised)
        status = 0
        try:
            sys.path.insert(0, HERE)
            import aiw_validate
            verdict = aiw_validate.validate(original, revised)
            print(aiw_validate.format_result(verdict))
            status = 0 if verdict["ok"] else 1
        except ImportError:
            print("aiw_validate.py not found; structural preservation check skipped.")
        lang = args.lang if args.lang in ("en", "de") else detect_language(revised)
        facts = (fact_findings(revised, original, lang, args.allow) + ladder_findings(revised, original, lang, args.genre)
                 + qualifier_findings(revised, original, lang) + hedge_findings(revised, original, lang))
        if facts:
            print("Facts in the revision that are not in the original:")
            for f in facts:
                line, col = line_col(revised, f["offset"])
                print("  %-3s L%d:%d  \"%s\"  %s" % (f["id"], line, col, f["text"], f["note"]))
            status = 1
        else:
            print("Facts: every number, date, phone number, URL, code, and ladder word in the revision is in the original.")
        return status
    except (OSError, UnicodeDecodeError) as err:
        sys.stderr.write("check.py: %s\n" % err)
        return 2


if __name__ == "__main__":
    sys.exit(main())
