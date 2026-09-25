# writing-craft

A Claude skill for three kinds of writing in English and German:

- **CVs and resumes:** English resumes and CVs, the German Lebenslauf, academic CVs, bullet points, summary lines, skills sections, and tailoring a CV to a job posting.
- **Scientific writing:** papers, abstracts, theses, methods and results sections, related work, discussion and limitations, figure captions, grant proposals, peer reviews, and responses to reviewers.
- **General prose:** cover letters and German Anschreiben, motivation letters to research groups, application and outreach emails, LinkedIn and blog posts, and any other prose.

It knows what good writing looks like in each genre and helps you produce it: it gives feedback, rewrites, drafts from your notes, and checks that an edit kept your facts. Removing signs of machine-generated text is part of the job, not the whole job. The skill merges three open-source "humanizer" skills (avoid-ai-writing, humanizer, stop-slop) and a German adaptation into one catalog, then adds genre knowledge and German rules built from German sources.

## Contents

1. [What it does and does not do](#what-it-does-and-does-not-do)
2. [Install](#install)
3. [When it activates](#when-it-activates)
4. [What each mode returns](#what-each-mode-returns)
5. [Source material and voice samples](#source-material-and-voice-samples)
6. [The checker scripts](#the-checker-scripts)
7. [Known limits](#known-limits)
8. [Files](#files)
9. [Tests](#tests)
10. [Maintaining](#maintaining)
11. [License](#license)
12. [Feature map](#feature-map)

## What it does and does not do

**It does:**

- Give feedback on your own text by default: findings ordered by severity, each with the quoted words, a pattern ID, a one-line reason, and a direction for the fix; a list of what already works; and a verdict (patch or rewrite).
- Rewrite when you ask, returning the final text once, a list of changes, and a second check.
- Draft new text only from the material you supply, marking every missing fact as `[NEED: ...]`.
- Apply each genre's conventions: CV bullet shapes and claim ladders, the English resume versus the German Lebenslauf, claim strength matched to evidence in science, section conventions for papers, reviews and reviewer responses, DIN 5008 for the Anschreiben, and structure for letters, emails, and posts.
- Treat German as its own language: German markers ("spielt eine entscheidende Rolle", "Darüber hinaus", "nicht nur ... sondern auch" used for weight, Nominalstil, needless Anglicisms, English calques), German typography, and guards against flagging ordinary German.
- Match your voice when you give it a sample of your writing.
- Check an edit against the original with optional scripts (numbers, dates, URLs, claim words, preservation of code and tables).

**It does not:**

- Invent or estimate facts. It never adds a number, name, date, title, metric, citation, award level, result, or experience, and never moves a claim up or down ("contributed to" never becomes "led"; "suggests" never becomes "shows"; "finalist" never becomes "winner"; "submitted" never becomes "published").
- Invent your motivation. "Why this company" and "why this group" are facts about you.
- Rewrite your text when you only asked for feedback.
- Judge whether someone else used AI. Its patterns are writing signals, not evidence of authorship.
- Store anything about you. Your CV or voice sample is used only in the session.
- Translate or summarize as a task in itself. It can adapt a document between English and German conventions when asked, keeping every fact.

## Install

The skill is a folder with `SKILL.md` at its root. The package `writing-craft.skill` is a zip of that folder.

### Claude chat (claude.ai)

1. Make sure skills are available on your plan and that code execution is turned on (skills run in Claude's code environment; the scripts are optional).
2. Open **Settings**, then the **Capabilities** section, and find **Skills**.
3. Upload `writing-craft.skill` (or a zip of the `writing-craft` folder).
4. Make sure the skill is switched on. Start a new chat and ask, for example, "Can you look over my cover letter?"

The menu names may differ slightly as the product changes; look for skills under your settings.

### Claude desktop app

The desktop app uses the same account settings as claude.ai: open **Settings**, go to **Capabilities**, and upload the same file under **Skills**. If you use Claude Code inside the desktop app, follow the Claude Code steps.

### Claude Code

Put the folder in a skills directory (a clone of the repository works the same way):

```bash
# For all your projects: unzip the package into your personal skills folder
mkdir -p ~/.claude/skills
unzip writing-craft.skill -d ~/.claude/skills/

# Or only for one project: copy the folder into the project
mkdir -p .claude/skills
cp -r writing-craft .claude/skills/writing-craft
```

Restart Claude Code or start a new session. Claude loads the skill when a request matches its description; you can also invoke it directly with `/writing-craft`. The scripts need Python 3 (3.9 or later). The vendored JavaScript versions need Node.js and are optional.

## When it activates

Claude reads the skill's description and loads it when your request is about writing in one of its genres, even if you never mention AI. You do not need special words.

| Genre | Example phrases that load it |
|---|---|
| CV | "Here's my resume, what would you change?", "Tailor my CV to this job ad", "Improve the summary line at the top of my CV", "Schreib mir einen Lebenslauf aus diesen Stichpunkten", "Kannst du meinen Lebenslauf in einen amerikanischen Resume umbauen?" |
| Science | "make this abstract tighter", "Check my methods section for clarity", "Help me respond to reviewer 2's comments", "Write a figure caption for this plot description", "Bitte prüfe die Einleitung meiner Bachelorarbeit" |
| Prose | "can you look over my cover letter?", "Kannst du mein Anschreiben überarbeiten?", "Draft an email to a professor asking about PhD openings", "Mein LinkedIn-Post klingt so steif – was kann ich besser machen?", "Humanize this blog post" |

| Mode | Example phrases |
|---|---|
| Critique (default for your own text) | "Is this good?", "can you look over ...", "Feedback zu ...", "Kannst du drüberschauen?" |
| Detect | "Just flag the AI tells, don't change it", "scan this", "nur prüfen" |
| Rewrite | "rewrite this", "tighten it", "make it sound less like AI", "überarbeite", "kürzen" |
| Edit in place | "Clean up the prose in docs/intro.md in place" (Claude Code) |
| Draft | "Write a cover letter from my CV and this posting", "Draft an abstract from these results" |
| Score | "Score this draft on directness and rhythm" |
| Verify | "Did my edit change any numbers or links compared to the original?" |

It does not load for code, plain translation, summaries, fact-checking, slides, or general questions.

### Forcing a genre, language, section, or mode

Say it in your request. Explicit settings always win over detection:

- `genre: cv`, `genre: science`, `genre: prose`
- `section: methods` (science: abstract, intro, related, methods, results, discussion, caption, proposal, review, response; CV: default, summary, academic)
- `type: linkedin` (prose: letter, email, linkedin, blog, tech-blog, investor, press, docs, casual)
- `lang: de` or `lang: en`
- `mode: critique`, `mode: detect`, `mode: rewrite`, `mode: draft`, `mode: score`, `mode: verify`
- Options: `strict` (stop-slop's full-strength rules, except where a genre protects a convention), `gentle`, `iterate 1` or `iterate 2`, `voice: casual | professional | technical | warm | blunt`, `style: <house-style config or guide>`, `show your working`.

For a mixed document (for example an English CV and a German Anschreiben pasted together), the skill splits it by section and applies each part's genre and language.

## What each mode returns

Examples are invented and shortened.

**Critique**

```
Reading: CV · experience bullets · English · critique (your own text)

Findings (most severe first)
1. [CV-3] All four bullets follow "Verb-ed X, leveraging Y, resulting in Z%". → Vary the shape: result first, scope first, a plain fact.
2. [CV-5] "resulting in improved code quality" has no measure. → Say what changed and how you know, or drop the clause.

What already works
- Exact numbers ("35% faster queries") and named tools.

Verdict: patch. Say "rewrite" if you want me to fix it.
Checks: check.py scan executed; the CV-5 finding is model-only.
```

**Detect**

```
Issues found
P1 — S13: "In today's rapidly evolving landscape"
P1 — S6: "collaboration is the currency of modern work"
P2 — R4: "Moreover" (in a cluster)
Clarity edits (Tier 1B, not evidence of AI writing) — "In order to" → "To"

Assessment
Clear problems: ... Judgment calls: ... Recommendation: rewrite
Checks: model-only. Editing passes: 0.
```

**Rewrite**

```
Rewrite
In our cross-sectional survey of 214 warehouse workers, longer night shifts suggest that sleep quality is associated with lower self-reported wellbeing.

Changes
- [R2b] Three stacked hedges reduced to one ("suggest"); association language kept for cross-sectional data (SCI-1).

Second check
- Remaining findings: none. Facts: 214 and "cross-sectional" unchanged.
- Editing passes: 1 of 2. Checks: check.py compare executed. Stop reason: no further justified edit.
```

**Draft**

```
Draft
Subject: PhD position inquiry: microplastics in river sediment
Dear Professor Lindqvist, ...
I am writing to your group because of your work on microplastics in sediments. [NEED: which paper or project, and what about it]

Open items
1. [NEED: which paper or project ...] — your notes say you forgot the title.

Facts used
- 40 samples from two rivers ← notes, line 2
```

**Score**

```
Directness 2/10 · Rhythm 2/10 · Trust 2/10 · Authenticity 2/10 · Density 1/10
Total 9/50, below 35: revise.
Detector score (script): 41/100, "Moderate AI signals" — a surface-pattern count, not a verdict.
```

**Verify**

```
FAIL — 1 preservation error
  error   [url-missing] URL removed or altered: https://example.org/bench/cache-2026?run=7
  warning [number-missing] 1,200
Claim shift: "may reduce" became "reduces" (F2).
```

**Edit in place** reports each change as location with before → after, the passes used, and whether the preservation check passed; it never pastes the whole file back.

## Source material and voice samples

**Source material** is what the skill may take facts from: your CV, notes, the job posting, results, reviewer comments, a previous draft. Give it everything relevant. Every number, name, date, and claim in a rewrite or draft must come from this material; anything missing becomes `[NEED: ...]` instead of a guess. This is also what lets the checker compare the output with the source.

**A voice sample** is two or three short pieces of your own writing (emails, a post, a paragraph). The skill matches its sentence length, word choice, punctuation (including dashes, if you use them), and openings. Without a sample, it takes the voice from the kind of text. The sample overrides style rules but never the fact rules or the conventions you did not ask to break. Nothing from the sample is kept after the session.

## The checker scripts

The skill works fully without scripts: Claude applies the catalog by reading it. Where Python 3 runs, the scripts add repeatable mechanical checks. Script hits are candidates; the skill's guards decide what is a finding.

```bash
# Catalog markers by genre and language, dashes, placeholders, [NEED: ...] markers,
# and with --source: numbers, dates, phone numbers, URLs, codes, ladder words,
# number qualifiers ("up to", "rund"), and removed hedges that are not in the source.
python3 scripts/check.py scan draft.md --genre cv --section default --lang en --source notes.txt

# Preservation check of a revision against the original, plus the same fact comparison
python3 scripts/check.py compare original.md revised.md

# Upstream detector: 53 categories and a 0 to 100 score (English-calibrated)
python3 scripts/aiw_detector.py draft.md --context general

# Upstream preservation validator, quote-marks pass, house-style mechanics, file gate
python3 scripts/aiw_validate.py original.md revised.md
python3 scripts/aiw_quotes.py changed.md --reference original.md --write
python3 scripts/aiw_style.py draft.md --config technical
python3 scripts/aiw_gate.py --glob "docs/**/*.md"
```

The `aiw_*.py` modules are Python ports of avoid-ai-writing's JavaScript tools; the original JavaScript is vendored unchanged in `scripts/upstream/` (run with `node scripts/upstream/bin/avoid-ai-writing.js`). Detector context modes correspond to prose types: `linkedin` and `investor` → `--context marketing`; `blog` → `general`; `tech-blog` and `docs` → `technical`; `casual` → `personal`. Only `technical` changes the detector's behavior.

Example: a CV draft checked against the user's notes (notes say "contributed to moving the nightly reports to Airflow", "finalist, internal hackathon 2022", "Data team"):

```
check.py scan · cv-draft.md · genre=cv section=default · lang=en · source=notes.txt
Facts (F)
  F2   L2:3  "Spearheaded"  ladder word not in source (possible claim upgrade)
  F1   L2:92  "40"  number not in source
  F1   L3:72  "99.9"  number not in source
  F2   L4:3  "Winner"  ladder word not in source (possible claim upgrade)
  F2   L5:3  "Led"  ladder word not in source (possible claim upgrade)
  F1   L5:17  "5"  number not in source
  F1   L6:30  "2 September 2025"  date not in source
P1
  I4   L2:3  "Spearheaded"  Overused vocabulary (at threshold)
  I4   L2:60  "leveraging"  Overused vocabulary
  I4   L3:3  "Orchestrated"  Overused vocabulary (at threshold)
P2
  R7   L2:1  "3 bullets end on a result clause"  cloned bullet skeleton
Summary: 7 fact finding(s), 0 open item(s), 4 style finding(s); 0 weak-alone or below-threshold hit(s) not shown.
Script hits are candidates; the skill's guards decide what is a finding.
```

The same dates written differently ("03/2021 - 06/2023" in the notes, "Mar 2021 – Jun 2023" in the draft) and the same phone number in another format ("+49 30 1234567" and "030 1234567") are recognized as matches. The script did not catch the job title "Data Engineer" (the notes say "Data team"); title and wording upgrades need the model's reading. Exit codes: `0` no fact findings, `1` fact findings (or a failed preservation check), `2` usage error.

## Known limits

- **Signals, not proof.** The patterns describe habits that generated text often has. People write them too, especially under deadline, in a second language, or in technical genres. Never use this skill, its findings, or the detector score to decide whether someone else used AI. Detectors misclassify second-language writers at high rates, and upstream's own measurements found the detector score near chance at paragraph level.
- **German evidence is thinner.** No corpus study of German LLM output backs the German vocabulary list; it rests on German Wikipedia's guide, practitioner sources, and German style references, and `references/lang-de.md` says where it is unsure (for example DIN 5008 details after the 2020 revision, photo and signature practice in the Lebenslauf, the "Ich" in German theses).
- **Model judgment varies.** The same request can produce slightly different results. The tests caught a regression in one rerun (an invented motivation in an Anschreiben) that the rules now forbid explicitly; similar slips remain possible, which is why Critique is the default and the second check lists facts.
- **Scripts are narrow.** The checker compares tokens, not meaning: it catches a new number or a missing hedge word, not a reworded title or a merged claim. The detector is calibrated for English.
- **Genre conventions change.** Funders' templates, DIN 5008, and CV norms change; the skill says so and defers to the template you supply.
- **Activation was simulated.** The activation tests ran as a simulation of skill selection, not inside claude.ai; real activation depends on the other skills you have installed.

## Files

```
writing-craft/
├── SKILL.md                     Router: facts rules, genre and language detection, mixed documents, mode choice, which files to load
├── README.md                    This guide
├── NOTICE.md                    Which ideas came from which source, with copyright lines
├── LICENSE                      MIT license for this skill
├── licenses/                    The four source repositories' LICENSE files, verbatim
├── references/
│   ├── patterns.md              The one catalog: 75 entries with IDs, tiers, weak-alone marks, guards, EN and DE markers, sources
│   ├── modes.md                 Editing contract and output of every mode; voice matching; modifiers; authorship questions
│   ├── genre-cv.md              CV settings and rules: bullets, verbs, claim ladders, metrics, summaries, skills, tailoring, academic CVs, resume vs Lebenslauf
│   ├── genre-science.md         Science settings per section and rules: evidence table, hedging, sections, captions, proposals, reviews, EN vs DE style
│   ├── genre-prose.md           Prose settings per type and rules: letters, Anschreiben, research-group letters, emails, posts, tests
│   ├── lang-en.md               English settings and conventions
│   └── lang-de.md               German settings, conventions, guards against flagging ordinary German, sources and confidence
├── scripts/
│   ├── check.py                 New checker: catalog markers by genre and language, fact comparison against a source
│   ├── aiw_detector.py          Python port of avoid-ai-writing's detector (score, 53 categories)
│   ├── aiw_validate.py          Python port of the preservation validator
│   ├── aiw_markdown.py          Python port of the Markdown protected-region scanner
│   ├── aiw_quotes.py            Python port of the quote-marks normalizer
│   ├── aiw_style.py             Python port of the house-style checker
│   ├── aiw_gate.py              Python port of the file gate
│   ├── aiw_jscompat.py          JavaScript-compatible helpers for the ports (UTF-16 offsets, regex and number semantics)
│   └── upstream/                avoid-ai-writing's JavaScript tools, verbatim, with example house-style configs
└── tests/
    ├── cases.md                 25 behavior cases with inputs and pass criteria
    ├── cases/                   Input files for the cases (all invented)
    ├── activation.md            25 prompts that should load the skill, 14 that should not
    ├── results.md               How the tests ran, every failure, every change, and reruns
    ├── test_check.py            Unit tests for check.py (markers per entry, guards, fact comparison)
    └── parity/                  Parity tests: Python ports against the vendored JavaScript
```

## Tests

- Behavior cases: see `tests/cases.md` and `tests/results.md`. Each ran in a fresh agent that saw only the prompt and the input.
- Unit tests: `python3 -m unittest discover -s tests -p 'test_*.py'`
- Parity: `python3 tests/parity/run_parity.py` (needs Node.js to run the JavaScript side). The last run compared the six Python ports with the vendored JavaScript in 4,072 comparisons (CLI output byte for byte, exit codes, and 1,210 library calls recorded from the upstream test suites) with 0 mismatches; possible divergences no fixture shows are listed in `tests/parity/KNOWN_DIFFERENCES.md`. The Python ports run about 5 to 10 times slower than Node on very large inputs.
- Activation: `tests/activation.md`; method and results in `tests/results.md`.

## Maintaining

- A new pattern goes into `references/patterns.md` once, with an ID, tier, guard, markers, and sources; genre and language files only get a settings row if the pattern needs to be relaxed or switched off there.
- Add a unit-test sample for every new marker and a behavior case for every new rule that changes output.
- Keep `SKILL.md` under 300 lines and its description under 1,024 characters.
- Validate the package with the skill-creator validator before release.
- The writing in this skill follows plain-language rules (humanizer's maintainer guide): lead with the point, common words, one term per thing.

## License

MIT (`LICENSE`). The skill builds on four MIT-licensed projects; their licenses are in `licenses/` and the attribution is in `NOTICE.md`:

- avoid-ai-writing, Copyright (c) 2026 Conor Bronsdon (router and workflow skills contributed by Mamdouh Aboammar)
- humanizer, Copyright (c) 2025 Siqi Chen
- stop-slop, Copyright (c) 2025 Hardik Pandya
- avoid-ai-writing-multilingual, Copyright (c) Conor Bronsdon (original) and Copyright (c) 2025 Jürgen Kraus (adaptations)

## Feature map

Every feature of the four source repositories, where it lives in this skill, and what exercises it. "unit" means a marker test in `tests/test_check.py`; case IDs refer to `tests/cases.md`; "parity" means `tests/parity/`; "catalog example" means the catalog entry's own worked example. Pattern features come from the `From:` lines in `references/patterns.md`.

| Source feature | Kind | Where it lives now | Exercised by |
|---|---|---|---|
| A-acknowledgment-loops | pattern | patterns.md: C3 Acknowledgment loops | C3: SCI-EN-3 |
| A-ai-url-params | pattern | patterns.md: C5 Tool leaks | C5: unit |
| A-aphorism-formulas | pattern | patterns.md: S6 Aphorisms and fake depth | S6: PR-EN-2, DETECT-1; unit |
| A-bold-overuse | pattern | patterns.md: M1 Bold and label formatting | M1: SCI-EN-3 |
| A-bullet-lists-of-bare-noun-phrases | pattern | patterns.md: M3 Structure where prose belongs | M3: catalog example |
| A-chatbot-artifacts | pattern | patterns.md: C1 Chatbot artifacts | C1: EDIT-1; unit |
| A-citation-markup-leaks | pattern | patterns.md: C5 Tool leaks | C5: unit |
| A-cold-outreach-flattery | pattern | patterns.md: C2 Flattery of the reader | C2: SCI-EN-3; unit |
| A-colon-into-a-triple | pattern | patterns.md: R1 Rule of three | R1: CV-DE-2, PR-DE-1 |
| A-confidence-calibration-phrases | pattern | patterns.md: R5 Filler, signposts, and importance markers | R5: DETECT-1; unit |
| A-consequence-free-explanation | pattern | patterns.md: S23 Vague declaratives | S23: unit |
| A-copula-avoidance | pattern | patterns.md: I12 Copula avoidance | I12: PR-DE-1; unit |
| A-curly-quotation-marks | pattern | patterns.md: M5 Quotation-mark and typography mismatch | M5: catalog example |
| A-cutoff-disclaimers | pattern | patterns.md: F5 Guesses and knowledge-limit disclaimers | F5: unit |
| A-det-cross-para | pattern | patterns.md: R8 Uniform rhythm | R8: catalog example |
| A-det-fnword-entropy | pattern | patterns.md: R8 Uniform rhythm | R8: catalog example |
| A-det-normflag | pattern | patterns.md: C5 Tool leaks, S17 Fake-casual register | C5: unit · S17: unit |
| A-det-punct-distribution | pattern | patterns.md: R8 Uniform rhythm | R8: catalog example |
| A-det-smart-punct | pattern | patterns.md: M5 Quotation-mark and typography mismatch | M5: catalog example |
| A-dev-blog-boilerplate | pattern | patterns.md: S22 Slogans in place of properties | S22: unit |
| A-diff-anchored-writing | pattern | patterns.md: C7 Writing about the previous version | C7: catalog example |
| A-domain-term-collision | pattern | patterns.md: I13 Ambiguous domain terms | I13: SCI-EN-1 |
| A-dramatized-crowd-contrast | pattern | patterns.md: S10 Invented opponents | S10: unit |
| A-em-dashes | pattern | patterns.md: R6 Dashes as the universal connector | R6: PR-DE-2; unit |
| A-emoji-in-headers | pattern | patterns.md: M2 Decorative headings and emoji | M2: catalog example |
| A-eval-case | pattern | patterns.md: F2 Claim shift (upgrade or downgrade) | F2: CV-DE-1, SCI-DE-2, VERIFY-1; unit |
| A-excessive-bullet-lists | pattern | patterns.md: M3 Structure where prose belongs | M3: catalog example |
| A-excessive-structure | pattern | patterns.md: M2 Decorative headings and emoji, M3 Structure where prose belongs | M2: catalog example · M3: catalog example |
| A-fake-casual | pattern | patterns.md: S12 Rhetorical questions | S12: PR-DE-2; unit |
| A-fake-casual-register | pattern | patterns.md: S17 Fake-casual register | S17: unit |
| A-false-agency | pattern | patterns.md: S19 False agency and transformation crutch | S19: catalog example |
| A-false-concession | pattern | patterns.md: S11 False concession | S11: unit |
| A-false-ranges | pattern | patterns.md: S21 Slot-fill templates and false ranges | S21: unit |
| A-filler-phrases | pattern | patterns.md: R5 Filler, signposts, and importance markers | R5: DETECT-1; unit |
| A-formulaic-challenges | pattern | patterns.md: I1 Significance inflation | I1: SCI-DE-1, PR-DE-1; unit |
| A-formulaic-openings | pattern | patterns.md: S13 Scene-setting openers | S13: SCI-DE-1, PR-EN-2, PR-DE-1, DETECT-1; unit |
| A-future-narrative-closers | pattern | patterns.md: I2 Generic conclusions and future closers | I2: PR-EN-1, PR-DE-1; unit |
| A-generic-conclusions | pattern | patterns.md: I2 Generic conclusions and future closers | I2: PR-EN-1, PR-DE-1; unit |
| A-hashtag-stuffing | pattern | patterns.md: M4 Hashtag stuffing | M4: PR-EN-2; unit |
| A-hedge-stacked-predictions | pattern | patterns.md: R2 Hedging: padding and stacks | R2: SCI-EN-2, SCI-DE-2; unit |
| A-hedging | pattern | patterns.md: F2 Claim shift (upgrade or downgrade), R2 Hedging: padding and stacks | F2: CV-DE-1, SCI-DE-2, VERIFY-1; unit · R2: SCI-EN-2, SCI-DE-2; unit |
| A-hollow-intensifiers | pattern | patterns.md: I8 Hollow intensifiers | I8: SCI-EN-1, SCI-DE-2, PR-DE-2; unit |
| A-hyphenated-modifier-stacking | pattern | patterns.md: R17 Hyphen problems | R17: unit |
| A-immaculate-typography | pattern | patterns.md: M5 Quotation-mark and typography mismatch, R16 Sanded-smooth prose | M5: catalog example · R16: PR-DE-2 |
| A-infomercial-hooks | pattern | patterns.md: S8 Teaser hooks and staged candor | S8: unit |
| A-inline-header-lists | pattern | patterns.md: M1 Bold and label formatting | M1: SCI-EN-3 |
| A-invented-contrast-pair-mirroring | pattern | patterns.md: S2 Invented contrast-pair mirroring | S2: catalog example |
| A-launch-copy-dramatic-introductions | pattern | patterns.md: S16 Launch-copy introductions | S16: unit |
| A-lets-constructions | pattern | patterns.md: S7 Announcing instead of saying | S7: PR-EN-2; unit |
| A-lingering-attention | pattern | patterns.md: S14 Stock reactions and lingering attention | S14: PR-EN-2, PR-DE-1; unit |
| A-list-label-periods | pattern | patterns.md: M1 Bold and label formatting | M1: SCI-EN-3 |
| A-load-bearing | pattern | patterns.md: I4 Overused vocabulary | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit |
| A-manufactured-punchlines-staccato | pattern | patterns.md: S4 Staccato fragments and one-line closers | S4: PR-EN-2; unit |
| A-marks-pass | pattern | patterns.md: M5 Quotation-mark and typography mismatch | M5: catalog example |
| A-missing-bridge-sentences | pattern | patterns.md: R13 Missing through-line | R13: catalog example |
| A-moral-adjective-category-errors | pattern | patterns.md: I10 Moral adjectives and sweeping quantifiers | I10: unit |
| A-narrated-candor | pattern | patterns.md: C6 Narrated candor | C6: catalog example |
| A-negation-chains | pattern | patterns.md: S3 Negation chains | S3: unit |
| A-never-inject | pattern | patterns.md: F1 Invented specifics, S10 Invented opponents | F1: CV-EN-1, CV-EN-3, PR-EN-3, PR-DE-1, MIX-1; unit · S10: unit |
| A-not-x-but-y | pattern | patterns.md: S1 Not X but Y | S1: SCI-DE-1, PR-EN-2, PR-DE-1; unit |
| A-notability-name-dropping | pattern | patterns.md: I5 Name-dropping and analogy stacking | I5: catalog example |
| A-novelty-inflation | pattern | patterns.md: I7 Novelty inflation and invented labels | I7: unit |
| A-numbered-list-inflation | pattern | patterns.md: M3 Structure where prose belongs | M3: catalog example |
| A-out-claims-needing-sources | pattern | patterns.md: F4 Unsourced authority | F4: SCI-DE-1; unit |
| A-over-polishing | pattern | patterns.md: R16 Sanded-smooth prose | R16: PR-DE-2 |
| A-paragraph-reshuffle-immunity | pattern | patterns.md: R13 Missing through-line | R13: catalog example |
| A-parenthetical-hedging | pattern | patterns.md: R3 Parenthetical hedging | R3: unit |
| A-performed-insight-phrases | pattern | patterns.md: S9 Performed insight | S9: PR-EN-2; unit |
| A-persuasive-authority-tropes | pattern | patterns.md: S6 Aphorisms and fake depth | S6: PR-EN-2, DETECT-1; unit |
| A-placeholders | pattern | patterns.md: F3 Unfilled placeholders | F3: PR-EN-3; unit |
| A-promotional-language | pattern | patterns.md: I3 Promotional language | I3: unit |
| A-quotes-infer | pattern | patterns.md: M5 Quotation-mark and typography mismatch | M5: catalog example |
| A-real-actual-inflation | pattern | patterns.md: I9 Real/actual inflation | I9: unit |
| A-reasoning-chain-artifacts | pattern | patterns.md: C4 Reasoning-chain artifacts | C4: unit |
| A-recap-flattery | pattern | patterns.md: C2 Flattery of the reader | C2: SCI-EN-3; unit |
| A-repeated-empty-concessions | pattern | patterns.md: S3 Negation chains | S3: unit |
| A-rhetorical-question-openers | pattern | patterns.md: S12 Rhetorical questions | S12: PR-DE-2; unit |
| A-rhythm-and-uniformity | pattern | patterns.md: R8 Uniform rhythm | R8: catalog example |
| A-rule-of-three | pattern | patterns.md: R1 Rule of three | R1: CV-DE-2, PR-DE-1 |
| A-safe-no-invention | pattern | patterns.md: F1 Invented specifics | F1: CV-EN-1, CV-EN-3, PR-EN-3, PR-DE-1, MIX-1; unit |
| A-same-opener-sentence-runs | pattern | patterns.md: R7 Repeated openings and cloned skeletons | R7: CV-EN-2, MIX-1; unit |
| A-self-labeling-significance | pattern | patterns.md: S18 Self-labeling significance | S18: unit |
| A-setup-reversal-punchlines | pattern | patterns.md: S5 Reversal tricks | S5: catalog example |
| A-significance-inflation | pattern | patterns.md: I1 Significance inflation | I1: SCI-DE-1, PR-DE-1; unit |
| A-social-endorsement-closers | pattern | patterns.md: S15 Endorsement closers | S15: unit |
| A-source-fidelity | pattern | patterns.md: F1 Invented specifics, F2 Claim shift (upgrade or downgrade) | F1: CV-EN-1, CV-EN-3, PR-EN-3, PR-DE-1, MIX-1; unit · F2: CV-DE-1, SCI-DE-2, VERIFY-1; unit |
| A-speculative-gap-filling | pattern | patterns.md: F5 Guesses and knowledge-limit disclaimers | F5: unit |
| A-speculative-scenario-openers | pattern | patterns.md: S13 Scene-setting openers | S13: SCI-DE-1, PR-EN-2, PR-DE-1, DETECT-1; unit |
| A-stacked-rhetorical-questions | pattern | patterns.md: S12 Rhetorical questions | S12: PR-DE-2; unit |
| A-stock-reaction-framing | pattern | patterns.md: S14 Stock reactions and lingering attention | S14: PR-EN-2, PR-DE-1; unit |
| A-stranded-auxiliary-contrast | pattern | patterns.md: S5 Reversal tricks | S5: catalog example |
| A-subjectless-fragments-and-agentless-passives | pattern | patterns.md: R10 Passive voice and missing actors | R10: SCI-EN-1, SCI-DE-2; unit |
| A-superficial-ing-analyses | pattern | patterns.md: I6 Superficial -ing analyses and meaning-telling | I6: unit |
| A-suspiciously-clean-grammar | pattern | patterns.md: R16 Sanded-smooth prose | R16: PR-DE-2 |
| A-sycophantic-tone | pattern | patterns.md: C2 Flattery of the reader | C2: SCI-EN-3; unit |
| A-synonym-cycling | pattern | patterns.md: R9 Synonym cycling and low vocabulary range | R9: catalog example |
| A-technical-exceptions | pattern | patterns.md: I4 Overused vocabulary | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit |
| A-template-phrases | pattern | patterns.md: S21 Slot-fill templates and false ranges | S21: unit |
| A-tier1a | pattern | patterns.md: I4 Overused vocabulary | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit |
| A-tier1b | pattern | patterns.md: I4 Overused vocabulary | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit |
| A-tier2 | pattern | patterns.md: I4 Overused vocabulary | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit |
| A-tier3 | pattern | patterns.md: I4 Overused vocabulary | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit |
| A-tier3-phrases | pattern | patterns.md: I4 Overused vocabulary | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit |
| A-title-case-headings | pattern | patterns.md: M2 Decorative headings and emoji | M2: catalog example |
| A-transformation-crutch | pattern | patterns.md: S19 False agency and transformation crutch | S19: catalog example |
| A-transitions | pattern | patterns.md: R4 Transition connectors, R5 Filler, signposts, and importance markers, S7 Announcing instead of saying, S13 Scene-setting openers | R4: MIX-1, SCI-DE-1, DETECT-1; unit · R5: DETECT-1; unit · S7: PR-EN-2; unit · S13: SCI-DE-1, PR-EN-2, PR-DE-1, DETECT-1; unit |
| A-treadmill-effect | pattern | patterns.md: R14 Treadmill: low information density | R14: SCI-EN-2 |
| A-uniform-paragraph-length | pattern | patterns.md: R8 Uniform rhythm | R8: catalog example |
| A-unnecessary-hyphenation | pattern | patterns.md: R17 Hyphen problems | R17: unit |
| A-vague-attributions | pattern | patterns.md: F4 Unsourced authority | F4: SCI-DE-1; unit |
| A-vague-endorsement | pattern | patterns.md: S15 Endorsement closers | S15: unit |
| A-vague-third-party-validation | pattern | patterns.md: F4 Unsourced authority | F4: SCI-DE-1; unit |
| A-vocabulary-diversity | pattern | patterns.md: R9 Synonym cycling and low vocabulary range | R9: catalog example |
| A-vocabulary-repetition-vs-cycling | pattern | patterns.md: R9 Synonym cycling and low vocabulary range | R9: catalog example |
| A-wall-of-text-replies | pattern | patterns.md: R15 Wall-of-text replies | R15: catalog example |
| H-1 | pattern | patterns.md: S1 Not X but Y | S1: SCI-DE-1, PR-EN-2, PR-DE-1; unit |
| H-10 | pattern | patterns.md: R17 Hyphen problems | R17: unit |
| H-11 | pattern | patterns.md: R10 Passive voice and missing actors | R10: SCI-EN-1, SCI-DE-2; unit |
| H-12 | pattern | patterns.md: I4 Overused vocabulary, I8 Hollow intensifiers | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit · I8: SCI-EN-1, SCI-DE-2, PR-DE-2; unit |
| H-13 | pattern | patterns.md: I1 Significance inflation, I2 Generic conclusions and future closers | I1: SCI-DE-1, PR-DE-1; unit · I2: PR-EN-1, PR-DE-1; unit |
| H-14 | pattern | patterns.md: I11 Vague association | I11: unit |
| H-15 | pattern | patterns.md: I6 Superficial -ing analyses and meaning-telling | I6: unit |
| H-16 | pattern | patterns.md: I3 Promotional language | I3: unit |
| H-17 | pattern | patterns.md: F4 Unsourced authority, I5 Name-dropping and analogy stacking | F4: SCI-DE-1; unit · I5: catalog example |
| H-18 | pattern | patterns.md: I12 Copula avoidance | I12: PR-DE-1; unit |
| H-19 | pattern | patterns.md: M1 Bold and label formatting | M1: SCI-EN-3 |
| H-2 | pattern | patterns.md: S4 Staccato fragments and one-line closers, S9 Performed insight | S4: PR-EN-2; unit · S9: PR-EN-2; unit |
| H-20 | pattern | patterns.md: M2 Decorative headings and emoji | M2: catalog example |
| H-21 | pattern | patterns.md: M5 Quotation-mark and typography mismatch | M5: catalog example |
| H-22 | pattern | patterns.md: C1 Chatbot artifacts, C2 Flattery of the reader | C1: EDIT-1; unit · C2: SCI-EN-3; unit |
| H-23 | pattern | patterns.md: F5 Guesses and knowledge-limit disclaimers | F5: unit |
| H-24 | pattern | patterns.md: M2 Decorative headings and emoji | M2: catalog example |
| H-25 | pattern | patterns.md: C7 Writing about the previous version | C7: catalog example |
| H-3 | pattern | patterns.md: S6 Aphorisms and fake depth | S6: PR-EN-2, DETECT-1; unit |
| H-4 | pattern | patterns.md: S7 Announcing instead of saying, S8 Teaser hooks and staged candor | S7: PR-EN-2; unit · S8: unit |
| H-5 | pattern | patterns.md: S10 Invented opponents | S10: unit |
| H-6 | pattern | patterns.md: R1 Rule of three | R1: CV-DE-2, PR-DE-1 |
| H-7 | pattern | patterns.md: R7 Repeated openings and cloned skeletons | R7: CV-EN-2, MIX-1; unit |
| H-8 | pattern | patterns.md: R6 Dashes as the universal connector | R6: PR-DE-2; unit |
| H-9 | pattern | patterns.md: R2 Hedging: padding and stacks | R2: SCI-EN-2, SCI-DE-2; unit |
| H-KeepVoiceDetails | pattern | patterns.md: R16 Sanded-smooth prose | R16: PR-DE-2 |
| H-Process | pattern | patterns.md: F1 Invented specifics, F2 Claim shift (upgrade or downgrade) | F1: CV-EN-1, CV-EN-3, PR-EN-3, PR-DE-1, MIX-1; unit · F2: CV-DE-1, SCI-DE-2, VERIFY-1; unit |
| H-README-Lisbon | pattern | patterns.md: F1 Invented specifics | F1: CV-EN-1, CV-EN-3, PR-EN-3, PR-DE-1, MIX-1; unit |
| H-TwoRules | pattern | patterns.md: R14 Treadmill: low information density | R14: SCI-EN-2 |
| M-1 | pattern | patterns.md: I1 Significance inflation | I1: SCI-DE-1, PR-DE-1; unit |
| M-10 | pattern | patterns.md: R9 Synonym cycling and low vocabulary range | R9: catalog example |
| M-11 | pattern | patterns.md: S21 Slot-fill templates and false ranges | S21: unit |
| M-12 | pattern | patterns.md: R4 Transition connectors | R4: MIX-1, SCI-DE-1, DETECT-1; unit |
| M-13 | pattern | patterns.md: S21 Slot-fill templates and false ranges | S21: unit |
| M-14 | pattern | patterns.md: R3 Parenthetical hedging | R3: unit |
| M-15 | pattern | patterns.md: R2 Hedging: padding and stacks | R2: SCI-EN-2, SCI-DE-2; unit |
| M-15a | pattern | patterns.md: R2 Hedging: padding and stacks | R2: SCI-EN-2, SCI-DE-2; unit |
| M-16 | pattern | patterns.md: R5 Filler, signposts, and importance markers | R5: DETECT-1; unit |
| M-17 | pattern | patterns.md: S1 Not X but Y | S1: SCI-DE-1, PR-EN-2, PR-DE-1; unit |
| M-18 | pattern | patterns.md: R6 Dashes as the universal connector | R6: PR-DE-2; unit |
| M-19 | pattern | patterns.md: R8 Uniform rhythm | R8: catalog example |
| M-2 | pattern | patterns.md: I5 Name-dropping and analogy stacking | I5: catalog example |
| M-20 | pattern | patterns.md: M1 Bold and label formatting | M1: SCI-EN-3 |
| M-21 | pattern | patterns.md: M2 Decorative headings and emoji | M2: catalog example |
| M-22 | pattern | patterns.md: M3 Structure where prose belongs | M3: catalog example |
| M-23 | pattern | patterns.md: S11 False concession | S11: unit |
| M-24 | pattern | patterns.md: S12 Rhetorical questions | S12: PR-DE-2; unit |
| M-25 | pattern | patterns.md: R4 Transition connectors | R4: MIX-1, SCI-DE-1, DETECT-1; unit |
| M-26 | pattern | patterns.md: C1 Chatbot artifacts | C1: EDIT-1; unit |
| M-27 | pattern | patterns.md: S7 Announcing instead of saying | S7: PR-EN-2; unit |
| M-28 | pattern | patterns.md: F5 Guesses and knowledge-limit disclaimers | F5: unit |
| M-29 | pattern | patterns.md: I2 Generic conclusions and future closers | I2: PR-EN-1, PR-DE-1; unit |
| M-3 | pattern | patterns.md: I6 Superficial -ing analyses and meaning-telling | I6: unit |
| M-30 | pattern | patterns.md: R5 Filler, signposts, and importance markers | R5: DETECT-1; unit |
| M-31 | pattern | patterns.md: R5 Filler, signposts, and importance markers | R5: DETECT-1; unit |
| M-32 | pattern | patterns.md: S14 Stock reactions and lingering attention | S14: PR-EN-2, PR-DE-1; unit |
| M-33 | pattern | patterns.md: C4 Reasoning-chain artifacts | C4: unit |
| M-34 | pattern | patterns.md: C2 Flattery of the reader | C2: SCI-EN-3; unit |
| M-35 | pattern | patterns.md: C3 Acknowledgment loops | C3: SCI-EN-3 |
| M-36 | pattern | patterns.md: M2 Decorative headings and emoji, M3 Structure where prose belongs | M2: catalog example · M3: catalog example |
| M-36a | pattern | patterns.md: R1 Rule of three | R1: CV-DE-2, PR-DE-1 |
| M-37 | pattern | patterns.md: R8 Uniform rhythm | R8: catalog example |
| M-38 | pattern | patterns.md: R16 Sanded-smooth prose | R16: PR-DE-2 |
| M-4 | pattern | patterns.md: I3 Promotional language | I3: unit |
| M-41 | pattern | patterns.md: I2 Generic conclusions and future closers | I2: PR-EN-1, PR-DE-1; unit |
| M-42 | pattern | patterns.md: M3 Structure where prose belongs | M3: catalog example |
| M-5 | pattern | patterns.md: F4 Unsourced authority | F4: SCI-DE-1; unit |
| M-6 | pattern | patterns.md: I1 Significance inflation | I1: SCI-DE-1, PR-DE-1; unit |
| M-7 | pattern | patterns.md: I7 Novelty inflation and invented labels | I7: unit |
| M-9 | pattern | patterns.md: I12 Copula avoidance | I12: PR-DE-1; unit |
| M-InventedFacts | pattern | patterns.md: F1 Invented specifics | F1: CV-EN-1, CV-EN-3, PR-EN-3, PR-DE-1, MIX-1; unit |
| M-Tier1 | pattern | patterns.md: I4 Overused vocabulary | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit |
| M-Tier2 | pattern | patterns.md: I4 Overused vocabulary, R18 Noun-heavy style | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit · R18: CV-DE-2, SCI-DE-1; unit |
| M-Tier3 | pattern | patterns.md: G1 Needless Anglicisms, I2 Generic conclusions and future closers, I4 Overused vocabulary, S1 Not X but Y, S13 Scene-setting openers | G1: unit · I2: PR-EN-1, PR-DE-1; unit · I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit · S1: SCI-DE-1, PR-EN-2, PR-DE-1; unit · S13: SCI-DE-1, PR-EN-2, PR-DE-1, DETECT-1; unit |
| M-Unterscheidung | pattern | patterns.md: R10 Passive voice and missing actors, R18 Noun-heavy style | R10: SCI-EN-1, SCI-DE-2; unit · R18: CV-DE-2, SCI-DE-1; unit |
| S-Adverbs | pattern | patterns.md: I8 Hollow intensifiers, R2 Hedging: padding and stacks, R11 Adverb load | I8: SCI-EN-1, SCI-DE-2, PR-DE-2; unit · R2: SCI-EN-2, SCI-DE-2; unit · R11: catalog example |
| S-BinaryContrasts | pattern | patterns.md: S1 Not X but Y | S1: SCI-DE-1, PR-EN-2, PR-DE-1; unit |
| S-BusinessJargon | pattern | patterns.md: I4 Overused vocabulary | I4: CV-EN-2, CV-DE-2, PR-EN-2, EMB-1; unit |
| S-DramaticFragmentation | pattern | patterns.md: S4 Staccato fragments and one-line closers | S4: PR-EN-2; unit |
| S-EmphasisCrutches | pattern | patterns.md: S6 Aphorisms and fake depth, S9 Performed insight, S23 Vague declaratives | S6: PR-EN-2, DETECT-1; unit · S9: PR-EN-2; unit · S23: unit |
| S-FalseAgency | pattern | patterns.md: S19 False agency and transformation crutch | S19: catalog example |
| S-FillerPhrases | pattern | patterns.md: R5 Filler, signposts, and importance markers, S6 Aphorisms and fake depth, S13 Scene-setting openers | R5: DETECT-1; unit · S6: PR-EN-2, DETECT-1; unit · S13: SCI-DE-1, PR-EN-2, PR-DE-1, DETECT-1; unit |
| S-FormulaicConstructions | pattern | patterns.md: S21 Slot-fill templates and false ranges | S21: unit |
| S-MetaCommentary | pattern | patterns.md: S6 Aphorisms and fake depth, S7 Announcing instead of saying, S8 Teaser hooks and staged candor | S6: PR-EN-2, DETECT-1; unit · S7: PR-EN-2; unit · S8: unit |
| S-NarratorFromADistance | pattern | patterns.md: S20 Narrator from a distance | S20: catalog example |
| S-NegativeListing | pattern | patterns.md: S1 Not X but Y | S1: SCI-DE-1, PR-EN-2, PR-DE-1; unit |
| S-PassiveVoice | pattern | patterns.md: F4 Unsourced authority, R10 Passive voice and missing actors | F4: SCI-DE-1; unit · R10: SCI-EN-1, SCI-DE-2; unit |
| S-PerformativeEmphasis | pattern | patterns.md: I8 Hollow intensifiers | I8: SCI-EN-1, SCI-DE-2, PR-DE-2; unit |
| S-QuickChecks | pattern | patterns.md: R6 Dashes as the universal connector, R8 Uniform rhythm, R10 Passive voice and missing actors, R11 Adverb load, R12 Wh- and "So" openers, S7 Announcing instead of saying, S19 False agency and transformation crutch | R6: PR-DE-2; unit · R8: catalog example · R10: SCI-EN-1, SCI-DE-2; unit · R11: catalog example · R12: catalog example · S7: PR-EN-2; unit · S19: catalog example |
| S-RhetoricalSetups | pattern | patterns.md: S7 Announcing instead of saying, S12 Rhetorical questions | S7: PR-EN-2; unit · S12: PR-DE-2; unit |
| S-RhythmPatterns | pattern | patterns.md: R1 Rule of three, R6 Dashes as the universal connector, S3 Negation chains, S4 Staccato fragments and one-line closers, S12 Rhetorical questions | R1: CV-DE-2, PR-DE-1 · R6: PR-DE-2; unit · S3: unit · S4: PR-EN-2; unit · S12: PR-DE-2; unit |
| S-Rule1 | pattern | patterns.md: R11 Adverb load | R11: catalog example |
| S-Rule3 | pattern | patterns.md: R10 Passive voice and missing actors, S19 False agency and transformation crutch | R10: SCI-EN-1, SCI-DE-2; unit · S19: catalog example |
| S-Rule4 | pattern | patterns.md: I10 Moral adjectives and sweeping quantifiers, S23 Vague declaratives | I10: unit · S23: unit |
| S-Rule5 | pattern | patterns.md: S20 Narrator from a distance | S20: catalog example |
| S-Rule6 | pattern | patterns.md: R1 Rule of three, R6 Dashes as the universal connector, R8 Uniform rhythm, S4 Staccato fragments and one-line closers | R1: CV-DE-2, PR-DE-1 · R6: PR-DE-2; unit · R8: catalog example · S4: PR-EN-2; unit |
| S-Rule7 | pattern | patterns.md: R2 Hedging: padding and stacks, R14 Treadmill: low information density | R2: SCI-EN-2, SCI-DE-2; unit · R14: SCI-EN-2 |
| S-Rule8 | pattern | patterns.md: S6 Aphorisms and fake depth | S6: PR-EN-2, DETECT-1; unit |
| S-Scoring | pattern | patterns.md: R14 Treadmill: low information density | R14: SCI-EN-2 |
| S-SentenceStarters | pattern | patterns.md: R4 Transition connectors, R12 Wh- and "So" openers, S8 Teaser hooks and staged candor | R4: MIX-1, SCI-DE-1, DETECT-1; unit · R12: catalog example · S8: unit |
| S-TellingNotShowing | pattern | patterns.md: I8 Hollow intensifiers | I8: SCI-EN-1, SCI-DE-2, PR-DE-2; unit |
| S-ThroatClearing | pattern | patterns.md: S6 Aphorisms and fake depth, S7 Announcing instead of saying | S6: PR-EN-2, DETECT-1; unit · S7: PR-EN-2; unit |
| S-VagueDeclaratives | pattern | patterns.md: S23 Vague declaratives | S23: unit |
| S-WordPatterns | pattern | patterns.md: I10 Moral adjectives and sweeping quantifiers, R11 Adverb load | I10: unit · R11: catalog example |
| A-det-tier1 | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I4 Overused vocabulary | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-tier1-clarity | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I4 Overused vocabulary | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-tier2 | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I4 Overused vocabulary | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-tier3 | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I4 Overused vocabulary | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-transition | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R4 Transition connectors | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-chatbot | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog C1 Chatbot artifacts | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-sycophantic | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog C2 Flattery of the reader | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-filler | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R5 Filler, signposts, and importance markers | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-generic-conclusion | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I2 Generic conclusions and future closers | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-lets-construction | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S7 Announcing instead of saying | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-reasoning-artifact | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog C4 Reasoning-chain artifacts | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-significance-inflation | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I1 Significance inflation | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-vague-attribution | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog F4 Unsourced authority | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-hollow-intensifier | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I8 Hollow intensifiers | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-emotional-flatline | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S14 Stock reactions and lingering attention | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-lingering-attention | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S14 Stock reactions and lingering attention | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-novelty-inflation | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I7 Novelty inflation and invented labels | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-cutoff-disclaimer | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog F5 Guesses and knowledge-limit disclaimers | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-ai-placeholder | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog F3 Unfilled placeholders | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-ai-citation-markup | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog C5 Tool leaks | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-ai-utm-source | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog C5 Tool leaks | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-template-phrase | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S21 Slot-fill templates and false ranges | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-false-concession | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S11 False concession | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-rhetorical-question | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S12 Rhetorical questions | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-hedge-stack | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R2 Hedging: padding and stacks | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-future-narrative | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I2 Generic conclusions and future closers | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-real-actual-inflation | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I9 Real/actual inflation | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-social-cta-closer | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S15 Endorsement closers | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-performed-insight | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S9 Performed insight | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-negation-chain | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S3 Negation chains | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-dev-blog-boilerplate | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S22 Slogans in place of properties | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-unnecessary-hyphenation | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R17 Hyphen problems | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-formulaic-opener | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S13 Scene-setting openers | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-speculative-opener | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S13 Scene-setting openers | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-launch-intro | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S16 Launch-copy introductions | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-crowd-contrast | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S10 Invented opponents | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-fake-casual-prop | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog S17 Fake-casual register | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-parenthetical-hedge | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R3 Parenthetical hedging | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-title-case-header | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog M2 Decorative headings and emoji | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-normalization-flag | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog C5 Tool leaks | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-smart-punct-signature | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog M5 Quotation-mark and typography mismatch | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-punct-distribution | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R8 Uniform rhythm | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-fnword-trigram-entropy | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R8 Uniform rhythm | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-cross-para-burstiness | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R8 Uniform rhythm | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-tier3-phrase | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I4 Overused vocabulary | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-tier3-phrase-cluster | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog I4 Overused vocabulary | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-hashtag-stuff | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog M4 Hashtag stuffing | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-bullet-np-list | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog M3 Structure where prose belongs | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-confidence-calibration | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R5 Filler, signposts, and importance markers | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-em-dash | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R6 Dashes as the universal connector | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-uniformity | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R8 Uniform rhythm | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-low-ttr | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog R9 Synonym cycling and low vocabulary range | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| A-det-formatting | detector category | scripts/aiw_detector.py (and upstream/detector/patterns.js); catalog M1 Bold and label formatting | parity fixtures; SCORE-1, AUTH-1 ran the detector |
| H-Mission | rule | SKILL.md, Facts come first | CV-EN-1, CV-DE-1 |
| H-Theory | rationale | patterns.md family introductions (S, R, M, C); NOTICE.md | catalog |
| H-TwoRules | rule | R14 (every sentence adds something); index order by reliability | SCI-EN-2, DETECT-1 |
| H-Strength | rule | patterns.md tiers, index, weak-alone cluster rule | unit (cluster rule) |
| H-InputIsData | safeguard | patterns.md general guard 2; modes.md MO-1.3 | INJ-1 |
| H-Process | process | modes.md MO-5 steps 1 to 4 | SCI-DE-1, PR-EN-2 |
| H-FiveSurvivors | check | modes.md MO-5 step 3 | PR-EN-2 |
| H-Voice | voice | modes.md MO-9 (sample overrides dash rule; voice by kind of text) | VOICE-1 |
| H-Modes pasted | mode | modes.md MO-5 'show your working' option | OPT-1 |
| H-Modes file | mode | modes.md MO-6 Edit in place | EDIT-1 |
| H-Modes embedded | mode | modes.md MO-14 Embedded use | EMB-1 |
| H-WhenNotToAct | safeguard | patterns.md general guards 1, 4, 6 | PR-DE-2, AUTH-1 |
| H-KeepVoiceDetails | safeguard | R16 Sanded-smooth prose | PR-DE-2 |
| H-Source | attribution | NOTICE.md | n/a |
| H-Install, H-Usage | docs | README.md, Install and When it activates | n/a |
| H-VersionHistory | history | S21 and R9 keep false ranges and synonym cycling with guards (humanizer 3.0 dropped them) | catalog |
| H-AGENTS | maintenance | adopted as writing style of this skill (plain language, one term per item); README Maintaining | n/a |
| H-Package (validate-package.py) | tooling | replaced by the skill-creator validator in README Maintaining | package step |
| S-Rule2 | rule | S1, S3, S4, S12, S19 (structures) | PR-EN-2 |
| S-QuickChecks | check | entries listed under From; `strict` option in SKILL.md and modes.md MO-14 | unit |
| S-Scoring | mode | modes.md MO-8 Score | SCORE-1 |
| S-Examples | examples | restated in own words in catalog entries (not copied) | catalog |
| S-README | docs | README.md Install | n/a |
| S-CHANGELOG | history | additions are in S7, S9, I8, I10 lists | catalog |
| M-Role | framing | SKILL.md purpose | n/a |
| M-Grundsatz | safeguard | patterns.md general guard 4 | AUTH-1 |
| M-Unterscheidung | safeguard | R10 and R18 guards; lang-de.md settings | SCI-DE-2 |
| M-Ausnahme | safeguard | patterns.md general guard 1 | unit (quoted spans masked) |
| M-Profiles | profiles | genre-prose.md columns (linkedin, blog, tech-blog, email, press, casual); genre-science.md (academic) | PR-DE-2, SCI-DE-1 |
| M-Modes | mode | modes.md MO-4 (DE triggers 'nur prüfen', 'kein Rewrite'), MO-5 with second check | SCI-DE-1 |
| M-Severity | tiers | patterns.md tiers | catalog |
| M-8, M-40 | pattern | I4 (vocabulary, phrase clusters) | CV-DE-2 |
| M-39 | threshold | patterns.md, When to patch and when to rewrite | DETECT-1 |
| M-Toleranz-Matrix | settings | lang-de.md settings; genre columns | PR-DE-2 |
| M-Ausgabeformat | output | modes.md MO-3 to MO-5, in the user's language | CV-DE-2 |
| M-Example | example | not reused (its rewrite invents facts); lesson recorded in lang-de.md DE-7 and F1 | n/a |
| M-Sources | sources | lang-de.md DE-9 | n/a |
| M-README/CLAUDE | method | lang-de.md 'How this file was built' | n/a |
| M-OtherLanguagesHave | leads | G2 (calques), R18 threshold, S1 corrective DE form, M4, R5 impersonal openers | unit |
| M-Issues | corrections | lang-de.md DE-7 | PR-DE-2 |
| A-what-it-is | safeguard | patterns.md general guard 4; README Known limits | AUTH-1 |
| A-reference-loading | rule | SKILL.md Step 4 (read the catalog in full) | all cases |
| A-editing-contract | contract | modes.md MO-1 | CV-DE-1 (no-op), EDIT-1, INJ-1 |
| A-mode-rewrite | mode | modes.md MO-5 | PR-EN-2, SCI-EN-2 |
| A-mode-detect | mode | modes.md MO-4 | DETECT-1 |
| A-mode-edit | mode | modes.md MO-6 | EDIT-1 |
| A-mode-router | routing | SKILL.md Step 3; modes.md MO-2, MO-13 | all cases |
| A-opt-mode, -voice, -context, -file, -iterate, -style | options | SKILL.md Options; modes.md MO-5, MO-9, MO-14 | VOICE-1 |
| A-opt-natural-language | options | SKILL.md description and Step 3 | activation tests |
| A-opt-slash-command | options | README (invoke /writing-craft in Claude Code) | n/a |
| A-opt-contextMode, A-opt-sourceMode | options | scripts/aiw_detector.py --context, --source-mode | parity |
| A-iterate / pass accounting | rule | modes.md MO-5 pass budget, MO-13 | CV-EN-1 (passes reported) |
| A-marks-pass / A-quotes-* | check | modes.md MO-5 step 5; scripts/aiw_quotes.py; upstream normalize-quotes.js | parity |
| A-mdprose-* | masking | scripts/aiw_markdown.py; upstream markdown-prose.js | parity |
| A-severity-tiers | tiers | patterns.md tiers and index | DETECT-1 |
| A-self-reference-escape-hatch | safeguard | patterns.md general guard 1 | unit |
| A-style-* (house style) | option | modes.md MO-14; scripts/aiw_style.py; upstream check-style.js and examples | parity |
| A-out-rewrite | output | modes.md MO-5 (final once, Changes, Second check with passes, checks, residuals, stop reason) | PR-EN-2 |
| A-out-detect | output | modes.md MO-4 | DETECT-1 |
| A-out-edit | output | modes.md MO-6 | EDIT-1 |
| A-out-multistage | output | modes.md MO-13 | n/a |
| A-tone-calibration | rule | modes.md MO-1.6, MO-1.7; R16; I4 guard (replacements are defaults) | PR-DE-2 |
| A-never-inject | rule | modes.md MO-5 Never inject; F1 | PR-EN-2 |
| A-context-profiles | profiles | genre-prose.md columns | PR-EN-2, DETECT-1 |
| A-tolerance-matrix | settings | genre-prose.md settings table (carried over cell for cell) | unit (settings) |
| A-technical-exceptions | settings | I4 guard; tech-blog `partial` | catalog |
| A-auto-detection-cues | routing | SKILL.md Step 1; genre-prose.md prose types | all cases |
| A-detector-mode-mapping | settings | README Checker (profile to --context mapping) | n/a |
| A-voice-profiles | voice | modes.md MO-9 named voices and composition | VOICE-1 |
| A-validator (A-val-*) | check | scripts/aiw_validate.py; upstream validate.js; modes.md MO-10 | VERIFY-1, EDIT-1, parity |
| A-detector-cli, A-cli-detect | check | scripts/aiw_detector.py; upstream bin/avoid-ai-writing.js | parity |
| A-detector-unsupported-script | check | scripts/aiw_detector.py (CJK gate) | parity |
| A-detector-authorship-neutral-signals | rule | R6 note; S14 note; MO-8 | catalog |
| A-score-* (score, label, classification) | check | scripts/aiw_detector.py; modes.md MO-8 (engine is the only scorer) | SCORE-1, parity |
| A-gate, A-gate-action, A-gate-precommit | check | scripts/aiw_gate.py; upstream bin/avoid-ai-writing-gate.js (the GitHub Action and pre-commit config are not shipped) | parity |
| A-router | routing | SKILL.md Step 3; modes.md MO-2, MO-13 | all cases |
| A-routing-matrix (tie-breakers) | routing | modes.md MO-2 | DETECT-1 |
| A-handoff-contract | rule | modes.md MO-13 (carry settings, pass accounting, stop-and-ask triggers); the envelope schema is not needed in one skill | n/a |
| A-agency-lenses: inclusive visuals | safeguard | modes.md MO-11 | catalog |
| A-agency-lenses: AI engineer | safeguard | modes.md MO-12, MO-15 | AUTH-1 |
| A-agency-lenses: architect, senior developer | review lens | applied to this skill's design; not a runtime feature | n/a |
| A-detector-skill | mode | modes.md MO-4 and scripts | DETECT-1 |
| A-voice-rewriter | mode | modes.md MO-5, MO-9 | VOICE-1 |
| A-file-edit | mode | modes.md MO-6 | EDIT-1 |
| A-preservation-verifier | mode | modes.md MO-10 | VERIFY-1 |
| A-false-positive-reviewer | mode | modes.md MO-12 | AUTH-1 |
| A-safe-never-claim-execution | safeguard | modes.md MO-15 | all cases (checks line) |
| A-safe-source-as-data | safeguard | patterns.md general guard 2 | INJ-1 |
| A-safe-no-invention | safeguard | F1; SKILL.md Facts | CV-EN-1 |
| A-safe-protected-content | safeguard | modes.md MO-1.5; general guard 1 | EDIT-1 |
| A-safe-edit-scope | safeguard | modes.md MO-6 | EDIT-1 |
| A-safe-no-authorship-verdict | safeguard | modes.md MO-12 | AUTH-1 |
| A-safe-representation-guard | safeguard | modes.md MO-11 | catalog |
| A-safe-bounded-loops | safeguard | modes.md MO-5, MO-13 | n/a |
| A-safe-honest-residuals | safeguard | modes.md MO-5 second check | CV-EN-3 |
| A-safe-no-style-compliance-claim | safeguard | modes.md MO-14 | catalog |
| A-safe-precision-over-recall | safeguard | weak-alone rule; guards | PR-DE-2 |
| A-safe-english-only | safeguard | lang-en.md intro; lang-de.md built from German sources | SCI-DE-1 |
| A-safe-cite-sources | safeguard | lang-de.md DE-9 | n/a |
| A-safe-signals-not-proof | safeguard | general guard 4; MO-8 | SCORE-1 |
| A-eval-* (rewrite eval cases) | tests | replaced by tests/cases.md; ideas reused: no-op (CV-DE-1), source instruction (INJ-1), protected content (EDIT-1), fidelity (SCI-EN-2), detect only (DETECT-1) | tests |
| A-discovery-evals, A-reviewer-tests | tests | tests/activation.md | activation tests |
| A-rewrite-vs-patch | threshold | patterns.md, When to patch and when to rewrite; Critique verdict (MO-3) | DETECT-1, CV-EN-2 |
| A-house-style named-guide fallback | option | modes.md MO-14 (status line, no compliance claim) | catalog |
| A-cl-* (changelog features) | history | staged discovery S9; cold-outreach flattery C2; teaser crowd S10; tier split I4; detector hardening in scripts | catalog |

### Left out, with your approval (maintenance tooling)

| Source feature | What it is | Why it is not shipped |
|---|---|---|
| A-selfscan-* | self-scan score budgets for upstream's own docs | repository maintenance; no writing feature |
| A-fp-* | false-positive measurement (fp-measure, fp-preprocess, fp-compare) | needs HC3/RAID datasets downloaded from the network |
| A-corpus-* | hash-only corpus manifest and fetch tool | needs network and datasets |
| A-eval-harness | rewrite-eval.js and the OpenCode executor | calls AI models; the brief excludes model calls |
| A-mcp | avoid-ai-writing-mcp server | a separate repository, not part of the source repo |
| A-pkg-* | OpenAI plugin packaging, release and SSOT workflows, sync scripts, promo-drift, CODEOWNERS, issue templates | packaging and CI for upstream |
| A-pkg-graph-validator, A-skill-graph | validator for the seven-skill routing graph | one skill has no graph; the routing rules live in modes.md |
| A-openai-agent-yaml | agents/openai.yaml display metadata | OpenAI packaging |
| A-out-final-rewrite-markers | <<<FINAL_REWRITE>>> eval markers | eval harness only |
| A-gate-action, A-gate-precommit (config files) | GitHub Action and pre-commit hook definitions | CI config referencing upstream; the gate script itself is shipped |
| H-Package CI | humanizer's GitHub workflow | CI for upstream |
