#!/usr/bin/env python3
"""Preservation validator: a Python port of avoid-ai-writing detector/validate.js.

Ported from avoid-ai-writing v3.36.0
(https://github.com/conorbronsdon/avoid-ai-writing), MIT License,
Copyright (c) 2026 Conor Bronsdon.

Checks that a rewrite left alone what it had no business touching: fenced
code, YAML frontmatter, blockquotes, tables, inline code, URLs (AI tracking
parameters ignored), paths, heading structure, figures, volume, and that it
did not add detector findings (residual check via aiw_detector).

Library use:
    from aiw_validate import validate, format_result
    print(format_result(validate(before, after)))

CLI (exit 0 pass, 1 preservation error, 2 usage):
    python3 aiw_validate.py <original-file> <rewritten-file>

Standard library only; Python 3.9 compatible.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiw_jscompat import (  # noqa: E402
    UNDEFINED, exec_all, from_u16, js_re, js_round, js_trim, js_trim_end, js_truthy,
    node_fs_error, read_file_utf8, to_u16, write_stderr, write_stdout,
)

INLINE_CODE = js_re(r'`[^`\n]+`', 'g')
YAML_FRONTMATTER = js_re(r'^---\n[\s\S]*?\n---(?=\n|$)', '')
BLOCKQUOTE_BLOCK = js_re(r'(?:^[ \t]*>[^\n]*(?:\n[ \t]*>[^\n]*)*)', 'gm')
MD_HEADING = js_re(r'^(#{1,6})[ \t]+(.+?)[ \t]*$', 'gm')
URL = js_re(r'''https?:\/\/[^\s)>\]"'`]+''', 'g')
MD_LINK_TARGET = js_re(r'\[[^\]\n]*\]\(([^)\s]+)[^)]*\)', 'g')
PATH = js_re(r'(?:^|[\s(])((?:\.{0,2}\/)[A-Za-z0-9._~\-]+(?:\/[A-Za-z0-9._~\-]+)*|[A-Za-z]:\\[A-Za-z0-9._\\~\-]+)', 'g')
NUMBER = js_re(r'\b\d[\d,]*(?:\.\d+)?%?\b', 'g')
AI_URL_PARAM = js_re(r'^(?:utm_source=(?:chatgpt\.com|openai(?:\.com)?|copilot\.com|claude\.ai|perplexity\.ai|gemini\.google\.com|grok\.com)|referrer=grok\.com)$', 'i')

RE_FENCE_MARKER = js_re(r'^[ \t]{0,3}(`{3,}|~{3,})', '')
RE_FENCE_CLOSE_TAIL = js_re(r'^[ \t]*\r?$', '')
RE_URL_PUNCTUATION = js_re('(?:[–—…][^&=%]*|[.,;:!?*_~|]+)$', '')
RE_INDENT4 = js_re(r'^(?: {4}|\t)', '')
RE_DELIM_CELL = js_re(r'^:?-+:?$', '')
RE_PIPE_PAD = js_re(r'\s*\|\s*', 'g')
RE_DASH_RUN = js_re(r'-{2,}', 'g')
RE_QUOTE_MARKER = js_re(r'^[ \t]*>[ \t]?', '')
RE_INDENTED = js_re(r'^(?: {4}|\t)\S', '')
RE_BLANK = js_re(r'^\s*$', '')
RE_LIST_ITEM = js_re(r'^\s*(?:[-*+]|\d+[.)])\s', '')
RE_WORD_RUN = js_re(r'\S+', 'g')


def fence_spans(text):
    spans = []
    cursor = 0
    open_fence = None
    for line in text.split('\n'):
        marker = RE_FENCE_MARKER.search(line)
        if open_fence is None:
            # CommonMark forbids backticks in the info string of a backtick fence.
            if marker and not (marker.group(1)[0] == '`' and '`' in line[len(marker.group(0)):]):
                open_fence = (marker.group(1)[0], len(marker.group(1)), cursor)
        elif (marker and marker.group(1)[0] == open_fence[0]
              and len(marker.group(1)) >= open_fence[1]
              and RE_FENCE_CLOSE_TAIL.search(line[len(marker.group(0)):])):
            spans.append((open_fence[2], cursor + len(line)))
            open_fence = None
        cursor += len(line) + 1
    if open_fence is not None:
        spans.append((open_fence[2], len(text)))
    return spans


def fence_block_texts(text):
    return [text[a:b] for a, b in fence_spans(text)]


def extract_all(rx, text):
    out = []
    for m in exec_all(rx, text):
        if rx.groups >= 1 and m.group(1) is not None:
            out.append(m.group(1))
        else:
            out.append(m.group(0))
    return out


def mask_code(text):
    """Fenced code blanked (newlines kept), then inline code spans as spaces."""
    out = list(text)
    for start, end in fence_spans(text):
        for i in range(start, end):
            if out[i] != '\n':
                out[i] = ' '
    joined = ''.join(out)
    parts = []
    last = 0
    for m in exec_all(INLINE_CODE, joined):
        parts.append(joined[last:m.start()])
        parts.append(' ' * (m.end() - m.start()))
        last = m.end()
    parts.append(joined[last:])
    return ''.join(parts)


def normalize_url(u):
    query_start = u.find('?')
    fragment_start = u.find('#')
    if query_start == -1 or (fragment_start != -1 and fragment_start < query_start):
        return u
    query_end = len(u) if fragment_start == -1 else fragment_start
    query = u[query_start + 1:query_end]
    suffix = u[query_end:]
    if query_start == len(u) - 1:
        return u
    if query_end == len(u):
        pm = RE_URL_PUNCTUATION.search(query)
        punctuation = pm.group(0) if pm else ''
        without = query[:len(query) - len(punctuation)]
        final_param = without[without.rfind('&') + 1:]
        if punctuation and AI_URL_PARAM.search(final_param):
            query = without
            suffix = punctuation
    params = query.split('&')
    kept = [p for p in params if p != '' and not AI_URL_PARAM.search(p)]
    if len(kept) == len(params):
        return u
    if kept:
        return u[:query_start] + '?' + '&'.join(kept) + suffix
    return u[:query_start] + suffix


def table_cells(line):
    if RE_INDENT4.search(line):
        return None
    trimmed = js_trim(line)
    separators = []
    for i, ch in enumerate(trimmed):
        if ch != '|':
            continue
        slashes = 0
        j = i - 1
        while j >= 0 and trimmed[j] == '\\':
            slashes += 1
            j -= 1
        if slashes % 2 == 0:
            separators.append(i)
    if not separators:
        return None
    cells = []
    start = 1 if separators[0] == 0 else 0
    for sep in separators:
        if sep < start:
            continue
        cells.append(trimmed[start:sep])
        start = sep + 1
    if start < len(trimmed):
        cells.append(trimmed[start:])
    return cells


def is_table_delimiter(line):
    cells = table_cells(line)
    return (cells is not None and len(cells) > 0
            and all(RE_DELIM_CELL.search(js_trim(c)) for c in cells))


def extract_table_blocks(text):
    lines = text.split('\n')
    blocks = []
    i = 1
    while i < len(lines):
        header = table_cells(lines[i - 1])
        delimiter = table_cells(lines[i])
        if not header or not is_table_delimiter(lines[i]) or len(header) != len(delimiter):
            i += 1
            continue
        end = i
        while end + 1 < len(lines) and table_cells(lines[end + 1]):
            end += 1
        blocks.append('\n'.join(lines[i - 1:end + 1]))
        i = end + 1
    return blocks


def _replace_all(rx, text, repl):
    parts = []
    last = 0
    for m in exec_all(rx, text):
        parts.append(text[last:m.start()])
        parts.append(repl)
        last = m.end()
    parts.append(text[last:])
    return ''.join(parts)


def normalize_table(block):
    rows = []
    for index, row in enumerate(block.split('\n')):
        normalized = _replace_all(RE_PIPE_PAD, js_trim(row), '|')
        rows.append(_replace_all(RE_DASH_RUN, normalized, '-') if index == 1 else normalized)
    return '\n'.join(rows)


def normalize_quote(block):
    lines = [js_trim_end(RE_QUOTE_MARKER.sub('', line, count=1)) for line in block.split('\n')]
    return js_trim_end('\n'.join(lines))


def extract_indented_blocks(text):
    blocks = []
    current = None
    in_list = False
    for line in text.split('\n'):
        is_indented = bool(RE_INDENTED.search(line))
        is_blank = bool(RE_BLANK.search(line))
        if RE_LIST_ITEM.search(line):
            in_list = True
        elif not is_blank and not is_indented:
            in_list = False
        if is_indented and not in_list:
            if current is None:
                current = []
            current.append(line)
        elif not is_blank and current is not None:
            blocks.append('\n'.join(current))
            current = None
    if current is not None:
        blocks.append('\n'.join(current))
    return blocks


def missing_from(a, b):
    """Items present in `a` more often than in `b`, in `a`'s order."""
    have = {}
    for item in b:
        have[item] = have.get(item, 0) + 1
    out = []
    for item in a:
        n = have.get(item, 0)
        if n == 0:
            out.append(item)
        else:
            have[item] = n - 1
    return out


