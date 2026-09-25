#!/usr/bin/env python3
"""Rebuild tests/parity/fixtures/ from an avoid-ai-writing checkout.

    python3 build_fixtures.py /path/to/avoid-ai-writing

1. Runs the upstream test suites under node with record_hook.js preloaded and
   keeps every distinct library call they make (analyzeText, validate,
   markdownProse, normalize, inferQuotes, check) as api/calls.jsonl (small)
   and api/calls_large.jsonl.gz (performance-sized inputs).
2. Copies documents: the `source` fields of evals/rewrite/cases.json, the
   upstream README/CHANGELOG/SKILL/references/patterns.md (chunked under
   10000 words, plus the unchunked originals as too-long cases) and the
   writing-craft references (English and German).
3. Writes hand-made edge cases (CRLF, BOM, astral characters, CJK, empty,
   too short, too long, invalid UTF-8, ...) and cli_cases.json, the
   argument/error cases mirrored from the upstream CLI tests.
"""

import base64
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PARITY = os.path.dirname(HERE)
FIXTURES = os.path.join(PARITY, 'fixtures')
SKILL_ROOT = os.path.dirname(os.path.dirname(PARITY))

TEST_SUITES = [
    'detector/patterns.test.js',
    'detector/validate.test.js',
    'scripts/normalize-quotes.test.js',
    'scripts/check-style.test.js',
    'bin/avoid-ai-writing.test.js',
    'bin/avoid-ai-writing-gate.test.js',
]
LARGE_LINE = 20000


