#!/usr/bin/env python3
"""Library-level parity driver (Python side).

Mirror of api_driver.js: reads JSONL call records from argv[1] and writes one
compact JSON result line per call, serialized exactly as JSON.stringify would.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'scripts'))

from aiw_jscompat import UNDEFINED, js_stringify, to_u16  # noqa: E402


def _u16(value):
    if isinstance(value, str):
        return UNDEFINED if value == '__undefined__' else to_u16(value)
    if isinstance(value, list):
        return [_u16(v) for v in value]
    if isinstance(value, dict):
        return dict((k, _u16(v)) for k, v in value.items())
    return value


def _analyze(text=UNDEFINED, options=UNDEFINED):
    import aiw_detector
    if options is UNDEFINED or options is None:
        if options is None:
            raise TypeError("Cannot read properties of null (reading 'contextMode')")
        options = {}
    return aiw_detector.analyze_u16(
        None if text is UNDEFINED else text,
        options.get('contextMode', UNDEFINED) if isinstance(options, dict) else UNDEFINED,
        options.get('sourceMode', UNDEFINED) if isinstance(options, dict) else UNDEFINED)


def _validate(original=UNDEFINED, rewritten=UNDEFINED, options=UNDEFINED):
    import aiw_validate
    opts = options if isinstance(options, dict) else {}
    return aiw_validate.validate_u16(
        original, rewritten,
        skip_residual=opts.get('skipResidual', UNDEFINED),
        max_shrink_ratio=opts.get('maxShrinkRatio', UNDEFINED))


def _markdown_prose(text):
    import aiw_markdown
    return aiw_markdown.markdown_prose(text)


def _normalize(text, quotes=UNDEFINED, reference=UNDEFINED):
    import aiw_quotes
    return aiw_quotes.normalize(text, 'auto' if quotes is UNDEFINED else quotes,
                                text if reference is UNDEFINED else reference)


def _infer(text):
    import aiw_quotes
    return aiw_quotes.infer_quotes(text)


def _check(text, mechanics=UNDEFINED):
    import aiw_style
    return aiw_style.check(text, None if mechanics is UNDEFINED else mechanics)


FUNCTIONS = {
    'detector/patterns.js:analyzeText': _analyze,
    'detector/validate.js:validate': _validate,
    'scripts/markdown-prose.js:markdownProse': _markdown_prose,
    'scripts/normalize-quotes.js:normalize': _normalize,
    'scripts/normalize-quotes.js:inferQuotes': _infer,
    'scripts/check-style.js:check': _check,
}


def main(path):
    out = []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            if not line.strip():
                continue
            call = json.loads(line)
            try:
                result = FUNCTIONS[call['fn']](*_u16(call['args']))
                record = {'ok': True, 'result': result}
            except Exception as exc:  # the JS side reports thrown errors the same way
                record = {'ok': False, 'error': '%s: %s' % (type(exc).__name__, exc)}
            out.append(js_stringify(record, 0))
    sys.stdout.buffer.write(('\n'.join(out) + '\n').encode('utf-8'))


if __name__ == '__main__':
    main(sys.argv[1])