def sample(items, n=5):
    shown = ', '.join(items[:n])
    return shown + (' (+%d more)' % (len(items) - n) if len(items) > n else '')


def word_count(text):
    return len(exec_all(RE_WORD_RUN, js_trim(mask_code(text))))


def _is_nullish(v):
    return v is None or v is UNDEFINED


def validate_u16(original, rewritten, skip_residual=UNDEFINED, max_shrink_ratio=UNDEFINED):
    """validate() over u16 strings (see aiw_jscompat)."""
    if not isinstance(original, str) or not isinstance(rewritten, str):
        raise TypeError('validate(original, rewritten): both arguments must be strings')
    errors = []
    warnings = []

    def err(code, message):
        errors.append({'code': code, 'message': message})

    def warn(code, message):
        warnings.append({'code': code, 'message': message})

    original = original.replace('\r\n', '\n')
    rewritten = rewritten.replace('\r\n', '\n')

    orig_fenced = fence_block_texts(original)
    new_fenced = fence_block_texts(rewritten)
    if len(orig_fenced) != len(new_fenced):
        err('code-block-count', 'Fenced code blocks changed in number: %d → %d.' % (len(orig_fenced), len(new_fenced)))
    else:
        changed = next((i for i, block in enumerate(orig_fenced) if block != new_fenced[i]), -1)
        if changed != -1:
            err('code-block-modified', 'Fenced code block #%d was modified.' % (changed + 1))

    orig_yaml = YAML_FRONTMATTER.search(original)
    new_yaml = YAML_FRONTMATTER.search(rewritten)
    if (orig_yaml.group(0) if orig_yaml else None) != (new_yaml.group(0) if new_yaml else None):
        err('frontmatter-modified', 'YAML frontmatter was modified, added, or removed.')

    orig_prose = mask_code(original)
    new_prose = mask_code(rewritten)

    lost_quotes = missing_from([normalize_quote(q) for q in extract_all(BLOCKQUOTE_BLOCK, orig_prose)],
                               [normalize_quote(q) for q in extract_all(BLOCKQUOTE_BLOCK, new_prose)])
    if lost_quotes:
        err('blockquote-modified', 'Blockquote content was modified or removed (%d block(s)). '
            'Quoted material is attributed to someone else.' % len(lost_quotes))

    lost_tables = missing_from([normalize_table(t) for t in extract_table_blocks(orig_prose)],
                               [normalize_table(t) for t in extract_table_blocks(new_prose)])
    if lost_tables:
        err('table-modified', 'Markdown table content was modified or removed (%d table(s)).' % len(lost_tables))

    lost_inline = missing_from(extract_all(INLINE_CODE, original), extract_all(INLINE_CODE, rewritten))
    if lost_inline:
        err('inline-code-missing', 'Inline code removed: %s' % sample(lost_inline))

    orig_urls = [normalize_url(u) for u in extract_all(URL, orig_prose) + extract_all(MD_LINK_TARGET, orig_prose)]
    new_urls = [normalize_url(u) for u in extract_all(URL, new_prose) + extract_all(MD_LINK_TARGET, new_prose)]
    lost_urls = missing_from(orig_urls, new_urls)
    if lost_urls:
        err('url-missing', 'URL removed or altered: %s' % sample(lost_urls))

    lost_paths = missing_from(extract_all(PATH, orig_prose), extract_all(PATH, new_prose))
    if lost_paths:
        err('path-missing', 'File path removed or altered: %s' % sample(lost_paths))

    orig_headings = [(len(m.group(1)), m.group(2)) for m in exec_all(MD_HEADING, original)]
    new_headings = [(len(m.group(1)), m.group(2)) for m in exec_all(MD_HEADING, rewritten)]
    if len(orig_headings) != len(new_headings):
        err('heading-count', 'Heading count changed: %d → %d. Restructuring the document is out of '
            'scope for a rewrite.' % (len(orig_headings), len(new_headings)))
    else:
        drift = next((i for i, h in enumerate(orig_headings) if h[0] != new_headings[i][0]), -1)
        if drift != -1:
            err('heading-level', 'Heading nesting changed at heading #%d: h%d → h%d.' % (
                drift + 1, orig_headings[drift][0], new_headings[drift][0]))
        reworded = [h for i, h in enumerate(orig_headings) if h[1] != new_headings[i][1]]
        if reworded:
            warn('heading-text', '%d heading(s) reworded. Expected when fixing Title Case or removing '
                 'emoji; check nothing else moved.' % len(reworded))

    lost_numbers = missing_from(extract_all(NUMBER, orig_prose), extract_all(NUMBER, new_prose))
    if lost_numbers:
        warn('number-missing', 'Figures present in the original are absent from the rewrite: %s. '
             'Legitimate when a numeral was spelled out; a fabrication risk otherwise.' % sample(lost_numbers))

    orig_words = word_count(original)
    new_words = word_count(rewritten)
    max_shrink = 0.4 if _is_nullish(max_shrink_ratio) else max_shrink_ratio
    if orig_words > 0 and new_words / orig_words < 1 - max_shrink:
        warn('large-shrink', 'Rewrite dropped %d%% of the words (%d → %d). Check for lost content.' % (
            js_round((1 - new_words / orig_words) * 100), orig_words, new_words))

    residual = None
    if not js_truthy(skip_residual):
        import aiw_detector
        before = aiw_detector.analyze_u16(original)
        after = aiw_detector.analyze_u16(rewritten)
        residual = {
            'issuesBefore': len(before['issues']),
            'issuesAfter': len(after['issues']),
            'scoreBefore': before['score'],
            'scoreAfter': after['score'],
        }
        if len(after['issues']) > len(before['issues']):
            err('residual-grew', 'Rewrite introduced AI patterns: %d → %d flagged issues. A rewrite may '
                'leave patterns behind; it may not add them.' % (len(before['issues']), len(after['issues'])))

    return {
        'ok': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'stats': {
            'wordsBefore': orig_words,
            'wordsAfter': new_words,
            'fencedBlocks': len(orig_fenced),
            'headings': len(orig_headings),
            'indentedBlocks': len(extract_indented_blocks(original)),
            'residual': residual,
        },
    }


