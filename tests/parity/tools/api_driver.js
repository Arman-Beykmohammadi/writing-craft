// Library-level parity driver (JavaScript side). Reads JSONL call records
// ({"fn": "<module>:<function>", "args": [...]}) from the file named in
// argv[2] and writes one compact JSON result line per call to stdout.
'use strict';

const fs = require('fs');
const path = require('path');

const UP = path.resolve(__dirname, '../../../scripts/upstream');
const modules = {
  'detector/patterns.js': require(path.join(UP, 'detector/patterns.js')),
  'detector/validate.js': require(path.join(UP, 'detector/validate.js')),
  'scripts/markdown-prose.js': require(path.join(UP, 'scripts/markdown-prose.js')),
  'scripts/normalize-quotes.js': require(path.join(UP, 'scripts/normalize-quotes.js')),
  'scripts/check-style.js': require(path.join(UP, 'scripts/check-style.js')),
};

const lines = fs.readFileSync(process.argv[2], 'utf8').split('\n').filter(Boolean);
const out = [];
for (const line of lines) {
  const { fn, args } = JSON.parse(line);
  const [mod, name] = fn.split(':');
  let record;
  try {
    record = { ok: true, result: modules[mod][name](...args) };
  } catch (error) {
    record = { ok: false, error: `${error.name}: ${error.message}` };
  }
  out.push(JSON.stringify(record));
}
fs.writeSync(1, out.join('\n') + '\n');
