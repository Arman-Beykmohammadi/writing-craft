## What to remove or fix

Use the editing contract in `../SKILL.md` before applying this catalog. Entries
describe candidate matches, not automatic edits. Check each entry's context,
pass conditions, protected status, and surrounding meaning before reporting a
finding; change it only when the user's mode and scope authorize that edit.
Replacement examples supply wording, not new facts.

### Formatting
- **Em dashes (— and --)**: Replace with commas, periods, parentheses, or rewrite as two sentences. Target: zero. Hard max: one per 1,000 words. This applies to headings and section titles too, not just body prose. Catch both the Unicode em dash (—) and the double-hyphen substitute (--). Carve-out: an em dash acting as the separator in a bulleted or numbered list item that opens with a bolded lead term or a markdown link (`- **Term** — description`, `- [label](url) — description`) is typography, not a prose splice — don't count it toward the rate. Only the list-item form qualifies: a mid-sentence splice still counts, as does a line-initial `**Bold lead** — full sentence` outside a list (itself an AI tell), and the double-hyphen substitute is never carved out.
- **Bold overuse**: Strip bold from most phrases. One bolded phrase per major section at most, or none. If something's important enough to bold, restructure the sentence to lead with it instead.
- **Emoji in headers**: Remove entirely. No `## 🚀 What This Means`. Exception: social posts may use one or two emoji sparingly — at the end of a line, never mid-sentence.
- **Excessive bullet lists**: Flag bullet-heavy sections whose content is not genuinely list-like. Convert them to prose only when the user's scope permits restructuring; otherwise report the structural problem. Feature comparisons, step-by-step instructions, and API parameters stay as lists.
- **Curly quotation marks (“ ” ‘ ’) and apostrophes**: Curly quotes and apostrophes (U+201C/U+201D, U+2018/U+2019) are a *weak* paste-from-chat signal — meaningful mainly in plain-text contexts like code comments, commit messages, or plaintext drafts, where nothing auto-curls. Treat as corroborating, never conclusive: Word, Google Docs, macOS, and iOS curl quotes by default, so most human prose contains them too. Don't flag curly apostrophes (U+2019) on their own. Replace with straight quotes in plain-text/code; leave them in finished publications and locale-correct punctuation (French « », German „ “).
- **Immaculate typography in casual registers**: Same tier as curly quotes — a *weak*, register-scoped signal, never conclusive alone. Perfect spacing, punctuation, and capitalization in a context where humans type fast (issue/PR comments, chat, DMs) is corroborating evidence, not proof: a careful human can type a flawless comment, and a rushed one can type a sloppy one. Judge it alongside other signals. Inverse case worth flagging the other direction: when editing a human's casual text (a Slack message, a quick reply), preserve their typos, contractions, and idiosyncratic capitalization rather than correcting them — smoothing away the rough edges erases the fingerprint that marks the text as theirs.

### Sentence structure
- **"It's not X — it's Y" / "This isn't about X, it's about Y"**: Rewrite as a direct positive statement. Max one per piece, and only if it serves the argument. This includes the **split-sentence form**, where the negation and the correction fall in two separate sentences rather than pivoting on a single dash or comma: "The headline isn't the speed. The real story is Y." Read on its own, each sentence looks like an innocent declarative, which is exactly why the split version slips past a check tuned to the joined phrasing — flag it the same way. AI also stacks the negation across several options before the reveal ("It's not the price. It's not the features. It's the trust."). The multi-negation countdown is the same move inflated; flag it and cut straight to the positive claim. The **tailing negation** is the clipped cousin: a bare negation fragment tacked onto the end of a sentence — "The options come from the selected item, no guessing." Write the constraint as a real clause ("without forcing the user to guess") or cut it. Carve-out: negations enumerating spec constraints in a list ("no dependencies, no telemetry") are list content, not a reveal. Adapted from `blader/humanizer` P9.
- **Hollow intensifiers**: Cut `genuine` / `genuinely`, `real` (as in "a real improvement"), `truly`, `quite frankly`, `to be honest`, `let's be clear`, `it's worth noting that`, and `actually` when it only adds emphasis. The default fix for `actually` is deletion, not substitution: "This actually makes the process simpler" becomes "This makes the process simpler." Keep it when it marks a specific correction or expectation gap the sentence names ("we expected a cache hit; it was actually a miss"), though a direct contrast may still be clearer ("it was a miss, not a hit"). Just state the fact.
- **Vague endorsement ("worth [verb]ing")**: Cut `worth reading`, `worth paying attention to`, `worth a look`, `worth exploring`, `worth checking out`, `worth your time` when it substitutes a generic thumbs-up for a reason. State why something matters only when the source supplies that reason.
- **Hedging**: Cut empty padding such as `it's important to note that` and redundant stacks such as `could potentially`. Preserve a modal or qualifier that carries uncertainty, a condition, or a technical limitation.
- **Missing bridge sentences**: Each paragraph should connect to the last. If paragraphs could be rearranged without the reader noticing, report the missing through-line. Add connective tissue only when the relationship already exists in the source and the user's scope permits structural editing.
- **Compulsive rule of three**: Review repeated ornamental triads. Preserve a grouping of three when the source has three real items or the repetition serves an intentional rhetorical purpose; do not add or remove an item to meet a rhythm quota.

### Words and phrases to replace

