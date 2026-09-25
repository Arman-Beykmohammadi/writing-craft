// Preload hook (node -r) used by extract_fixtures.py. It wraps the public
// functions of the upstream modules and appends every call's arguments to the
// JSONL file named by AIW_RECORD. Child processes inherit it via NODE_OPTIONS,
// so CLI invocations spawned by the upstream tests are recorded as well.
'use strict';

const fs = require('fs');
const Module = require('module');

const out = process.env.AIW_RECORD;
const wrapped = new WeakSet();

function record(fn, args) {
  if (!out) return;
  try {
    fs.appendFileSync(out, JSON.stringify({ fn, args }) + '\n');
  } catch (_) {
    // A value that cannot be serialized (a custom detector object) is skipped.
  }
}

const TARGETS = {
  'detector/patterns.js': ['analyzeText'],
  'detector/validate.js': ['validate'],
  'scripts/markdown-prose.js': ['markdownProse'],
  'scripts/normalize-quotes.js': ['normalize', 'inferQuotes'],
  'scripts/check-style.js': ['check'],
};

const originalLoad = Module._load;
Module._load = function load(request, parent, isMain) {
  const exported = originalLoad.apply(this, arguments);
  let filename;
  try {
    filename = Module._resolveFilename(request, parent, isMain).replace(/\\/g, '/');
  } catch (_) {
    return exported;
  }
  for (const [suffix, names] of Object.entries(TARGETS)) {
    if (!filename.endsWith(suffix) || !exported || wrapped.has(exported)) continue;
    wrapped.add(exported);
    for (const name of names) {
      const fn = exported[name];
      if (typeof fn !== 'function') continue;
      exported[name] = function recorded(...args) {
        const serializable = args.map((a) => {
          if (a && typeof a === 'object' && !Array.isArray(a)) {
            const copy = {};
            for (const [k, v] of Object.entries(a)) {
              if (typeof v !== 'function' && !(v && typeof v === 'object' && typeof v.analyzeText === 'function')) copy[k] = v;
              else copy[k] = '__non_serializable__';
            }
            return copy;
          }
          return a === undefined ? '__undefined__' : a;
        });
        while (serializable.length && serializable[serializable.length - 1] === '__undefined__') serializable.pop();
        record(`${suffix}:${name}`, serializable);
        return fn.apply(this, args);
      };
    }
  }
  return exported;
};
