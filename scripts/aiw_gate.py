#!/usr/bin/env python3
"""Finding-count gate: a Python port of avoid-ai-writing bin/avoid-ai-writing-gate.js.

Ported from avoid-ai-writing v3.36.0
(https://github.com/conorbronsdon/avoid-ai-writing), MIT License,
Copyright (c) 2026 Conor Bronsdon.

Fails when any scanned file has more deterministic detector findings
(deduplicated issues, see aiw_detector) than the threshold. The composite
0-100 score is never used. --glob expands through `git ls-files`.

CLI (exit 0 all pass, 1 a file failed, 2 usage/glob/read/limit error):
    python3 aiw_gate.py [--glob <pattern>] [--threshold 6] [--context technical]
                        [--source-mode rendered-markdown] [--json] [--] [files...]

Standard library only; Python 3.9 compatible.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aiw_jscompat import js_stringify, js_trim, write_stderr, write_stdout  # noqa: E402
from aiw_detector import analyze_u16, read_input_fatal  # noqa: E402

USAGE = """Usage: avoid-ai-writing-gate [options] [files...]

Fails when any scanned file has more deterministic detector findings than
the configured threshold. This gate never uses the composite 0-100 score.

Options:
  --glob <pattern>                         Git glob to scan (for CI)
  --threshold <count>                     Maximum findings per file (default: 6)
  --context <general|technical|marketing|personal>  Detector context (default: technical)
  --source-mode <plain|rendered-markdown>  Source mode (default: rendered-markdown)
  --json                                   Emit machine-readable JSON on stdout
  -h, --help                               Show this help

Examples:
  avoid-ai-writing-gate --glob "**/*.md" --threshold 6
  avoid-ai-writing-gate --context technical README.md docs/guide.md
