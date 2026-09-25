#!/usr/bin/env python3
"""Parity check: the Python ports in scripts/ against the vendored JavaScript.

    python3 tests/parity/run_parity.py [--tool NAME ...] [--jobs N] [--show N] [--skip-api] [--skip-cli]

Two layers, both compared exactly:

* library level: every call recorded from the upstream test suites
  (fixtures/api/*.jsonl) is replayed through tools/api_driver.js and
  tools/api_driver.py; the JSON.stringify output of each result must match.
* CLI level: the JS CLI and the Python CLI run with the same argv, stdin, cwd
  and files. stdout, stderr and the exit code must match. For the detector
  and `check-style --json`, stdout must also be deep-equal JSON (key order
  included). Files a CLI writes (--write) are compared byte for byte.

Tools: detector, validate, quotes, style, gate (plus markdown, library only).
Requires node on PATH. Exit code 0 when every comparison matches.
"""

import argparse
import base64
import gzip
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SCRIPTS = os.path.join(ROOT, 'scripts')
UPSTREAM = os.path.join(SCRIPTS, 'upstream')
FIXTURES = os.path.join(HERE, 'fixtures')
TOOLS = os.path.join(HERE, 'tools')

CLIS = {
    'detector': (os.path.join(UPSTREAM, 'bin', 'avoid-ai-writing.js'), os.path.join(SCRIPTS, 'aiw_detector.py')),
    'validate': (os.path.join(UPSTREAM, 'detector', 'validate.js'), os.path.join(SCRIPTS, 'aiw_validate.py')),
    'quotes': (os.path.join(UPSTREAM, 'scripts', 'normalize-quotes.js'), os.path.join(SCRIPTS, 'aiw_quotes.py')),
    'style': (os.path.join(UPSTREAM, 'scripts', 'check-style.js'), os.path.join(SCRIPTS, 'aiw_style.py')),
    'gate': (os.path.join(UPSTREAM, 'bin', 'avoid-ai-writing-gate.js'), os.path.join(SCRIPTS, 'aiw_gate.py')),
}
API_TOOL = {
    'detector/patterns.js:analyzeText': 'detector',
    'detector/validate.js:validate': 'validate',
    'scripts/markdown-prose.js:markdownProse': 'markdown',
    'scripts/normalize-quotes.js:normalize': 'quotes',
    'scripts/normalize-quotes.js:inferQuotes': 'quotes',
    'scripts/check-style.js:check': 'style',
}
DETECTOR_MODES = [[], ['--context', 'technical'], ['--source-mode', 'rendered-markdown'],
                  ['--context', 'technical', '--source-mode', 'rendered-markdown']]
STYLE_CONFIGS = {
    'all-straight.json': {'name': 'All straight', 'mechanics': {
        'quotes': 'straight', 'headings': 'sentence', 'latinAbbrev': 'parentheses',
        'emDash': 'sparing', 'spellNumbersUpTo': 10, 'serialComma': True}},
    'all-curly.json': {'mechanics': {
        'quotes': 'curly', 'headings': 'title', 'latinAbbrev': 'never',
        'emDash': 'deliberate', 'spellNumbersUpTo': 999}},
}
ENV = dict(os.environ, NODE_OPTIONS='', PYTHONIOENCODING='utf-8')


# ─── fixtures ──────────────────────────────────────────────────────────────

def load_api_calls():
    lines = []
    with open(os.path.join(FIXTURES, 'api', 'calls.jsonl'), encoding='utf-8') as fh:
        lines += [l.rstrip('\n') for l in fh if l.strip()]
    large = os.path.join(FIXTURES, 'api', 'calls_large.jsonl.gz')
    if os.path.exists(large):
        with gzip.open(large, 'rt', encoding='utf-8') as fh:
            lines += [l.rstrip('\n') for l in fh if l.strip()]
    return lines


def text_fixtures():
    out = []
    base = os.path.join(FIXTURES, 'texts')
    for dirpath, _, names in os.walk(base):
        for n in sorted(names):
            path = os.path.join(dirpath, n)
            with open(path, 'rb') as fh:
                out.append((os.path.relpath(path, base), fh.read()))
    out.sort()
    return out


def encodable(s):
    try:
        return s.encode('utf-8')
    except UnicodeEncodeError:
        return None  # lone surrogates cannot live in a UTF-8 file


# ─── library level ─────────────────────────────────────────────────────────