def record_calls(upstream):
    seen = set()
    small, large = [], []
    tmp = tempfile.mkdtemp(prefix='aiw-record-')
    try:
        for suite in TEST_SUITES:
            out = os.path.join(tmp, suite.replace('/', '_') + '.jsonl')
            open(out, 'w').close()
            env = dict(os.environ, AIW_RECORD=out,
                       NODE_OPTIONS='-r ' + os.path.join(HERE, 'record_hook.js'))
            proc = subprocess.run(['node', suite], cwd=upstream, env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print('%-40s exit %d' % (suite, proc.returncode))
            with open(out, encoding='utf-8') as fh:
                for line in fh:
                    line = line.strip()
                    if not line or '__non_serializable__' in line:
                        continue
                    key = hashlib.sha1(line.encode('utf-8', 'surrogatepass')).hexdigest()
                    if key in seen:
                        continue
                    seen.add(key)
                    (large if len(line) > LARGE_LINE else small).append(line)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(os.path.join(FIXTURES, 'api'), exist_ok=True)
    with open(os.path.join(FIXTURES, 'api', 'calls.jsonl'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(small) + '\n')
    with gzip.open(os.path.join(FIXTURES, 'api', 'calls_large.jsonl.gz'), 'wt', encoding='utf-8') as fh:
        fh.write('\n'.join(large) + '\n')
    print('api calls: %d small, %d large' % (len(small), len(large)))


def chunk_words(text, limit=8000):
    """Split at blank lines into chunks of fewer than `limit` words."""
    paragraphs = text.split('\n\n')
    chunks, cur, count = [], [], 0
    for p in paragraphs:
        n = len(p.split())
        if cur and count + n >= limit:
            chunks.append('\n\n'.join(cur) + '\n')
            cur, count = [], 0
        cur.append(p)
        count += n
    if cur:
        chunks.append('\n\n'.join(cur))
    return chunks


def write_text(rel, content):
    path = os.path.join(FIXTURES, 'texts', rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = content if isinstance(content, bytes) else content.encode('utf-8')
    with open(path, 'wb') as fh:
        fh.write(data)


def copy_documents(upstream):
    cases = json.load(open(os.path.join(upstream, 'evals', 'rewrite', 'cases.json'), encoding='utf-8'))
    for case in cases:
        write_text('evals/%s.txt' % case['id'], case['source'])
    for rel in ('README.md', 'CHANGELOG.md', 'SKILL.md', 'references/patterns.md'):
        text = open(os.path.join(upstream, rel), encoding='utf-8').read()
        base = 'upstream-' + rel.replace('/', '-')[:-3]
        chunks = chunk_words(text)
        for i, chunk in enumerate(chunks):
            write_text('docs/%s.part%d.md' % (base, i + 1), chunk)
        if len(chunks) > 1:
            write_text('docs/%s.full.md' % base, text)
    refs = os.path.join(SKILL_ROOT, 'references')
    for name in sorted(os.listdir(refs)):
        if not name.endswith('.md'):
            continue
        text = open(os.path.join(refs, name), encoding='utf-8').read()
        chunks = chunk_words(text)
        for i, chunk in enumerate(chunks):
            write_text('refs/%s.part%d.md' % (name[:-3], i + 1), chunk)
        if len(chunks) > 1:
            write_text('refs/%s.full.md' % name[:-3], text)


AI_PARA = ("In today's rapidly evolving landscape, we delve into a robust and comprehensive "
           "tapestry of ideas. Moreover, it is important to note that this is a testament to "
           "innovation — truly a game-changer for the ecosystem. Experts believe the future "
           "looks bright, and studies show that we must leverage seamless synergy.")


def edge_cases():
    e = {}
    e['empty.txt'] = ''
    e['whitespace-only.txt'] = ' \n\t　 \n'
    e['short.txt'] = 'Only a few words here.'
    e['exactly-ten-words.txt'] = 'one two three four five six seven eight nine ten'
    e['nine-words.txt'] = 'one two three four five six seven eight nine'
    e['exactly-10000-words.txt'] = ' '.join(['word'] * 10000)
    e['long-10001-words.txt'] = ' '.join(['word'] * 10001) + '\n'
    e['crlf.md'] = ('---\r\ntitle: "CRLF doc"\r\ntags: [a, b]\r\n---\r\n\r\n'
                    '## Benefits And Strategic Considerations\r\n\r\n' + AI_PARA + '\r\n\r\n'
                    '> Quoted line one delves into a robust idea.\r\n> Quoted line two.\r\n\r\n'
                    '<!-- TODO: add the pricing table -->\r\n\r\n'
                    '```js\r\nconst robust = leverage();\r\n```\r\n\r\n'
                    '- Stable mining efficiency\r\n- Reliable pool connectivity\r\n'
                    '- Optimized RandomX performance\r\n- Seamless wallet sync\r\n- Low latency relays\r\n\r\n'
                    'No fluff, no filler, no jargon. Turns out it just works.\r\n')
    e['lone-cr.txt'] = AI_PARA.replace('. ', '.\r') + '\r## Title Case Heading For The Win\r'
    e['bom.md'] = '﻿---\ntitle: BOM\n---\n\n' + AI_PARA + '\n'
    e['bom-plain.txt'] = '﻿' + AI_PARA
    e['zero-width-homoglyph.txt'] = ('We d​elve into the rоbust tapestry of ideаs. '
                                     'This is ‌a testament to the οpen landscape today, friends.')
    e['roleplay.txt'] = ('*nods slowly* I think we should delve deeper into this. *smiles warmly* '
                         'The plan is robust and the team is ready for the launch next week.')
    e['emoji.md'] = ('# \U0001F680 Launch Notes For The Team\n\n'
                     '\U0001F600 We delve into the tapestry \U0001F4A1 of robust ideas — truly. '
                     '*nods \U0001F642 slowly* The [Your \U0001F600 Name Here] placeholder stays. '
                     'Meet Flowdesk, your new favorite dashboard \U0001F389. #ai #ml #tech #data #cloud #devops\n\n'
                     '\U00010400\U00010401 Deseret capitals delve here, and \U0001D400\U0001D401 math letters too.\n\n'
                     'Moreover, experts believe it is important to note that \U0001F9E0 this is a testament.\n')
    e['cjk-chinese.txt'] = '这个函数返回一个承诺，调用方不应假设句柄之后仍可重用。' * 30
    e['cjk-japanese.txt'] = 'この関数はプロミスを返します。カタカナもあります。 ' * 20
    e['cjk-mixed-english.txt'] = 'The Tokyo (東京) office owns the retry limit docs, and we delve into them weekly.'
    e['cjk-astral.txt'] = '\U00020000\U00020001\U0002A700 ' * 40 + 'a b c'
    e['hangul.txt'] = '이 함수는 약속을 반환합니다 그리고 다시 사용할 수 있습니다 정말로.'
    e['unicode-whitespace.txt'] = ('We delve into　the robust tapestry of '
                                   'ideas and it is important to note that this matters.')
    e['turkish-greek-case.txt'] = ('İstanbul teams delve into robust tapestry work. İİİ '
                                   'Moreover, ΟΔΟΣ ΣΟΦΙΑΣ is a testament to innovation.')
    e['rendered-markdown.md'] = ('---\ntitle: Rendered\ndescription: "robust comprehensive seamless"\n---\n\n'
                                 '<!-- delve robust tapestry leverage -->\n\n'
                                 'Text with `<!-- not a comment -->` inline code and a real <!-- hidden robust --> comment.\n\n'
                                 '```\n<!-- fenced comment -->\n```\n\n'
                                 '    <!-- indented code comment -->\n\n'
                                 '- item\n\n    <!-- list continuation comment -->\n\n'
                                 'The deploy finished after the migration. The team checked logs, verified the '
                                 'database, and closed the incident.\n')
    e['markdown-heavy.md'] = ('# Title Case Heading And More Words\n\n'
                              '## [3.21.0] — 2026-07-30\n\n'
                              '- **Term** — definition of the term\n'
                              '- [label](https://example.com/?utm_source=chatgpt.com) — a link\n'
                              '1. **Bold** (`code`) — numbered separator\n\n'
                              '| a | b |\n|---|---|\n| code-base | data-set |\n\n'
                              'We moved the code-base in real-time. The data-set is over the long-term plan. '
                              'It works out-of-the-box. See ./docs/code-base/ and https://code-base.dev/x.\n\n'
                              '"The code-base" said nobody. **one** **two** **three** **four** bold phrases here.\n\n'
                              '#include <stdio.h> #fff #1a2b3c #88 #tag1 #tag2 #tag3 #tag4 #tag5 #tag6\n')
    e['invalid-utf8.bin'] = b'Valid start \xc3\x28 invalid \xff\xfe bytes and \xed\xa0\x80 surrogate.'
    e['nul-and-controls.txt'] = 'Text with a NUL \x00 and bell \x07 and vertical \x0b tab, delve robust tapestry.'
    e['only-punctuation.txt'] = '.!?' * 100 + ' ' + ' '.join(['w'] * 12)
    e['blockquote-only.md'] = '> one delve\n> two robust\n> three tapestry\n\nshort tail here with words to count for real now.'
    e['stats-heavy.txt'] = '\n\n'.join([AI_PARA] * 6)
    return e


def write_edge_cases():
    for name, content in edge_cases().items():
        write_text('edge/' + name, content)


def b64(data):
    return {'b64': base64.b64encode(data).decode('ascii')}


FLAGGED = "In today's fast-paced world, it is important to note that this is a testament to innovation."
CLEAN = ('The deploy finished after the migration. The team checked logs, verified the database, '
         'and closed the incident.')


def cli_cases():
    cases = []

    # `files` is a dict of name -> content, or the name of a shared fileset.
    def add(tool, name, args, files=None, stdin=None, cwd='tmp', stderr='exact', compare_files=None):
        cases.append({'tool': tool, 'name': name, 'args': args, 'files': files or {}, 'stdin': stdin,
                      'cwd': cwd, 'stderr': stderr, 'compare_files': compare_files or []})

    # ── detector CLI (bin/avoid-ai-writing.test.js) ──
    s = {'sample.txt': FLAGGED}
    add('detector', 'stdin', [], stdin=FLAGGED)
    add('detector', 'stdin dash', ['-'], stdin=FLAGGED)
    add('detector', 'file', ['sample.txt'], s)
    add('detector', 'both options', ['--context', 'technical', '--source-mode', 'rendered-markdown'], stdin=FLAGGED)
    for ctx in ('general', 'technical', 'marketing', 'personal'):
        add('detector', 'context ' + ctx, ['--context', ctx], stdin=FLAGGED)
    add('detector', 'repeated context', ['--context', 'technical', '--context', 'general'], stdin=FLAGGED)
    add('detector', 'help', ['--help'])
    add('detector', 'help short', ['-h'])
    add('detector', 'dash file', ['--', '-draft.md'], {'-draft.md': FLAGGED})
    add('detector', 'invalid utf8', ['bad.txt'], {'bad.txt': b64(b'\xc3\x28')})
    add('detector', 'bom stripped', ['bom.txt'], {'bom.txt': b64(b'\xef\xbb\xbf' + FLAGGED.encode())})
    add('detector', 'empty stdin', [], stdin='')
    add('detector', 'empty stdin technical', ['--context', 'technical'], stdin='')
    add('detector', 'empty rendered', ['--source-mode', 'rendered-markdown'], stdin='  \n')
    for name, args in [('unknown option', ['--nope']), ('unknown after help', ['--help', '--nope']),
                       ('missing value', ['--context']), ('missing source value', ['--source-mode']),
                       ('invalid context', ['--context', 'nope']), ('invalid source', ['--source-mode', 'nope']),
                       ('multiple files', ['sample.txt', 'sample.txt']), ('missing file', ['missing.txt']),
                       ('directory', ['.']), ('single dash option', ['-x'])]:
        add('detector', name, args, s)

    # ── validate CLI ──
    add('validate', 'no args', [])
    add('validate', 'one arg', ['a.md'], {'a.md': 'x'})
    add('validate', 'empty first arg', ['', 'a.md'], {'a.md': 'x'})
    add('validate', 'missing original', ['missing.md', 'a.md'], {'a.md': 'x'}, stderr='error-line')
    add('validate', 'missing rewrite', ['a.md', 'missing.md'], {'a.md': 'x'}, stderr='error-line')
    add('validate', 'identical', ['a.md', 'a.md'], {'a.md': FLAGGED})
    add('validate', 'residual grew', ['a.md', 'b.md'], {'a.md': CLEAN, 'b.md': FLAGGED + ' ' + CLEAN})
    add('validate', 'extra args ignored', ['a.md', 'b.md', 'c.md'], {'a.md': CLEAN, 'b.md': CLEAN})
    add('validate', 'invalid utf8 lossy', ['a.md', 'b.md'], {'a.md': b64(b'caf\xc3 ok \xff'), 'b.md': b64(b'caf\xc3 ok')})
    add('validate', 'bom kept', ['a.md', 'b.md'], {'a.md': b64(b'\xef\xbb\xbf---\nx: 1\n---\ntext'), 'b.md': '---\nx: 1\n---\ntext'})

    # ── normalize-quotes CLI (scripts/normalize-quotes.test.js) ──
    src = '﻿---\r\ntitle: "Raw"\r\n---\r\n"live"'
    add('quotes', 'filename equals option value', ['--quotes', 'curly', 'curly'], {'curly': src, 'other.md': src})
    add('quotes', 'write', ['curly', '--write', '--quotes', 'curly'], {'curly': src, 'other.md': src},
        compare_files=['curly', 'other.md'])
    add('quotes', 'write unchanged', ['a.md', '--write'], {'a.md': 'no quotes here'}, compare_files=['a.md'])
    for i, args in enumerate([[], ['a.md', '--quotes'], ['a.md', '--quotes', 'invalid'],
                              ['a.md', '--reference'], ['a.md', '--reference', '--write'],
                              ['a.md', '--reference', 'missing.md'], ['a.md', '--reference', 'a.md', '--quotes', 'curly'],
                              ['a.md', '--reference', 'a.md', '--reference', 'a.md'],
                              ['a.md', '--quotes', 'curly', '--bogus'], ['a.md', 'b.md', '--quotes', 'curly'],
                              ['a.md', '--quotes', 'curly', '--quotes', 'straight'], ['missing.md', '--quotes', 'curly'],
                              ['.', '--quotes', 'curly', '--write'], ['.', '--quotes', 'curly'],
                              ['a.md', '--write', '--write'], ['', '--quotes', 'curly'], ['-x']]):
        add('quotes', 'error %d' % i, args, {'a.md': '"unchanged"'}, compare_files=['a.md'])
    orig, draft = '“Old.” It\'s done.', '"New." It’s done.'
    qf = {'original.md': orig, 'draft.md': draft}
    add('quotes', 'reference preview', ['draft.md', '--reference', 'original.md'], qf)
    add('quotes', 'reference write', ['draft.md', '--quotes', 'auto', '--reference', 'original.md', '--write'], qf,
        compare_files=['draft.md', 'original.md'])
    add('quotes', 'auto default', ['draft.md'], qf)
    add('quotes', 'reference auto explicit', ['draft.md', '--reference', 'original.md', '--quotes', 'auto'], qf)
    add('quotes', 'invalid utf8 lossy', ['a.md', '--quotes', 'curly'], {'a.md': b64(b'"caf\xc3" and \'x\' \xff')})

    # ── check-style CLI (scripts/check-style.test.js) ──
    md = {'a.md': '# ok\n\ntext', 'b.md': '# ok\n\ntext'}
    add('style', 'clean technical', ['input.md', '--config', 'technical'], {'input.md': '# ok\n\nplain text'})
    add('style', 'hard technical', ['input.md', '--config', 'technical'], {'input.md': '# ok\n\nuse the “curly” quote'})
    add('style', 'no such guide', ['input.md', '--config', 'no-such-guide'], {'input.md': '# ok\n\ntext'})
    add('style', 'second file', ['a.md', 'b.md', '--config', 'technical'], md)
    add('style', 'unknown flag', ['a.md', '--config', 'technical', '--bogus'], md)
    add('style', 'missing config value', ['a.md', '--config'], md)
    add('style', 'config then flag', ['a.md', '--config', '--json'], md)
    add('style', 'no args', [])
    add('style', 'file named like config', ['technical', '--config', 'technical'], {'technical': '# ok\n\nplain text'})
    add('style', 'bare name case/space', ['a.md', '--config', ' TECHNICAL '], md)
    add('style', 'bare name prose json', ['a.md', '--config', 'prose', '--json'], md)
    add('style', 'missing file', ['missing.md', '--config', 'technical'], md)
    add('style', 'directory file', ['.', '--config', 'technical'], md)
    add('style', 'directory config', ['a.md', '--config', 'cfgdir/'], dict(md, **{'cfgdir/x': ''}))
    add('style', 'missing path config', ['a.md', '--config', './nope.json'], md)
    bad_configs = {
        'mech-null': '{"mechanics": null}', 'mech-array': '{"mechanics": []}',
        'mech-ok': '{"mechanics": {"quotes": "straight"}}', 'no-mech': '{"name": "x"}',
        'array': '[1, 2]', 'string': '"text"', 'number': '0', 'null': 'null',
        'empty': '', 'ws': '   \n', 'trailing-comma': '{"mechanics": {"quotes": "straight"},}',
        'missing-colon': '{"mechanics" {}}', 'bom': '﻿{"mechanics": {}}',
        'single-quotes': "{'mechanics': {}}", 'unterminated': '{"mechanics": {"quotes": "straight',
        'bad-escape': '{"name": "a\\qb", "mechanics": {}}', 'control': '{"name": "a\tb", "mechanics": {}}',
        'nan': 'NaN', 'long-garbage': '{"mechanics": {"quotes": "straight"}} trailing garbage text here',
        'long-token': '{"name": "long name for context", "mechanics": {"quotes": straight}}',
        'number-leading-zero': '{"mechanics": {"spellNumbersUpTo": 09}}',
        'multi-line': '{\n  "name": "x",\n  "mechanics": {\n    "quotes": "straight",\n  }\n}',
        'crlf-lines': '{\r\n  "mechanics": {\r\n    "quotes": x\r\n  }\r\n}',
        'unknown-keys': '{"name": 42, "mechanics": {"quotes": "fancy", "2": true, "1": [1, {"b": 2, "0": 1}], '
                        '"constructor": "x", "__proto__": 1, "toString": null, "spellNumbersUpTo": "9", '
                        '"serialComma": "yes", "headings": null, "emDash": 5, "latinAbbrev": ["never"]}}',
        'name-array': '{"name": ["a", null, 1.50, true], "mechanics": {"emDash": "sparing"}}',
        'name-object': '{"name": {"a": 1}, "mechanics": {}}',
        'name-empty': '{"name": "", "mechanics": {"quotes": "curly"}}',
        'name-float': '{"name": 1e21, "mechanics": {"quotes": "curly"}}',
        'dup-keys': '{"mechanics": {"quotes": "curly", "quotes": "straight"}, "name": "dup"}',
    }
    doc = {'a.md': '# Heading Title Case Words\n\n"Straight" quotes, e.g. this, and 5 items — fine.\n'}
    for name, content in bad_configs.items():
        files = dict(doc, **{'c.json': content})
        add('style', 'config ' + name, ['a.md', '--config', 'c.json'], files)
        add('style', 'config %s json' % name, ['a.md', '--json', '--config', 'c.json'], files)

    # ── gate CLI (bin/avoid-ai-writing-gate.test.js) ──
    g = {'flagged.md': FLAGGED, 'clean.md': CLEAN,
         'too-long.md': 'word ' * 10001 + '\n',
         'cjk.md': '这个函数返回一个承诺，调用方不应假设句柄之后仍可重用。' * 50,
         'mixed.md': 'The Tokyo (東京) office owns the retry limit docs.',
         '-draft.md': FLAGGED, '-': CLEAN,
         'comment.md': '<!-- ' + FLAGGED + ' -->\nThe deploy finished.\n',
         'bad.md': b64(b'\xc3\x28 bad'), 'bom.md': b64(b'\xef\xbb\xbf' + FLAGGED.encode()),
         'sub/deep.md': FLAGGED}
    for name, args in [
            ('strict', ['--threshold', '0', 'flagged.md']), ('permissive', ['--threshold', '999', 'flagged.md']),
            ('help', ['--help']), ('help short', ['-h']), ('default threshold', ['clean.md']),
            ('bad threshold', ['--threshold', '1.5', 'flagged.md']),
            ('unsafe threshold', ['--threshold', '999999999999999999999999999999', 'flagged.md']),
            ('infinity threshold', ['--threshold', '1' * 400, 'flagged.md']),
            ('leading zero threshold', ['--threshold', '0000000000000000000000007', 'flagged.md']),
            ('max safe threshold', ['--threshold', '9007199254740991', 'flagged.md']),
            ('over max safe', ['--threshold', '9007199254740992', 'flagged.md']),
            ('negative threshold', ['--threshold', '-1', 'flagged.md']),
            ('empty threshold', ['--threshold', '', 'flagged.md']),
            ('no input', []), ('too long', ['too-long.md']), ('cjk', ['cjk.md']), ('mixed cjk', ['mixed.md']),
            ('dash prefixed', ['--threshold', '0', '--', '-draft.md']), ('literal dash file', ['-']),
            ('hook default', ['--context', 'technical', '--source-mode', 'rendered-markdown', '--threshold', '6', '--', '-draft.md']),
            ('hook strict', ['--context', 'technical', '--source-mode', 'rendered-markdown', '--threshold', '6', '--threshold', '0', '--', '-draft.md']),
            ('comment rendered', ['--threshold', '0', '--', 'comment.md']),
            ('comment plain', ['--threshold', '0', '--source-mode', 'plain', '--', 'comment.md']),
            ('bad context', ['--context', 'not-a-context', '--', 'flagged.md']),
            ('bad source', ['--source-mode', 'not-a-mode', '--', 'flagged.md']),
            ('json passing', ['--json', 'clean.md']), ('json failing', ['--threshold', '0', '--json', 'flagged.md']),
            ('json mixed', ['--threshold', '0', '--json', 'clean.md', 'flagged.md']),
            ('json custom', ['--threshold', '2', '--context', 'general', '--source-mode', 'plain', '--json', 'clean.md']),
            ('json too long', ['--json', 'clean.md', 'too-long.md']), ('json cjk', ['--json', 'clean.md', 'cjk.md']),
            ('json missing', ['--json', 'clean.md', 'missing.md']), ('json bad threshold', ['--json', '--threshold', '1.5', 'clean.md']),
            ('text then missing', ['clean.md', 'flagged.md', 'missing.md']),
            ('invalid utf8', ['clean.md', 'bad.md']), ('bom', ['--threshold', '0', 'bom.md']),
            ('directory', ['sub']), ('duplicates normalized', ['./clean.md', 'clean.md', 'sub/../clean.md', 'sub//deep.md', 'sub/./deep.md']),
            ('unknown option', ['--nope']), ('missing value', ['--threshold']), ('missing glob value', ['--glob']),
            ('glob outside git', ['--glob', '**/*.md']), ('glob outside git json', ['--glob', '**/*.md', '--json'])]:
        add('gate', name, args, 'gate')
    # Globs run in a directory inside the writing-craft git work tree (read-only git ls-files).
    for name, args in [('glob md', ['--glob', '**/*.md', '--threshold', '0']),
                       ('glob md json', ['--glob', '**/*.md', '--json']),
                       ('glob plus file', ['--glob', 'docs/*.md', 'top.md']),
                       ('glob no match', ['--glob', 'nonexistent/**/*.md']),
                       ('glob no match json', ['--glob', 'nonexistent/**/*.md', '--json']),
                       ('glob txt', ['--glob', '*.txt', '--threshold', '999'])]:
        add('gate', name, args, cwd='glob')
    return {'filesets': {'gate': g}, 'cases': cases}


def write_glob_tree():
    root = os.path.join(FIXTURES, 'gate_glob')
    if os.path.isdir(root):
        shutil.rmtree(root)
    for rel, content in {'top.md': CLEAN, 'docs/draft.md': FLAGGED, 'docs/clean.md': CLEAN,
                         'docs/nested/deep.md': FLAGGED + ' ' + CLEAN, 'notes.txt': FLAGGED,
                         'ignore.js': 'const x = 1;\n'}.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(content)


def main(argv):
    if len(argv) != 1:
        print(__doc__)
        return 2
    upstream = os.path.abspath(argv[0])
    texts = os.path.join(FIXTURES, 'texts')
    if os.path.isdir(texts):
        shutil.rmtree(texts)
    record_calls(upstream)
    copy_documents(upstream)
    write_edge_cases()
    write_glob_tree()
    with open(os.path.join(FIXTURES, 'cli_cases.json'), 'w', encoding='utf-8') as fh:
        json.dump(cli_cases(), fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    total = 0
    for dirpath, _, names in os.walk(FIXTURES):
        total += sum(os.path.getsize(os.path.join(dirpath, n)) for n in names)
    print('fixtures: %.2f MB' % (total / 1e6))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
