#!/usr/bin/env python3
"""House-style mechanics check: a Python port of scripts/check-style.js.

Ported from avoid-ai-writing v3.36.0
(https://github.com/conorbronsdon/avoid-ai-writing), MIT License,
Copyright (c) 2026 Conor Bronsdon.

Verifies that a document applied the mechanics of a house-style config
(quotes, latinAbbrev as hard rules; headings, emDash, spellNumbersUpTo as
advisories). It does not judge register. Protected Markdown is skipped via
aiw_markdown. A bare --config name resolves to upstream/examples/<name>.json.

CLI (exit 0 clean, 1 hard violation, 2 tool/usage error):
    python3 aiw_style.py <file.md> --config <config.json|name> [--json]

Standard library only; Python 3.9 compatible.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, HERE)

from aiw_jscompat import (  # noqa: E402
    JSONParseError, exec_all, from_u16, js_json_parse, js_key_order, js_lower, js_re, js_stringify,
    js_to_string, js_trim, js_truthy, js_typeof, node_fs_error, py_re, read_file_utf8,
    write_stderr, write_stdout, WS,
)
from aiw_markdown import markdown_prose  # noqa: E402

EXAMPLES_DIR = os.path.join(HERE, 'upstream', 'examples')

KNOWN = {
    'quotes': ['straight', 'curly'],
    'headings': ['sentence', 'title'],
    'latinAbbrev': ['parentheses', 'never', 'any'],
    'emDash': ['sparing', 'deliberate'],
    'spellNumbersUpTo': 'number',
    'serialComma': 'boolean',
}
# `k in KNOWN` on a plain JS object also finds Object.prototype members; the
# value is then a function (or the prototype itself), whose String() appears
# in the "expected ..." detail.
_PROTOTYPE_MEMBERS = {
    'constructor': 'function Object() { [native code] }',
    '__proto__': '[object Object]',
    'hasOwnProperty': 'function hasOwnProperty() { [native code] }',
    'isPrototypeOf': 'function isPrototypeOf() { [native code] }',
    'propertyIsEnumerable': 'function propertyIsEnumerable() { [native code] }',
    'toString': 'function toString() { [native code] }',
    'valueOf': 'function valueOf() { [native code] }',
    'toLocaleString': 'function toLocaleString() { [native code] }',
    '__defineGetter__': 'function __defineGetter__() { [native code] }',
    '__defineSetter__': 'function __defineSetter__() { [native code] }',
    '__lookupGetter__': 'function __lookupGetter__() { [native code] }',
    '__lookupSetter__': 'function __lookupSetter__() { [native code] }',
}

SMALL = frozenset(['a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'in', 'of', 'on', 'or', 'the',
                   'to', 'with', 'vs', 'nor', 'so', 'yet'])

RE_EMPHASIS = js_re(r'[*_`]', 'g')
RE_WS_SPLIT = py_re(WS + '+')
RE_NON_ALPHA = js_re(r'[^A-Za-z]', 'g')
RE_WORD = js_re(r'\b\w+\b', 'g')
RE_HEADING = js_re(r'^#{1,6}\s+(.*)$', '')
RE_CURLY = js_re('[“”‘’]', '')
RE_PRIME = js_re(r'''(\d)['"]''', 'g')
RE_APOSTROPHE = js_re(r"[A-Za-z]'[A-Za-z]|[A-Za-z]'(?!\w)|(^|\s)'", '')
RE_LATIN = js_re(r'\b(e\.g\.|i\.e\.)', 'gi')
RE_LIST_LINE = js_re(r'^\s*([-*]|\d+\.)\s', '')
RE_SMALL_NUMBER = js_re(r'(?<![\w.$:])\d{1,3}(?![\w.%:])', 'g')
RE_PATHISH = js_re(r'[\\/]', '')
RE_JSON_SUFFIX = js_re(r'\.json$', 'i')


def _exists(path):
    try:
        return os.path.exists(path)
    except (ValueError, OSError):
        return False


def resolve_config(arg):
    """A path-shaped arg is used as-is; a bare name maps to upstream/examples/<name>.json."""
    if not arg:
        return None
    if RE_PATHISH.search(arg) or RE_JSON_SUFFIX.search(arg):
        return arg if _exists(arg) else None
    q = js_lower(js_trim(arg))
    direct = os.path.normpath(os.path.join(EXAMPLES_DIR, from_u16(q) + '.json'))
    return direct if _exists(direct) else None


def _sub(rx, text, repl):
    out = []
    last = 0
    for m in exec_all(rx, text):
        out.append(text[last:m.start()])
        out.append(repl(m))
        last = m.end()
    out.append(text[last:])
    return ''.join(out)


def major_words(h):
    words = RE_WS_SPLIT.split(js_trim(_sub(RE_EMPHASIS, h, lambda m: '')))[1:]
    out = []
    for w in words:
        b = _sub(RE_NON_ALPHA, w, lambda m: '')
        if b and b != b.upper() and b.lower() not in SMALL:
            out.append(b)
    return out


def is_title_case(h):
    return len([b for b in major_words(h) if 'A' <= b[0] <= 'Z']) >= 2


def looks_sentence_case(h):
    w = major_words(h)
    return len(w) >= 1 and all('a' <= b[0] <= 'z' for b in w)


def _in_known(k):
    return k in KNOWN or k in _PROTOTYPE_MEMBERS


def check(text, mechanics):
    """Returns {hard, advisory, warnings} for the config's mechanics."""
    m = mechanics if js_truthy(mechanics) else {}
    if isinstance(m, dict):
        m = js_key_order(m)
    warnings = []
    for k, v in (m.items() if isinstance(m, dict) else []):
        if not _in_known(k):
            warnings.append({'rule': 'unknown-key', 'detail': k})
            continue
        spec = KNOWN.get(k)
        if isinstance(spec, list):
            if not any(v == s and isinstance(v, str) for s in spec):
                warnings.append({'rule': 'unknown-value', 'detail': '%s: %s' % (k, js_stringify(v, 0))})
        elif spec is None or js_typeof(v) != spec:
            expected = spec if spec is not None else _PROTOTYPE_MEMBERS[k]
            warnings.append({'rule': 'unknown-value',
                             'detail': '%s: %s (expected %s)' % (k, js_stringify(v, 0), expected)})

    get = m.get if isinstance(m, dict) else (lambda key: None)
    prose_info = markdown_prose(text)
    prose, para_break = prose_info['prose'], prose_info['paraBreak']
    joined = '\n'.join(prose)
    words = len(exec_all(RE_WORD, joined))
    hard = []
    advisory = []
    heads = []
    for i, line in enumerate(prose):
        h = RE_HEADING.search(line)
        if h:
            heads.append((i + 1, h))

    quotes = get('quotes')
    if quotes == 'straight':
        for i, line in enumerate(prose):
            if RE_CURLY.search(line):
                hard.append({'line': i + 1, 'rule': 'quotes-should-be-straight'})
    elif quotes == 'curly':
        for i, line in enumerate(prose):
            c = _sub(RE_PRIME, line, lambda mm: mm.group(1))
            if '"' in c:
                hard.append({'line': i + 1, 'rule': 'double-quote-should-be-curly'})
            if RE_APOSTROPHE.search(c):
                hard.append({'line': i + 1, 'rule': 'apostrophe-should-be-curly'})

    headings = get('headings')
    if headings == 'sentence':
        for ln, h in heads:
            if is_title_case(h.group(1)):
                advisory.append({'line': ln, 'rule': 'heading-may-need-sentence-case'})
    elif headings == 'title':
        for ln, h in heads:
            if looks_sentence_case(h.group(1)):
                advisory.append({'line': ln, 'rule': 'heading-may-need-title-case'})

    latin = get('latinAbbrev')
    if latin in ('parentheses', 'never'):
        depth = 0
        for i, line in enumerate(prose):
            if para_break[i]:
                depth = 0
                continue
            for mm in exec_all(RE_LATIN, line):
                if latin == 'never':
                    hard.append({'line': i + 1, 'rule': 'latin-abbrev-not-allowed'})
                    continue
                before = line[:mm.start()]
                at = depth + before.count('(') - before.count(')')
                if at <= 0:
                    hard.append({'line': i + 1, 'rule': 'latin-abbrev-outside-parens'})
            depth = max(0, depth + line.count('(') - line.count(')'))

    if get('emDash') == 'sparing':
        em = joined.count('—')
        if em > words // 1000:
            advisory.append({'rule': 'em-dash-rate', 'detail': '%d in %d words' % (em, words)})

    limit = get('spellNumbersUpTo')
    if js_typeof(limit) == 'number':
        for i, line in enumerate(prose):
            if RE_LIST_LINE.search(line):
                continue
            nums = [mm.group(0) for mm in exec_all(RE_SMALL_NUMBER, line) if int(mm.group(0)) <= limit]
            if nums:
                advisory.append({'line': i + 1, 'rule': 'number-may-need-spelling', 'detail': ', '.join(nums)})

    return {'hard': hard, 'advisory': advisory, 'warnings': warnings}