def run_api(lines, tools, show):
    tmp = tempfile.mkdtemp(prefix='aiw-api-')
    try:
        path = os.path.join(tmp, 'calls.jsonl')
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(lines) + '\n')
        js = subprocess.run(['node', os.path.join(TOOLS, 'api_driver.js'), path], env=ENV,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        py = subprocess.run([sys.executable, os.path.join(TOOLS, 'api_driver.py'), path], env=ENV,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if js.returncode or py.returncode:
        print('api driver failed:\n', js.stderr.decode()[-2000:], py.stderr.decode()[-2000:])
    jl = js.stdout.decode('utf-8').split('\n')
    pl = py.stdout.decode('utf-8').split('\n')
    results = {}
    for i, line in enumerate(lines):
        tool = API_TOOL[json.loads(line)['fn']]
        if tools and tool not in tools and not (tool == 'markdown' and ('quotes' in tools or 'style' in tools)):
            continue
        a = jl[i] if i < len(jl) else None
        b = pl[i] if i < len(pl) else None
        stat = results.setdefault(tool, [0, []])
        stat[0] += 1
        if a != b:
            stat[1].append({'call': line[:400], 'js': (a or '')[:1200], 'py': (b or '')[:1200]})
    return results


# ─── CLI level ─────────────────────────────────────────────────────────────

def materialize(directory, files):
    for name, content in files.items():
        path = os.path.join(directory, name)
        os.makedirs(os.path.dirname(path) or directory, exist_ok=True)
        if isinstance(content, dict):
            data = base64.b64decode(content['b64'])
        elif isinstance(content, bytes):
            data = content
        else:
            data = content.encode('utf-8')
        with open(path, 'wb') as fh:
            fh.write(data)


def run_one(argv, cwd, stdin):
    proc = subprocess.run(argv, cwd=cwd, env=ENV, input=stdin if stdin is not None else b'',
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def ordered_json(data):
    try:
        return json.loads(data.decode('utf-8'), object_pairs_hook=lambda pairs: ('obj', pairs))
    except ValueError:
        return ('unparseable', data)


def run_case(case):
    tool = case['tool']
    js_cli, py_cli = CLIS[tool]
    stdin = case.get('stdin')
    stdin = stdin.encode('utf-8') if isinstance(stdin, str) else stdin
    outcomes = []
    for argv0 in (['node', js_cli], [sys.executable, py_cli]):
        if case.get('cwd') == 'glob':
            cwd, tmp = os.path.join(FIXTURES, 'gate_glob'), None
        else:
            tmp = tempfile.mkdtemp(prefix='aiw-cli-')
            cwd = tmp
            materialize(tmp, case.get('files') or {})
        try:
            code, out, err = run_one(argv0 + case['args'], cwd, stdin)
            written = {}
            for name in case.get('compare_files') or []:
                path = os.path.join(cwd, name)
                written[name] = open(path, 'rb').read() if os.path.exists(path) else None
        finally:
            if tmp:
                shutil.rmtree(tmp, ignore_errors=True)
        outcomes.append((code, out, err, written))
    (jc, jo, je, jw), (pc, po, pe, pw) = outcomes
    problems = []
    if jc != pc:
        problems.append('exit %s vs %s' % (jc, pc))
    if jo != po:
        problems.append('stdout differs')
    if case.get('json') and ordered_json(jo) != ordered_json(po):
        problems.append('JSON not deep-equal')
    if case.get('stderr') == 'error-line':
        # Node dies with an uncaught exception here; compare its "Error: ..." line only.
        js_line = next((l for l in je.decode('utf-8', 'replace').split('\n') if l.startswith('Error: ')), None)
        if js_line is None or pe.decode('utf-8', 'replace').split('\n')[0] != js_line:
            problems.append('error line differs')
    elif je != pe:
        problems.append('stderr differs')
    if jw != pw:
        problems.append('written files differ')
    if not problems:
        return None
    return {'case': case['name'], 'args': case['args'], 'problems': problems,
            'js': {'exit': jc, 'stdout': jo[:800].decode('utf-8', 'replace'), 'stderr': je[:600].decode('utf-8', 'replace')},
            'py': {'exit': pc, 'stdout': po[:800].decode('utf-8', 'replace'), 'stderr': pe[:600].decode('utf-8', 'replace')}}


def bulk_cases(api_lines):
    cases = []
    texts = text_fixtures()
    # Detector: every text fixture in all four modes, plus the string inputs the
    # upstream detector tests pass to analyzeText (with their CLI-valid options).
    for name, data in texts:
        for mode in DETECTOR_MODES:
            cases.append({'tool': 'detector', 'name': '%s %s' % (name, ' '.join(mode)), 'json': True,
                          'args': mode + ['input.txt'], 'files': {'input.txt': data}})
    seen = set()
    validate_pairs = []
    for line in api_lines:
        call = json.loads(line)
        args = call['args']
        if call['fn'].endswith('analyzeText') and args and isinstance(args[0], str):
            data = encodable(args[0])
            opts = args[1] if len(args) > 1 and isinstance(args[1], dict) else {}
            mode = []
            if opts.get('contextMode') in ('general', 'technical', 'marketing', 'personal'):
                mode += ['--context', opts['contextMode']]
            if opts.get('sourceMode') in ('plain', 'rendered-markdown'):
                mode += ['--source-mode', opts['sourceMode']]
            key = (data, tuple(mode))
            if data is None or key in seen or len(data) > 400000:
                continue
            seen.add(key)
            cases.append({'tool': 'detector', 'name': 'test input %d %s' % (len(seen), ' '.join(mode)), 'json': True,
                          'args': mode + ['input.txt'], 'files': {'input.txt': data}})
        if call['fn'].endswith('validate') and len(args) >= 2 and all(isinstance(a, str) for a in args[:2]):
            a, b = encodable(args[0]), encodable(args[1])
            if a is not None and b is not None:
                validate_pairs.append(('test pair %d' % len(validate_pairs), a, b))
    # Validate: recorded pairs, and deterministic rewrites of every text fixture.
    for name, data in texts:
        text = data.decode('utf-8', 'replace')
        paras = text.split('\n\n')
        validate_pairs.append((name + ' identical', data, data))
        validate_pairs.append((name + ' reversed paragraphs', data, '\n\n'.join(reversed(paras)).encode('utf-8')))
        validate_pairs.append((name + ' edited', data, text.replace('`', '').replace('https://', 'http://')
                               .replace('## ', '# ').replace('the ', '').encode('utf-8')))
    for name, a, b in validate_pairs:
        cases.append({'tool': 'validate', 'name': name, 'args': ['before.md', 'after.md'],
                      'files': {'before.md': a, 'after.md': b}})
    # Quotes: every text fixture in each mode, and auto against the next fixture as reference.
    for i, (name, data) in enumerate(texts):
        ref = texts[(i + 1) % len(texts)][1]
        for q in (['--quotes', 'auto'], ['--quotes', 'straight'], ['--quotes', 'curly'], ['--reference', 'ref.md']):
            cases.append({'tool': 'quotes', 'name': '%s %s' % (name, ' '.join(q)), 'args': ['doc.md'] + q,
                          'files': {'doc.md': data, 'ref.md': ref}})
    # Style: every text fixture against both example configs and two full custom configs.
    cfg_files = dict((k, json.dumps(v)) for k, v in STYLE_CONFIGS.items())
    for name, data in texts:
        for cfg in ('technical', 'prose', 'all-straight.json', 'all-curly.json'):
            for extra in ([], ['--json']):
                files = dict(cfg_files)
                files['doc.md'] = data
                cases.append({'tool': 'style', 'name': '%s %s %s' % (name, cfg, ' '.join(extra)),
                              'json': bool(extra), 'args': ['doc.md', '--config', cfg] + extra, 'files': files})
    # Gate: every text fixture, text and JSON output.
    for name, data in texts:
        cases.append({'tool': 'gate', 'name': name, 'args': ['doc.md'], 'files': {'doc.md': data}})
        cases.append({'tool': 'gate', 'name': name + ' json general plain',
                      'args': ['--json', '--threshold', '0', '--context', 'general', '--source-mode', 'plain', 'doc.md'],
                      'files': {'doc.md': data}})
    return cases


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--tool', action='append', choices=sorted(CLIS) + ['markdown'])
    ap.add_argument('--jobs', type=int, default=os.cpu_count() or 4)
    ap.add_argument('--show', type=int, default=3, help='mismatches to print per tool')
    ap.add_argument('--skip-api', action='store_true')
    ap.add_argument('--skip-cli', action='store_true')
    args = ap.parse_args()
    tools = set(args.tool or [])

    api_lines = load_api_calls()
    summary = {}
    if not args.skip_api:
        for tool, (n, bad) in sorted(run_api(api_lines, tools, args.show).items()):
            summary['%s (library)' % tool] = (n, bad)

    if not args.skip_cli:
        spec = json.load(open(os.path.join(FIXTURES, 'cli_cases.json'), encoding='utf-8'))
        cases = []
        for case in spec['cases']:
            if isinstance(case['files'], str):
                case['files'] = spec['filesets'][case['files']]
            case['json'] = case['tool'] == 'detector' or (case['tool'] == 'style' and '--json' in case['args'])
            cases.append(case)
        cases += bulk_cases(api_lines)
        cases = [c for c in cases if not tools or c['tool'] in tools]
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(run_case, cases))
        for case, res in zip(cases, results):
            stat = summary.setdefault('%s (CLI)' % case['tool'], (0, []))
            summary['%s (CLI)' % case['tool']] = (stat[0] + 1, stat[1] + ([res] if res else []))

    failed = 0
    print('%-22s %9s %11s' % ('check', 'compared', 'mismatches'))
    for key in sorted(summary):
        n, bad = summary[key]
        failed += len(bad)
        print('%-22s %9d %11d' % (key, n, len(bad)))
    for key in sorted(summary):
        for item in summary[key][1][:args.show]:
            print('\n--- %s mismatch' % key)
            print(json.dumps(item, indent=1, ensure_ascii=False)[:4000])
    print('\n%s' % ('PARITY OK' if failed == 0 else 'PARITY FAILED: %d mismatch(es)' % failed))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
