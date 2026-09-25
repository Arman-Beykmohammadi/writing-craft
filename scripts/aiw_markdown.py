"""Offset-stable Markdown prose mask: a Python port of scripts/markdown-prose.js.

Ported from avoid-ai-writing v3.36.0
(https://github.com/conorbronsdon/avoid-ai-writing), MIT License,
Copyright (c) 2026 Conor Bronsdon. Shared by aiw_quotes.py and aiw_style.py.

markdown_prose(text) returns a dict with:
  masked     the text with every protected character replaced by NUL
             (newlines and carriage returns stay in place)
  context    the same, with protected characters shown as 'a' (or '*' for
             characters inside an HTML tag), for quote-direction decisions
  prose      the prose lines: masked split at \\n, trailing \\r and NULs removed
  paraBreak  one boolean per line, True for a blank (paragraph-break) line

Protected: YAML frontmatter, fenced and indented code, raw HTML blocks, code
spans, HTML tags/comments/autolinks, escapes, link destinations and titles,
reference definitions and their labels, bare URLs, a leading BOM.

Strings are UTF-16 code-unit strings when called from the other ports (see
aiw_jscompat); plain Python strings without astral characters work as-is.
Standard library only; Python 3.9 compatible.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiw_jscompat import JS_WS_CHARS, exec_all, js_lower, js_re, js_trim, py_re  # noqa: E402

REF_DEF = js_re(
    '^ {0,3}\\[((?:\\\\.|[^\\]\\n])+)\\]:[ \\t]*(?:\\r?\\n[ \\t]*)?(?:<[^>\\n]*>|\\S+)'
    '(?:[ \\t]*(?:\\r?\\n[ \\t]*)?(?:"(?:\\\\.|[^"\\\\])*"|\'(?:\\\\.|[^\'\\\\])*\'|\\((?:\\\\.|[^)\\\\])*\\)))?'
    '[ \\t]*\\r?$', 'gm')
TAG_SOURCE = ('<\\/?[a-zA-Z][a-zA-Z0-9-]*(?:\\s+[a-zA-Z_:][\\w:.-]*(?:\\s*=\\s*(?:"[^"]*"|\'[^\']*\'|'
              '[^\\s"\'=<>`]+))?)*\\s*\\/?>')
# The inline HTML constructs, tried in this order at each '<' (sticky /y regexes).
HTML = [
    js_re(TAG_SOURCE, 'y'),
    js_re(r'<!--[\s\S]*?(?:-->|$)', 'y'),
    js_re(r'<\?[\s\S]*?(?:\?>|$)', 'y'),
    js_re(r'<!\[CDATA\[[\s\S]*?(?:\]\]>|$)', 'y'),
    js_re(r'<![A-Z][^>]*>', 'y'),
    js_re(r'<(?:[a-zA-Z][a-zA-Z0-9+.-]{1,31}:[^<>\s]*|[^<>\s@]+@[^<>\s@]+)>', 'y'),
]
ESCAPABLE = js_re(r'[!"#$%&\'()*+,\-./:;<=>?@[\]^_`{|}~\\]', '')
ESCAPABLE_WITH_CURLY = js_re('[!"#$%&\'()*+,\\-./:;<=>?@[\\]^_`{|}~\\\\\u201c\u201d\u2018\u2019]', '')
LABEL_ESCAPE = js_re(r'\\([!"#$%&\'()*+,\-./:;<=>?@[\]^_`{|}~\\])', 'g')
WS_RUN = js_re(r'\s+', 'g')
REFS = js_re(r'\[((?:\\.|[^\]\\\n])*)\](?:[ \t]*\[((?:\\.|[^\]\\\n])*)\])?', 'g')
URLS = js_re('\\bhttps?:\\/\\/[^\\s<>"\u201c\u201d\\x00]+', 'g')
QUOTED_URL_END = js_re("[\u2019'][).,;:!?]*$", '')
BLANK_PAIR = js_re(r'\n[ \t\r]*\n', '')

RE_FM_OPEN = js_re(r'^---[ \t]*$', '')
RE_FM_CLOSE = js_re(r'^(?:---|\.\.\.)[ \t]*$', '')
RE_QUOTE_PREFIX = js_re(r'^(?: {0,3}>[ \t]?)+', '')
RE_INDENT = js_re(r'^[ \t]*', '')
RE_LIST_MARKER = js_re(r'^( *)(?:[-*+]|\d{1,9}[.)])([ \t]+|$)', '')
RE_FENCE = js_re(r'^( {0,3})(`{3,}|~{3,})(.*)$', '')
RE_BLANK = js_re(r'^\s*$', '')
RE_RAW_HTML_START = js_re(r'^ {0,3}<(script|style|pre|textarea)(?:[ \t>]|$)', 'i')
RE_ATX = js_re(r'^ {0,3}#{1,6}(?:[ \t]|$)', '')
RE_SETEXT = js_re(r'^ {0,3}(?:=+|-+)[ \t]*$', '')
RE_THEMATIC = js_re(r'^ {0,3}(?:(?:\*[ \t]*){3,}|(?:_[ \t]*){3,}|(?:-[ \t]*){3,})$', '')
RE_IND4 = js_re(r'^(?: {4}| *\t)', '')
RE_TICKS = py_re('`+')


def label_key(s):
    out = []
    last = 0
    for m in exec_all(LABEL_ESCAPE, s):
        out.append(s[last:m.start()])
        out.append(m.group(1))
        last = m.end()
    out.append(s[last:])
    s = js_trim(''.join(out))
    parts = []
    last = 0
    for m in exec_all(WS_RUN, s):
        parts.append(s[last:m.start()])
        parts.append(' ')
        last = m.end()
    parts.append(s[last:])
    return js_lower(''.join(parts))


def _is_escapable(ch):
    return ch != '' and bool(ESCAPABLE.search(ch))


def inline_link_ends(s):
    """Return linkEnd(start): the index of the ')' closing an inline link
    destination (and optional title) that starts at `start`, or -1."""
    n = len(s)
    escaped = [0] * (n + 1)
    i = 0
    while i < n:
        if s[i] == '\\' and i + 1 < n and _is_escapable(s[i + 1]):
            i += 1
            escaped[i] = 1
        i += 1
    bare = [0] * (n + 2)
    space = [0] * (n + 1)
    lines = [0] * (n + 1)
    delimiters = ('"', "'", ')', '>')
    closing = dict((d, [-1] * (n + 1)) for d in delimiters)
    bare[n] = space[n] = n
    for i in range(n - 1, -1, -1):
        ch = s[i]
        ws = ch in ' \t\r\n'
        space[i] = space[i + 1] if ws else i
        lines[i] = lines[i + 1] + (1 if ch == '\n' else 0) if ws else 0
        for d in delimiters:
            blocked = (ch == '\0' or (ch == '\n' and lines[i] > 1)
                       or (d == '>' and ch in '<>\r\n' and ch != '>')
                       or (d == ')' and ch == '(' and not escaped[i]))
            if blocked:
                closing[d][i] = -1
            elif ch == d and not escaped[i]:
                closing[d][i] = i
            else:
                closing[d][i] = closing[d][i + 1]
        if ch == '\\' and escaped[i + 1]:
            bare[i] = bare[i + 2]
        elif ch == '(' and not escaped[i]:
            end = bare[i + 1]
            bare[i] = bare[end + 1] if end < n and s[end] == ')' and not escaped[end] else i
        elif ch in JS_WS_CHARS or ch < '\x20' or ch in '<>' or (ch == ')' and not escaped[i]):
            bare[i] = i
        else:
            bare[i] = bare[i + 1]

    def at(k):
        return s[k] if 0 <= k < n else ''

    def skip_space(k):
        return -1 if lines[k] > 1 else space[k]

    def link_end(start):
        k = skip_space(start)
        if k < 0:
            return -1
        if at(k) == '<':
            end = closing['>'][k + 1]
            if end < 0:
                return -1
            k = end + 1
        else:
            k = bare[k]
        if at(k) == ')':
            return k
        end = skip_space(k)
        if end < 0 or end == k:
            return -1
        if at(end) == ')':
            return end
        delimiter = ')' if at(end) == '(' else at(end)
        if delimiter != '"' and delimiter != "'" and at(end) != '(':
            return -1
        title_end = closing[delimiter][end + 1]
        if title_end < 0:
            return -1
        k = skip_space(title_end + 1)
        return k if k >= 0 and at(k) == ')' else -1

    return link_end


def _bare(line):
    return line[:-1] if line.endswith('\r') else line


def markdown_prose(text):
    chars = list(text)
    transparent = set()

    def protect(a, b, tag=False):
        for i in range(a, b):
            if text[i] == '\n' or text[i] == '\r':
                continue
            chars[i] = '\0'
            if tag:
                transparent.add(i)

    lines = text.split('\n')
    fm_end = -1
    first = _bare(lines[0])
    if first.startswith('\ufeff'):
        first = first[1:]
    if RE_FM_OPEN.search(first) and len(lines) > 1 and js_trim(lines[1]):
        for k in range(1, len(lines)):
            if RE_FM_CLOSE.search(_bare(lines[k])):
                fm_end = k
                break

    fence = None
    in_indent = False
    prev_blank = True
    offset = 0
    quote_depth = 0
    list_indents = []
    para_break = []
    block_starts = set()
    raw_html = None
    for i, line in enumerate(lines):
        start = offset
        offset += len(line) + 1
        if i <= fm_end:
            protect(start, offset - 1)
            para_break.append(False)
            continue
        b = _bare(line)
        if b.startswith('\ufeff'):
            b = b[1:]
        # Strip container prefixes for block recognition, retaining source offsets.
        if fence:
            quote = (py_re('(?: {0,3}>[ \t]?){%d}' % quote_depth).match(b) if quote_depth else None)
        else:
            quote = RE_QUOTE_PREFIX.search(b)
        depth = quote.group(0).count('>') if quote else 0
        if depth != quote_depth:
            fence = None
            raw_html = None
            in_indent = False
            prev_blank = True
            list_indents = []
            block_starts.add(start)
            quote_depth = depth
        if quote:
            b = b[len(quote.group(0)):]
        blank = not js_trim(b)
        indent = len(RE_INDENT.search(b).group(0).replace('\t', '    '))
        # A fenced block belongs to its list item; dedenting leaves that container.
        if fence and fence['listIndent'] and not blank and indent < fence['listIndent']:
            fence = None
            prev_blank = True
            block_starts.add(start)
        if raw_html and raw_html['listIndent'] and not blank and indent < raw_html['listIndent']:
            raw_html = None
        if not blank and not fence:
            while list_indents and indent < list_indents[-1]:
                list_indents.pop()
        base = list_indents[-1] if list_indents else 0
        marker = None if fence else RE_LIST_MARKER.search(b)
        if marker and indent - base < 4:
            # More than four spaces after a marker starts code at the item's content indent.
            padding = 1 if len(marker.group(2)) > 4 else max(1, len(marker.group(2)))
            content_indent = len(marker.group(0)) - len(marker.group(2)) + padding
            list_indents.append(content_indent)
            block_starts.add(start)
            b = b[min(content_indent, len(b)):]
            prev_blank = True
            in_indent = False
        elif base:
            consumed = 0
            columns = 0
            while consumed < len(b) and b[consumed] in ' \t' and columns < base:
                columns += 4 - columns % 4 if b[consumed] == '\t' else 1
                consumed += 1
            b = b[consumed:]

        fm = RE_FENCE.search(b)
        if fence:
            if (fm and fm.group(2)[0] == fence['char'] and len(fm.group(2)) >= fence['length']
                    and RE_BLANK.search(fm.group(3))):
                fence = None
            protect(start, offset - 1)
            para_break.append(False)
            prev_blank = False
            continue
        if fm and not (fm.group(2)[0] == '`' and '`' in fm.group(3)):
            fence = {'char': fm.group(2)[0], 'length': len(fm.group(2)),
                     'listIndent': list_indents[-1] if list_indents else 0}
            protect(start, offset - 1)
            para_break.append(False)
            in_indent = False
            prev_blank = False
            continue
        raw_start = RE_RAW_HTML_START.search(b)
        if not raw_html and raw_start:
            raw_html = {'name': raw_start.group(1), 'listIndent': list_indents[-1] if list_indents else 0}
        if raw_html:
            if re.search('</' + raw_html['name'] + '[ \t]*>', b, re.I | re.A):
                raw_html = None
            protect(start, offset - 1)
            para_break.append(False)
            prev_blank = False
            continue
        # Inline spans cannot consume headings, thematic breaks, or a following block.
        if RE_ATX.search(b) or RE_SETEXT.search(b) or RE_THEMATIC.search(b):
            block_starts.add(start)
            block_starts.add(offset)
        if blank:
            block_starts.add(start)
            block_starts.add(offset)
        ind4 = bool(RE_IND4.search(b))
        if not blank:
            in_indent = ind4 and (prev_blank or in_indent)
        if in_indent and not blank:
            protect(start, offset - 1)
        para_break.append(blank)
        prev_blank = blank

    # Reference definitions must precede link masking.
    s = ''.join(chars)
    labels = set()
    definitions = {}
    for m in exec_all(REF_DEF, s):
        if '\0' in m.group(0) or BLANK_PAIR.search(m.group(0)):
            continue
        definitions[m.start()] = (m.end(), label_key(m.group(1)))

    # Consume competing inline constructs in source order.
    s = ''.join(chars)
    link_end = inline_link_ends(s)
    n = len(s)
    next_block = [0] * (n + 1)
    boundary = n
    for i in range(n, -1, -1):
        next_block[i] = boundary
        if i in block_starts or (i < n and s[i] == '\0'):
            boundary = i
    link_openers = []
    i = 0
    while i < n:
        definition = definitions.get(i)
        if definition:
            labels.add(definition[1])
            protect(i, definition[0])
            i = definition[0]
            continue
        ch = s[i]
        if ch == '\\' and i + 1 < n and ESCAPABLE_WITH_CURLY.search(s[i + 1]):
            protect(i, i + 2)
            i += 2
            continue
        if ch == '`':
            run_len = len(RE_TICKS.match(s, i).group(0))
            pos = i + run_len
            found = False
            while True:
                close = RE_TICKS.search(s, pos)
                if close is None or close.start() >= next_block[i]:
                    break
                pos = close.end()
                if len(close.group(0)) != run_len:
                    continue
                protect(i, close.end())
                i = close.end()
                found = True
                break
            if not found:
                i += run_len
            continue
        if ch == '<':
            matched = False
            for rx in HTML:
                m = rx.match(s, i)
                if not m or '\0' in m.group(0):
                    continue
                protect(i, m.end(), rx is HTML[0])
                i = m.end()
                matched = True
                break
            if matched:
                continue
        if ch == '[':
            link_openers.append(next_block[i])
        if ch == ']':
            opener_boundary = link_openers.pop() if link_openers else None
            if opener_boundary is not None and i < opener_boundary and i + 1 < n and s[i + 1] == '(':
                end = link_end(i + 2)
                if 0 <= end < next_block[i]:
                    protect(i + 1, end + 1)
                    i = end
        i += 1

    s = ''.join(chars)
    for m in exec_all(REFS, s):
        if '\0' in m.group(0):
            continue
        last = m.end()
        if m.group(2) is not None:
            if not m.group(2):
                if label_key(m.group(1)) in labels:
                    protect(m.start(), last)
            elif label_key(m.group(2)) in labels:
                protect(last - len(m.group(2)) - 2, last)
        elif (last >= len(s) or s[last] != '\0') and label_key(m.group(1)) in labels:
            protect(m.start(), last)

    # Bare URLs exclude prose quotes and terminal punctuation.
    s = ''.join(chars)
    for m in exec_all(URLS, s):
        url = m.group(0)
        end = len(url)
        before = s[m.start() - 1] if m.start() > 0 else ''
        surrounding_quote = before in ('\u2018', "'") and before != ''
        quoted_end = QUOTED_URL_END.search(url) if surrounding_quote else None
        if quoted_end:
            end = quoted_end.start() + 1
        bounded = url[:end]
        extra = bounded.count(')') - bounded.count('(')
        while end > 0:
            last = url[end - 1]
            if last in '.,;:!?':
                end -= 1
            elif surrounding_quote and last in ('\u2019', "'"):
                end -= 1
                surrounding_quote = False
            elif extra > 0 and last == ')':
                end -= 1
                extra -= 1
            else:
                break
        protect(m.start(), m.start() + end)
    if text[:1] == '\ufeff':
        protect(0, 1)
    masked = ''.join(chars)
    context = ''.join(('*' if i in transparent else 'a') if ch == '\0' else ch for i, ch in enumerate(chars))
    prose = [_bare(l).replace('\0', '') for l in masked.split('\n')]
    return {'masked': masked, 'context': context, 'prose': prose, 'paraBreak': para_break}
