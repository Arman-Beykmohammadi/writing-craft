### R9 · Synonym cycling and low vocabulary range
Tier P1 for cycling; weak alone for low range.
- **Looks like:** a paragraph that rotates synonyms for one referent ("developers ... engineers ... practitioners ... builders"), obscuring whether they are the same people; or the opposite, a text locked on a narrow vocabulary (type-token ratio under 0.40 in general prose of 200+ words; human prose usually lands around 0.50 to 0.65 in English). DE: "Entwickler ... Programmierer ... Softwareingenieure ... Codeautoren".
- **Guard:** the right word repeated three times is fine; narrow topics, technical reference, and second-language writing compress vocabulary legitimately; German school teaching encourages synonym variation (relaxed in German). humanizer 3.0 dropped synonym cycling as a human habit; kept here as avoid-ai-writing keeps it, with these guards.
- **Fix:** use the clearest term consistently. Never thesaurus the text to raise TTR; use specific cases already in the source.
- **From:** A-synonym-cycling, A-vocabulary-diversity (TTR), A-vocabulary-repetition-vs-cycling, M-10 (relaxed).

### R10 · Passive voice and missing actors
Tier P2, weak alone.
- **Looks like:** the actor hidden or the subject dropped where it matters: "No configuration file needed.", "The results are preserved automatically.", "Support for nested queries was added.", "Mistakes were made.", "The decision was reached." stop-slop's full rule: every sentence needs a human subject doing something; no passive constructions. DE: "Es wurde beschlossen, dass", "Fehler wurden gemacht", "Seitens der Geschäftsführung wurde entschieden".
- **Guard:** methods sections and captions (`off`); CV bullets (`off`); terse reference registers (README feature lists, changelogs, parameter docs, commit subjects); German Vorgangspassiv in technical text; when the actor is irrelevant, unknown, or obvious; a single deliberate fragment.
- **Fix:** name the actor if the source identifies it and it clarifies the sentence; never invent "you", a team, or a system component. `strict` applies stop-slop's rule at full strength in genres where it is not `off`.
- **From:** A-subjectless-fragments-and-agentless-passives, H-11, S-Rule3, S-PassiveVoice, S-QuickChecks ("Any passive voice?"), M-Unterscheidung.