def _py(value):
    if isinstance(value, str):
        return from_u16(value)
    if isinstance(value, list):
        return [_py(v) for v in value]
    if isinstance(value, dict):
        return dict((k, _py(v)) for k, v in value.items())
    return value


def validate(original, rewritten, skip_residual=False, max_shrink_ratio=None):
    """Port of validate(original, rewritten, {skipResidual, maxShrinkRatio})."""
    if isinstance(original, str):
        original = to_u16(original)
    if isinstance(rewritten, str):
        rewritten = to_u16(rewritten)
    return _py(validate_u16(original, rewritten, skip_residual, max_shrink_ratio))


def format_result(result):
    lines = ['PASS — preservation checks clear' if result['ok']
             else 'FAIL — %d preservation error(s)' % len(result['errors'])]
    for e in result['errors']:
        lines.append('  error   [%s] %s' % (e['code'], e['message']))
    for w in result['warnings']:
        lines.append('  warning [%s] %s' % (w['code'], w['message']))
    return '\n'.join(lines)


def main(argv):
    orig_path = argv[0] if len(argv) > 0 else ''
    new_path = argv[1] if len(argv) > 1 else ''
    if not orig_path or not new_path:
        write_stderr('usage: node detector/validate.js <original-file> <rewritten-file>\n')
        return 2
    texts = []
    for p in (orig_path, new_path):
        try:
            texts.append(read_file_utf8(p))
        except OSError as exc:
            # Node dies here with an uncaught exception (exit 1, stack trace).
            write_stderr('Error: %s\n' % node_fs_error(exc, p))
            return 1
    result = validate_u16(texts[0], texts[1])
    write_stdout(format_result(result) + '\n')
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
