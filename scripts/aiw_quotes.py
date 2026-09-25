#!/usr/bin/env python3
"""Quote/apostrophe normalization: a Python port of scripts/normalize-quotes.js.

Ported from avoid-ai-writing v3.36.0
(https://github.com/conorbronsdon/avoid-ai-writing), MIT License,
Copyright (c) 2026 Conor Bronsdon.

Every edit is a 1:1 character substitution outside protected Markdown
(code, links, HTML, frontmatter; see aiw_markdown), so line endings and
whitespace survive verbatim. --quotes auto infers the convention from the
document itself or from --reference.

CLI (exit 0 success, 2 usage/I/O error):
    python3 aiw_quotes.py <file.md> [--quotes auto|straight|curly]
                          [--reference original.md] [--write]

Standard library only; Python 3.9 compatible.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiw_jscompat import (  # noqa: E402
    JS_WS_CHARS, encode_utf8, from_u16, node_fs_error, read_file_utf8, to_u16, write_stderr, write_stdout,
)
from aiw_markdown import markdown_prose  # noqa: E402

DIGITS = '0123456789'


def straighten(s):
    return (s.replace('“', '"').replace('”', '"')
            .replace('‘', "'").replace('’', "'"))


def educate(s):
    chars = list(s)
    n = len(chars)
    for i in range(n):
        if chars[i] != '"' and chars[i] != "'":
            continue
        p, q = i - 1, i + 1
        # Emphasis delimiters are transparent when deciding a quotation's direction.
        while p >= 0 and chars[p] in '*_~':
            p -= 1
        while q < n and chars[q] in '*_~':
            q += 1
        prev = chars[p] if p >= 0 else ''
        nxt = chars[q] if q < n else ''
        # Match the checker's feet/inch carve-out. Already-curly marks stay curly.
        if prev != '' and prev in DIGITS:
            continue
        opening = ((not prev or prev in JS_WS_CHARS or prev in '([{—–-“‘')
                   and nxt != '' and nxt not in JS_WS_CHARS)
        if chars[i] == '"':
            chars[i] = '“' if opening else '”'
        else:
            chars[i] = '‘' if opening and not (nxt != '' and nxt in DIGITS) else '’'
    return ''.join(chars)


def infer_quotes(text):
    """Infer double and single marks independently; ties use the first observed style."""
    masked = markdown_prose(text)['masked']
    counts = {'double': {'straight': 0, 'curly': 0}, 'single': {'straight': 0, 'curly': 0}}
    first = {}
    for i, ch in enumerate(masked):
        if ch not in '"\'“”‘’':
            continue
        if ch in '"\'' and i > 0 and masked[i - 1] in DIGITS:
            continue
        kind = 'double' if ch in '"“”' else 'single'
        style = 'straight' if ch in '"\'' else 'curly'
        counts[kind][style] += 1
        if kind not in first:
            first[kind] = style
    out = {}
    for kind, c in counts.items():
        if c['straight'] == c['curly']:
            out[kind] = first.get(kind)
        else:
            out[kind] = 'straight' if c['straight'] > c['curly'] else 'curly'
    return out


def normalize(text, quotes='auto', reference=None):
    """normalize(text, quotes, reference): reference defaults to text."""
    if quotes not in ('auto', 'straight', 'curly') or not isinstance(quotes, str):
        raise TypeError('quotes must be auto, straight or curly')
    if reference is None:
        reference = text
    convention = infer_quotes(reference) if quotes == 'auto' else {'double': quotes, 'single': quotes}
    prose = markdown_prose(text)
    masked, context = prose['masked'], prose['context']
    straight = straighten(context)
    curly = educate(context)
    out = []
    for i, ch in enumerate(context):
        if masked[i] == '\0':
            out.append(text[i])
            continue
        style = convention['double' if ch in '"“”' else 'single']
        if style == 'straight':
            out.append(straight[i])
        elif style == 'curly':
            out.append(curly[i])
        else:
            out.append(ch)
    return ''.join(out)


def normalize_text(text, quotes='auto', reference=None):
    """normalize() for ordinary Python strings (astral characters allowed)."""
    return from_u16(normalize(to_u16(text), quotes, None if reference is None else to_u16(reference)))


class _UsageError(Exception):
    pass


def main(argv):
    file = quotes = reference = None
    write = False
    try:
        i = 0
        while i < len(argv):
            a = argv[i]
            if a == '--quotes' and quotes is None:
                i += 1
                quotes = argv[i] if i < len(argv) else ''
                if quotes not in ('auto', 'straight', 'curly'):
                    raise _UsageError('--quotes requires auto, straight or curly')
            elif a == '--reference' and reference is None:
                i += 1
                reference = argv[i] if i < len(argv) else ''
                if not reference or reference.startswith('--'):
                    raise _UsageError('--reference requires a file')
            elif a == '--write' and not write:
                write = True
            elif a.startswith('--'):
                raise _UsageError('unknown or repeated flag: %s' % a)
            elif file is None:
                file = a
            else:
                raise _UsageError('unexpected extra argument: %s' % a)
            i += 1
        if not file:
            raise _UsageError('usage: normalize-quotes.js <file> [--quotes auto|straight|curly] '
                              '[--reference original.md] [--write]')
        if reference and quotes and quotes != 'auto':
            raise _UsageError('--reference requires auto quotes')
        quotes = quotes or 'auto'
        try:
            source = read_file_utf8(file)
        except OSError as exc:
            raise _UsageError(node_fs_error(exc, file))
        if reference:
            try:
                ref_text = read_file_utf8(reference)
            except OSError as exc:
                raise _UsageError(node_fs_error(exc, reference))
        else:
            ref_text = source
        result = normalize(source, quotes, ref_text)
        if write:
            if result != source:
                try:
                    with open(file, 'wb') as fh:
                        fh.write(encode_utf8(result))
                except OSError as exc:
                    raise _UsageError(node_fs_error(exc, file))
            write_stderr('normalized %s (--quotes %s)\n' % (file, quotes))
        else:
            write_stdout(result)
    except _UsageError as exc:
        write_stderr('%s\n' % exc)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