def _print(line):
    write_stdout(line + '\n')


def main(argv):
    cfg_arg = None
    as_json = False
    file = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--config':
            nx = argv[i + 1] if i + 1 < len(argv) else None
            if nx is not None and not nx.startswith('--'):
                cfg_arg = nx
                i += 1
        elif a == '--json':
            as_json = True
        elif a.startswith('--'):
            write_stderr('unknown flag: %s\n' % a)
            return 2
        elif file is None:
            file = a
        else:
            write_stderr('unexpected extra argument: %s\n' % a)
            return 2
        i += 1
    if not file or not cfg_arg:
        write_stderr('usage: check-style.js <file> --config <config.json|name> [--json]\n')
        return 2
    cfg_path = resolve_config(cfg_arg)
    if not cfg_path:
        write_stderr('config not found: "%s"\nPass a path to a JSON config, or a name matching a file in '
                     'examples/ (for example, --config technical). See examples/README.md.\n' % cfg_arg)
        return 2
    try:
        config = js_json_parse(read_file_utf8(cfg_path))
    except OSError as exc:
        write_stderr('could not read config "%s": %s\n' % (cfg_path, node_fs_error(exc, cfg_path)))
        return 2
    except JSONParseError as exc:
        write_stderr('could not read config "%s": %s\n' % (cfg_path, exc))
        return 2
    mechanics = config.get('mechanics') if isinstance(config, dict) else None
    if not js_truthy(config) or not isinstance(config, (dict, list)) or not isinstance(mechanics, dict):
        write_stderr('config "%s" has no "mechanics" object\n' % cfg_path)
        return 2
    try:
        text = read_file_utf8(file)
    except OSError as exc:
        write_stderr('could not read file "%s": %s\n' % (file, node_fs_error(exc, file)))
        return 2
    r = check(text, mechanics)
    if as_json:
        _print(js_stringify(r, 2))
    else:
        w = ', %d config warning(s)' % len(r['warnings']) if r['warnings'] else ''
        name = config.get('name')
        title = js_to_string(name) if js_truthy(name) else cfg_path
        _print('%s: %d hard, %d advisory%s' % (title, len(r['hard']), len(r['advisory']), w))
        for x in r['warnings']:
            _print('  ! %s: %s' % (x['rule'], x['detail']))
        for x in r['hard']:
            _print('  L%s  %s' % (x.get('line') or '-', x['rule']))
        for x in r['advisory']:
            detail = ': %s' % x['detail'] if x.get('detail') else ''
            _print('  L%s  %s (advisory)%s' % (x.get('line') or '-', x['rule'], detail))
    return 1 if r['hard'] else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
