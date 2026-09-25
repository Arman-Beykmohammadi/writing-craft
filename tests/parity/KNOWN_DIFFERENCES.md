# Known differences

The last full run of `run_parity.py` found no mismatches: 4,072 comparisons across the six tools. What follows is the one place where the runner relaxes its comparison, and the places where the ports could still diverge on inputs the fixtures do not contain.

## Relaxed comparison

- **`validate` with a missing input file.** Covered by the `missing original` and `missing rewrite` cases in `fixtures/cli_cases.json`. Node does not catch the `readFileSync` error, so it exits with status 1 and prints a stack trace. The trace contains Node-internal frames and line numbers, which change between Node versions. `aiw_validate.py` also exits 1, and prints only the `Error: ENOENT: no such file or directory, open '<path>'` line. For these cases the runner compares the exit code, the stdout, and that `Error:` line. Every other case compares the whole of stderr exactly.

## Where divergence is still possible (no fixture shows it)

- **Unicode version.** Case mapping (`toLowerCase` versus `str.lower`) uses the Unicode tables of the runtime. Node 24 has Unicode 17 and Python 3.9 has Unicode 13, so letters added after Unicode 13 could lowercase differently. The CJK script table in `aiw_detector.py` was generated from Node 24's `\p{Script_Extensions}` and matches it exactly, but it is fixed at Unicode 17.
- **Floating point.** `Math.log2` in V8 and `math.log2` in libm could differ in the last bit. That only matters when a trigram-entropy value or the length factor sits exactly on a threshold or on a rounding tie.
- **Node error text.** File-system messages are rebuilt for ENOENT, EACCES, EISDIR, ENOTDIR, EMFILE, ELOOP, ENAMETOOLONG and EPERM. Other errno codes use Python's strerror text. `JSON.parse` messages come from a re-implementation of V8's parser errors. That parser matched Node on all 3,000 inputs of a randomized mutation run, which was done once and is not part of the runner.
- **Speed.** The Python ports are slower than Node, about 5 to 10 times on the upstream performance inputs. Output is the same. The quadratic `SEPARATOR_DASH_RE` scan is replaced by a linear scan that is equivalent to it.