Words are organized into three tiers based on how reliably they signal AI-generated text. This tiered approach — adapted from [brandonwise/humanizer](https://github.com/brandonwise/humanizer)'s vocabulary research — reduces false positives on words that are fine in isolation but suspicious in clusters.

- **Tier 1 — Review every match.** These words are strong candidates in their listed senses. Apply the context exceptions and preserve legitimate technical or author-specific uses.
- **Tier 2 — Flag in clusters.** Individually fine, but two or more in the same paragraph is a strong AI signal. Flag when they appear together.
- **Tier 3 — Flag by density.** Common words that AI simply overuses. Only flag when they make up a noticeable fraction of the text (roughly 3%+ of total words).

**Match inflected forms.** Each entry below covers the listed word *and its morphological variants* — adverb (`-ly`), gerund/participle (`-ing`), plural, comparative/superlative, and verb conjugations — unless a variant carries a distinct, legitimate meaning. So `genuine` also flags `genuinely`, `leverage` also flags `leveraging` / `leveraged`, `delve` covers `delving`, and `meticulous` covers `meticulously`. When a variant has a separate honest sense (e.g. `real` meaning factual, not the intensifier in "a real improvement"), judge by context rather than matching blindly.

#### Tier 1 — Default replacements

Tier 1 splits into two bands. Once a match is a justified finding and editing is authorized, both bands use the same replacement approach. What differs is what a flag *means*.

**1A — AI frequency markers.** Words claimed to appear far more often in machine text than in human writing. A cluster of these is evidence about how a passage was produced.

**1B — Clarity edits.** Wordiness and inflated formality. Replacing them is good writing regardless of who wrote the sentence, and a 1B hit is **not** evidence of machine authorship. Measured against 257 paragraphs of verified pre-2023 human prose, 1B entries fire on ordinary professional and formal writing at a meaningful rate — `in order to`, `utilize`, `commence`, `ascertain`, and `endeavor` are simply the words some people reach for. The detector emits these as `tier1-clarity`, weights them like Tier 2, and excludes them from the dense-AI-vocabulary signal so a wordiness fix can never push a document toward an AI classification.

In `detect` mode, report the two bands separately. Presenting a wordiness fix as authorship evidence is the error this split exists to prevent.

Caveat worth keeping visible: the "appears far more often in AI text" claim behind 1A is **inherited, not measured here**. It traces to [brandonwise/humanizer](https://github.com/brandonwise/humanizer), which states a 5–20x ratio without publishing a method or dataset. Treat 1A as a well-supported convention rather than a verified statistic until this repo measures the ratios itself against a machine-written corpus.

##### Tier 1A — AI frequency markers

| Replace | With |
|---|---|
| delve / delve into | explore, dig into, look at |
| landscape (metaphor) | field, space, industry, world |
| tapestry | (describe the actual complexity) |
| realm | area, field, domain |
| paradigm | model, approach, framework |
| embark | start, begin |
| beacon (metaphor) | example, guide, source of hope (name what provides the example or guidance) |
| testament to | shows, proves, demonstrates |
| robust | strong, reliable, solid |
| comprehensive | thorough, complete, full |
| cutting-edge | latest, newest, advanced |
| leverage (verb) | use |
| pivotal | important, key, critical |
| underscores | highlights, shows |
| meticulous / meticulously | careful, detailed, precise |
| seamless / seamlessly | smooth, easy, without friction |
| game-changer / game-changing | describe what specifically changed and why it matters |
| hit differently / hits different | (say what specifically changed, or cut) |
| watershed moment | turning point, shift (or describe what changed) |
| marking a pivotal moment | (state what happened) |
| the future looks bright | (cut — say something specific or nothing) |
| only time will tell | (cut — say something specific or nothing) |
| nestled | is located, sits, is in |
| vibrant | (describe what makes it active, or cut) |
| thriving | growing, active (or cite a number) |
| despite challenges… continues to thrive | (name the challenge and the response, or cut) |
| showcasing | showing, demonstrating (or cut the clause) |
| deep dive / dive into | look at, examine, explore |
| unpack / unpacking | explain, break down, walk through |
| bustling | busy, active (or cite what makes it busy) |
| intricate / intricacies | complex, detailed (or name the specific complexity) |
| complexities | (name the actual complexities, or use "problems" / "details") |
| ever-evolving | changing, growing (or describe how) |
| enduring | lasting, long-running (or cite how long) |
| daunting | hard, difficult, challenging |
| holistic / holistically | complete, full, whole (or describe what's included) |
| actionable | practical, useful, concrete |
| impactful | effective, significant (or describe the impact) |
| learnings | lessons, findings, takeaways |
| thought leader / thought leadership | expert, authority (or describe their actual contribution) |
| best practices | what works, proven methods, standard approach |
| at its core | (cut — just state the thing) |
| synergy / synergies | (describe the actual combined effect) |
| interplay | relationship, connection, interaction |
| keen (as intensifier) | interested, eager, enthusiastic (or cut — just state the interest) |
| genuinely / genuine (as intensifier) | (cut — just state the fact) |
| symphony (metaphor) | (describe the actual coordination or combination) |
| embrace (metaphor) | adopt, accept, use, switch to |
| load-bearing *(metaphor)* | essential, critical, necessary — or say what breaks if you remove it |

**Hyphen required:** unhyphenated "load bearing" is ordinary English ("the load bearing down on the bridge") — only the hyphenated compound is the tell.

**Abstract-noun boundary:** Flag hyphenated `load-bearing` only when it immediately modifies, on the same line, `assumption`, `claim`, `invariant`, `premise`, `constraint`, `dependency`, `argument`, or `abstraction` (including plurals). Preserve literal building terminology, unlisted nouns, intervening modifiers, and predicative uses such as "the wall in the kitchen is load-bearing" or "that claim is load-bearing." Mixed physical/abstract nouns (`structure`, `element`, `frame`, `foundation`, `test`, `detail`) also pass. This deliberately misses some metaphors to avoid flagging ordinary writing; see issue #56.

##### Tier 1B — Clarity edits

Wordiness and formality, not authorship evidence. Same fix, weaker claim.

| Replace | With |
|---|---|
| utilize | use |
| in order to | to |
| due to the fact that | because |
| serves as | is |
| features (verb) | has, includes |
| boasts | has |
| presents (inflated) | is, shows, gives |
| commence | start, begin |
| ascertain | find out, determine, learn |
| endeavor | effort, attempt, try |

#### Tier 2 — Flag when 2+ appear in the same paragraph

These words are legitimate on their own. When two or more show up together, the paragraph likely needs a rewrite.

| Replace | With |
|---|---|
| harness | use, take advantage of |
| navigate / navigating | work through, handle, deal with |
| foster | encourage, support, build |
| elevate | improve, raise, strengthen |
| unleash | release, enable, unlock |
| streamline | simplify, speed up |
| empower | enable, let, allow |
| bolster | support, strengthen, back up |
| spearhead | lead, drive, run |
| resonate / resonates with | connect with, appeal to, matter to |
| revolutionize | change, transform, reshape (or describe what changed) |
| facilitate / facilitates | enable, help, allow, run |
| underpin | support, form the basis of |
| nuanced | specific, subtle, detailed (or name the actual nuance) |
| crucial | important, key, necessary |
| multifaceted | (describe the actual facets, or cut) |
| ecosystem (metaphor) | system, community, network, market |
| myriad | many, numerous (or give a number) |
| plethora | many, a lot of (or give a number) |
| encompass | include, cover, span |
| catalyze | start, trigger, accelerate |
| reimagine | rethink, redesign, rebuild |
| galvanize | motivate, rally, push |
| augment | add to, expand, supplement |
| cultivate | build, develop, grow |
| illuminate | clarify, explain, show |
| elucidate | explain, clarify, spell out |
| juxtapose | compare, contrast, set side by side |
| paradigm-shifting | (describe what actually shifted) |
| transformative / transformation | (describe what changed and how) |
| cornerstone | foundation, basis, key part |
| paramount | most important, top priority |
| poised (to) | ready, set, about to |
| burgeoning | growing, emerging (or cite a number) |
| nascent | new, early-stage, emerging |
| quintessential | typical, classic, defining |
| overarching | main, central, broad |
| quietly | cut, or name the concrete contrast |
| deeply *(significance collocations only — "deeply integrated," "deeply committed," "deeply rooted"; literal uses like "deeply nested" or "cares deeply" never count toward a cluster)* | cut, or name what specifically runs deep |
| underpinning / underpinnings | basis, foundation, what supports |

#### Tier 3 — Flag only at high density

These are normal words. Only flag them when the text is saturated with them — a sign that AI filled space with vague praise instead of specifics.

| Word | What to do |
|---|---|
| significant / significantly | Replace some with specifics: numbers, comparisons, examples |
| innovative / innovation | Describe what's actually new |
| effective / effectively | Say how or cite a metric |
| dynamic / dynamics | Name the actual forces or changes |
| scalable / scalability | Describe what scales and to what |
| compelling | Say why it compels |
| unprecedented | Name the precedent it breaks (or cut) |
| exceptional / exceptionally | Cite what makes it an exception |
| remarkable / remarkably | Say what's worth remarking on |
| sophisticated | Describe the sophistication |
| instrumental | Say what role it played |
| world-class / state-of-the-art / best-in-class | Cite a benchmark or comparison |
| verbatim | Usually redundant with the verb ("copies X verbatim" = "copies X") — cut it. If the exactness marks a contrast, name it: byte-for-byte, word for word, unchanged. Term of art in legal/research/QA registers ("verbatim transcript / record / testimony"), so weigh density in that context before flagging |

#### Tier 3 phrases — Flag at density or in clusters

Multi-word boilerplate that's individually unobjectionable but stacks heavily in AI-generated content (crypto, web3, DePIN, AI/infra reviews are the worst offenders). Flag at **2+ uses of the same phrase** (the per-phrase rule — lower threshold than single-word Tier 3 because a two-word match repeated twice is already stronger evidence than re-using "significant"), *plus* a **cluster rule**: three or more *distinct* phrases from this table in one piece is a strong signal even when each phrase only appears once — that's the shape LLMs take when they vary their own boilerplate to seem less repetitive.

| Phrase | What to do |
|---|---|
| emerging sector / emerging space / emerging category | Name the actual sector or what's emerging about it |
| the integration of (X with Y) | Describe what's being integrated and what changes for the user |
| the intersection of (X and Y) | Pick the specific overlap that matters or cut the framing |
| community-driven | Name what the community does. "Community-driven" alone is filler |
| long-term sustainability | Cite the time horizon and the constraint. "Long-term" is hand-waving |
| user engagement | Name the action. "Engagement" is a wrapper around clicks/comments/retention |
| decentralized compute | Specify the architecture or cut. The phrase has become a category label, not a claim |
| (sustainable) reward emissions | Cite the emission schedule and the sink |
| tokenized incentive structures | Describe the actual mechanism (vesting, gauge, bonded LP, etc.) |
| designed for long-term [X] | Cut "designed for" — either it is or it isn't. Then state the property |

#### Audience-fit note: domain-term collision (judgment only)

In cryptography writing, flag generic "proof" or "proof point" only when a reader could mistake supporting evidence for a cryptographic proof. This is a P2 clarity check, outside the vocabulary tiers and deterministic phrase table. Preserve literal cryptographic proofs, ordinary "proof of purchase," and strategy uses whose meaning is clear. Adapted from `welttowelt/stop-slop-refined` ([#108](https://github.com/conorbronsdon/avoid-ai-writing/issues/108)).

| Ambiguous use | Clarify using source facts |
|---|---|
| "The launch is our proof" in a discussion of cryptographic guarantees | "The launch is evidence of demand" only if demand is the claim being supported; otherwise ask what the launch demonstrates. |
| "This demo is our proof point" when readers could infer a security proof | Name what the demo demonstrates; preserve "proof point" when the passage already distinguishes it from a cryptographic proof. |

### Template phrases (avoid)

These slot-fill constructions signal that a sentence was generated, not written. If a phrase has a blank where a noun or adjective could go and still sound the same, it's too generic.

- "a [adjective] step towards [adjective] AI infrastructure" → use a capability, benchmark, or outcome already supplied; otherwise cut the empty modifier or flag the missing detail
- "a [adjective] step forward for [noun]" → same rule: say what changed only when the source establishes it
- "Whether you're [X] or [Y]" → false-breadth construction. Pick the audience you're actually addressing, or cut. "Whether you're a startup founder or an enterprise architect" means nothing — it's just "everyone."
- "I recently had the pleasure of [verb]-ing" → review/social AI pattern. Just say what happened: "I talked to," "I read," "I attended."

### Transition phrases to remove or rewrite
- "Moreover" / "Furthermore" / "Additionally" → restructure so the connection is obvious, or use "and," "also," "on top of that"
- "In today's [X]" / "In an era where" → cut or state specific context
- "It's worth noting that" / "Notably" → just state the fact
- "Here's what's interesting" / "Here's what caught my eye" / "Here's what stood out" → reader-steering frames. Let the content signal its own importance. If the source explains why a detail matters, lead with that explanation; do not invent one to replace the frame.
- "In conclusion" / "In summary" / "To summarize" → your conclusion should be obvious
- "When it comes to" → just talk about the thing directly
- "At the end of the day" → cut
- "That said" / "That being said" → cut or use "but," "yet," or "however." Don't overuse any one of them.

### Structural issues
- **Uniform paragraph length**: Review repeated same-size paragraphs when their boundaries do not follow the argument or the rhythm sounds accidental. Preserve regular structure when the genre, source voice, or content calls for it. If editing is justified and authorized, adjust boundaries around source-supported ideas rather than imposing short and long paragraph quotas.
- **Formulaic openings**: If the piece opens with broad context before getting to the point ("In the rapidly evolving world of..."), cut local throat-clearing during ordinary cleanup. Moving context or rebuilding the opening requires scope that permits structural editing; use only news or insight already supplied.
- **Suspiciously clean grammar**: Don't sand away all personality. Deliberate fragments, sentences starting with "And" or "But," comma splices for effect: if the natural voice uses them, keep them.

### Significance inflation
- Phrases like "marking a pivotal moment in the evolution of..." or "a watershed moment for the industry" inflate routine events into history-making ones. State what happened and let the reader judge significance.
- If the sentence still works after you delete the inflation clause, delete it.

### Aphorism formulas
- Slot-fill profundity: "X is the language of Y," "X is the currency of Z," "the architecture of trust," "X becomes a trap," "X is not a tool but a mirror." The formula turns an ordinary claim into something that sounds quotable without adding precision — the shape does the persuading instead of the evidence.
- Fix: replace the formula with the source-supported claim it gestures at. If the source says users found symmetric layouts more predictable, state that result directly; do not invent it from the metaphor alone.
- Distinct from significance inflation (which puffs up an event's importance) and from the persuasive-authority tropes under Confidence calibration (which announce depth): this pattern manufactures a general law out of a specific observation.
- Carve-out: quotations and established idioms ("time is money") are attributed speech or common coin — leave them. Adapted from `blader/humanizer` P32.

### Generic future-narrative closers
- "May become one of the most important narratives of the next market cycle," "could become the defining trend of the coming decade," "is poised to become the next major chapter in [X]." AI defaults to this shape when it needs to land a closing thought without committing to a falsifiable claim. The closer is grammatically a prediction but contains no testable content.
- Pattern: modal (may / could / will / is poised to) + "become" + (one of) the most [adjective] + (narrative / story / trend / theme / chapter / movement / force).
- Fix: use a falsifiable version only when the source supplies the claim and its details; otherwise cut the empty closer or flag the missing detail. "DePIN compute may exceed AWS spot pricing for embarrassingly parallel workloads by 2027" is a prediction when those terms came from the source. "The intersection of AI and DePIN may become one of the most important narratives of the next market cycle" is not.

### Hedge-stacked predictions
- Stacking a modal with a hedge adverb: "could potentially create," "may eventually unlock," "might ultimately transform." Either word alone is acceptable; the stack is the tell. Each hedge cancels the next, leaving a sentence that asserts nothing while sounding cautious and thoughtful.
- Fix: keep the one qualifier that retains the source's intended uncertainty. If the intended confidence is unclear and the distinction matters, leave it and ask rather than choosing a stronger claim.

### "Real/actual" adjective inflation
- "Real on-chain tokenomics," "actual reward sustainability," "genuine utility," "true product-market fit." Using `real` / `actual` / `genuine` / `true` as an empty intensifier on an abstract noun implies the rest of the field is fake or superficial — without naming what makes this instance the real one. Common in crypto/AI/web3 content where the writer wants to signal sophistication.
- Distinct from the existing "hollow intensifiers" rule (genuine / truly / quite frankly as sentence-level hedges). This is the noun-modifier form, where the intensifier latches onto an abstract noun to manufacture a contrast that goes unsaid.
- **Carve-out — named contrast:** if the sentence explicitly names what the fake/superficial version is, leave it. "Real on-chain settlement, not bridged IOUs" or "actual revenue from paying customers, not grants" is honest contrastive writing. The AI tell is the unsaid contrast.
- Fix when no contrast is named: drop the adjective. Add a specific claim only when the source supplies it. For example, a source that already says rewards come from monthly fees rather than emissions can state that contrast directly.

### Moral-adjective category errors
- AI glues moral or character adjectives (`honest`, `genuine`, `faithful`, `truthful`) onto non-agentic technical nouns (`shape`, `number`, `representation`, `accuracy`, `curve`, `output`) where the adjective cannot literally modify the noun. "An honest shape" — shapes are not moral agents; it is a category error. The same move appears as the adverb form: "described honestly," "flagged honestly" — the passive voice hides that there is no subject capable of honesty.
- **Fix:** state a concrete property only when the source establishes it; `realistic` and `clearer` are valid replacements only when those are the intended properties. Otherwise cut the unsupported moral adjective or flag the missing property. Cut empty moral adverbs from passive constructions — "flagged honestly" → "flagged" or "noted" when that preserves the source action.
- **Related — ontological slop on assumptions:** "The assumption stops being true." Assumptions do not flip from true to false; they degrade in adequacy. Write "the assumption breaks down" or "no longer holds."
- **Related — gratuitous universal quantifiers:** "Taught in every first-year biochemistry course" instead of "taught in introductory biochemistry." The universal claim ("every") is unverifiable and unnecessary — it borrows authority from a scope the writer cannot check. Replace with the actual scope or drop the quantifier.

### Transformation crutch
- Flag repeated unexplained relabeling across a passage: "the concern turns into panic," "a feature turns into a strategy," "the risk becomes real." Ask what changed; read the surrounding passage before deciding the explanation is missing. Treat this as a P2 clarity judgment, not evidence of AI authorship.
- For a flagged passage, ask what changed. If the writer supplies the missing action, threshold, or consequence, use those supplied facts in the rewrite; never invent a mechanism or actor. If the explanation was already present, apply the pass conditions below instead of rewriting it under this rule.
- Preserve literal transformations ("water turns into ice"), supported metaphors, and changes explained anywhere in the passage ("the queue turns into a bottleneck" after a stated capacity limit). Deliberate summaries of explained changes pass, including multiple summaries in one passage. Repeated labels with no explanation still flag. Adapted from `welttowelt/stop-slop-refined` ([#108](https://github.com/conorbronsdon/avoid-ai-writing/issues/108)).

### Hashtag stuffing
- Long trailing hashtag blocks (6+ hashtags on a single short post) are near-universal in LLM-generated social content and rare in thoughtful human posts. The block usually mixes a project-specific tag with broad category tags (#AI #Crypto #Web3 #Innovation #FutureTech #Technology) — the categorical ones do nothing for discoverability and read as bot output.
- **Why 6?** Empirical floor. LinkedIn and X organic engagement plateaus or declines past 3-5 tags; human posts that exceed 5 are usually launch posts trading reach for engagement, while LLM-generated posts default to 10-15. Six is the threshold where false positives on legitimate human use start dropping below false negatives on AI output. The detector treats 6+ as a hard flag; the spec treats 5+ as a soft tell worth a second look on `linkedin` and `investor-email` profiles.
- **What doesn't count.** A `#` in technical prose is usually not a tag. Issue and PR references (`#88`, `#1234`), 6- and 8-character CSS hex colours that contain a digit (`#1a2b3c`), C preprocessor directives (`#include`), URL fragments, `owner/repo#88`, Markdown headings, and anything inside a code span or fence are all subtracted before the threshold applies. Short hex-shaped words stay counted, because `#fff`, `#dad`, `#b2b` and `#decade` are also real tags. A channel name (`#general`) is the same token as a tag and stays counted too, since separating them needs a guess about intent.
- Fix: 2-3 specific tags max, or none. If a hashtag wouldn't help a reader find related work, it's filler.

### Bullet lists of bare noun phrases
- A list of 5+ consecutive bullet items where each item is a short (≤6 word) adjective-plus-noun phrase with no verb. "Stable mining efficiency / Reliable pool connectivity / Optimized RandomX performance / Low failed share rates / Effective hardware utilization / Consistent thermal stability." Reads as a marketing one-pager because that's the shape LLMs default to when asked to summarize features.
- The tell is the *symmetry*: every item is the same grammatical shape, every item is parallel in length, none of them assert anything checkable. A genuine list of observations would have varying length, occasional verbs, and at least one item that doesn't fit the pattern.
- Fix: when structural editing is authorized, convert the list to prose or rewrite items as full claims using details the source provides. If the source records a rate and measurement period, state those values instead of "Low failed share rates"; do not invent them. If the list is genuinely the right form, preserve it rather than changing item count or shape merely for variation.
- This rule does *not* apply to genuine list content (changelog entries, todo lists, parameter docs, ingredient lists) where bare noun phrases are the correct form. The detector keys on absence of finite verbs to separate the two — but in prose audits, ask whether the bullets are summarizing claims (rewrite) or enumerating items (leave).

### Copula avoidance
- Review passages that replace "is" or "has" with fancier verbs such as "serves as," "features," "boasts," "presents," or "represents." The substitutions can make plain prose sound like a press release when they add no meaning.
- Default to "is" or "has" unless a more specific verb genuinely adds meaning.

### Subjectless fragments and agentless passives
- Sentences with the subject dropped or the actor hidden: "No configuration file needed." "The results are preserved automatically." "Support for nested queries was added." The clipped no-subject form is a shape LLMs reach for when compressing feature descriptions, and the passive hides who does what.
- Fix: name the actor when the source identifies it and the actor clarifies the sentence. Prefer active voice unless the actor is irrelevant; do not invent `you`, a team, or a system component.
- Carve-out: terse reference registers where the fragment is the correct form — README feature lists, changelog entries, parameter docs, commit subjects ("No breaking changes"). Flag in flowing prose; skip in docs and casual registers (see the tolerance matrix). A single deliberate fragment for emphasis is rhythm, not a tell. Adapted from `blader/humanizer` P13.

### False agency
- Flag an obscured accountable decision-maker: "The decision emerged after the offsite" leaves unclear who made the choice. Apply only when a specific person or team exercised judgment or choice and naming them matters to the passage. This is a P2 clarity judgment, not evidence of AI authorship.
- Name the actor only when the source identifies them. If the passage identifies the board as the decision-maker, write "The board decided after the offsite." Otherwise ask who decided; do not invent "we," a team, or an interpreter for the data.
- Preserve conventional personification ("the data shows adoption is early"), literal system behavior, and collective shorthand ("the market rewards shipping"). "The culture shifted" may describe emergent change; "a bet lives or dies on distribution" expresses causal dependence. Neither alone establishes a hidden decision-maker. A consequential choice attributed to an abstraction, with its responsible actor missing, still flags. Adapted from `welttowelt/stop-slop-refined` ([#108](https://github.com/conorbronsdon/avoid-ai-writing/issues/108)).

### Synonym cycling
- Review a paragraph that rotates synonyms such as "developers… engineers… practitioners… builders" for the same referent. If the variation obscures the clearest term, use that term consistently.
- If the same noun or verb appears three times in a paragraph and that's the right word, keep all three. Forced variation reads as thesaurus abuse.

### Vague attributions
- "Experts believe," "Studies show," "Research suggests," "Industry leaders agree" — without naming the expert, study, or leader. Cite the specific source when the user or source supplies it. Otherwise flag the gap or cut the unsupported claim; do not turn an attributed claim into the writer's own assertion by simply dropping the attribution.

### Filler phrases
- Strip mechanical padding that adds words without meaning:
  - "It is important to note that" → (just state it)
  - "In terms of" → (rewrite)
  - "The reality is that" → (cut or just state the claim)
- Note: "In order to," "Due to the fact that," and "At the end of the day" are covered in the word/phrase table and transition sections above — don't duplicate rules.

### Generic conclusions
- "The future looks bright," "Only time will tell," "One thing is certain," "As we move forward" — these are filler disguised as conclusions. Cut them. Add a closing thought only when the source supplies one; do not invent a specific conclusion to replace filler.

### Chatbot artifacts
- "I hope this helps!", "Certainly!", "Absolutely!", "Great question!", "Feel free to reach out," "Let me know if you need anything else" — these are conversational tics from chat interfaces, not writing. Remove entirely.
- Also watch for: "In this article, we will explore…" or "Let's dive in!" — these are AI-generated meta-narration. Cut or rewrite with a direct opening.

### "Let's" constructions
- "Let's explore," "Let's take a look," "Let's break this down," "Let's examine" — AI uses "let's" as a false-collaborative opener to ease into a topic. It's filler that delays the actual point. Just start with the point. "Let's dive in" is covered above under chatbot artifacts, but the pattern is broader than that — flag any "let's + verb" that's functioning as a transition rather than a genuine invitation to act.

### Notability name-dropping
- AI text piles on prestigious citations to manufacture credibility: "cited in The New York Times, BBC, Financial Times, and The Hindu." If a supplied source matters, use its existing context. Do not invent an interview date, venue, or argument to replace the list. One relevant, supported reference beats four name-drops.
- Related — **historical analogy stacking**: rapid-fire lists of past technologies or companies to borrow their weight ("like the printing press, the telegraph, and the internet before it"). The montage substitutes for the argument. Name the one parallel that does analytical work and say what it explains, or cut. Source: tropes.fyi (Historical Analogy Stacking).

### Vague third-party validation
- AI manufactures credibility by pointing at an **unnamed** external authority, usually paired with a generic superlative: "an outside party measuring the same models everyone runs and putting us on top," "independent testing confirms," "third-party benchmarks show we lead," "analysts agree," "studies consistently show." The authority is faceless and the claim unfalsifiable — the reader can't tell who measured what, against whom, or go check.
- Fix: name the source, test, and result only when those facts appear in the supplied material or an explicit user correction. If they are missing, flag the gap or cut the unsupported validation claim rather than inventing a benchmark, date, rank, or metric.
- Carve-out: specifically attributed, checkable validation is legitimate and stays unflagged — a named benchmark, a linked report, a dated audit ("SOC 2 Type II, audited by Prescient Assurance"). The tell is the *vagueness*, not the act of citing outside proof.
- Distinct from **Notability name-dropping**: that flags piling on *specific* prestigious names to borrow their weight; this is the inverse move — the authority is deliberately *unnamed*, which is both harder to check and easier to invent. A passage can run both at once (a vague authority plus a superlative); judge each on its own terms. Raised in #39.

### Superficial -ing analyses
- Strings of present participles used as pseudo-analysis: "symbolizing the region's commitment to progress, reflecting decades of investment, and showcasing a new era of collaboration." These say nothing. Replace them with facts already supplied, or cut them.
- The same move shows up without the -ing: declarative "meaning-telling" that glosses a mundane subject as if it were profound — "this represents a broader shift," "the decision symbolizes a commitment to excellence," "it speaks to a larger trend in the industry." Use a specific consequence only when the source supplies it; otherwise cut the unsupported gloss. Adapted from `Aboudjem/humanizer-skill` P40.

### Promotional language
- AI defaults to tourism-brochure prose: "nestled within the breathtaking foothills," "a vibrant hub of innovation," "a thriving ecosystem." Use a plain description grounded in the source, such as an existing location or startup count. If the source supplies no concrete replacement, cut the promotional modifier rather than inventing one.

### Formulaic challenges
- "Despite challenges, [subject] continues to thrive" or "While facing headwinds, the organization remains resilient." This is a non-statement. Name the challenge and response only when the source supplies them; otherwise cut the unsupported sentence or flag the gap.

### Speculative scenario openers
- "Imagine a world where…", "Picture a future in which…", "Envision a world where…" AI opens an argument with a hypothetical that lists desirable outcomes instead of making a claim. The scenario does the persuading; no evidence is offered.
- Fix: cut the scene-setting and retain the source's claim at the same confidence. "Imagine a world where every deploy is instant" becomes "Every deploy would be instant." Add an effect on release time only when the source supplies it.
- Carve-out: fiction, a thought experiment with a stated payoff, and instructional "imagine you have a sorted array" (a teaching device pointing at a concrete example, not a speculative world) are fine. Flag only the world/future-scenario opener that stands in for an argument. Source: tropes.fyi (Imagine a World Where).

### False ranges
- AI creates false breadth by pairing unrelated extremes: "from the Big Bang to dark matter," "from ancient civilizations to modern startups." These sound sweeping but say nothing. List the actual topics or pick the one that matters.

### Inline-header lists
- Bullet lists where each item starts with a bold header that repeats itself: "**Performance:** Performance improved by..." A targeted cleanup can strip the redundant label and retain the supplied point. Converting the list to paragraphs requires structural scope.

### List-label periods
- In bulleted lists where each item leads with a short label, review a period that makes the label look like a complete sentence before the explanation continues. Strongest form: bold labels (`**Intros.**`, `**Content distribution.**`, `**Developer GTM.**`); the colon form (`**Intros:**`) makes the label-to-explanation relationship explicit. The same shape without bold (`- Intros. Years of conferences and operator network.`) can create the same break — a short noun-phrase label followed by a gloss. The colon reads as "here's what this label means"; the period reads as a sentence that the following clause then contradicts by continuing. Example tell: `- **Intros.** Years of conferences and operator network.` becomes `- **Intros:** years of conferences and operator network.` Fix the period to a colon and lowercase the start of the gloss, or drop the label and write the point as a plain sentence. Carve-outs: when the label span is a full sentence on its own (not a label introducing a gloss), the period is correct; and for the unbolded form, only flag when the leading fragment is clearly a label (a 1-4 word noun phrase, no verb) — a short complete sentence opening a bullet is fine.

### Title case headings
- Review title-case subheadings such as "Strategic Negotiations And Key Partnerships" when the surrounding document uses sentence case. Use sentence case for subheadings; reserve title case for the piece's main title when the house style calls for it.

### Hyphenated modifier stacking
- AI stacks compound modifiers: "a high-quality, well-architected, future-proof solution." The individual hyphens may be correct; the tell is the density. Cut to the modifier that matters. Adapted from `blader/humanizer` P26.

### Unnecessary hyphenation
- Check welded open noun phrases: "research-impact aggregator" becomes "research impact aggregator," "data-source strategy" becomes "data source strategy," and "Python-package usage" becomes "Python package usage."
- Close compounds whose standard form is one word: "code-base," "data-set," "time-frame," and "road-map" become "codebase," "dataset," "timeframe," and "roadmap."
- Remove attributive hyphens when the phrase is used adverbially or as a noun: "in real-time" becomes "in real time" and "works out-of-the-box" becomes "works out of the box." Keep the same compounds before a noun: "real-time analytics," "long-term plan," and "out-of-the-box support."
- Preserve established and technical compounds such as "high-quality," "open-access," "third-party," "machine-readable," "server-side," "field-normalized," and "family-owned." Spelling varies by dialect and house style, so ambiguous pairs are judgment calls rather than automatic rewrites.
- Treat a clear hit as P2 copyediting, not evidence of machine authorship. The deterministic detector uses a curated list and excludes code, quoted material, URLs, paths, filenames, and command flags. General attributive-versus-predicate cases stay judgment-only.

### Cutoff disclaimers
- "While specific details are limited based on available information," "As of my last update," "I don't have access to real-time data." These are model limitations leaking into prose. Use corrected information only when the user supplies it; otherwise remove the unsupported sentence or flag the gap. Never turn missing information into a confident factual claim.

### Speculative gap-filling
- When the model lacks a fact, it fills the gap with hedged speculation dressed up as background: "maintains a relatively low public profile," "is believed to have," "likely began his career in," "appears to have studied." These are guesses formatted as statements. Distinct from cutoff disclaimers, which *admit* the gap — this one hides it behind plausible-sounding filler, which is worse because the reader can't tell what's known from what's invented. Cut the speculation, or use a fact supplied in the source or an explicit user correction. Adapted from `blader/humanizer` P21.

### Unfilled placeholders
- Bracketed slot-fillers that were meant to be replaced before publishing: `[Your Name]`, `[INSERT SOURCE URL]`, `[Describe the specific section]`, `2025-XX-XX`, `<!-- Add citation if available -->`. A visible placeholder in publication-ready prose is an editorial bug: fill it only with content the user supplies, or flag the missing value and leave or delete the surrounding sentence as the authorized scope permits. Preserve placeholders in templates and drafts where they are intentional.
- Catch the obvious shapes: `\[(?:Your|Insert|Add|Enter|Describe|Specify|Choose)[^\]]+\]`, `\b\d{4}-XX-XX\b`, HTML/Markdown comments with placeholder verbs (`add`, `fill in`, `todo`, `insert`).

### Chatbot citation markup leaks
- Internal citation tokens that leak through when text is copy-pasted from chat UIs: `citeturn0search0`, `contentReference[oaicite:0]{index=0}`, `oai_citation`, `[attached_file:1]`, `grok_card`. These are not patterns — they are fingerprints. Their presence is essentially proof the text was generated by a specific chat tool and pasted without cleanup.
- The fix is mechanical: strip every markup token. If the source or user supplies the intended reference, insert it; otherwise flag the citation gap rather than fabricating a reference. Don't try to humanize the markup.
- Adapted from `Aboudjem/humanizer-skill` P34. Worth catching even when nothing else in the text reads as AI — the token itself is enough.

### AI-tool URL parameters
- Tracking parameters that AI tools auto-append to URLs they generate, surviving copy-paste into published content: `utm_source=chatgpt.com`, `utm_source=copilot.com`, `utm_source=openai`, `utm_source=claude.ai`, `utm_source=perplexity.ai`, `referrer=grok.com`. Same logic as citation markup leaks — the presence of the parameter is the signature, regardless of what the surrounding text reads like.
- The fix: strip the AI-referrer tracking parameter from every URL that carries one, and leave the rest of the query string alone — the tracking parameter is the signature, and a functional parameter (`?page=2`, `?v=4`) is not evidence of anything. Keep the URL itself if the link is meaningful; lose only the parameter. Adapted from `Aboudjem/humanizer-skill` P35.

### Novelty inflation
- Unsupported novelty claims present established concepts as if the speaker invented or discovered them: "He introduced a term," "She coined the phrase," "a concept nobody's naming," "a failure mode nobody talks about." Wording alone does not establish that an idea is new.
- Two problems. First, the claim is factually risky: if the concept already has a Wikipedia page or conference talks from last year, claiming novelty makes the writer look uninformed. Second, it flatters the subject in a way that reads as promotional rather than analytical.
- The fix: remove the unsupported novelty claim while preserving any supported action and first-person experience. If the source says Michel demonstrated context poisoning, describe that demonstration; the sentence alone does not establish it. When novelty is uncertain, retain the uncertainty or flag the gap rather than assuming either novelty or prior art.
- Related patterns to flag: "the failure mode nobody's naming," "a problem nobody talks about," "the insight everyone's missing," "what nobody tells you about." These are engagement-bait framings that claim scarcity of knowledge where none exists.
- Also flag invented labels: pseudo-analytical compound terms coined mid-sentence and never defined ("the supervision paradox," "the context-collapse problem," "a coordination tax"). Naming a concept is not explaining it. Define the term on first use or describe the mechanism instead of branding it. Source: tropes.fyi (Invented Labels).

### Infomercial engagement hooks
- Punchy fragment-hooks that tee up a reveal: "The catch?", "The kicker?", "Here's the thing.", "But here's the kicker:", "The best part?", "Plot twist:", "The result?". AI uses these to fake momentum and manufacture suspense around ordinary information — the prose equivalent of a late-night infomercial.
- Distinct from rhetorical-question openers (which stall before a point) and chatbot artifacts (which perform helpfulness): these are mid-flow teasers that pad the rhythm. The fix is to delete the hook and state the thing. "The catch? It only works on weekends." becomes "It only works on weekends." Adapted from `Aboudjem/humanizer-skill` P41.
- The same move in a fake-candid register: "Honestly?", "Look,", "Real talk:", "Let's be honest —" as standalone openers that stage a pause before an ordinary point. The tell is the theatrical setup-and-reveal, not the word — "honestly" or "look" mid-sentence in casual prose is ordinary English and stays unflagged. Adapted from `blader/humanizer` P33.
