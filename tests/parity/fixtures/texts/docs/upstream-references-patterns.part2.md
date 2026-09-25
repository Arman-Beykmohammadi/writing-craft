### Launch-copy dramatic introductions
- "Enter Flowdesk." / "Meet Flowdesk, your new favorite treasury dashboard" / "Say hello to Flowdesk" / "Think Notion meets Figma" — the default LLM shape for product and launch posts, near-deterministic in short social copy. The move introduces the product like a game-show contestant instead of saying anything about it. Sits next to the stale social-ad tells (unlock, elevate, link in bio), but no other entry names the introduction move itself.
- Fix: state only what the source establishes. "Meet Flowdesk, your new favorite treasury dashboard" becomes "Flowdesk is a treasury dashboard." Add capabilities or an audience only when the source supplies them.
- What the detector actually matches, stated exactly: a sentence-initial `Meet` or `Think`, then **one** capitalized token of 2-30 characters. After `Meet X,` it requires one of four launch-copy heads — "your new favorite", "your new go-to", or "the new home/way/standard", and those last three only when followed by "of" / "to" / "in|for" or by the end of the clause. After `Think X` it requires "meets" and a second capitalized token. Three surfaces stay judgment-only on purpose. "Say hello to X", because "Say hello to Grandma." is ordinary human prose. The bare "Meet X, your new [role]" form, which is how humans introduce colleagues, pets, and babies ("Meet Sarah, your new account manager") — the head list is what keeps that clean. And bare "Enter X.", because it is also how UI and documentation instructions are written: "Enter Password.", "Enter Amount.", "Enter Username — your work email." No terminator class or field-name denylist separates those from "Enter Flowdesk.", and the same shape carries stage directions in dramatic scripts ("Enter Hamlet.") and column-style narrative ("Enter Rashford."). Flag it here by judgment, in launch and announcement copy.
- Disclosed residue and misses, measured. Residue: the heads do not know a product name from a person, so "Meet Alice, your new favorite aunt" and "Think Alice meets Bob at noon" fire. Both are accepted — they are person-name variants of the two surfaces this rule exists to catch, and narrowing them would cost the surfaces themselves. Misses: the name is one token, so a two-token product name is not detected ("Meet North Star", "Think Google Docs meets Microsoft Word"). Before the head nouns required a tail, "Meet Rosa, the new home secretary" and "Meet Emma, the new way station manager" fired — the tail is what separates a launch-copy head from a compound noun. Source: `welttowelt/stop-slop-refined` ([#108](https://github.com/conorbronsdon/avoid-ai-writing/issues/108)).

### Fake-casual register
- The register models emit when asked for a lowercase-casual social voice. Infomercial engagement hooks (above) catch "Plot twist:" and the fake-candid openers; the rest of the kit is what survives cleanup, because it sits closest to an actual casual voice:
  - one-word verdict closers as the whole closing line: "wild." / "insane." / "unhinged."
  - stage directions: "*checks notes*", "*chef's kiss*", "*mic drop*"
  - wink asides: "(yes, really)", "(no, seriously)"
  - label-prefix openers beyond plot twist: "hot take", "fun fact", "pro tip", "PSA", "unpopular opinion" — with or without the colon
  - "because of course it does"
  - the self-QA volley: "Is it fast? Yes. Is it cheap? Also yes."
- The tell across all six props is that the drama is outsourced to the prop instead of carried by the content. A post can clear every vocabulary tier and still be wearing this costume, which is exactly why it slips through cleanup.
- Fix: delete the label, wink, or stage business and keep the source's observation. Replace a verdict word with a specific surprise only when the source supplies it; do not invent a reaction.
- Carve-out: a writer whose established voice runs on these props keeps them — the register is a tell for *imposed* casualness, not a ban on playfulness. The detector covers only the mechanical props, and both lists are closed: exactly six asterisk stage directions ("checks notes", "chef's kiss" — the apostrophe is required, straight or curly, because without it "*chefs kiss*" matches the ordinary sentence "At midnight, *chefs kiss* their spouses goodbye" — "mic drop", "takes a deep breath", "sips coffee/tea", "nervous laughter") and exactly four parentheticals, the full (yes|no) x (really|seriously) grid. Verdict closers, label-prefix openers, the self-QA volley and "because of course it does" need register judgment and stay skill-only — no tense gate separates the wink from the ordinary grumble, which uses the same form ("The build failed because of course it did."). Disclosed misses, measured: neighbours in the same register do not fire, including "*checks calendar*" and "(yes, honestly)". A closed list is the price of the precision. Source: `welttowelt/stop-slop-refined` ([#108](https://github.com/conorbronsdon/avoid-ai-writing/issues/108)).

### Social endorsement closers
- The curatorial sign-off LLMs append to LinkedIn and X posts that share or recommend something — usually a colon teeing up a link: "This one is worth your time:", "This one's a must-read:", "I highly recommend giving this a read.", "Do yourself a favor and read this.", "You won't want to miss this one.", "Save this for later.", "Bookmark this.", "Don't sleep on this one.", "Trust me, you'll want to read this.", "Thank me later."
- Why it's a tell: it performs a recommendation without giving the reader a reason to click. The endorsement is generic and demonstrative-anchored ("THIS one is worth your time") — it could sit under any link, which is exactly why an LLM reaches for it to close a share post.
- Distinct from the bare "worth [verb]ing" word-table entry (a single weak word inside a sentence) and from infomercial engagement hooks (mid-flow teasers like "The catch?"): this is the whole closing line of a social post.
- The fix: use a reason or audience only when the source already supplies one, then drop the generic CTA. For example, a source that says a post explains context-window leakage to RAG developers can lead with that description. Do not invent an author, superlative, first-person judgment, technical claim, or audience. If the source gives no specific reason, the share does not need a sign-off; let the link stand on its own.

### Stock reaction framing
- Treat this as a **style heuristic, not an authorship signal**. The current corpus produces no detector hits for this category in either class, so it cannot estimate a direction. For this challenged, unobserved category, the precision-first choice is to keep the finding visible without moving the authorship score.
- Flag the **stock framing**, not the existence of a named emotion: "What surprised me most," "I was fascinated to discover," "What struck me was," "I was excited to learn," "The most interesting part," and the bare section-header variant: "Interesting part of the project:" / "Interesting thing here:" / "Interesting aspect:". These can function as generic list introductions or significance pre-announcements when the sentence would say the same thing without them.
- Keep authentic, specific reactions. "I was surprised" is not a machine tell by itself, and a rewrite must not replace a named emotion with theatrical body language just to satisfy "show, don't tell." Add the changed expectation and reason only when the source supplies them; otherwise preserve the reaction as written.
- Fix only the empty frame. If the reaction adds nothing, lead with the source's concrete fact. If the source supplies the expectation and reason, a specific form such as "I expected X; the 40% drop surprised me because Y" can preserve the reaction. Otherwise keep the authentic reaction or flag the missing context rather than inventing experience.
- Related pattern: "hit differently" / "hits different." Treat it the same way: a vague relatability shortcut is a style problem; a concrete description of what changed or why it mattered is better. Do not infer authorship from the phrase alone.

### Lingering-attention claims
- The share-post frame that claims a thing has occupied the writer's mind: "the line I keep coming back to," "I can't stop thinking about this," "still thinking about this one," "this has been rattling around in my head all week," "I've been chewing on this since Tuesday." The claim is about the writer's attention, not about the thing, and it arrives *before* the reader has any reason to care.
- Distinct from stock reaction framing, which claims a **feeling** ("What surprised me most"). This claims **duration** of attention, which is unfalsifiable and self-flattering in a way a feeling isn't: nobody can check whether you kept coming back to it, and the frame implies the quote earned repeat visits without showing what it earned them with. Also distinct from social endorsement closers, which vouch for a link at the end of a post; this opens one.
- **Carve-out — reason attached.** Leave it when the sentence says *why* the thing recurred: "I keep coming back to Hirschman's exit-voice framing because it predicts which engineers quit and which ones file the RFC." That's a claim about the idea's explanatory reach. The tell is the bare frame with the reason missing.
- Fix: delete the unsupported attention claim and open on the supplied point. "The line I keep coming back to: agents are teenagers" becomes "Agents are teenagers." Attribute the comparison only when the source names its speaker.

### False concession structure
- "While X is impressive, Y remains a challenge" or "Although X has made strides, Y is still an open question." AI uses this to sound balanced without actually weighing anything. Both halves are vague. Make the concession specific only with details and stance the source supplies; otherwise cut the empty frame while preserving both claims and their uncertainty. Do not choose a side for the writer.

### Invented contrast-pair mirroring
- An AI-specific form of forced symmetry: one half of a contrast pair is a legitimate term of art, and the other is the AI inventing its mirror to balance the sentence. "False precision rather than genuine accuracy" — "false precision" is a real statistical term; "genuine accuracy" is a phantom counterpart generated for parallelism. The asymmetry is invisible unless you know which half is real. The same pattern can produce pairs like "real data rather than theoretical models" (both real) or "practical results rather than abstract speculation" (both real), but the AI-specific tell is when one term is borrowed from the domain and the other is entirely fabricated.
- **Fix:** if you need a contrast, reach for an actual opposite. If no real opposite exists, drop the contrast structure and state the positive claim directly. "May create a misleadingly exact number rather than a more accurate one" — the contrast works because both halves are real descriptions.

### Rhetorical question openers
- "But what does this mean for developers?" / "So why should you care?" / "What's next?" — AI uses rhetorical questions to stall before the actual point. State an answer only when the source supplies it; otherwise cut an empty transition or leave an open question open. Rhetorical questions are earned by strong setup, not dropped as section transitions.

### Parenthetical hedging
- "(and, increasingly, Z)" / "(or, more precisely, Y)" / "(and perhaps more importantly, W)" — AI inserts parenthetical asides to sound nuanced without committing. If the aside matters, give it its own sentence. If it doesn't, cut it.

### Numbered list inflation
- "Three key takeaways" / "Five things to know" / "Here are the top seven" — AI defaults to numbered lists because they're structurally safe. A numbered list is justified when the source has that many discrete, parallel items. Report padding during ordinary cleanup; remove or rebuild the list only when structural editing is authorized.

### Reasoning chain artifacts
- "Let me think step by step," "Breaking this down," "To approach this systematically," "Step 1:," "Here's my thought process," "First, let's consider," "Working through this logically" — these are artifacts of chain-of-thought reasoning leaking into published prose. Cut local scaffolding while preserving the supplied reasoning. Reordering the conclusion and evidence requires structural scope.
- Also watch for numbered reasoning steps that read like an internal monologue rather than an argument meant for an audience.

### Sycophantic tone
- "Great question!", "Excellent point!", "You're absolutely right!", "That's a really insightful observation" — these are conversational rewards from chat interfaces, not writing. Remove entirely.
- Distinct from chatbot artifacts: sycophancy specifically validates the reader/questioner rather than just performing helpfulness.
- **Cold-outreach flattery asks.** "I'd value your take on this", "I'd love your perspective", "Curious to hear your thoughts" as the whole ask of a cold email or DM. The line flatters the recipient's judgment to get a reply without saying what the question is or why this person is the one to answer it. Fix: state the specific question and, when the source supplies it, the reason for asking this recipient; if neither exists, cut the line and leave the ask plain. Carve-out: a colleague asking for feedback on a named draft ("I'd value your take on the retry section before Friday") is an ordinary request. Judgment-only. Source: [Charity Majors](https://charity.wtf/p/confessions-of-an-unrepentant-slop) ([#325](https://github.com/conorbronsdon/avoid-ai-writing/issues/325)).

### Narrated candor
- Announcing your own disclosure instead of disclosing: "Two caveats I would rather flag than let you discover later:", "I want to be upfront:", "To be fully transparent:", "Rather than bury this, I'll say it plainly:", "I could have left this out, but:", "Being honest about the limitations here:". The content is "Two caveats:"; the rest advertises the writer's forthrightness.
- Completes the set with two neighbours. Chatbot artifacts perform **helpfulness** ("I hope this helps!"); sycophantic tone validates **the reader** ("Great question!"); this performs **candor about oneself**. Assistant training rewards visible transparency, so the model narrates being forthcoming rather than simply being it.
- Note the shape is usually a matched antithesis (flag rather than let you discover, say plainly rather than bury), which is its own tell — the symmetry is doing the work that content should.
- **The deletion test.** Cut the frame. If the sentence loses no information, it was never content: "Two caveats I would rather flag than let you discover later: X and Y" and "Two caveats: X and Y" say the same thing.
- **Carve-out — the disclosure itself.** Substantive admissions stay, and are the point: "I haven't tested this on Windows", "the numbers in the commit message don't reproduce on my hardware", "this is a mitigation, not a fix". Those carry information. The tell is the separable clause *about* disclosing, not the disclosure.
- **Carve-out — conflict-of-interest disclosure.** "In the interest of full disclosure, I own shares in the company discussed here" is not narrated candor. In journalism, academia, finance, and open-source governance that opening is the conventional label that makes a disclosure legible, and the sentence carries the material fact. Leave it. The same words with nothing behind them ("in the interest of full disclosure, I want to be upfront about my thinking here") are the tell.
- **Not the ordinary comparative.** "I'd rather fix it than let you inherit the mess" is a preference about work, not an announcement about disclosing. The construction only counts when what follows the frame is the *disclosure itself*.
- **Judgment-only, deliberately.** This was implemented as a detector and reverted: every regex tight enough to spare the two carve-outs above stopped matching the tell, and the phrasings are shared with idiomatic disclosure language. Deciding it requires reading whether the clause carries information or only announces that information is coming, which is what a reader can do and a pattern cannot.

### Acknowledgment loops
- "You're asking about," "To answer your question," "That's a great question. The..." — AI restates the prompt before answering. In writing, this is pure filler. The reader knows what they asked. Just answer.
- Related pattern: opening a section by summarizing what the previous section said. If the structure is clear, the reader doesn't need a recap.
- **The deletion test.** Cut the opener. If the reply loses nothing, it was a loop: "You're asking about retries. Retries are how the client handles failures" restates the prompt twice before saying anything.
- **Carve-out — replies that orient the reader.** "To answer your question from Tuesday: the invoice went out on the 3rd" and "You're asking about the retry limit. It is five by default" point at which question is being answered, then answer it. Email, support, and docs replies open this way on purpose.
- **Not analytical framing.** "The question of whether the effect persists is still open" names an open question; it is ordinary academic English, not a restatement of a prompt.
- **Judgment-only, deliberately.** This was a detector and was retired: the phrases are shared with the carve-outs above, and the two reply openers were document-initial in the false positives, so position cannot separate them from the tell. Deciding it requires reading whether the restatement adds anything before the answer arrives.

### Confidence calibration phrases
- "It's worth noting that," "Interestingly," "Surprisingly," "Importantly," "Significantly," "Notably," "Certainly," "Undoubtedly," "Without a doubt" — AI uses these to signal how the reader should feel about a fact instead of letting the fact speak for itself.
- "Here's what's interesting," "Here's the interesting part," "Here are the parts I found interesting" — reader-steering cue that pre-interprets importance. Works when followed by genuinely surprising data; fails when it introduces a restatement of something obvious (which is the AI default).
- One "notably" in a 2,000-word piece is fine. Three in 500 words is AI-style emphasis stacking. Flag by density.
- Related — **persuasive-authority tropes**: "the real question is," "at its core," "fundamentally," "make no mistake," "the truth is." Same move as the calibration phrases above, but they assert depth or stakes instead of feeling: they announce that what follows is important rather than showing it. Cut the trope and lead with the substance. Adapted from `blader/humanizer` P27.

- **Consequence-free explanation:** "This matters because" and "here's why that matters" flag only when they introduce a restatement of importance: "This matters because it is important." Preserve a concrete consequence: "This matters because retries can charge the customer twice." Cut an empty restatement or use an explanation already present; never invent stakes. This addition is a P2 judgment-only clarity check.

### Self-labeling significance
- After listing or describing several items, the writer points back at one and labels it as contrarian / clever / surprising / counterintuitive / key: "That last move is the contrarian one," "This is the interesting part," "That third bullet is the real story," "Here's where it gets clever," "The last bit is the counterintuitive one."
- The label does the work the content was supposed to do. If a move is genuinely contrarian, the reader recognizes it from the description; if it isn't recognizable without the label, the label is unearned. The pattern reads as the writer auditing their own list to flag which item should matter, instead of writing the list so the right item carries the weight on its own.
- Distinct from confidence calibration ("Notably," "Interestingly") which front-loads the cue, and from emotional flatline ("What surprised me most," "The most interesting part") which prefaces a single claim. This pattern back-points after the fact, usually as "[that / this / the Xth / the last] [noun] is the [adjective] one."
- Significance-adjectives that signal the pattern: contrarian, clever, surprising, counterintuitive, interesting, key, important, unusual, smart, brilliant, real, actual.
- Fix: cut the labeling sentence and let the explanation that follows do the work directly. Reordering or expanding an item requires structural scope and source-supported detail.
- Example. Before: "→ Two separate indexes for tiered storage. That last move is the contrarian one. Co-locating related data usually helps cache locality." After: "→ Two separate indexes for tiered storage. Co-locating related data usually helps cache locality." The unsupported label is gone; no reason for splitting the indexes is invented.

### Dramatized contrast against the crowd
- A claim propped on an implied lagging crowd, usually stamped with a date: "shipped it in 2022, while everyone else was still debating timelines," "built it in a weekend, while the industry wrote thinkpieces." A strawman with a timestamp — the crowd is invented, so the contrast costs nothing.
- The never-inject list guards the rewrite side of this move (forced contrarianism); this entry flags it on input. Adjacent to significance inflation and self-labeling significance, but the detectable surface is its own: the trailing "while everyone else..." clause with a dismissive verb.
- **The teaser form.** The same invented, lagging crowd without the "while" clause, usually in a newsletter headline or opener: "the call most leaders still won't make", "the move most founders are too scared to make". The crowd flatters the writer and the reader by implication and names no one. Fix: state the call itself; say who hasn't made it only when the source names them. Judgment-only: the detector matches only the "while everyone else..." branches below. Source: [Charity Majors](https://charity.wtf/p/confessions-of-an-unrepentant-slop) ([#325](https://github.com/conorbronsdon/avoid-ai-writing/issues/325)).
- Fix: state the supported fact and cut the crowd clause. Name a competitor and its action only when the source or user supplies them; otherwise do not replace one invented crowd with a more specific invented foil.
- Carve-out: literal simultaneity is ordinary narrative and stays unflagged — "she read while everyone else watched the movie," "others debated the amendment." The detector matches three branches, gated differently. The debate/speculation branch requires one of "was", "were", "is" or "are", then "still", then a dismissive verb in its **-ing** form, so wire copy, memoir, and fiction using those verbs literally stay clean, as do the adjective ("was still deliberate about"), the passive ("was still debated by pundits"), and the bare present. The think-pieces branch accepts "writing" or "wrote"; the catch-up branch accepts "play", "plays", "played" or "playing", with the auxiliary and "still" both optional. The other two branches carry no "was still" requirement because their wording is stereotyped on its own: "while everyone else wrote think-pieces" and "while everyone else played catch-up". Disclosed residue, measured rather than assumed: the first branch fires on any literal progressive use of its verbs, not just "was still debating" — "while the market was still speculating about the price" and "while others were still arguing about procedure" are ordinary wire copy and both fire. The other two branches fire on literal contrasts of their own: "while everyone else wrote think-pieces from Washington" (a real reporting contrast) and "while everyone else played catch-up in the spring" (sports and classroom narrative). All of that is accepted under precision-over-recall only because the surrounding clause is the tell far more often than not; it is not a gate. The crowd is a closed list too — "everyone else", "others", "the industry", "the market", "the competition" — so measured misses include "while every competitor was still debating timelines" and "while our rivals were still debating timelines". Source: `welttowelt/stop-slop-refined` ([#108](https://github.com/conorbronsdon/avoid-ai-writing/issues/108)).

### Wall-of-text replies (missing line breaks)
- In conversational registers — issue and PR comments, chat, DMs, casual email — humans break a reply at thought boundaries: one idea, then a break, then the next. LLMs default to a single dense block regardless of length. The tell: a reply-length text (roughly under 150 words) with four or more sentences delivered as one unbroken paragraph, no line break anywhere in it.
- Fix: report the missing breaks during ordinary cleanup. When the user's scope permits restructuring, break at thought boundaries already present in the source; do not impose a fixed paragraph pattern.
- Observed in the wild: a maintainer on a GitHub issue called out an assisted-sounding reply with "I prefer to talk human to human" — the dense block-paragraph shape was the tell, not any single word in it.
- Distinct from paragraph-length uniformity (which is about long-form prose where every paragraph is the same size): this rule is about short, reply-length text having *zero* breaks at all, not uneven ones.
- Carve-out: a single dense paragraph is the *correct* shape in formal, long-form registers — a blog intro, a docs paragraph, a deliberately tight one-paragraph email. This rule fires only in conversational reply registers; never flag continuous long-form prose just because it lacks internal breaks. That false-positive class is exactly why the structural detector was reverted (see `detector/CATEGORIES.md` §C), and why the tolerance matrix below is the wrong home for it: a plain issue comment auto-detects to the `blog` profile, so the scoping has to live in this rule's judgment, not in a per-profile strictness cell.

### Recap-flattery opener
- Replying to a person by summarizing their own work back at them with praise before getting to the point: "Thanks for all the legwork here — the migration script and the rollback plan you worked through are what made this possible." The reader already knows what they did; the recap performs appreciation instead of conveying information.
- Distinct from a genuine thank-you, which is short and moves on. The tell is the *recap* — restating specifics the other person already knows, dressed as gratitude, ahead of the actual point.
- Distinct also from two nearby conversational tells: **Sycophantic tone** (generic validation of the reader — "Great question!") and **Acknowledgment loops** (restating the prompt or the prior section). Those echo the *question or context*; recap-flattery echoes the other person's *own work* back at them, dressed as praise.
- Fix: cut the recap and keep any thanks or substantive response the source already contains. Do not add agreement, a review judgment, or promised comments merely to replace the opener.
- Observed in the wild: the same exchange that surfaced the wall-of-text tell above — an assisted-sounding reply opened by recapping the maintainer's own prior work back at them before answering the actual question.

### Excessive structure
- Too many headers in short text: more than 3 headings in under 300 words can signal unnecessary scaffolding. Report the structure during ordinary cleanup; merge sections or use prose transitions only when the user's scope permits restructuring.
- Too many list items: review 8+ bullet points in under 200 words when the material is not genuinely list-shaped. Convert the list to prose only when structural editing is authorized.
- Formulaic section headers: "Overview," "Key Points," "Summary," "Conclusion," "Introduction" — these are default AI scaffolding. During ordinary cleanup, flag an empty label. Rename, merge, or remove headers only when structural editing is authorized, using the source's own subject matter.
- Fragmented headers: a heading followed by a one-line warm-up that restates it ("## Performance", then "Speed matters.") before the real content starts. Cut the warm-up; the heading already did that job. Adapted from `blader/humanizer` P29.

### Diff-anchored writing
- Documentation or comments narrating a change instead of describing the thing as it is: "This function was added to replace the previous approach of iterating through all items." A reader without the commit history gets archaeology, not documentation. The tell comes from how assistants work — they write docs in the context of the edit they just made, so the prose anchors to the diff; a person documenting later writes from the artifact.
- Fix: describe current behavior using implementation and rationale already present in the source. Do not replace change history with an invented data structure, complexity claim, or reason. If the history matters, it belongs in the changelog or commit message when the user's scope permits moving it.
- Carve-out: documents that are inherently version-scoped — changelogs, release notes, migration guides, decision records — narrate change correctly and stay unflagged. Adapted from `blader/humanizer` P30.

### Performed-insight phrases
- A family of essayist tics that announce profundity instead of delivering it: "sit with that for a moment", "that's not nothing", "you already know the answer", "the punchline is", "worth naming", "don't take my word for it", "that's the whole point", "is the entire business model", "that's the part nobody mentions", "the only metric that matters", "X is dead; long live X", "that's why it mattered", the sentence-initial "Turns out", and staged discoveries that frame a judgment as a twist the writer found ("the recording turned out to be the least interesting part", "the real story was"; "what surprised me most" is covered under emotional flatline). Each stages a reveal; none adds a fact.
- One hit can be a stylistic choice — several in one piece is a tell. In short social copy (a post of a few sentences), one staged discovery that carries the post's payoff is enough to fix: it usually stands in for a concrete claim the post never makes. Fix: state the source's claim without the announcement. Replace "That's not nothing" with a size only when the source supplies one; remove "the punchline is" without inventing a new point.
- Carve-out: quoted speech and genuinely comedic writing, where a punchline is literal. The deterministic detector omits "the punchline" and "worth naming" because their literal senses cannot be separated reliably by regex. Source: Simon Willison's [LLM cliché highlighter](https://tools.simonwillison.net/llm-cliche-highlighter).

### Negation chains
- Two or more "no …" items in a row ("No fluff, no filler, no jargon."), two or more "didn't …" clauses stacked for rhythm ("It didn't ask. It didn't wait."), and the negated-then-repeated verb ("Don't call it a pivot. Call it a correction."). The chain performs decisiveness; the items are rarely load-bearing.
- Fix: say what the thing *is*. One negation earns its place when the reader would otherwise assume the opposite; a chain of them is a drumroll.
- Distinct from Manufactured punchlines (same-shape *fragments* for drama) — this fires on the negation structure itself, fragments or not. Source: Simon Willison's LLM cliché highlighter.
- Carve-outs: mid-sentence factual inventories ("the endpoint takes no arguments, no headers, and no body") and sequential narration with restated subjects ("I did not sleep well. I did not eat breakfast.") are ordinary prose. The detector matches only sentence-initial chains of three or more short "no …" items and comma-joined "did not …" chains with the subject elided; two-item chains and everything outside those narrow forms are judgment calls.

### Dev-blog boilerplate
- Stock simplicity claims from developer marketing: "batteries included", "it just works", "zero config", "sane defaults", "small enough to fit in your head". Each substitutes a slogan for a property you could demonstrate.
- Fix: name a concrete behavior only when the source supplies it. "Zero config" may become "installs with no config file" when that equivalence is established; replace "fits in your head" with an API size only when the source gives the count. Otherwise cut the slogan or flag the missing detail.
- Carve-out: quoting a product's own tagline, or discussing the phrase itself. The deterministic detector omits "batteries included" because a software slogan and literal package contents have the same surface form. Source: Simon Willison's LLM cliché highlighter.

### Stacked rhetorical questions
- Two or more questions fired in a row, usually fragments after the first: "Do I know how it works? Where it breaks? Which corners it cut?" Extends Rhetorical question openers (one question stalling before a point) to the chain form, which reads as a performance of curiosity.
- Fix: keep at most one question and use answers or claims already supplied in the passage. Do not convert an open question into an assertion or invent its answer. This remains a judgment call: interviews, FAQs, and dialogue stack questions legitimately, and a regex cannot read register. Source: Simon Willison's LLM cliché highlighter.

### Same-opener sentence runs
- Three or more consecutive sentences opening on the same word ("Maybe nobody needed it. Maybe it solved the wrong problem. Maybe the timing was off."), and its cousin: consecutive sentences built on the same repeated skeleton ("A cart is an object in the system. A chat room is an object in the system."). Deliberate anaphora is a rhetorical device; LLMs reach for it constantly, so a run that isn't doing persuasive work is a tell.
- Fix: keep the first, vary or merge the rest. Judgment-only: whether the repetition is earned is exactly what a pattern can't read, and pronoun-opener runs ("He… He… He…") are ordinary narration. Source: Simon Willison's LLM cliché highlighter.

### Stranded auxiliary contrast
- Landing a reversal on a bare auxiliary: "The tool died; the data didn't." / "Reading mostly passed. Writing didn't." One is a fine sentence; as a recurring rhythm it is a signature LLM move — the clipped contrast poses as earned insight.
- Fix: ration it. If the piece already has one, write the next contrast out in full. Judgment-only: the single instance is legitimate style, and only density across a piece distinguishes voice from tic. Source: Simon Willison's LLM cliché highlighter.

### Colon into a triple
- A colon opening onto exactly three comma-separated items: "separate ports, processes, and local state." The most common shape LLM prose uses to sound concrete — three is the default rhythm, whether or not the content has three parts.
- Fix: audit the list. If there are really two things, or four, write that; if the items are padding, cut to the one that matters. Judgment-only, and noisy by design in technical writing, where three-item lists are often just true — weigh it by genre, not per hit. Source: Simon Willison's LLM cliché highlighter.

### Manufactured punchlines and staccato drama
- A run of clipped fragments engineered so every beat lands like a quotable closer: "It had no preference for symmetry. No aesthetic prior. No nostalgia for human taste. The old rules were gone." Each fragment poses as a reveal; stacked, they read as a drumroll.
- This composes with Rhythm and uniformity below, which encourages fragments and varied lengths: variation is the human signal, and one short sentence that lands a point is exactly that. The tell here is the opposite of variation — three or more same-shape fragments in a row, each carrying manufactured drama.
- Fix: keep a fragment that earns its emphasis and fold the rest into ordinary sentences using only the supplied subject, claims, and causal links. Do not add a product name, rationale, or conclusion that the fragment run does not establish. Adapted from `blader/humanizer` P31.

- **Repeated empty concessions:** Pairs such as "Not always. Not perfectly." flag at P2 only when repeated across a passage to stage honesty without explaining where the claim fails. Preserve two meaningful concessions ("Not during failover. Not for expired tokens.") and an isolated intentional pair. Fold repeated empty concessions into a limitation already stated in the source, or cut them; never invent a failure case. Adapted from `welttowelt/stop-slop-refined` ([#108](https://github.com/conorbronsdon/avoid-ai-writing/issues/108)).

- **Repeated setup/reversal punchlines (P2, judgment-only).** A paraprosdokian reverses the expectation set up by the first part of a sentence. Review two or more such reversals in one piece, especially in hooks, closers, or final list items. Flag only when the repeated reversals replace concrete claims with generic surprise or deflation; repetition alone is not a finding. This subtype concerns setup and payoff across sentences, while the fragment rule above concerns three or more same-shape beats. Treat it as a clarity and rhythm edit, not proof of AI authorship. Adapted from [cland4449's contribution (#130)](https://github.com/conorbronsdon/avoid-ai-writing/pull/130).
- Flag example, in an otherwise unexplained passage: "We planned for every failure mode. Except the one that happened. The migration went smoothly, which is how we knew something was wrong." Both reversals stand in for the missing explanation. A repeated scale-then-deflate line such as "Four steps, and only one of them is yours" belongs here only when the passage never explains the steps or the reader's role. Nearby negative parallelism or staccato drama can support the judgment but does not override these conditions.
- Pass: one supported, voice-appropriate reversal, and repeated reversals that communicate concrete distinctions. "We rebuilt billing to group charges by project. Your invoice total didn't change" carries a specific contrast and stays. Intentional comedy, fiction, speeches, and quotations stay, including pieces with multiple reversals. Read the surrounding passage before deciding that an explanation is missing.
- Fix: keep the supported claim and remove the empty twist. "We planned for every failure mode. Except the one that happened" becomes "We missed a failure mode." If the writer has not named the failure, ask for it; do not invent disk failures, network partitions, clock skew, or other causes. Preserve supplied facts and intentional voice.

### Rhythm and uniformity

These aren't individual word or phrase problems — they're patterns in how the text flows as a whole. AI text is metronomic; human text has varied rhythm.

Structural regularity can matter more than a vocabulary swap. Consistent sentence construction, uniform pacing, and symmetrical phrasing are worth reviewing across a passage, but regularity alone does not authorize a rewrite or establish authorship.

- **Sentence length uniformity**: Review a run of similarly shaped sentences when the rhythm sounds accidental or obscures emphasis. Vary it by clarifying the source, not by imposing word-count bands, adding questions, or chopping sentences into fragments.
- **Paragraph length uniformity**: Review repeated same-size paragraphs when their boundaries do not follow the argument. Keep a regular structure when the genre or content calls for it; do not create one-sentence paragraphs merely for variation.
- **Vocabulary repetition vs. synonym cycling**: AI either repeats the same word mechanically or cycles through synonyms conspicuously. Human writers repeat when the word is right and vary when it's natural — there's no formula.
- **Read-aloud test**: If the text sounds like it could be read by a text-to-speech engine without sounding weird, it's probably too uniform. Human writing has rhythm that resists robotic delivery.
- **Speaker and stance**: Preserve first person, opinions, preferences, and reactions when the source contains them. Their absence is not a finding by itself. An explicit voice transformation may recast an existing stance, but never invent a speaker experience or opinion.
- **Over-polishing**: Aggressively editing out every irregularity can push human writing *toward* AI statistical profiles. Natural disfluency, idiosyncratic word choices, and uneven pacing are what keep text out of the "AI-generated" classification. Don't sand away all personality in pursuit of clean prose. This skill should make writing sound more human, not less — if you apply every rule at maximum strictness, you risk creating the very uniformity you're trying to avoid.

### Vocabulary diversity (stylometric)

In longer pieces (200+ words), look at how much vocabulary the text actually uses. The type-token ratio (TTR) — distinct word types divided by total tokens — is a classical stylometric signal that's easy to read by eye. Human prose at this length usually lands somewhere around 0.50–0.65 in English. AI text trends flatter, sometimes drifting under 0.40 when the model gets locked on a small vocabulary loop.

A very low TTR is not by itself proof of AI authorship — narrow topics, technical reference material, and second-language writing all legitimately compress vocabulary. But on general prose where you'd expect range (essays, articles, social content over ~200 words), a TTR below 0.40 is worth a second look. The fix is rarely to thesaurus the text. Use specific things and cases already present in the source, and repeat a technical term when it is the accurate term.

This is the first of four stylometric signals on the roadmap. Sentence-length burstiness has since shipped in approximated form as the `cross-para-burstiness` detector category. The other two (function-word z-scores against a human-prose reference, POS-bigram log-odds) require either a POS tagger or a reference distribution and aren't implemented as detector categories yet.

### Paragraph-reshuffle immunity (structure test)
- A writer-side diagnostic, not a regex: can you swap two body paragraphs without breaking the piece? If the order doesn't matter, you've written a list of points, not an argument that builds. AI prose often fails this — each paragraph is a self-contained module with no load-bearing connection to its neighbors.
- The diagnosis is structural, not lexical. Report it during ordinary cleanup. Establish a through-line, reorder paragraphs, or convert them to a list only when the user's scope permits restructuring, and use relationships already supported by the source. Adapted from `Aboudjem/humanizer-skill` P38.

### Treadmill effect / low information density (content test)
- Another writer-side test: read each paragraph and ask "what's actually new here?" AI prose frequently restates the premise in fresh words instead of advancing it — lots of motion, no distance covered. The tell is that you could cut 40-60% and lose no information.
- For each paragraph, identify the fact, claim, or turn it contributes. A targeted cleanup may remove local throat-clearing. Substantial condensation or rebuilding requires user scope broad enough for structural editing. Adapted from `Aboudjem/humanizer-skill` P43.

### When to rewrite from scratch vs. patch

Five or more justified vocabulary findings across multiple categories, three or more distinct pattern categories, and uniform sentence or paragraph structure can support a structural diagnosis. Report that diagnosis during ordinary cleanup and patch only the authorized spans. Rebuild from the source's core point only when the user explicitly permits broad restructuring; pattern density does not supply that permission or prove that the structure is AI-generated.

---

## Context profiles

Pass an optional context hint to adjust rule applicability and thresholds. If no context is specified, infer the closest profile from content cues. When the cues are weak or the genre is unfamiliar, keep context-dependent borderline cases as judgment calls.

### Profile definitions

**`linkedin`** — Short-form social. Punchy fragments, visual formatting matter.
**`blog`** — Default. Standard long-form prose. All rules apply at full strength.
**`technical-blog`** — Long-form with code, architecture, APIs. Technical terms get a pass.
**`investor-email`** — High-trust audience. Tighten everything; promotional language is the biggest risk.
**`docs`** — Documentation, READMEs, guides. Clarity over voice.
**`casual`** — Slack messages, internal notes, quick replies. Only catch the worst offenders.

### Detector mode mapping

The skill context profiles map to the detector's `contextMode` values as follows:

| Profile | Detector mode | What differs |
|---|---|---|
| `linkedin` | `marketing` | Uses the LinkedIn tolerance profile in the skill; detector currently scores `marketing` like `general`. |
| `blog` | `general` | Baseline detector behavior; the skill applies the blog tolerance profile. |
| `technical-blog` | `technical` | Enables the detector's technical-context suppressions and applies the technical-blog tolerance profile in the skill. |
| `investor-email` | `marketing` | Uses the stricter investor-email tolerance profile in the skill; detector currently scores `marketing` like `general`. |
| `docs` | `technical` | Enables the detector's technical-context suppressions and applies the docs tolerance profile in the skill. |
| `casual` | `personal` | Uses the casual tolerance profile in the skill; detector currently scores `personal` like `general`. |

The mapping aligns the skill's audience-specific profiles with the detector's broader context modes. The skill still owns the full tolerance matrix; detector modes only control the engine behavior described above.

### Tolerance matrix

Rules not listed in the table apply at full strength across all profiles.

| Rule | linkedin | blog | technical-blog | investor-email | docs | casual |
|------|----------|------|----------------|----------------|------|--------|
| Em dashes | relaxed (2/post OK) | strict | strict | strict | relaxed | skip |
| Bold overuse | relaxed (bold hooks OK) | strict | strict | strict | relaxed | skip |
| Emoji in headers | relaxed (1-2 end-of-line OK) | strict | strict | strict | skip | skip |
| Excessive bullets | skip (lists work on LinkedIn) | strict | relaxed (technical lists OK) | strict | skip (lists are docs) | skip |
| Hedging | strict | strict | relaxed ("may" is accurate in technical) | strict | relaxed | skip |
| Word table (full list) | strict | strict | **partial** (see below) | strict | relaxed | P0 only |
| Promotional language | relaxed (some sell is expected) | strict | strict | **extra strict** | strict | skip |
| Significance inflation | strict | strict | strict | **extra strict** | relaxed | skip |
| Copula avoidance | skip | strict | relaxed | strict | skip | skip |
| Uniform paragraph length | skip (short-form) | strict | strict | strict | relaxed | skip |
| Numbered list inflation | relaxed | strict | relaxed | strict | skip | skip |
| Rhetorical questions | relaxed (1 as hook OK) | strict | strict | strict | strict | skip |
| Transition phrases | skip (short-form) | strict | strict | strict | relaxed | skip |
| Generic conclusions | skip | strict | strict | **extra strict** | skip | skip |
| Hashtag stuffing | strict | strict | strict | **extra strict** | skip (no hashtags in docs) | skip |
| Bullet-NP lists | strict | strict | relaxed (technical option lists OK) | strict | relaxed (parameter lists OK) | skip |
| Tier 3 phrase clustering | strict | strict | strict | **extra strict** | relaxed | skip |
| Future-narrative closers | strict | strict | strict | **extra strict** | skip | skip |
| Social endorsement closers | strict (the LinkedIn share-post tell) | strict | strict | strict | skip | relaxed (1 OK in a DM) |
| Hedge-stacked predictions | strict | strict | relaxed ("could" is hedged accuracy) | **extra strict** | relaxed | skip |
| Real/actual inflation | strict | strict | strict | **extra strict** | relaxed | skip |
| Moral-adjective category errors | strict | strict | relaxed | strict | relaxed | skip |
| Invented contrast-pair mirroring | strict | strict | relaxed | strict | relaxed | skip |
| Subjectless fragments and agentless passives | relaxed (short-form fragments are the register) | strict | relaxed | strict | skip (fragment lists are docs) | skip |

**Technical-blog word table exceptions:** These terms have legitimate technical meaning and should not be flagged in technical context: `robust`, `comprehensive`, `seamless`, `ecosystem`, `leverage` (when discussing actual platform leverage/APIs), `facilitate`, `underpin`, `streamline`, and the noun `harness` in established terms such as `test harness`. Still flag ornamental uses and the listed senses of `delve`, `tapestry`, `beacon`, `embark`, `testament to`, and `game-changer`; `harness` as a stock verb remains subject to its normal rule.

**"Extra strict"** means: review every applicable instance rather than waiting for repetition. The rule's sense and pass conditions still apply. In investor emails, a single unsupported "thriving ecosystem" can undermine the message.

**"Skip"** means: don't audit this category for this profile. The rule doesn't apply or isn't worth the edit.

### Auto-detection cues

When no context is specified, infer from these signals:

| Signal | Inferred context |
|--------|-----------------|
| Under 300 words + hashtags or mentions | `linkedin` |
| Code blocks, API references, or technical architecture | `technical-blog` |
| Salutation ("Hi [name]", "Dear") + investor/fundraising language | `investor-email` |
| Step-by-step instructions, parameter docs, README structure | `docs` |
| No strong signals | `blog` for audit coverage; do not force borderline context-dependent edits |

When the inferred profile materially affects a finding, say which profile you used and why. The user can override it.

---


## Voice profiles

Context profiles (above) set *how strict* to be for an audience. Voice profiles set *how the prose should sound* — the persona. They're independent axes: you can write blunt for a blog or warm for docs. Voice is **optional** — if the writer doesn't name one, infer it from the input's existing register and don't impose a persona on text that already has one.

Every target below is bounded by the Never-inject guardrails: a voice profile can bring out what the source already has, never manufacture what it doesn't.

Each profile is a set of concrete targets, not a vibe:

**`casual`** — When explicitly requested, prefer contractions and direct, conversational sentences; do not force fragments or a sentence-length quota. When inferred, preserve the source's existing casual markers rather than intensifying them. Keep first-person and concrete touches the source establishes. Prefer everyday wording while retaining jargon the audience needs. Keep meaningful warm hedges and cut corporate padding such as "it's worth noting." *Blog posts, social, community.*
