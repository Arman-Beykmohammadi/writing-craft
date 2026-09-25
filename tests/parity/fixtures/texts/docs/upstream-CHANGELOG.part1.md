# Changelog

All notable changes to this project are documented here.

---

## [Unreleased]

### Added

- The bundled `ai-writing-detector` script accepts `--source-mode <plain|rendered-markdown>`, so the published plugin can reach rendered-Markdown scoring instead of flagging YAML frontmatter as the author's prose. It also accepts the `marketing` and `personal` contexts the root CLI and the detector already support, which it previously rejected. Blank input reports the selected context and source mode instead of an empty `stats` object, matching the root CLI. A bad argument now prints the usage message and exits 2 instead of throwing an uncaught stack trace (#244).

### Changed

- Performed-insight phrases now cover staged discoveries: a judgment framed as a twist the writer found ("the recording turned out to be the least interesting part", "the real story was"). The detector keeps the superlative-plus-insight-noun form and reveal-style "real story" continuations narrow, so literal uses such as "turned out to be the most expensive option" and "the real story was covered" stay clean. Nested emotional-flatline wording and sentence-initial "Turns out" count once when contained in a staged discovery. In short social copy, one staged discovery carrying the payoff is enough to fix. The fabricated-speaker-perspective guardrail now also covers drafting new copy in someone else's voice. No new category.
- Cover two phrasings flagged in #325 as judgment-only examples: cold-outreach flattery asks ("I'd value your take on this") under sycophantic tone, and the teaser form of the crowd contrast ("the call most leaders still won't make"). No detector change and no new category.

## [3.36.0] — 2026-09-23

### Added

