# Test results

## How the tests were run

- **Behavior tests** (`tests/cases.md`): each case ran in a fresh subagent that loaded the skill from disk, read only SKILL.md and the files SKILL.md told it to load, saw only the user's prompt and that case's input files, and never saw `cases.md` or this file. Executors ran on Claude Sonnet 5 (a smaller model than the one that built the skill, to make the test stricter). Each reply was saved to a file and graded against every pass criterion by the skill's author (Claude Opus 5.5). A case passes only if all criteria hold. The grader is not independent of the author; the pass criteria were written before any run to limit that bias.
- **Script tests**: `python3 -m unittest discover -s tests -p 'test_*.py'` (checker markers, guards, fact comparison) and `python3 tests/parity/run_parity.py` (Python ports against the vendored JavaScript).
- **Activation tests** (`tests/activation.md`): see "Activation" below for the method and its limits.

## Round 1

| Case | Result | What happened |
|---|---|---|
| CV-EN-1 | FAIL | The rewrite added no numbers and kept "helped build", but the reply offered "illustrative" example bullets with invented numbers ("3 wards", "~500 records"). A user could paste them. |
| CV-EN-2 | FAIL | Found the cloned skeleton, template verbs, and missing baselines, but did not flag "resulting in improved code quality" as a result with no measure at all. |
| CV-EN-3 | FAIL | Correct requirement map and gap list (Kubernetes, Terraform), but the new summary said "On call for production systems" (the CV says "order system") while the change list claimed "production" had not been added anywhere. |
| CV-DE-1 | PASS | Kept Finalist, Teilnahme, beantragt; German no-op rewrite with an explanation and fact-gated questions. |
| CV-DE-2 | PASS | German critique; template bullets, Nominalstil, and soft-skill triad flagged; the concrete Prüfstand bullet praised. |
| SCI-EN-1 | PASS | Passive voice not flagged; "carefully" and missing n, kit, software, ethics flagged. |
| SCI-EN-2 | FAIL | Removed the triple stacks but kept "may suggest", a modal on a hedge verb: still two hedges. |
| SCI-EN-3 | PASS | One opening thanks; unfinished map marked `[NEED: ...]`; no invented page or line numbers. |
| SCI-DE-1 | FAIL | Removed most German tells and marked the missing source, but kept "gewinnt ... zunehmend an Bedeutung" (a catalog S13 marker the checker missed because the verb was split by a long insertion) and merged two claims so that "AI" became the subject of a claim about route planning. |
| SCI-DE-2 | PASS | Passive and "man" not flagged; "belegt eindeutig" flagged as too strong for n = 12. (It suggested "legt nahe, dass ... könnte", the same double hedge as SCI-EN-2; fixed with it.) |
| PR-EN-1 | PASS | Critique, swap test, human clichés named as clichés, strengths quoted, verdict patch. |
| PR-EN-2 | PASS | Rewrite kept only the two facts; tells and hashtags removed. |
| PR-EN-3 | PASS | `[NEED: ...]` for the forgotten paper and the signature name; no flattery; facts-used list. |
| PR-DE-1 | PASS | DIN 5008 layout, all facts from the Lebenslauf, reason left as `[NEED: ...]`. The checker raised a false F1 on "C1-Niveau" (the CV says "Englisch C1"). |
| PR-DE-2 | FAIL | Few findings and a good verdict, but flagged the casual mid-sentence "Ehrlich gesagt" at P1. |
| MIX-1 | FAIL | Split correctly and caught "fünf Jahre" against 2021–2024, but praised "Mit freundlichen Grüßen," with a comma as correct. |
| VOICE-1 | PASS | Matched the sample's lowercase, dashes, "thanks"; no invented date. |
| DETECT-1 | PASS | Detect format, Tier 1B kept apart, 0 passes. Exposed an index inconsistency (I1 listed as P0 everywhere). |
| SCORE-1 | PASS | Five dimensions, 9/50; detector score shown only because the script ran. |
| AUTH-1 | PASS | No verdict, human explanations, process evidence. |
| EDIT-1 | not run | Waiting for the Python validator port. |
| VERIFY-1 | not run | Waiting for the Python validator port. |

**Round 1: 13 pass, 7 fail, 2 not run.**

### Changes after round 1

| Failure | Change |
|---|---|
| CV-EN-1 | F1 and `modes.md` MO-5: examples never contain made-up numbers, names, or details, even labeled illustrative; use `[NEED: ...]` slots inside examples. |
| CV-EN-2 | CV-5: a result with no measure ("improved code quality", "gesteigerte Effizienz") is a claim without evidence; flag and ask. |
| CV-EN-3 | MO-5: write the change list and second check from the final text and confirm every claimed change and non-change. CV-8: a summary may not generalize a fact into the posting's wording. |
| SCI-EN-2, SCI-DE-2 | SCI-2 and R2b: a hedge verb is already the hedge; a modal on it is a stack ("may suggest", "könnte darauf hindeuten", "legt nahe, dass ... könnte"); new markers. |
| SCI-DE-1 | Marker gaps raised from 60 to 100 characters for German split verbs; new S13 split-verb markers; MO-5 second check now checks language markers including split verbs and forbids claim merges that change a claim's subject or scope. |
| PR-DE-2 | I8 guard: "honestly", "to be honest", "ehrlich gesagt" inside a casual sentence are ordinary; markers now only fire at sentence start. |
| MIX-1 | G4 extended to DIN 5008 letter slips (comma after the Grußformel, "Betreff:" label) with markers; PR-10 checklist item 8 now says to check the input's closing; DE-2 states closings take no punctuation. |
| Script | Code tokens match by hyphen part ("C1-Niveau" vs "C1"); I1 index tier corrected; DE-1 now allows the spaced form for Lebenslauf month ranges. New unit tests cover each change. |
