# Notice

writing-craft combines and extends three MIT-licensed skills and checks a fourth MIT-licensed adaptation. Patterns are restated in this skill's own words; example corpora were not copied. Each source's LICENSE file is reproduced verbatim in `licenses/`. The JavaScript files in `scripts/upstream/` are verbatim copies; the Python modules `scripts/aiw_*.py` are ports of them.

## Sources

### avoid-ai-writing

- Repository: https://github.com/conorbronsdon/avoid-ai-writing (commit 1be7702, version 3.36.0)
- Copyright (c) 2026 Conor Bronsdon. MIT License: `licenses/avoid-ai-writing-LICENSE`.
- Its router and workflow skills (router, detector, voice-preserving rewriter, file edit in place, preservation verifier, false-positive reviewer) were contributed by Mamdouh Aboammar under the same MIT License, per that repository's NOTICE.md.
- Used as the base catalog. Ideas taken: the editing contract (candidate, finding, authorized edit; scope; source as data; source fidelity; protected content; no-op), the rewrite, detect, and edit-in-place modes, the two-pass budget and iterate option, the verification report, the quote-marks pass, house-style configs, the severity tiers P0 to P2, the Tier 1A, 1B, 2, and 3 vocabulary lists and phrase clusters, the technical exceptions, the context profiles and their tolerance matrix (carried into `genre-prose.md`), the five voice profiles, the never-inject list, the self-reference escape hatch, nearly all of the pattern entries in `patterns.md` (listed per entry under "From: A-..."), the router's routing, handoff, repair, and stop rules (folded into `modes.md`), the false-positive reviewer's authorship guardrail, the human-representation guard, and the detector, validator, quote normalizer, style checker, and gate (vendored and ported).
- avoid-ai-writing credits some of its own entries to further projects; those credits carry over: brandonwise/humanizer (vocabulary tiering), Aboudjem/humanizer-skill, welttowelt/stop-slop-refined, isatimur/de-slop (subtract-and-sharpen guardrail), devswha/patina (hash-only corpus idea), tropes.fyi, and Simon Willison's LLM cliché highlighter.

### humanizer

- Repository: https://github.com/blader/humanizer (commit 9862685, version 3.0.0)
- Copyright (c) 2025 Siqi Chen. MIT License: `licenses/humanizer-LICENSE`.
- Ideas taken: the theory that tells are default choices (staging, rhythm by rule, inflation, formatting by rule, leftovers) and that structural tells outlast vocabulary; "every sentence you keep must add something"; strength ordering with "weak alone" marks; the four-step process and the second check for the five tells that most often survive a rewrite; checking rewrites for added or dropped facts, rankings, and simultaneity claims; voice-sample matching that overrides the dash rule; voice without a sample by kind of text; the voice-carrying details to keep; "when not to act" (quotations, titles, names, pre-November-2022 text, salutations, judging by feel); pasted, file, and embedded modes; arguing with no one and fake alternatives (S10); vague association (I11); repeated sentence openings (R7); decorative arrows, rules, and repeated titles (M2); and humanizer's word additions to I4.

### stop-slop

- Repository: https://github.com/hardikpandya/stop-slop (commit 8da1f03)
- Copyright (c) 2025 Hardik Pandya. MIT License: `licenses/stop-slop-LICENSE`.
- Ideas taken: the eight core rules; the quick checks; the five-dimension scoring rubric with the 35/50 threshold (Score mode); the throat-clearing, emphasis-crutch, business-jargon, meta-commentary, performative-emphasis, telling-not-showing, and vague-declarative lists; the binary-contrast, negative-listing, dramatic-fragmentation, rhetorical-setup, formulaic-construction, false-agency, narrator-from-a-distance, passive-voice, sentence-starter, rhythm, and word-pattern tables. Its blanket bans on adverbs, fragments, and passive voice are kept as catalog entries (R10, R11, R12, S4, S20) and switched off or relaxed per genre; the `strict` option applies them at full strength outside protected conventions.

### avoid-ai-writing-multilingual (checked, not treated as an authority)

- Repository: https://github.com/jurigis/avoid-ai-writing-multilingual (commit 4e5aa4c)
- Copyright (c) Conor Bronsdon (original work); Copyright (c) 2025 Jürgen Kraus (multilingual adaptations). MIT License: `licenses/avoid-ai-writing-multilingual-LICENSE`.
- Ideas taken from SKILL-DE.md, after checking each against German usage: the principle that passive voice, Nominalstil, and loanwords are not AI markers on their own; German context profiles (academic, press release, social, email) mapped onto this skill's genre columns; German vocabulary leads (tiers, "tauchen wir ein", "kann" density, "eine Vielzahl an", "eine breite Palette an"); the German output format with a second pass; and, from its other languages, the idea of a calque pattern (G2) and a nominalization-chain threshold (R18). Claims found wrong for German practice are listed in `references/lang-de.md`, DE-7, and are not used.

## Other sources consulted

- Wikipedia:Anzeichen für KI-generierte Inhalte (German Wikipedia), for German markers. Ideas and short common phrases only; no text copied.
- Wikipedia:Signs of AI writing (English Wikipedia), the common root of the three skills above.
- German style and usage references (Duden, DIN 5008, Wolf Schneider, Ludwig Reiners) as background for `lang-de.md`, cited as practice rather than quoted.

## This skill

Copyright (c) 2026 the writing-craft contributors. Released under the MIT License (`LICENSE`).