- Add machine-readable `--json` output to `avoid-ai-writing-gate` and expose `pass`, `total-findings`, and `failed-files` step outputs in the GitHub Action (#252).
- Note in the README that the pinned `v3.35.0` Action example predates the step outputs and `--json`, and cover the gate's `--json` operational-error paths and the Action's output writer with executed tests.

### Changed

- Return one final rewrite after audit, correction, and available verification instead of publishing a first-pass draft and a superseding copy. Corrective edits and preservation repairs now share the two-pass limit; `--iterate 1|2`, clean no-ops, protected or intentional residuals, edit-in-place reporting, and unavailable-check status remain explicit (#203).

- Define one editing contract for rewrite and file-edit decisions. Cleanup now separates candidate matches, justified findings, and authorized edits; preserves source-supported facts, attribution, negation, uncertainty, technical terms, intentional rhetoric, protected content, and established voice; allows explicitly requested structure or register changes without invented evidence or experience; respects context skips before voice targets; leaves clean input unchanged when no separate transformation is requested; and no longer requires confirmation solely because a clearly scoped file is large (#202).

- Link the GitHub Marketplace listing from the Action instructions and pin the
  example workflow to the released `v3.35.0` tag.
- Make acknowledgment loops a judgment-only rule. The detector no longer reports the `acknowledgment-loop` type: its three phrases also open ordinary email, support, and docs replies ("To answer your question from Tuesday: ...", "You're asking about the retry limit. It is five by default ..."), and "the question of whether" is standard analytical English. The engine now exposes 53 issue types. The skill keeps the rule, with the deletion test and carve-outs (#239).

### Fixed

- Require explicit skill names matching their directories and reject duplicate frontmatter keys, including mixed quoted/unquoted keys, while retaining required names in every generated distribution (#259).
- Accept `--context marketing` and `--context personal` in the `avoid-ai-writing` scoring CLI, which previously rejected them with exit 2 even though the engine and the gate CLI support all four contexts. `--help` now lists the same values in both binaries (#207).
- Detect unsegmented-script documents (Chinese/Japanese: no inter-word spaces) before the word gate and label them `Unsupported script` instead of `Too short`, with the reason and CJK character count in `stats`. The check recognizes the full Unicode Han and kana scripts (including supplementary-plane and halfwidth forms) and declines only when CJK characters dominate the non-whitespace text, so newline-wrapped lines cannot bypass it and short English documents with an incidental place name stay scorable. The gate CLI now exits 2 on such files — matching the documented unscannable-input exit code — instead of passing silently at every threshold, and the repository self-scan reports declined documents instead of scoring them as clean while keeping raw and exemption-aware declines distinct (#241).
- Align false-positive preprocessing with CommonMark for backtick fence info strings and multiline setext headings, preserve unique normalized units as modified when only whitespace boundaries move their source spans, reject Windows OpenCode command shims with an actionable native-binary error, and recognize first-person `I` inside otherwise targeted Title Case headings (#314).
- Restrict Title Case header word separators and trailing whitespace to horizontal whitespace, so a match can never run past one physical line. `\s` also ate newlines, which let two unrelated lines or a blank-line-separated fragment combine into a single heading match that neither line independently satisfied (#291).
- Report the underlying OpenCode export launch error instead of a secondary `stderr.trim()` exception during rewrite evaluation.
- Preserve non-tracking query parameters when removing AI-referrer parameters from URLs during rewrite validation (#210). Removing a tracker that sits directly before bold markers, a dash, or an ellipsis no longer reports the URL as altered.
- Replace four superlinear Markdown scans reachable through the detector API with bounded or forward-only parsing. Validate corpus cache IDs, stage and retry cache replacements, isolate CLI-test files in private temporary directories, and require push-triggered releases to prove the package version changed.
- Replace the preservation validator's fenced-code regex with a line scanner that tracks the opening fence marker and run length, so a fence closes only on the same marker at equal or greater length per CommonMark. A `~~~` line inside a ``` block (the normal way to document Markdown fences) is content, and a three-backtick line inside a four-backtick fence no longer closes it. The same scanner replaces the marker-agnostic matcher in `scripts/self-scan.js` (#236).
- Stop the preservation validator's fence scanner from opening a fence on a backtick line whose info string contains a backtick, which CommonMark forbids. A prose line that began with a triple-backtick inline span opened a fence that ran to end of document, so every later prose edit reported `code-block-modified`. `scripts/self-scan.js` had the same gap and exempted the rest of the document from its scan.

## [3.35.0] — 2026-09-13

### Changed

- Allow pre-commit `args` to override the gate defaults by moving the filename separator out of `entry` and into default `args` (#243).
- Add npm package keywords, homepage, issue tracker, and author metadata.
- Rename the user-facing "Emotional flatline" category to "Stock reaction framing" while preserving its `emotional-flatline` API type. Keep specific reactions, flag empty framing, and make the style finding neutral in authorship scoring until relevant positive evidence establishes a direction (#82).

### Added

- Add an explicit OpenCode 1.18.30 executor for frozen rewrite-evaluation plans. It limits calls to the observed free-model allowlist, disables tools, verifies prompt and model receipts, retains failed attempts, and revalidates evidence before import. Model runs remain opt-in; benchmark judgments and release gates remain separate (#201).
- Add opt-in `fp-measure.js --dump-units PATH` provenance records and a fixed-detector `fp-compare.js` comparison of legacy and repaired preprocessing. Reports include selected and skipped units, source spans, corpus hashes, detector exclusions, and zero-observation categories (#288, #289).
- Package the deterministic detector as a composite GitHub Action and pre-commit hook, backed by a new `avoid-ai-writing-gate` CLI. The gate uses per-file finding counts rather than the composite score, defaults to `technical` + `rendered-markdown`, and uses a corpus-backed threshold of 6 findings per file (1.9% human-control failure rate across 376 documents, versus 31.4% at zero). Strict zero-findings policies remain available with an explicit threshold of 0. Preservation validation stays separate because it requires before/after inputs (#86).

### Fixed

- Recognize GFM tables without outer pipes in preservation validation and self-scan exemptions, including compact one- and two-hyphen delimiter cells, while requiring a delimiter row so prose containing a bare pipe remains editable (#209).
- Suppress eight technical-legitimate vocabulary terms (`robust`, `comprehensive`, `seamless`, `ecosystem`, `leverage`, `facilitate`, `underpin`, `streamline`) when analyzing text under `--context technical` mode (#237).

- Keep mid-paragraph years and other ordered markers above one in prose during false-positive measurement; expose blank-separated continuation merges and distinct measurement/preprocessor fingerprints; and pair attached headings with their unique legacy body span in comparison output without changing source spans or unit IDs (#293).
- Preserve Markdown structure and document content during corpus measurement. Separate structural cleanup from paragraph selection, retain eligible 400-word bodies after headings, and account for oversized units without silently deleting text. Keep tab-indented fences atomic, reject source hash mismatches, and construct scored rows from the verified source snapshot (#178, #179, #180, #288, #289).
- Report top detection categories for documents the self-scan scores in chunks. `scoreLongText()` now counts issue types across every accepted chunk, so `scanFile()` returns a populated `topTypes` for a chunked file and the `--check` over-budget diagnostic names categories instead of printing `none` (#264).
- Validate CLI `--unit` argument in `scripts/fp-measure.js` before starting measurement, exiting with code 2 on missing, unrecognized, or repeated values, and on `--unit=VALUE` syntax (`paragraph` and `document` accepted).
- Accept acronyms (`AI`, `API`, `CLI`) and the capitalised single-letter function word `A` as interior tokens in the Title Case header rule, so headings like `## The Future Of AI In Production` and `## Why Your Team Needs A Better Testing Strategy` are flagged like the original tell. First and last tokens still require an ordinary Title Case word, so all-caps banner lines such as `## HTTP API REFERENCE` stay clean (#240).
- Consume bodyless punctuation runs once when splitting sentence highlights, avoiding the quadratic punctuation-prefix regression introduced in #260 while preserving trailing-fragment boundaries.
- Remove four quadratic scans from `analyzeText()`: the sentence splitter behind highlight regions, its boundary-whitespace trim in rendered-Markdown mode, the Markdown table delimiter test, and the line-anchored `Interesting part:` opener all rescanned a long whitespace or blank-line run from every position, so a document that ended in blank lines or carried a large masked comment block took seconds instead of milliseconds. Sentence boundaries are unchanged; the regression test compares them against the former regex on every boundary shape and asserts linear growth by ratio rather than by a wall-clock budget (#235).
- Preserve detector issue indexes and sentence-highlight ranges against the original source after blockquote and normalization preprocessing (#189).
- Include every observed corpus register in `corpus.js list`; preserve the preferred accepted-register order and sort additional registers deterministically.
- Make rendered-Markdown HTML comment masking linear with a source-order scanner that preserves fenced, inline, and indented-code precedence without rescanning the document per comment (#190).
- Fix three README link targets: the dead Cowork URL, the pattern-catalog pointer, and the
  voice-profile link that led to the triggering section.
- Correct the `analyzeText()` result table in `detector/README.md`: the six score labels the
  engine returns, the `UNSCORED` classification on early-exit paths, and all four accepted `contextMode` values.
- Align `contextMode` comments in `detector/patterns.js` and mode list in
  `detector/CATEGORIES.md` with runtime behavior: four accepted modes, only
  `technical` changes flagging (#173).

## [3.34.0] — 2026-09-11

### Added

- Add the `avoid-ai-writing` command-line interface (package `bin`) for scoring one file or piped text as JSON, with `--context` and `--source-mode` options, `--help`, a `--` end-of-options separator, and usage/I/O errors on stderr with exit code 2, covered by child-process tests (#158).
- Add a pattern proposal issue form so a new rule arrives with a should-fire
  example, a must-not-fire example, and its false-positive risk; link it from `CONTRIBUTING.md`.

### Changed

- Add repository-local SSOT CI checks for the detector's Node requirement,
  advisory discovery, and drift controls; pin the existing promo checker.
- Point the bundled house-style examples at the canonical public README so the link still works when the skill package is installed without the repository root.
- Keep em-dash overuse as a P2 writing-quality flag while excluding it from the authorship score, label, probabilities, confidence, and classification (#73). Existing rate thresholds and carve-outs are unchanged. Scores may be lower for text where em-dash overuse previously contributed weight.
- Keep paired prose quotes around bare URLs visible to quote normalization even when the URL contains an unmatched opening parenthesis. Preserve internal URL apostrophes and explicit Markdown link destinations.
- Add a GitHub follow invitation to the README's maintainer section.

---

## [3.33.0] — 2026-09-05

### Changed

- Restrict `load-bearing` detection to an explicit abstract-noun allowlist. Literal construction language, predicative uses, and unlisted nouns now pass (#56).
- Publish with an OIDC-capable npm runtime and fail early when npm is too old for trusted publishing.
- **Published in the OpenAI Plugins Directory** as [Avoid AI Writing](https://chatgpt.com/plugins/plugins_6a9b77b18b8881918efa9c1255868164) (version 3.29.0, approved 2026-09-04). The bundled canonical skill now omits the frontmatter `metadata` block, which the portal rejects (#146); TERMS.md and PRIVACY.md state the plugin's scope and data handling in the terms OpenAI's plugin guidelines ask for (#147).
- **Plugin validation now fails closed on deferred port-integrity gaps.** `agents/openai.yaml` rejects scalar policies and malformed mapping/list lines, SVG assets must have an actual `<svg>` root, and the bundled routing matrix carries a checked graph digest plus generated edge inventory so it cannot silently drift from `skill-graph.json`.
- **README adds a restrained related-work block.** Links to Conor's public
  builds, Chain of Thought, and `repo-audit` now sit after the core product and
  usage documentation.
- **Corpus manifest documents the register gap with two auditable seed entries.**
  RFC 8259 provides a pre-LLM `docs` source and a 1995 W3C mailing-list message
  provides a pre-LLM `conversational` source. The corpus README records that
  both registers remain under-sampled and that `social` and `email` still have
  no entries; the additions do not authorize publishing a rate.

- Split the entry skill from its pattern and profile reference for directory-aware agents (#52). Generate a complete source artifact and portable paste instructions from both files, with drift checks.
- Claude bundles include the style checker, quote normalizer, shared Markdown protection, preservation validator, and examples they invoke (#102).

## [3.32.0] — 2026-09-05

### Added

- **Automatic quote normalization after rewrites (#104).** The bundled normalizer defaults to automatic convention inference and accepts the original document with `--reference`. Rewrite and edit workflows normalize editable prose before delivery; explicit straight/curly targets remain available.

### Fixed

- Preserve inline HTML attributes and raw HTML code during quote normalization. Stop code masks at heading and list boundaries; keep escaped reference text and URL-adjacent prose visible to checks.

- Validate inline link destinations and titles so malformed links cannot hide following prose. Precomputed boundaries prevent repeated unmatched link openers from scanning the same suffix quadratically. Regression tests cover normalization, style checks, CLI behavior and the bundled command.

---

## [3.31.0] — 2026-09-05

### Added

- **Judgment-only clarity rules from [odinfree's contribution (#129)](https://github.com/conorbronsdon/avoid-ai-writing/pull/129).** Flag obscured accountable decision-makers and repeated unexplained relabeling while preserving conventional personification, collective actors, and changes explained elsewhere in a passage. Add an audience-fit note for ambiguous proof terminology in cryptography, outside the vocabulary tiers. Narrow consequence-free restatements and repeated empty concession pairs; preserve concrete consequences and meaningful limitations. Rewrites use source facts or ask for missing details. The deterministic detector is unchanged.

---

## [3.30.0] — 2026-09-05

### Added

- **Repeated setup/reversal punchlines as a judgment-only subtype of manufactured punchlines.** Complete [cland4449's contribution (#130)](https://github.com/conorbronsdon/avoid-ai-writing/pull/130) with a P2 test for repeated reversals that replace concrete claims. Supported contrasts, isolated intentional lines, comedy, fiction, speeches, and quotations pass. Rewrites preserve source facts and ask for missing details instead of inventing failure modes. The deterministic detector is unchanged.

---

## [3.29.0] — 2026-09-03

### Added

- **A native ChatGPT and Codex plugin package.** The package contains seven
  Codex Skills, including a router for multi-stage requests, plus the
  `.codex-plugin/plugin.json` manifest and scripts for packaging and
  validation. The canonical `SKILL.md` remains the editorial authority.
- **Three detector-backed patterns from the `welttowelt` merged-system diff
  ([#108](https://github.com/conorbronsdon/avoid-ai-writing/issues/108)).**
  Launch-copy dramatic introductions — `Meet X,` followed by one of four
  launch-copy heads (`your new favorite`, `your new go-to`, or
  `the new home/way/standard` with its own tail), plus `Think X meets Y`;
  bare `Enter X.` and `Say hello to X` stay judgment-only, since
  `Enter Password.` and "Say hello to Grandma." are ordinary human prose. Dramatized contrast against the crowd, in three
  separately gated branches: the progressive debate/speculation branch
  (`while everyone else was still debating ...`, restricted to `-ing` forms,
  so `was still deliberate about` and `was still debated by pundits` stay
  clean) plus two stereotyped variants matched on their own wording
  (`writing think-pieces`, `playing catch-up`). And the fake-casual register,
  with a closed list of mechanical props detected (six asterisk stage
  directions, the four `(yes|no) x (really|seriously)` parentheticals) and
  the register judgment — including `because of course it does` — left to
  the skill. Every entry states its own residue and its own measured misses.

---

## [3.28.0] — 2026-08-28

### Added

- **Seven rhetorical-tic pattern categories adapted from Simon Willison's
  [LLM cliché highlighter](https://tools.simonwillison.net/llm-cliche-highlighter).**
  Three ship with detector types: `performed-insight` (essayist tics that
  announce profundity — "sit with that", "that's not nothing", sentence-initial
  "Turns out", "is the whole point", "X is dead; long live X"),
  `negation-chain` (three-part "no fluff, no filler, no jargon" chains,
  stacked "didn't …" clauses, "don't call it X — call it Y"), and
  `dev-blog-boilerplate` ("it just works", "zero config", "sane defaults",
  "fits in your head"). Four are skill-only
  judgment rules with the reasons recorded in `CATEGORIES.md`: stacked
  rhetorical questions, same-opener sentence runs, stranded auxiliary
  contrast, and colon into a triple. Negation-chain items carry a stop-list
  so idiomatic pairs ("no more, no less", "no matter") stay clean.

### Fixed

- **The deterministic subset stays narrower than the judgment rules.** The
  `no …` matcher now requires three short items, literal "the punchline",
  "worth naming", and "batteries included" senses stay out of regex matching,
  and "it just works out of the box" remains detectable without reviving the
  ordinary "works out to" false positive.

---

## [3.27.0] — 2026-08-26

### Added

- **`analyzeText()` can score rendered Markdown instead of source-only
  metadata (#123).** Pass `sourceMode: "rendered-markdown"` to mask initial
  YAML frontmatter and HTML comments before pattern and document analysis.
  Code-span comment examples remain visible, frontmatter recognition accepts
  LF, CRLF, and CR without hiding thematic-break sections, and masks preserve
  issue and sentence-highlight offsets. `stats` reports the selected mode,
  explicit fallbacks, and masked-span counts. Plain mode remains compatible
  with its existing scoring behavior.

---

## [3.26.0] — 2026-08-24

### Fixed

- **Edit mode now limits rewrites to prose files (#101).** Source code,
  configuration, and generated data are refused so prose-oriented edits cannot
  corrupt structured content.

---

## [3.25.2] — 2026-08-24

### Changed

- **README documents `npx skills add` as the fastest cross-agent install path.** The community [`skills`](https://github.com/vercel-labs/skills) CLI auto-detects installed coding agents and covers 75+ of them. Commands pin the installer at `skills@1.5.23`, note its Node `>=22.20.0` requirement, and clarify that the skill payload still follows this repository's current default branch. For this public root-level skill, the GitHub blob fast path normally installs only `SKILL.md`; if that path is unavailable, the CLI can fall back to cloning the full root skill directory. `skills update` refreshes whichever scope you select rather than every install at once. Existing manual per-platform steps (git clone, `clawhub install`, curl) stay as a no-Node fallback; nothing about them changed. No rule, detector, or word-table changes: the catalog stays 62 / 112.
- **`SKILL.md`'s frontmatter carries a `repository` field.** A copy installed via the `skills` CLI's SKILL.md-only fast path previously had no link back to the project or its contributor community; `metadata.repository` now points to `github.com/conorbronsdon/avoid-ai-writing` alongside the existing `author` field. The generated plugin copy stays in sync via the existing `sync-plugin-skill.sh`.

---

## [3.25.1] — 2026-08-21

### Fixed

- **Voice-profile targets are bound to the Never-inject guardrails (#100).** `casual`, `professional`, and `warm` each had a target that could only be satisfied by adding content the source lacks (a first-person touch, a concrete claim or ask, an acknowledgment). Each target now applies only where the source already has the material, and the section opens with one line stating the guardrails bind voice targets. Wording ported back from the downstream resolution in wshobson/agents#645. Contributed by @mahinNadir (#133).

---

## [3.25.0] — 2026-08-12

### Added

- **`Actually` is now a cut-first hollow intensifier.** When it only adds
  emphasis ("this actually makes the process simpler"), delete it rather than
  swapping in another word. Keep it when it carries a named correction or
  expectation gap, though a direct contrast may still be clearer.
- **The deterministic detector deliberately stays unchanged.** A regex cannot
  distinguish filler from ordinary corrective prose ("we expected a cache hit;
  it was actually a miss") without false positives, so this remains an
  LLM-judgment rule under the repo's precision-over-recall policy. The catalog
  stays at 62 categories, the engine at 48 `type`s, and the word table at 112.

---

## [3.24.0] — 2026-08-07

### Added

- **Unnecessary hyphenation is now a P2 copyedit with deterministic detector
  coverage (#107).** The rule handles three bounded subclasses: welded open
  noun phrases (`research-impact aggregator` → `research impact aggregator`),
  compounds with an established closed form (`code-base` → `codebase`), and
  attributive compounds used adverbially (`in real-time` → `in real time`,
  while `real-time analytics` stays unchanged). The catalog goes from 61 to 62
  categories and the engine from 47 to 48 `type`s.
- **Protected spans and legitimate compounds stay out of the detector.** It
  masks fenced and inline code, quotes, Markdown blockquotes, URLs, paths,
  filenames, command flags, identifiers, version strings, YAML metadata,
  Markdown tables, and HTML attributes. Fixtures preserve `high-quality`,
  `family-owned`, `third-party`, `real-time dashboard`, `long-term plan`, and
  `out-of-the-box support`.
- **The general grammar call remains editorial judgment.** Open-ended compound
  detection would flag ordinary technical writing, so the engine uses a curated
  list and reports suggestions instead of rewriting text. The optional `-ly`
  adverb cleanup discussed in #107 is deliberately absent from this release;
  the issue agreement allowed it to ship later as opt-out style cleanup rather
  than as an AI tell.

### Changed

- **Hyphenated-pair overuse is now named hyphenated modifier stacking.** Its
  signal is the density of otherwise valid compounds, not the correctness of
  each hyphen. Incorrect but deterministic forms belong to the new rule.
- **P2 hyphenation copyedits do not contribute to the AI score.** They remain
  visible as editing suggestions without changing the label, class
  probabilities, or trinary classification in short documents.

### Fixed

- **Path and filename masking remains linear on adversarial input.** Bounded
  path components remove the superlinear backtracking exposed by long kebab
  identifiers, with a timing regression fixture covering the failure shape.

---

## [3.23.1] — 2026-08-05

### Fixed

- **`constructor` in prose no longer fires the detector.** Tier lookups now use
  `Object.hasOwn`, so words that collide with `Object.prototype` property names
  can't false-positive (#109, #112).

### Changed

- **npm publishing is automated, guarded, and carries provenance.** Merging a
  version bump to main creates the GitHub release and publishes to npm in one
  pipeline: package.json and CHANGELOG.md must agree on the version, the run
  must be the exact commit the release tag names (so npm content can't drift
  from the GitHub release and `--provenance` can't attest the wrong commit),
  and duplicate runs queue and no-op (#113).
- **The cursor-rules leak gate closed its nested-path hole**, self-tests a
  review matrix on every run, and the README pattern-count copy is asserted in
  CI (#110, #111, #114, #115).

---

## [3.23.0] — 2026-08-03

### Added

- **Optional `--style` house-style layer, with no bundled guides.** `--style ./house.json` applies a user-supplied config (`register` directives the model follows, plus `mechanics`) and `scripts/check-style.js` verifies the checkable ones deterministically: `quotes` and `latinAbbrev` gate the exit code (0 clean / 1 hard / 2 tool error), `headings`, `emDash` and `spellNumbersUpTo` are advisory, `serialComma` is never checked. `examples/` holds two generic starters and the schema.
- **A bare `--style "APA"` is a best-effort fallback, not a feature.** `SKILL.md` instructs the model to open with a status line claiming no compliance and not to reproduce the guide's text. Those are instructions rather than checked rules, so that path is unverified by construction. The README says where encoded guides actually live, and the licensing rule behind it is recorded in #88.
- No detector changes, so the catalog stays 61 / 112. 39 tests in `scripts/check-style.test.js`, most of them pinning must-not-fire cases: link titles and reference definitions, HTML attributes, nested and tilde fences, BOM'd frontmatter, parentheticals that wrap or span a code block, URLs containing parentheses, and indented code blocks (while lazy continuation, list-item content, and a document opening with a thematic break stay checked). Each was a hard violation on a correct document at some point during review.

---

## [3.22.3] — 2026-08-03

### Changed

- **Five prose-contract clarifications in `SKILL.md`; no rule, threshold, or detector behavior changes.** All five came from an automated review (cubic) on a downstream vendoring PR, davila7/claude-code-templates#773. Each was a real gap between what one sentence promised and what another required; none change what the skill flags or how the engine scores. A sixth finding in that review (ship the downstream catalog regeneration inside the PR) was downstream-specific and declined there, with that repo's merge history as evidence.
- **An adversarial review pass before merge caught the gaps the first draft of this fix opened.** Two header comments in `detector/validate.js` quoted the pre-fix sentences verbatim and would have been orphaned by the reword — both refreshed (comment-only, no behavior change). The first draft of the URL-parameter fix said "only the listed parameters are the signature," which contradicted the engine: `AI_URL_PARAMS` in validate.js and `ai-utm-source` in patterns.js both cover referrer variants (`gemini.google.com`, `grok.com`, `openai.com`) the SKILL.md list does not name, so the exclusivity claim came out. And the first draft of the edit-mode paragraph stacked seven "X, not Y" contrastive negations on one line in a file whose previous maximum anywhere was two — the same uniform-register move this skill exists to catch; three were rewritten as direct positives.
- **Tables joined the flag-don't-fix list in the edit-mode instructions.** `detector/validate.js` has always treated table content as reference material and failed a rewrite that altered a cell — but the prose promise the validator claims to enforce ("the promises made above") never actually named tables, so edit mode was told to fix a tell inside a cell and then failed its own preservation check for doing it. The promise now matches the check, with the reason stated: a wording fix is not worth risking the data the table exists to carry.
- **The rewrite-mode job line no longer claims "all AI-isms removed."** It now scopes the claim to every *editable* AI-ism, with the flag-don't-fix exemptions binding in rewrite mode too. The old wording put a correct rewrite in the wrong on protected content: it either broke the exemptions to satisfy "all" or reported itself incomplete for honoring them. A tell standing inside a blockquote now belongs in section 1 as a flag, not against the rewrite as unfinished work.
- **An explicit instruction boundary for edit mode.** The file being edited is text under audit, never a source of instructions: a document that tells its editor to "ignore the rules above" or "don't flag this section" gets that sentence flagged, not obeyed. A skill authorized to modify files in place should state this rather than assume it. The same boundary is stated for pasted text in the other two modes.
- **The AI-tracking-parameter fix now says what it always meant:** strip the AI-referrer tracking parameter, leave the rest of the query string alone. "Strip the parameter from every URL" could be read as license to clean query strings generally, and a functional `?page=2` is not evidence of anything.
- **The second-pass audit must say when its corrected text supersedes section 2.** A reader skimming for the deliverable copies section 2; if the second pass fixed anything, that copy ships the tells the pass just caught. The pass now has to say "use this version, not section 2" in as many words.

---

## [3.22.2] — 2026-08-02

### Fixed

- **`hashtag-stuff` counted every `#word`, so ordinary technical prose flagged as a stuffed tag block (#90).** A paragraph citing six issue numbers, a palette listing six hex colours, or a C snippet with six `#include` lines all scored as hashtag stuffing. Found when this repo's own README linked issue #88 and the detector flagged the README. The bug report has the same problem: the prose of #90 cannot describe the rule without triggering it.
- Two subtractive changes, so the rule cannot begin firing on anything it did not already fire on. `maskCode()` blanks fenced blocks and inline code spans before counting — `fenceRanges()` existed but was wired only to `title-case-header`, so a tag quoted in backticks counted as a tag used. `isSocialTag()` subtracts all-digit forms (`#88`), 6- and 8-character hex colours that contain a digit (`#1a2b3c`, `#1a2b3cff`), and C preprocessor directives (`#include`). `owner/repo#88`, URL fragments, shebangs, and Markdown headings already passed on the rule's own anchor and are untouched.
- **Recall changes, both deliberate and both worth stating.** An unclosed fence masks everything after it, so a trailing tag block below one no longer flags; this follows `fenceRanges`' documented run-to-end rule and matches how renderers behave. A stray backtick pairs with a later span's opener and masks the prose between them, which is CommonMark-correct code-span pairing.
- **Two false negatives were introduced during development and removed before merge, both found by adversarial review.** Carving out 3- and 4-digit hex deleted `#b2b`, `#e2e`, `#dad`, `#cafe` and `#face`; the carve-out now needs 6 or 8 characters *and* a digit, so `#decade` and `#facade` survive too. Masking indented blocks silenced any tag block sitting four spaces under a list marker, where four spaces is a paragraph continuation rather than a code block; that pass was dropped entirely rather than patched. Both were the same mistake: buying a false positive with a false negative on the one shape the rule exists to catch.
- Ambiguous word tags stay counted on purpose: `#main` as a CSS id and `#general` as a channel are the same token as a tag, and separating them needs a guess about intent that costs more precision than it buys.
- Nine fixtures, five that must not fire and four that must. Every carve-out and both masking passes are mutation-tested: disabling any one of them fails the suite, as does widening the hex pattern or dropping its 8-character or digit requirement. No new detector `type`, so the catalog count stays 61 and `CATEGORIES.md` is unchanged.

---

## [3.22.1] — 2026-07-31

### Fixed

- **`title-case-header` never fired on a Markdown heading (#62).** The pattern was anchored `^[A-Z][a-z]+`, which requires the line to begin with a capital letter. A Markdown heading begins with `#`, so the anchor failed and `## Benefits And Strategic Considerations` produced no issue. The rule caught the bare-line form (`Benefits And Strategic Considerations`) while missing the commonest way a heading is actually written, which is also the form the bare line usually gets converted from. Now accepts and discards an optional `#{1,6}` prefix. Setext headings were already covered, since their text line is bare.
- Reported by a downstream that vendors `detector/patterns.js` byte-identical to a pinned commit, so they filed rather than patching locally. Worth noting as the first externally-reported detection gap.
- Two fixture groups pin it: the rule fires on `#`, `##` and `######` headings, and stays quiet on a sentence-case heading, on `##Text` with no space (not a heading), and on seven hashes (not a heading). Sentence case is the correct form, so flagging it would invert the rule.
- **The false-positive claim in the first version of this entry was wrong, and worth recording as such.** It read "no measurable false-positive cost", citing `npm run fp` being byte-identical before and after. It is: `title-case-header` does not appear in that corpus at all, because the corpus is prose with no Markdown headings. An instrument that cannot see a change returning "no change" is not evidence, and the entry stated that limitation and drew the opposite conclusion from it in adjacent sentences. Adversarial review found the regression the measurement could not.


### Fixed (follow-up, same day)

- **The heading prefix leaked into the proper-noun guard.** `matchPatterns` reports `match[0]`, so a Markdown hit arrived as `## Terms Of Service` and `##` counted as a token — silently lowering the guard from four content words to three, for headings only. `## Terms Of Service`, `## Bank Of America`, `## Table Of Contents` and `## Pride And Prejudice` all flagged: ordinary human headings, on a detector whose first priority is not firing on human writing. The filter now strips the prefix and trims before counting.
- **A `HUMAN_ONLY` → `MIXED` claim was removed from this entry rather than corrected.** It cited an unnamed README and could not be reproduced. Writing an unverifiable number into the entry that exists to retract an unverifiable number is the same mistake twice, so it is recorded rather than quietly deleted. The measured numbers below replace it.
- **Headings opening with a function word are no longer flagged, and this is the measured part.** The proper-noun guard tested `/\b(?:And|Or|Of|The|…)\b/` against the whole title with no position constraint, so a leading `The` satisfied it — while the guard's own comment has always specified a *mid-sentence* "And". Across 989 real Markdown files this rule went from 0 hits on `main` (the `^[A-Z]` anchor made it dead on `#` headings) to 35. On an 81-file subcorpus that provably predates LLMs — 2018-19 eBooks stamped `year:`, 2020 posts — it produced **13 false positives against zero on main**, every one opening with `The`: "The New Security Landscape", "The Microsoft Approach to Identity", "The Four Keys to a Successful and Secure Modern Workplace". Requiring the function word to be interior eliminates all 13 and leaves the target case firing. Those six headings are now fixtures.
- **Fence detection rewritten to track the opening delimiter instead of counting delimiters.** A parity count is wrong on the exact case the check exists for: a four-backtick fence wrapping a three-backtick example — how you document fences — inverts it. Also handles CommonMark's up-to-three-space indent and an unclosed fence running to end of document. Computed once per scan rather than re-slicing the document per candidate, which was quadratic on a heading-dense file.
- **A latent off-by-one on the bare-line form is fixed as a side effect.** The pattern's trailing `\s*` swallowed the following newline, so `Terms Of Service` split into four tokens and fired on `main` despite having three content words. The `.trim()` corrects that, which means three-word Title Case lines are now quiet in both forms. This is a behaviour change beyond headings and a strict reduction in flags.
- **Still fires, deliberately:** a four-content-word Title Case heading such as `# The Art Of War` or `## Notes On The Design`. The `>= 4` guard cannot distinguish those from `## Benefits And Strategic Considerations` — same shape. Pre-existing, identical for the bare-line form, out of scope here.
- **Ten fixtures now pin this rule**, including a value assertion on `issue.text` (a presence-only check is what let the prefix defect through), the six pre-LLM human headings above, the four fence shapes a parity count gets wrong, and an indented-line case. Six mutations were run against the result — dropping the mid-title constraint, the token floor, the prefix strip, the trim, tab support, and the word anchors — and all six fail a test. The tab-support fixture had to be rewritten to catch its mutant: on a heading whose function word is interior, an unstripped `##` only raises the token count and the verdict is unchanged, so the probe has to open with a function word.

### Note

`#67` (em-dash carve-out for changelog headings and bold-lead parentheticals) and `#69` (hedge-stack over-matching `could not possibly`) were both fixed in 3.22.0 and verified here against the shipped detector. The issues are still open and can be closed.

---

## [3.22.0] — 2026-07-31

### Added

Two pieces of enforcement. The catalog stays at 61; the engine goes from 46 to 47 `type`s (`tier1-clarity`, split out of the Tier 1 vocabulary rule).

> **Corrected 2026-08-02.** This entry originally read "No new detection categories: the catalog stays at 61 and the engine at 46 `type`s." The release added `tier1-clarity`, so the engine went to 47. The README had already been stale at 45 since v3.20.0, whose entry stated its own bump correctly, so an accurate changelog did not prevent the rot and a wrong one did not cause it. Both point at the same gap: nothing compared prose to `TYPE_LABELS`. Recorded rather than silently rewritten because the audit trail is the point.

- **Preservation validator** (`detector/validate.js`, `detector/validate.test.js`). Edit mode writes to files, and until now the promises it makes were prose instructions to a model with nothing checking them. `validate(original, rewritten)` errors when a rewrite modifies a fenced code block, YAML frontmatter, a blockquote, a table cell, inline code, a URL, a file path, or the heading count and nesting, and when the rewrite ends with more flagged patterns than it started with. Warnings cover reworded headings, figures that vanished, and rewrites that drop more than 40% of the words. There is a CLI (`node detector/validate.js before.md after.md`) that exits 1 on any error. 23 tests, no dependencies.
- **Two carve-outs, because a validator that fires on its own skill's instructions gets switched off.** URLs are compared with AI tracking parameters stripped from both sides, since the skill tells you to strip them; heading text changing is a warning rather than an error, since the skill tells you to sentence-case Title Case headings and cut emoji from them.
- **Self-scan and `PROOF.md`** (`scripts/self-scan.js`). Scores this repo's documentation with this repo's detector and publishes both numbers: raw, which counts every pattern quoted as an example, and exempt, which applies the self-reference escape hatch `SKILL.md` has documented in prose since v1 and never implemented. Budgets gate the exempt column in CI and only move down.
- The scan found two gaps in our own work, both recorded in `PROOF.md` rather than quietly patched: the em-dash rule carves out list-item separators but not Keep-a-Changelog version headings (`## [3.21.0] — 2026-07-30`) or a bold lead term with a parenthetical before the dash, and roughly half of `CHANGELOG.md`'s residual score is release notes enumerating the very words each new rule catches.

- **"Never inject these" guardrails** in `SKILL.md`, under Tone calibration. The instruction to put voice back on purpose has a predictable failure mode: the model installs a personality the author never had, trading one detectable register for a louder one. Seven additions are now out of bounds regardless of how the result scores: fake first person, manufactured stakes, forced contrarianism, performed candor, em-dash theatrics, staccato conversion, and invented specifics. The governing test is provenance: subtraction and sharpening are in scope, addition of stance, personality, or fact is not. These are constraints on the editor rather than detections on the text, which is why they sit with the rewrite instructions and do not change the catalog count. Adapted from `isatimur/de-slop`'s guardrails.
- **False-positive issue template** (`.github/ISSUE_TEMPLATE/false_positive.yml`). A rule firing on human writing is the defect this project most wants reported, and the form collects what makes a report measurable rather than anecdotal: the shortest text that fires, the register, how the text was actually written, and whether it can become a public fixture. Register is the field that matters most, since false-positive rates differ sharply across blog, docs, academic, and chat prose.

- **Human-control corpus and false-positive measurement** (`corpus/`, `scripts/corpus.js`, `scripts/fp-measure.js`). This repo has always asserted things about false positives — the tiering exists to reduce them, the tolerance matrix relaxes rules per register, `SKILL.md` opens with "signals, not proof" — and had never measured one. Every document in the corpus was written by a person, so every flag on it is a false positive by construction: no labelling, no judge, no model in the loop. The corpus is hash-only; text is fetched into a gitignored cache or read from wherever it already lives, and only hashes and metadata are committed. Register is the unit of analysis, following patina's finding that false-positive rates ran from 4% to 34% across registers inside one language.
- **First measurement: 0.0% false positives at every threshold across 560 paragraphs, Wilson 95% CI 0.0–0.7%, worst paragraph 11 out of 100.** The corpus is nine public-domain works (1788–1907) plus 25 of the maintainer's own blog posts from 2019 to December 2022, read from pre-2023 `web.archive.org` captures rather than the live site. At the document-score level the detector does not fire on human prose. The same measurement against the current published versions of those posts also returned 0.0% across 628 paragraphs, so the result does not depend on which copy was measured.
- **Provenance is verified, not assumed.** The old site used compressed slugs (`beveragetax`, `challengerfunnel`) that do not match current URLs, so archived candidates were found by slug similarity and then confirmed by content: a capture is accepted only at 0.45+ Jaccard similarity against the current text. Genuine matches land between 0.76 and 0.98; four slug guesses scored below 0.17 and were rejected by that check rather than silently accepted. Nine posts with no verifiable pre-2023 capture were dropped rather than included on their current-site text. Worth recording separately: the median archived capture is only 0.92 similar to its currently published counterpart, so the live site's posts have been edited since, and measuring "pre-2023 writing" against them would have measured the wrong thing.
- **The flag level says something else, and `detect` mode shows users flags rather than scores.** On the maintainer's Wayback-verified pre-2023 posts, `em-dash` fires on 18.3% of paragraphs and `tier1` on 12.5%. The Tier 1 words responsible are `embrace` (7), `leverage` and inflections (7), `when it comes to` (5), `in order to` (4), `that said` (4). Those are not AI tells in that text; they are a marketer's ordinary 2019 vocabulary, written years before the models existed. Both rates are slightly higher on the verified originals than on the current published versions, which is what later editing passes would do. Recorded in `corpus/README.md` as a decision to make rather than a defect to patch.
- Two defects surfaced and are filed rather than patched here: `hedge-stack` matches ordinary negation such as "could not possibly" (#69), and the `em-dash` flags on the public-domain leg are an artifact of era and Gutenberg transcription, so nineteenth-century text cannot test that rule at all.
- Corpus hygiene worth recording: two guest posts were excluded by byline, and three posts carrying "Looking back from 2025" retrospective inserts were dropped because their pre-LLM provenance is broken. The second was caught by reading the worst-scoring paragraphs, not by any check in the tooling.
- `scripts/corpus.test.js` covers the extraction helpers with 15 tests. A silent extraction bug would not crash anything; it would quietly change a published rate. Two tests exist purely to protect the measurement: em dashes must survive extraction, since the em-dash rule is scored against this corpus, and extraction must throw rather than return empty text, since an empty document would shrink the denominator without saying so.
- **Tier 1 split into 1A frequency markers and 1B clarity edits.** Tier 1 is defined by an empirical claim — these words "appear 5–20x more often in AI text than human text" — and several members could not plausibly meet it. `in order to`, `utilize`, `serves as`, `features`, `boasts`, `commence`, `ascertain`, and `endeavor` are wordiness and formality edits: worth making, but not evidence that a machine wrote the sentence. They now emit `tier1-clarity`, are weighted like Tier 2, and are excluded from the dense-AI-vocabulary signal, so a wordiness fix can no longer push a document toward an AI classification. The edit advice is unchanged for every word; what changed is what a flag claims. Detect mode reports the two bands separately.
- **The measurement that prompted it.** Against 257 paragraphs of the maintainer's verified pre-2023 writing, Tier 1 fired on 12.5%. Split, that is 8.9% markers and 3.5% clarity, with no paragraph triggering both. Roughly a quarter of Tier 1 hits on genuine human prose were wordiness being reported as an AI signal. `commence` and `ascertain` firing on the Federalist Papers and Faraday is the same problem from the formal-register end.
- **The 5–20x claim is now labelled as inherited rather than measured.** It traces to `brandonwise/humanizer`, which asserts the ratio in two places and publishes no method or dataset. `SKILL.md` says so plainly and commits to re-deriving the ratios once a machine-written corpus exists. The conflation of wordiness with frequency evidence is inherited too: `in order to`, `utilize`, and `serves as` are on that upstream list.
- **Machine-written corpus, and the first true-positive rate this project has ever had.** Two external datasets, neither generated by anyone with a stake in these numbers: RAID (Dugan et al. 2024, MIT — 11 model families, sampled by byte-range from an 11.8 GB CSV) and HC3 (Guo et al. 2023, CC-BY-SA-4.0 — paired human and ChatGPT answers to the same questions). Same hash-only design as the human half. `scripts/csv-lite.js` vendors a small RFC 4180 reader because the RAID generations contain commas, quotes, and newlines, and splitting on delimiters would silently corrupt the text being measured.
- **The composite score does not separate the classes.** ROC-AUC 0.501 at paragraph level pooled (HC3 0.554, RAID 0.451) and 0.623 at document level (HC3 0.654, RAID 0.599). The best operating point found costs 12.8% false positives to catch 27.7% of machine text. 0.5 is a coin flip.
- **The 0–100 scale uses about a tenth of its range.** No paragraph of either class scored above 11, so every threshold at or above 15 reports 0.0% on both sides, and `SKILL.md`'s own band puts everything at or under 15 in "Minimal AI signals". Category weights run 2–12 and `rawScore` is divided by `max(1, log2(words / 50))`. This is a calibration defect rather than a detection failure, and it is the most fixable finding on the page.
- **The discriminating signal is structural, not lexical.** At document level `uniformity` fires on 2.1% of human text and 25.1% of machine text, a lift of 11.7x — the best discriminator in the engine by an order of magnitude. `filler` is 3.4x; `chatbot`, `hedge-stack`, and `fnword-trigram-entropy` are machine-only. The 112-entry vocabulary table has a lift of **0.9**: it fires slightly more often on human writing than on machine writing. That is what `NulightJens/humanizer-stack` argues from StoryScope and what `harshaneel/humanize` reaches independently, and on this engine they look right.
- **`em-dash` is inverted as an authorship signal**, firing on 9.9% of human documents and 1.9% of machine ones (lift 0.2). It holds on both legs and is not a transcription artifact. Unchanged as writing advice; recorded because it points the wrong way as evidence.
- Sampling note worth keeping: evenly spaced byte offsets across RAID returned *fewer* model families at 40 windows than at 16, having resonated with the file's domain-then-model sort order and missed gpt4, chatgpt, and cohere entirely. Offsets now follow a golden-ratio low-discrepancy sequence, and the builder warns at build time when model, domain, or unit coverage falls short.
- **Fixed the two defects the measurement found.** `hedge-stack` allowed two words between the modal and the hedge adverb, so `could not possibly` and inverted questions like `could a savage possibly` both fired; it now allows at most one and never a negator (#69). The em-dash rule carved out list-item separators but not Keep-a-Changelog version headings (`## [3.21.0] — 2026-07-30`) or a bold lead term carrying a parenthetical (#67); both are carve-outs now. The version-heading pattern is deliberately narrow — a bracketed semver, a dash, an ISO date, nothing else — because `SKILL.md` applies the em-dash rule to headings too, and a prose dash in a heading still counts.
- **Both fixes improved discrimination, measured on the corpus.** `hedge-stack` went from firing on 0.6% of human units with a lift below 1 (it fired more on human text than machine text) to 0.2% with a lift of 2.2. `em-dash` false hits on human text dropped from 17.9% to 13.7%. Its lift stays inverted at 0.1, which is a finding about the signal rather than a bug in the rule.

### Changed