"""

CONTEXTS = ['general', 'technical', 'marketing', 'personal']
SOURCE_MODES = ['plain', 'rendered-markdown']
MAX_SAFE_INTEGER = 2 ** 53 - 1


def _parse_threshold(value):
    # /^\d+$/ then Number.isSafeInteger(Number(value)).
    if not value or any(c not in '0123456789' for c in value):
        return None
    digits = value.lstrip('0') or '0'
    if len(digits) > 16:
        return None
    num = int(digits)
    return num if num <= MAX_SAFE_INTEGER else None


def parse_args(argv):
    options = {'help': False, 'json': False, 'glob': None, 'threshold': 6, 'context': 'technical',
               'sourceMode': 'rendered-markdown', 'files': []}
    end_of_options = False
    i = 0
    while i < len(argv):
        arg = argv[i]
        if end_of_options:
            options['files'].append(arg)
        elif arg == '--':
            end_of_options = True
        elif arg in ('-h', '--help'):
            options['help'] = True
        elif arg == '--json':
            options['json'] = True
        elif arg in ('--glob', '--threshold', '--context', '--source-mode'):
            if i + 1 >= len(argv):
                return {'error': '%s requires a value' % arg}
            value = argv[i + 1]
            i += 1
            if arg == '--glob':
                options['glob'] = value
            elif arg == '--threshold':
                num = _parse_threshold(value)
                if num is None:
                    return {'error': 'invalid --threshold value: %s' % value}
                options['threshold'] = num
            elif arg == '--context':
                if value not in CONTEXTS:
                    return {'error': 'invalid --context value: %s' % value}
                options['context'] = value
            else:
                if value not in SOURCE_MODES:
                    return {'error': 'invalid --source-mode value: %s' % value}
                options['sourceMode'] = value
        elif arg.startswith('-') and arg != '-':
            return {'error': 'unknown option: %s' % arg}
        else:
            options['files'].append(arg)
        i += 1
    if not options['help'] and not options['glob'] and not options['files']:
        return {'error': 'provide at least one file or --glob'}
    return options


def files_from_glob(pattern, cwd=None):
    cmd = ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', ':(glob)' + pattern]
    try:
        result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as exc:
        import errno
        return {'error': 'cannot expand --glob with git: spawnSync git %s' % errno.errorcode.get(exc.errno, 'EIO')}
    if result.returncode != 0:
        detail = js_trim(result.stderr.decode('utf-8', 'replace'))
        return {'error': 'cannot expand --glob with git: %s' % (detail or 'git ls-files failed')}
    return {'files': [f for f in result.stdout.decode('utf-8', 'replace').split('\0') if f]}


def node_normalize(path):
    """path.posix.normalize."""
    if not path:
        return '.'
    is_absolute = path[0] == '/'
    trailing = path[-1] == '/'
    res = ''
    last_segment_length = 0
    last_slash = -1
    dots = 0
    code = ''
    n = len(path)
    for i in range(n + 1):
        if i < n:
            code = path[i]
        elif code == '/':
            break
        else:
            code = '/'
        if code == '/':
            if last_slash == i - 1 or dots == 1:
                pass
            elif dots == 2:
                if len(res) < 2 or last_segment_length != 2 or res[-1] != '.' or res[-2] != '.':
                    if len(res) > 2:
                        idx = res.rfind('/')
                        if idx == -1:
                            res = ''
                            last_segment_length = 0
                        else:
                            res = res[:idx]
                            last_segment_length = len(res) - 1 - res.rfind('/')
                        last_slash = i
                        dots = 0
                        continue
                    elif len(res) != 0:
                        res = ''
                        last_segment_length = 0
                        last_slash = i
                        dots = 0
                        continue
                if not is_absolute:
                    res = res + '/..' if res else '..'
                    last_segment_length = 2
            else:
                segment = path[last_slash + 1:i]
                res = res + '/' + segment if res else segment
                last_segment_length = i - last_slash - 1
            last_slash = i
            dots = 0
        elif code == '.' and dots != -1:
            dots += 1
        else:
            dots = -1
    if not res:
        if is_absolute:
            return '/'
        return './' if trailing else '.'
    if trailing:
        res += '/'
    return '/' + res if is_absolute else res


def main(argv):
    parsed = parse_args(argv)
    if 'error' in parsed:
        write_stderr('avoid-ai-writing-gate: %s\n\n%s' % (parsed['error'], USAGE))
        return 2
    if parsed['help']:
        write_stdout(USAGE)
        return 0
    files = list(parsed['files'])
    if parsed['glob']:
        expanded = files_from_glob(parsed['glob'])
        if 'error' in expanded:
            write_stderr('avoid-ai-writing-gate: %s\n' % expanded['error'])
            return 2
        files.extend(expanded['files'])
    unique = []
    seen = set()
    for f in files:
        f = node_normalize(f)
        if f not in seen:
            seen.add(f)
            unique.append(f)
    files = unique
    if not files:
        if parsed['json']:
            write_stdout(js_stringify({
                'schemaVersion': 1, 'threshold': parsed['threshold'], 'context': parsed['context'],
                'sourceMode': parsed['sourceMode'], 'pass': True, 'totalFindings': 0,
                'failedFiles': 0, 'files': [],
            }, 2) + '\n')
            return 0
        write_stdout('avoid-ai-writing-gate: no matching files; nothing to scan\n')
        return 0
    failed = False
    total = 0
    failed_files = 0
    entries = []
    for file in files:
        text, error = read_input_fatal(file, file)
        if error:
            write_stderr('avoid-ai-writing-gate: %s\n' % error)
            return 2
        result = analyze_u16(text, parsed['context'], parsed['sourceMode'])
        if result.get('tooLong'):
            wc = result.get('stats', {}).get('wordCount')
            detail = ' (%d words)' % wc if isinstance(wc, int) else ''
            write_stderr('avoid-ai-writing-gate: cannot scan %s: detector limit exceeded%s\n' % (file, detail))
            return 2
        if result.get('unsupportedScript'):
            write_stderr('avoid-ai-writing-gate: cannot scan %s: unsegmented-script document '
                         '(no inter-word spaces to count)\n' % file)
            return 2
        count = len(result['issues'])
        types = sorted(set(i['type'] for i in result['issues']))
        over = count > parsed['threshold']
        if over:
            failed = True
            failed_files += 1
        total += count
        entries.append({'path': file.replace(os.sep, '/'), 'findings': count, 'pass': not over, 'types': types})
        if not parsed['json']:
            summary = ' [%s]' % ', '.join(types) if types else ''
            write_stdout('%s %s — %d finding(s), threshold %d%s\n' % (
                'FAIL' if over else 'PASS', file, count, parsed['threshold'], summary))
    if parsed['json']:
        write_stdout(js_stringify({
            'schemaVersion': 1, 'threshold': parsed['threshold'], 'context': parsed['context'],
            'sourceMode': parsed['sourceMode'], 'pass': not failed, 'totalFindings': total,
            'failedFiles': failed_files, 'files': entries,
        }, 2) + '\n')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