### R11 · Adverb load
Tier P2, weak alone (stop-slop's blanket rule, relaxed by genre; `off` in science).
- **Looks like:** stop-slop's rule: no -ly words, no softeners, no intensifiers, no hedges; specific offenders: really, just, literally, genuinely, honestly, simply, actually, deeply, truly, fundamentally, inherently, inevitably, interestingly, importantly, crucially. DE: wirklich, einfach (as filler), eigentlich, tatsächlich, absolut, total, extrem, unglaublich.
- **Guard:** adverbs that carry meaning (only, not, rarely, approximately, independently, statistically significantly, jointly, gern as politeness); German modal particles.
- **Fix:** cut the adverb or show the degree with a sourced fact. Emphasis adverbs are covered more strictly by I8.
- **From:** S-Rule1 ("all adverbs"), S-Adverbs, S-WordPatterns, S-QuickChecks ("Any adverbs? Kill them.").
Density (model): 4 emphasis adverbs per 100 words.

### R12 · Wh- and "So" openers
Tier P2, weak alone (stop-slop rule; `off` in science and CVs).
- **Looks like:** sentences starting with What, When, Where, Which, Who, Why, How as a crutch, especially pseudo-clefts ("What makes this hard is ..."); paragraphs starting with "So". DE: "Was das schwierig macht, ist ...", "Was wir gelernt haben: ...".
- **Guard:** real questions; relative clauses; "When the server restarts, ..." (a normal temporal clause).
- **Fix:** lead with the subject or the verb: "The constraint is ..." or better, name the constraint.
- **From:** S-SentenceStarters, S-QuickChecks.
Check (en): re:^(?:What|Where|Why|How) (?:makes|made|matters|mattered|happens|happened|I (?:learned|found|mean))\b | ^So,
Check (de): re:^Was (?:das|dies) [^.]{0,40}\bmacht, ist\b | ^Was wir gelernt haben

### R13 · Missing through-line
Tier P2.
- **Looks like:** paragraphs that could be rearranged without the reader noticing; no bridge from one paragraph to the next; each paragraph a self-contained module (paragraph-reshuffle immunity).
- **Guard:** genuinely list-like content (FAQs, CV entries, reference entries).
- **Fix:** report the missing through-line. Add connective tissue only when the relationship exists in the source and the scope allows structural edits.
- **From:** A-missing-bridge-sentences, A-paragraph-reshuffle-immunity.

### R14 · Treadmill: low information density
Tier P2 (`extra` in abstracts, letters, emails).
- **Looks like:** paragraphs that restate the premise in fresh words instead of advancing it; 40 to 60 percent could go without losing information. humanizer's first rule: every sentence you keep must add something the reader did not have. stop-slop's density check: anything cuttable?
- **Guard:** deliberate summaries in long documents; abstracts that must restate the title's topic once.
- **Fix:** name what each paragraph contributes; cut throat-clearing locally; substantial condensation needs structural scope.
- **From:** A-treadmill-effect, H-TwoRules (rule 1), S-Scoring (density), S-Rule7.

### R15 · Wall-of-text replies
Tier P2. Conversational registers only (issue and PR comments, chat, DMs, casual email).
- **Looks like:** a reply of roughly under 150 words with four or more sentences and no line break at all.
- **Guard:** formal long-form registers, where one dense paragraph is correct. Upstream tried and reverted a detector for this; it is judgment only.
- **Fix:** report the missing breaks; break at thought boundaries in the source when scope allows.
- **From:** A-wall-of-text-replies.

### R16 · Sanded-smooth prose
Tier P2, weak alone. Also a guard on every rewrite.
- **Looks like:** every irregularity polished away: perfect typography in a register where people type fast (a chat reply, an issue comment); no contractions, no asides, no rough edges in a personal post.
- **Guard:** careful writers exist; immaculate typography is corroborating at most.
- **Fix:** as a finding, note only. As a rewrite rule: keep the writer's typos in casual text if the user did not ask for proofreading, keep contractions, deliberate fragments, sentences starting with "And" or "But", comma splices the voice uses, and the details that carry voice: a specific unusual detail, mixed feelings, dated references, a first-person choice the writer can explain, a genuine aside or self-correction. Over-polishing pushes human text toward the uniformity this catalog flags.
- **From:** A-over-polishing, A-suspiciously-clean-grammar, A-immaculate-typography, H-KeepVoiceDetails, M-38.

### R17 · Hyphen problems
Tier P2.
- **Looks like:** (a) stacked compound modifiers ("a high-quality, well-architected, future-proof solution"); (b) unnecessary hyphens: welded open noun phrases ("research-impact aggregator"), compounds whose standard form is closed ("code-base", "data-set", "time-frame", "road-map"), attributive hyphens used adverbially ("in real-time", "works out-of-the-box", "for the long-term"); hyphenated pairs in predicate position ("the report is high-quality"). DE: split compounds (English interference): "Software Entwickler", "Kunden Service", "Projekt Management" instead of "Softwareentwickler"/"Software-Entwickler"; missing hyphens in multi-part compounds ("E-Mail Adresse" → "E-Mail-Adresse").
- **Guard:** established compounds (high-quality before a noun, open-access, third-party, machine-readable, server-side, real-time dashboard); dialect and house-style variation; hyphenation is copyediting, never authorship evidence.
- **Fix:** keep the hyphen before a noun, drop it after; close standard compounds; keep the modifier that matters. German: join or hyphenate the compound.
- **From:** A-hyphenated-modifier-stacking, A-unnecessary-hyphenation, H-10, N (German split compounds).
Check (en): code-base | data-set | time-frame | road-map | re:\bin real-time(?=\s*[,.!?;:]|\s*$) | re:\bout-of-the-box\b(?=\s*[,.!?;:]|\s*$)
Check (de): re:\bE-Mail (?:Adresse|Konto|Verteiler)\b | re:\b(?:Software|Kunden|Projekt|Daten|Qualitäts) (?:Entwickler|Service|Management|Analyse|Sicherung)\b

### R18 · Noun-heavy style
Tier P1 in German (Nominalstil), P2 and weak alone in English (zombie nouns).
- **Looks like:** actions turned into nouns on weak verbs. EN: "the implementation of the optimization of the process", "make a decision", "conduct an analysis of", "perform an evaluation", "provide assistance". DE: chains of -ung, -heit, -keit, -ion, -ität nouns ("Die Durchführung der Optimierung der Prozessgestaltung erfolgte"), genitive chains of three or more links, Funktionsverbgefüge ("zur Anwendung bringen", "in Betracht ziehen", "zum Einsatz kommen", "einen Beitrag leisten", "Maßnahmen ergreifen", "eine Entscheidung treffen", "Lösungen entwickeln", "in der Lage sein").
- **Guard:** established and legal terms (Qualitätssicherung, Datenschutz-Folgenabschätzung); CV bullets and headings (relaxed); one or two nominalizations; Funktionsverbgefüge that carry a nuance. Threshold: three or more such nouns in one clause, or a three-link genitive chain.
- **Fix:** turn the action back into a verb with an actor from the source (`lang-de.md`, DE-4).
- **From:** M-Tier2 (Funktionsverbgefüge), M-Unterscheidung (only in combination: kept as the threshold), avoid-ai-writing-multilingual RO #16 (nominalization-chain threshold, adapted), N (Schneider, Reiners).
Check (de): zur Anwendung bringen | zur Anwendung kommen | zum Einsatz kommen | in Betracht ziehen | einen Beitrag leisten | Maßnahmen ergreifen | re:\b\w+(?:ung|heit|keit|ion|ität)\s+(?:der|des)\s+\w+(?:ung|heit|keit|ion|ität)\s+(?:der|des)\s+\w+(?:ung|heit|keit|ion|ität)\b
Check (en): conduct an analysis | perform an evaluation | make a decision to | provide assistance to | re:\bthe \w+(?:tion|ment|ance|ence) of the \w+(?:tion|ment|ance|ence) of\b

---

## M. Markup and typography

Templates and visual editors also produce clean formatting. The tell is decoration on every item.

### M1 · Bold and label formatting
Tier P1.
- **Looks like:** bold on phrases with no reason (more than one bolded phrase per major section, or more than three in a short text); vertical lists where every item opens with a bold label and a colon ("**Performance:** Performance improved by ..."); labels closed with a period that makes them look like sentences ("**Intros.** Years of conferences.").
- **Guard:** CV conventions (job titles, employers); proposals and responses to reviewers (bold labels are convention); a bold hook on LinkedIn (relaxed).
- **Fix:** strip most bold; lead the sentence with the key point instead. Strip redundant labels; turn a labeled list into prose only when the labels carry nothing and the scope allows. A label period becomes a colon with a lowercase gloss, or drop the label.
- **From:** A-bold-overuse, A-inline-header-lists, A-list-label-periods, H-19, M-20.
Density (model): more than 3 bold phrases per text (the script counts this).

### M2 · Decorative headings and emoji
Tier P2.
- **M2a Emoji:** emoji in headings or at the start of list items ("## 🚀 What This Means", "💡 **Key Insight:**"); arrows (→) as decoration. Social posts may carry one or two emoji at line ends (relaxed), never mid-sentence.
- **M2b Title case:** subheadings with every major word capitalized when the document uses sentence case ("Strategic Negotiations And Global Partnerships"). In German, nouns are capitalized anyway; the tell is capitalized verbs, adjectives, or conjunctions ("Strategische Verhandlungen Und Partnerschaften").
- **M2c Scaffolding:** a horizontal rule between every section; a top-level heading that repeats the title; formulaic headers ("Overview", "Key Points", "Summary", "Conclusion", "Key Takeaways", "Kernpunkte", "Überblick") on short texts; a heading followed by a one-line warm-up that restates it ("## Performance" / "Speed matters.").
- **Guard:** house styles that use title case; "Fazit" and "Zusammenfassung" as the standard German conclusion headings; CV section headings.
- **Fix:** sentence case, no decoration, the title once; cut the warm-up line; rename a formulaic header with the section's subject only when the scope allows.
- **From:** A-emoji-in-headers, A-title-case-headings, A-excessive-structure (formulaic and fragmented headers), H-20, H-24, M-21 (corrected for German), M-36.
Check (en): re:^#{1,6}\s*[☀-➿\U0001F300-\U0001FAFF] | re:^\s*[-*]?\s*[☀-➿\U0001F300-\U0001FAFF]\s*\*\*
Check (de): re:^#{1,6}\s*[☀-➿\U0001F300-\U0001FAFF] | re:^#{1,6}\s+.*\s(?:Und|Oder|Für|Mit|Von|Zu)\s

### M3 · Structure where prose belongs
Tier P1 for bare noun-phrase lists; P2 otherwise.
- **M3a Excessive bullets:** bullet-heavy sections whose content is not list-shaped; eight or more bullets in under 200 words.
- **M3b Numbered-list inflation:** "Three key takeaways", "Five things to know", "Here are the top seven", "Hier sind 7 Gründe, warum" when the source has no such count of discrete items.
- **M3c Bare noun-phrase bullets:** five or more consecutive bullets of six words or fewer, no verbs, parallel shape ("Stable mining efficiency / Reliable pool connectivity / Optimized performance ..."); DE: "Stabile Systemperformance / Zuverlässige Infrastruktur / Optimierte Prozesse".
- **M3d Too many headers:** more than three headings in under 300 words.
- **Guard:** real lists (steps, parameters, changelogs, ingredients, feature comparisons, API options); CV bullets and skills lines; docs; reviewer responses.
- **Fix:** report during ordinary cleanup; convert to prose or rewrite items as full claims with source details only when the scope allows structural edits. Do not change the item count merely for variation.
- **From:** A-excessive-bullet-lists, A-numbered-list-inflation, A-bullet-lists-of-bare-noun-phrases, A-excessive-structure, M-22, M-36, M-42.
Check (en): re:^(?:here are )?(?:the )?(?:top )?(?:three|four|five|six|seven|eight|nine|ten|\d+) (?:key )?(?:takeaways|things|ways|reasons|tips|lessons)\b
Check (de): re:^hier sind (?:die )?(?:\d+|drei|vier|fünf|sechs|sieben|acht|neun|zehn) (?:Gründe|Tipps|Dinge|Wege|Lektionen)\b

### M4 · Hashtag stuffing
Tier P0 on LinkedIn and investor texts; P2 on blogs.
- **Looks like:** a trailing block of six or more hashtags on a short post, usually mixing one specific tag with broad category tags (#AI #Innovation #FutureTech #Leadership). Five or more is a soft tell on `linkedin` and `investor`.
- **Guard:** not tags: issue and PR numbers (#88, owner/repo#88), 6- and 8-digit hex colours containing a digit (#1a2b3c), C preprocessor directives (#include), URL fragments, Markdown headings, anything in code. Channel names (#general) count, as they are the same token.
- **Fix:** two or three specific tags, or none.
- **From:** A-hashtag-stuffing, avoid-ai-writing-multilingual FR #44 (lead).
Density (model): 6 or more per text; 5 is a soft tell on linkedin and investor (the script counts this).

### M5 · Quotation-mark and typography mismatch
Tier P2, weak alone.
- **Looks like:** curly quotes where the writer or format uses straight ones (plain-text contexts: code comments, commit messages, chat), or the reverse; English curly quotes (“…”) in German text that otherwise uses „…“; mixed styles in one document.
- **Engine-only composite:** the upstream detector also reports a "smart-punctuation signature" (curly quotes, em dash, Oxford comma, and no typos together in 80+ words) as a weak corroborating signal; the script reports it, the model never treats it as evidence alone.
- **Guard:** Word, Google Docs, macOS, and iOS curl quotes by default; curly apostrophes alone are never a finding; locale-correct marks („…“, »…«, «…») stay; finished publications.
- **Fix:** normalize to the document's majority style (the rewrite "marks pass", `modes.md`): straight and curly families are inferred separately; a house-style setting overrides.
- **From:** A-curly-quotation-marks, A-immaculate-typography (typography), A-det-smart-punct, A-marks-pass, A-quotes-infer, H-21, N (German marks).

---

## G. German only

These entries apply only to German text. They have no English counterpart in this catalog (English interference is by definition a German problem).

### G1 · Needless Anglicisms
Tier P2, weak alone. AI link uncertain: these are a German style problem whoever writes them; generated German text often carries them because it is shaped by English.
- **Looks like:** English words used where ordinary German exists and adds nothing: performen, committed sein, Commitment, Learnings, Challenge, Impact (als Schlagwort), Mindset, Awareness, Skills (in prose), Deep Dive, Gamechanger, on top, nice to have, "Best Practices", "State of the Art", upskillen, pitchen (outside startups), leveragen, "einen Call haben".
- **Guard:** established loanwords (Team, Software, Feedback, Workshop, Know-how, Marketing, Start-up, E-Mail, Laptop, Meeting, Management, Projekt); technical terms of the field (Machine Learning, Pipeline, Framework, Deployment, Stakeholder in project management); terms used in the job posting (mirror the posting); IT CVs where English is the domain language; the writer's established voice.
- **Fix:** the German word when it is just as precise (Erkenntnisse, Herausforderung, Wirkung, Denkweise, Fähigkeiten, zusätzlich); otherwise keep the term.
- **From:** N (the user's brief; Duden and German editorial practice), M-Tier3 (Best Practices, State of the Art).
Check (de): ~performen | ~performt | ~Learnings | ~Mindset | ~Gamechanger | ~Game Changer | ~nice to have | ~on top | ~leveragen | ~upskillen | ~committed sein | ~Commitment
Threshold (de): 3 per text

### G2 · English calques and interference
Tier P2.
- **Looks like:** English structure in German words. Idioms: "Sinn machen" (for "Sinn ergeben"; now widespread and listed by Duden as common usage, so weak), "in 2024" (for "2024" or "im Jahr 2024"), "am Ende des Tages", "einmal mehr", "nicht wirklich", "Das ist, wo ...", "ich realisiere" (for "mir wird klar"), "etwas adressieren" (for "ansprechen, angehen"), "einen Unterschied machen", "in Deutsch" (for "auf Deutsch"), "Ich freue mich darauf, von Ihnen zu hören" (weak; common in German letters now). Punctuation: a comma after a sentence-initial adverbial ("Im Jahr 2020, gründete sie ..."); a missing comma before "dass" or a relative clause; genitive apostrophe ("Peter's Buch"); English quotation marks. Word order: English-like placement of the verb in subordinate clauses in careless drafts.
- **Guard:** quotations; established idioms; the writer's register in informal posts.
- **Fix:** the German construction (`lang-de.md`, DE-1, DE-7).
- **From:** N (the user's brief), avoid-ai-writing-multilingual SV #17a, IT #4/#45, RO #10 (calque patterns other languages have; DE lacked one).
Check (de): macht Sinn | Sinn machen | re:\bin (?:19|20)\d{2}\b | am Ende des Tages | einmal mehr | nicht wirklich | ich realisiere | adressieren | einen Unterschied machen | re:\b[A-ZÄÖÜ][a-zäöüß]+'s\b

### G3 · Overstretched verb bracket
Tier P2, weak alone.
- **Looks like:** the finite verb and its completing part (participle, infinitive, separable prefix) separated by a long insertion, so the reader waits for the meaning ("Die Abteilung hat im vergangenen Quartal nach intensiver Abstimmung mit allen beteiligten Fachbereichen und unter Berücksichtigung der neuen Vorgaben die Umstellung ... abgeschlossen"); Schachtelsätze nested two levels or deeper.
- **Guard:** legal text; academic German (relaxed); a short insertion.
- **Fix:** move the completing verb forward, split the sentence, put the main point in the main clause (`lang-de.md`, DE-5).
- **From:** N (Wolf Schneider, practice).

### G4 · Address, register, and letter-convention slips
Tier P1.
- **Looks like:** "Sie" and "du" mixed for the same reader; lowercase "sie/ihnen" for formal address; informal closings in formal texts ("LG", "Liebe Grüße" in an application); "Hallo" to a professor in a first contact; inconsistent gender-inclusive forms in one document; DIN 5008 slips in letters: a comma or period after "Mit freundlichen Grüßen", the word "Betreff:" in the subject line, a capital letter after the comma of the Anrede when the next word is not a noun.
- **Guard:** a quotation; a deliberate register shift the writer explains; private letters (DIN 5008 is a convention for business letters).
- **Fix:** one address form throughout; Grußformel without punctuation (`lang-de.md`, DE-2, DE-3; `genre-prose.md`, PR-2).
- **From:** N.
Check (de): ^LG | ^Liebe Grüße | ^Lieben Gruß | re:^[ \t]*Mit freundlichen Grüßen[ \t]*[,.!] | re:^[ \t]*Betreff:

---

## When to patch and when to rewrite

A structural diagnosis ("the problem is the structure, not the words") is justified when a passage shows five or more vocabulary findings across several families, three or more distinct entries beyond vocabulary, and uniform sentence or paragraph structure. Report that diagnosis (Critique verdict "rewrite"). Rebuild from the source's core point only in Rewrite mode or when the user permits broad restructuring; pattern density neither supplies that permission nor proves the structure is AI-generated.

From: A-rewrite-vs-patch, M-39.
