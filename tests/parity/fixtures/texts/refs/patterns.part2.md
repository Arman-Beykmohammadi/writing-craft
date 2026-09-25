### I8 · Hollow intensifiers
Tier P1 for genuine/genuinely, truly, quite frankly, to be honest, let's be clear, it's worth noting; weak alone for the other adverbs.
- **Looks like:** words that assert intensity or sincerity instead of showing it. EN: genuine, genuinely, truly, real (as in "a real improvement"), quite frankly, to be honest, let's be clear, it's worth noting that, actually (emphasis only), really, just, literally, honestly, simply, deeply, fundamentally, inherently, inevitably, interestingly, importantly, crucially, highly, successfully (in CVs), incredibly. Telling instead of showing: "This is genuinely hard", "This is what leadership actually looks like", "actually matters". Performative emphasis: "creeps in", "I promise", "They exist, I promise". Boosters in science: clearly, undoubtedly, remarkably, strikingly. DE: wirklich, echt, absolut, total, extrem, ehrlich gesagt, tatsächlich (emphasis only), zutiefst, schlichtweg, eindeutig (booster), zweifellos, erfolgreich (as filler before every noun), hochgradig.
- **Guard:** "honestly", "to be honest", "ehrlich gesagt" inside a casual or personal sentence are ordinary speech ("Ehrlich gesagt hatte ich ja Bammel"); only a staged opener before a routine claim (S8) or repeated use counts; "actually" marking a specific correction the sentence names ("we expected a hit; it was actually a miss"); "just" meaning "only" or "a moment ago"; "really" in quoted speech; German modal particles (ja, doch, halt, eben, mal) carry tone and are not intensifiers; "genuine" meaning authentic ("a genuine Stradivarius").
- **Fix:** delete; the default fix is deletion, not substitution. Show the degree with a fact from the source if one exists.
- **From:** A-hollow-intensifiers, S-Adverbs (specific offenders), S-TellingNotShowing, S-PerformativeEmphasis, H-12 (actually), N (German, science boosters).
Check (en): genuinely | truly | quite frankly | ^to be honest, | let's be clear | let us be clear | it's worth noting | this is genuinely | actually looks like | actually matters | I promise
Check (de): ^ehrlich gesagt, | schlichtweg | zutiefst | zweifellos
Density (model): the weak markers count at 3 per 300 words.

### I9 · Real/actual inflation
Tier P1.
- **Looks like:** "real", "actual", "genuine", "true" as empty intensifiers on an abstract noun, implying the rest are fake without saying how: "real on-chain tokenomics", "actual reward sustainability", "genuine utility", "true product-market fit", "real impact". DE: "echter Mehrwert", "wirkliche Innovation", "tatsächlicher Impact".
- **Guard:** a named contrast ("real on-chain settlement, not bridged IOUs"; "actual revenue from paying customers, not grants").
- **Fix:** drop the adjective; add a specific claim only if the source supplies it.
- **From:** A-real-actual-inflation.
Check (en): re:\b(?:real|actual|genuine|true)\s+(?:on-?chain\s+)?(?:tokenomics|economics|utility|adoption|sustainability|impact|revenue|fundamentals|demand|value|innovation|traction)\b
Check (de): echter Mehrwert | echten Mehrwert | wirkliche Innovation | tatsächlicher Impact | echter Impact

### I10 · Moral adjectives and sweeping quantifiers
Tier P1.
- **Looks like:** (a) moral or character adjectives on things that cannot have them: "an honest shape", "a faithful number", "flagged honestly", "described honestly"; (b) ontological slop: "the assumption stops being true" (assumptions break down or no longer hold); (c) sweeping quantifiers doing vague work: every, always, never, everyone, everybody, nobody, all, "taught in every first-year course" (stop-slop's lazy extremes). DE: "eine ehrliche Zahl", "ehrlich benannt", "jeder weiß", "immer", "niemand", "alle" in unsupported claims.
- **Guard:** literal universals that are true ("every request is logged" when the source says so); idioms; quantifiers in quoted speech.
- **Fix:** state the concrete property the source establishes ("realistic", "clearer") or cut; replace the universal with the actual scope, or drop it.
- **From:** A-moral-adjective-category-errors (with ontological slop and gratuitous universal quantifiers), S-WordPatterns (lazy extremes), S-Rule4.
Check (en): honest shape | honest number | flagged honestly | described honestly | stops being true
Check (de): eine ehrliche Zahl | ehrlich benannt

### I11 · Vague association
Tier P2.
- **Looks like:** two things said to be connected without saying how: associated with, in association with, connected to, in connection with, linked to, tied to. "He was associated with the leadership of the company" hides whether he was CEO, board member, or consultant. DE: im Zusammenhang mit, in Verbindung mit, verbunden mit, steht in Verbindung zu.
- **Guard:** statistics ("X is associated with Y" is the correct verb for correlation; see SCI-1); the source does not say more (keep the vague wording rather than inventing a role).
- **Fix:** name the relationship the source gives.
- **From:** H-14.
Check (en): in association with | in connection with
Check (de): in Verbindung mit | steht in Verbindung zu

### I12 · Copula avoidance
Tier P2.
- **Looks like:** simple verbs replaced with longer ones: serves as, stands as, functions as, operates as, marks, represents [a], refers to; boasts, features, offers, maintains [a] (for "has"). DE: dient als, fungiert als, stellt ... dar, zeichnet sich durch ... aus, verfügt über (for "hat"), bietet (for "hat"), präsentiert sich als.
- **Guard:** the specific verb adds meaning ("the committee serves as the appeals body" when that is its formal function; "stellt eine Verletzung dar" in legal German).
- **Fix:** use is, are, has; ist, sind, hat.
- **From:** A-copula-avoidance, H-18, M-9.
Check (en): serves as | stands as | functions as | operates as | boasts
Check (de): dient als | fungiert als | zeichnet sich durch | präsentiert sich als

### I13 · Ambiguous domain terms
Tier P2 (`extra` in science).
- **Looks like:** a word with a technical sense used loosely where readers could take it technically. Science: "significant" without a test, "robust" without a robustness check, "optimal" without an optimization, "proof" or "proves" for empirical support, "novel" as decoration, "validate" for a single test. Cryptography: "proof" or "proof point" where readers could mistake evidence for a cryptographic proof. DE: "signifikant" without a test, "beweist" for empirical support, "optimal".
- **Guard:** the technical sense is meant and supported; the passage already distinguishes the senses.
- **Fix:** use the plain word ("large", "consistent", "best of those tested", "evidence") or supply the technical basis from the source.
- **From:** A-domain-term-collision (generalized), N (science).

---

## S. Staging instead of stating

The sentence signals importance, stages a moment, or argues with a phantom instead of adding a fact. These are the strongest structural tells and persist across model versions.

### S1 · Not X but Y
Tier P1. At most one deliberate use per piece, and only if it serves the argument.
- **Looks like:** the negative half names something no one claimed, so the positive half sounds larger. Forms: "It's not X, it's Y"; "This isn't about X, it's about Y"; "not just/not only/not merely X, but Y"; the reversed "X rather than Y"; the split form across sentences ("This does not mean X. It means Y." / "The headline isn't the speed. The real story is Y."); the multi-negation countdown ("It's not the price. It's not the features. It's the trust."); negative listing ("Not a X. Not a Y. A Z." / "It wasn't X. It wasn't Y. It was Z."); stop-slop's table: "Not because X. Because Y.", "[X] isn't the problem. [Y] is.", "The answer isn't X. It's Y.", "It feels like X. It's actually Y.", "The question isn't X. It's Y.", "stops being X and starts being Y", "doesn't mean X, but actually Y", "is about X but not Y", "not just X but also Y"; the clipped negative tail ("The options come from the selected item, no guessing"). DE: "nicht nur X, sondern auch Y" used for weight ("nicht nur effizient, sondern auch nachhaltig"), "Es geht nicht um X, sondern um Y", "Das ist kein X. Das ist Y.", "Nicht X. Sondern Y.", "kein X, sondern Y", tailing "..., ganz ohne Rätselraten".
- **Guard:** the negative half corrects a belief the reader actually holds, or both halves carry information; negations listing spec constraints ("no dependencies, no telemetry"); in German, "nicht nur ..., sondern auch" linking two real, non-trivial facts ("nicht nur in Berlin, sondern auch in Wien") is ordinary additive German: flag only when it adds weight, repeats, or the first half is trivial.
- **Fix:** state Y directly. Write a tailing negation as a real clause ("without forcing the user to guess") or cut it.
- **Example (invented):** "Our onboarding isn't just a checklist. It's a culture." → "New hires pair with a colleague for their first two weeks." (only if the source says so; otherwise "Our onboarding has a checklist and a buddy system", or ask what the culture claim means).
- **From:** A-not-x-but-y (split form, countdown, tailing negation), H-1, S-BinaryContrasts, S-NegativeListing, M-17, M-Tier3 (nicht nur ... sondern auch), W (negativer Parallelismus), N (Es geht nicht um ... sondern).
Check (en): re:\bit'?s not (?:just |only |merely )?[^.;]{1,60}[,;] it'?s\b | re:\bthis isn'?t (?:about|just)\b[^.]{0,60}\bit'?s\b | re:\bnot (?:just|only|merely) [^.]{1,60}\bbut\b | re:\bnot because [^.]{1,60}\. because\b | re:\bthe (?:answer|question|problem) isn'?t\b | stops being … starts being
Check (de): ~nicht nur … sondern auch | re:\bes geht nicht um [^.]{1,60}, sondern\b | re:\bdas ist kein [^.]{1,40}\. das ist\b | re:\bnicht [^.,]{1,40}\. sondern\b
Threshold (de): 2 per text

### S2 · Invented contrast-pair mirroring
Tier P1.
- **Looks like:** one half of a contrast is a real term of art and the other is invented to balance it: "false precision rather than genuine accuracy" ("false precision" is a statistical term; "genuine accuracy" is a phantom). DE: "Scheingenauigkeit statt echter Präzision".
- **Guard:** both halves are real descriptions ("a misleadingly exact number rather than a more accurate one").
- **Fix:** use a real opposite, or drop the contrast and state the positive claim.
- **From:** A-invented-contrast-pair-mirroring.

### S3 · Negation chains
Tier P2.
- **Looks like:** two or more "no ..." items in a row for rhythm ("No fluff, no filler, no jargon."), stacked "didn't" clauses ("It didn't ask. It didn't wait."), the negated-then-repeated verb ("Don't call it a pivot. Call it a correction."). Repeated empty concessions ("Not always. Not perfectly.") that stage honesty without saying where the claim fails. DE: "Kein Blabla, keine Floskeln, kein Fachchinesisch.", "Nicht immer. Nicht perfekt."
- **Guard:** mid-sentence factual inventories ("the endpoint takes no arguments, no headers, and no body"); narration with restated subjects ("I did not sleep. I did not eat."); two meaningful concessions ("Not during failover. Not for expired tokens.").
- **Fix:** say what the thing is. Keep one negation when the reader would otherwise assume the opposite. Fold empty concessions into a limitation the source states, or cut them; never invent a failure case.
- **From:** A-negation-chains, A-repeated-empty-concessions, S-RhythmPatterns ("Not always. Not perfectly.").
Check (en): re:(?:^|[.!?]\s)No [a-z'-]+(?: [a-z'-]+)?, no [a-z'-]+(?: [a-z'-]+)?, (?:and |or )?no [a-z'-]+ | not always. not perfectly
Check (de): re:(?:^|[.!?]\s)Kein(?:e|en)? \w+, kein(?:e|en)? \w+, (?:und )?kein(?:e|en)? \w+ | nicht immer. nicht perfekt

### S4 · Staccato fragments and one-line closers
Tier P1.
- **Looks like:** a run of three or more same-shape fragments engineered so each lands like a quotable closer ("It had no preference for symmetry. No aesthetic prior. No nostalgia."); "[Noun]. That's it. That's the [thing]."; "X. And Y. And Z."; "This unlocks something. [Word]."; a one-sentence paragraph that restates the paragraph before it; the same closer after several sections ("That is the real win."); "Read that again."; one word in ALL CAPS or with periods between words ("every. single. day."); every paragraph ending on a punchy one-liner. DE: "Das ist alles. Mehr nicht.", "Punkt.", "Jeden. Einzelnen. Tag.", "Genau das."
- **Guard:** CV bullets and headings (fragments by design); captions; the LinkedIn register (relaxed); one short sentence that carries a new fact; a single deliberate fragment.
- **Fix:** keep a fragment that earns its emphasis; fold the rest into ordinary sentences using only the source's claims. Cut a closer that repeats. Vary paragraph endings. Do not create staccato while fixing other patterns.
- **From:** A-manufactured-punchlines-staccato, H-2, S-DramaticFragmentation, S-RhythmPatterns ("Every paragraph ends punchily", "Staccato fragmentation"), S-Rule6 ("End paragraphs differently").
Check (en): that's the real win | read that again | let that sink in | that's it. that's | ~re:\b(?:[A-Za-z]+\. ){2,}[A-Za-z]+\.(?=\s|$)
Check (de): lies das nochmal | lesen Sie das noch einmal | ~re:\b(?:[A-Za-zÄÖÜäöüß]+\. ){2,}[A-Za-zÄÖÜäöüß]+\.(?=\s|$)
Threshold: 2 per text

### S5 · Reversal tricks
Tier P2, judgment only.
- **Looks like:** (a) repeated setup and reversal punchlines that replace a concrete claim with a twist ("We planned for every failure mode. Except the one that happened." / "The migration went smoothly, which is how we knew something was wrong."), especially in hooks, closers, and final list items; (b) the stranded auxiliary contrast as a recurring rhythm ("The tool died; the data didn't." / "Reading mostly passed. Writing didn't.").
- **Guard:** one supported, voice-appropriate reversal; reversals that carry concrete distinctions ("We rebuilt billing to group charges by project. Your invoice total didn't change."); comedy, fiction, speeches, quotations.
- **Fix:** keep the supported claim, remove the empty twist ("We missed a failure mode."); ask for the missing detail rather than inventing causes. Ration stranded auxiliaries: write the next contrast out in full.
- **From:** A-setup-reversal-punchlines, A-stranded-auxiliary-contrast.

### S6 · Aphorisms and fake depth
Tier P1.
- **Looks like:** an ordinary point dressed as a hidden truth or a quotable law. EN: the real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter, the truth is, the uncomfortable truth is, the real [X] is, make no mistake; formulas: "X is the language of Y", "X is the currency of Z", "the architecture of trust", "X becomes a trap", "X is not a tool but a mirror", "X is a feature, not a bug", "dressed up as". Pull-quote sentences (stop-slop: "if it sounds like a pull-quote, rewrite it"). DE: Im Kern geht es um, Die eigentliche Frage ist, Letztlich geht es darum, Die Wahrheit ist, Am Ende zählt nur, X ist die Währung von Y, X ist die Sprache von Y.
- **Guard:** quotations and established idioms ("time is money"); literal "X is the Y of Z" ("Paris is the capital of France").
- **Fix:** replace the saying with the specific claim it gestures at, if the source supplies it.
- **From:** A-aphorism-formulas, A-persuasive-authority-tropes, H-3, S-Rule8 (cut quotables), S-ThroatClearing (The uncomfortable truth is, The truth is, The real [X] is), S-EmphasisCrutches (Make no mistake), S-FillerPhrases (At its core, The reality is), S-MetaCommentary (X is a feature, not a bug; Dressed up as).
Check (en): the real question is | at its core | what really matters | the deeper issue | the heart of the matter | the truth is | the uncomfortable truth | make no mistake | is the currency of | is the language of | the architecture of | is a feature, not a bug | dressed up as
Check (de): im Kern geht es | die eigentliche Frage ist | letztlich geht es darum | die Wahrheit ist | am Ende zählt nur | ist die Währung | ist die Sprache der

### S7 · Announcing instead of saying
Tier P1.
- **Looks like:** the writer announces the point, the structure, or the next step instead of making it. EN: Let's dive in, Let's explore, Let's take a look, Let's break this down, Let's examine, Let's consider/discuss/unpack/walk through; here's what you need to know, now let's look at, without further ado, heads up, quick note; Here's the thing, Here's what [X], Here's why [X], Here's what I find interesting, Here's what's interesting, Here's what caught my eye, Here's what stood out, Here's what I mean:, Here's the problem though; It turns out; Let me be clear; I'll say it again:; I'm going to be honest; Can we talk about; Think about it:; And that's okay.; meta-commentary: Hint:, You already know this, but, But that's another post, The rest of this essay explains, Let me walk you through, In this section, we'll, As we'll see, I want to explore; "one thing that bit me, so pay attention". DE: Tauchen wir ein, Tauchen Sie ein in, Schauen wir uns an, Werfen wir einen Blick auf, In diesem Beitrag beleuchten wir, Im Folgenden möchte ich, Lassen Sie uns gemeinsam, Hier ist, was Sie wissen müssen, Denken Sie mal darüber nach.
- **Guard:** a genuine invitation ("Let's meet Tuesday"); a one-sentence roadmap in a thesis or long paper; didactic German "Betrachten wir die Funktion f" in teaching text; "Here's the agenda" in an actual agenda email.
- **Fix:** start with the point. Remove the run-up, not just its tone.
- **From:** A-lets-constructions, A-transitions ("Here's what's interesting" family), H-4, S-ThroatClearing, S-MetaCommentary, S-RhetoricalSetups ("Here's what I mean:", "Think about it:", "And that's okay."), S-QuickChecks ("here's what/this/that" throat-clearing; meta-joiners), M-27.
Check (en): ^let's dive in | ^let's explore | ^let's take a look | ^let's break this down | ^let's examine | re:^let'?s (?:consider|discuss|delve|unpack|walk through)\b | here's what you need to know | without further ado | ^here's the thing | ^here's what | ^here's why | here's what I mean | here's the problem though | ^it turns out | let me be clear | I'll say it again | I'm going to be honest | can we talk about | think about it: | and that's okay | the rest of this essay | let me walk you through | in this section, we'll | as we'll see | I want to explore | you already know this, but | but that's another post
Check (de): tauchen wir ein | tauchen Sie ein | schauen wir uns an | werfen wir einen Blick | in diesem Beitrag beleuchten | im Folgenden möchte ich | lassen Sie uns gemeinsam | hier ist, was Sie wissen müssen

### S8 · Teaser hooks and staged candor
Tier P1.
- **Looks like:** fragment hooks that tee up an ordinary reveal: The catch?, The kicker?, But here's the kicker:, The best part?, The result?, Plot twist:, Spoiler:; staged candor as a standalone opener: Honestly?, Look,, Real talk:, Let's be honest, The thing is. DE: Der Haken?, Das Beste daran?, Das Ergebnis?, Der Clou?, Spoiler:, Ehrlich gesagt?, Mal ehrlich:, Klartext:.
- **Guard:** "honestly" or "look" inside a casual sentence is ordinary; the tell is the staged pause before a routine claim.
- **Fix:** delete the hook and state the thing ("The catch? It only works on weekends." → "It only works on weekends.").
- **From:** A-infomercial-hooks (with fake-candid openers), H-4 (staged candor), S-SentenceStarters ("Look,"), S-MetaCommentary (Plot twist:, Spoiler:).
Check (en): the catch? | the kicker? | here's the kicker | the best part? | the result? | plot twist: | spoiler: | ^honestly? | ^look, | real talk | let's be honest | ^the thing is
Check (de): der Haken? | das Beste daran? | das Ergebnis? | der Clou? | spoiler: | ^ehrlich gesagt? | mal ehrlich: | ^Klartext:

### S9 · Performed insight
Tier P1 (one hit may be style; several are a tell; in short social copy one staged discovery that carries the payoff is enough).
- **Looks like:** phrases that announce profundity instead of delivering it: sit with that for a moment, that's not nothing, you already know the answer, the punchline is, worth naming, don't take my word for it, that's the whole point, is the entire business model, that's the part nobody mentions, the only metric that matters, X is dead; long live X, that's why it mattered, sentence-initial "Turns out"; emphasis crutches: Full stop., Period., Let that sink in., Make no mistake; staged discoveries: "the recording turned out to be the least interesting part", "the real story was". DE: Lassen Sie das kurz wirken, Das ist nicht nichts, Punkt., Und genau darum geht es, Das ist der eigentliche Punkt, Die einzige Kennzahl, die zählt, Die eigentliche Geschichte ist.
- **Guard:** quoted speech; comedy where a punchline is literal; "period" in its literal senses.
- **Fix:** state the claim without the announcement. Replace "that's not nothing" with a size only if the source gives one.
- **From:** A-performed-insight-phrases (with staged discoveries), S-EmphasisCrutches (Full stop., Period., Let that sink in.), H-2 (Let that sink in).
Check (en): sit with that | that's not nothing | you already know the answer | the punchline is | don't take my word for it | that's the whole point | the entire business model | the part nobody mentions | the only metric that matters | long live | that's why it mattered | ^turns out | full stop. | let that sink in | turned out to be the least interesting | the real story was
Check (de): das ist nicht nichts | und genau darum geht es | die einzige Kennzahl, die zählt | die eigentliche Geschichte

### S10 · Invented opponents
Tier P1.
- **Looks like:** answering an objection no one raised, rejecting an option no one proposed, or propping a claim on an invented, lagging crowd. EN: This isn't (mainly) about, I'm not saying, To be clear, Don't get me wrong, This is not to say, Some might say ... but, A tempting approach would be, One might be tempted to, An obvious approach would be, You might think ... but, It would be easy to just; "while everyone else was still debating", "while the industry wrote think-pieces", "while others played catch-up"; teaser crowds: "the call most leaders still won't make", "the move most founders are too scared to make"; forced contrarianism ("Everyone says X, but they're wrong"). DE: Ich sage nicht, dass; Um es klar zu sagen; Man könnte meinen ..., doch; Versteh mich nicht falsch; während andere noch diskutierten; was die meisten sich nicht trauen.
- **Guard:** an objection the text attributes or answers in full; an option a reader would actually weigh; literal simultaneity ("she read while everyone else watched the film"); a named competitor and its action from the source; positioning against cited prior work in science.
- **Fix:** remove the defense; state the claim if it holds one. State the supported fact and cut the crowd clause. Never replace one invented foil with a more specific invented one. Several unrelated rejections in a row are a stronger sign than one.
- **From:** H-5 (with fake alternatives), A-dramatized-crowd-contrast (with teaser form), A-never-inject (forced contrarianism).
Check (en): I'm not saying | don't get me wrong | this is not to say | a tempting approach would be | one might be tempted to | it would be easy to just | while everyone else | re:\bwhile (?:the industry|the market|the competition|others) (?:was|were|is|are) still\b | most leaders still won't | most founders are too
Check (de): ich sage nicht, dass | versteh mich nicht falsch | verstehen Sie mich nicht falsch | man könnte meinen | während andere noch | was die meisten sich nicht trauen

### S11 · False concession
Tier P1.
- **Looks like:** a balanced-sounding frame where both halves are vague: "While X is impressive, Y remains a challenge", "Although X has made strides, Y is still an open question", "Despite its challenges, X". DE: "Obwohl X Fortschritte gemacht hat, bleibt Y eine Herausforderung", "So beeindruckend X auch ist, ...", "Trotz aller Fortschritte".
- **Guard:** temporal "while" ("While the build ran, I wrote the notes"); a concession with specific content on both sides.
- **Fix:** make the concession specific with the source's details and stance, or cut the frame and keep both claims with their uncertainty. Do not choose a side for the writer.
- **From:** A-false-concession, M-23.
Check (en): re:\bwhile \w+ is impressive\b | re:\balthough \w+ has made strides\b | remains a challenge | is still an open question
Check (de): so beeindruckend | bleibt eine Herausforderung | trotz aller Fortschritte

### S12 · Rhetorical questions
Tier P1.
- **Looks like:** questions that stall before the point ("But what does this mean for developers?", "So why should you care?", "What's next?", "What if [reframe]?"); questions answered immediately by the writer; stacked questions ("Do I know how it works? Where it breaks? Which corners it cut?"); the self-Q&A volley ("Is it fast? Yes. Is it cheap? Also yes."); engagement-bait closers ("Agree?", "Thoughts?"). DE: "Was bedeutet das konkret?", "Warum ist das wichtig?", "Was wäre, wenn ...?", "Und jetzt?", "Sind Sie bereit für den nächsten Schritt?".
- **Guard:** FAQs, interviews, dialogue, teaching texts; one earned hook in a LinkedIn post (relaxed); a research question in a paper (relaxed); a real question to a real audience.
- **Fix:** state the answer if the source gives it; cut an empty transition; leave a genuinely open question open. Keep at most one in a stack.
- **From:** A-rhetorical-question-openers, A-stacked-rhetorical-questions, A-fake-casual (self-QA volley), S-RhetoricalSetups ("What if"), S-RhythmPatterns ("Questions answered immediately"), M-24.
Check (en): but what does this mean for | so why should you care | what's next? | ^what if | ^agree? | ^thoughts?
Check (de): was bedeutet das konkret | warum ist das wichtig? | ^was wäre, wenn | sind Sie bereit für den nächsten Schritt | seid ihr bereit

### S13 · Scene-setting openers
Tier P1 (`extra` in letters).
- **Looks like:** opening with broad context or a hypothetical before the point. EN: In today's [fast-paced/digital/competitive] world, In the rapidly evolving world/landscape of, In an era where, In a world where, In the digital age, As we continue to evolve, has emerged as a leading/key, has become increasingly important, Imagine a world where, Picture a future in which, Envision a world where, "In today's competitive job market". DE: In der heutigen schnelllebigen Zeit, In der heutigen Zeit, Im Zeitalter der Digitalisierung, In einer sich rasant wandelnden Welt, In der modernen Arbeitswelt, In Zeiten von, Stellen Sie sich eine Welt vor, in der, hat sich als ... etabliert, gewinnt zunehmend an Bedeutung.
- **Guard:** fiction; a thought experiment with a stated payoff; instructional "imagine you have a sorted array"; context that is itself the news.
- **Fix:** cut the scene-setting and keep the claim at the same confidence ("Imagine a world where every deploy is instant" → "Every deploy would be instant"). Moving context requires structural scope.
- **From:** A-formulaic-openings, A-speculative-scenario-openers, A-transitions ("In today's", "In an era where"), S-FillerPhrases ("In today's [X]", "In a world where"), M-Tier3 (Zeitalter, schnell wandelnde Welt, heutige Zeit), N.
Check (en): re:\bin today'?s\b | in an era where | in a world where | re:\bin the (?:rapidly |ever-?\s*)?(?:evolving|changing|expanding|growing|shifting) (?:world|landscape|realm|space|field|domain|era) of\b | in the digital age | has emerged as a | has become increasingly | re:\b(?:imagine|picture|envision) a (?:world|future|reality) (?:where|in which)\b
Check (de): in der heutigen schnelllebigen Zeit | in der heutigen Zeit | im Zeitalter der | in einer sich rasant | in einer sich schnell wandelnden | in der modernen Arbeitswelt | stellen Sie sich eine Welt vor | stell dir eine Welt vor | gewinnt … zunehmend an Bedeutung | gewinnen … zunehmend an Bedeutung

### S14 · Stock reactions and lingering attention
Tier P1 (a style heuristic; upstream gives it zero authorship weight).
- **Looks like:** (a) stock reaction frames: What surprised me most, I was fascinated to discover, What struck me was, I was excited to learn, The most interesting part, "Interesting part of the project:"; "hit differently"; "I'm thrilled to announce/share/apply", "I am excited to submit my application", "I have always been passionate about"; (b) lingering-attention claims: "the line I keep coming back to", "I can't stop thinking about this", "still thinking about this one", "rattling around in my head", "I've been chewing on this since Tuesday". DE: Was mich am meisten überrascht hat, Ich war fasziniert zu entdecken, Ich freue mich riesig, Ich bin stolz, verkünden zu dürfen, Mit großer Begeisterung, Ihre Stellenausschreibung hat mich sofort angesprochen, Das geht mir nicht mehr aus dem Kopf.
- **Guard:** a named, specific reaction the writer actually has ("I was surprised" is not a tell by itself); a reason attached ("I keep coming back to this framing because it predicts who quits"). Never replace a named emotion with theatrical body language.
- **Fix:** cut the empty frame and lead with the fact; if the source gives the expectation and reason, keep the reaction in specific form.
- **From:** A-stock-reaction-framing, A-lingering-attention, M-32, N (application openers).
Check (en): what surprised me most | I was fascinated to | what struck me was | I was excited to learn | the most interesting part | I keep coming back to | I can't stop thinking about | still thinking about this one | rattling around in my | I'm thrilled to | I am thrilled to | hits different | hit differently
Check (de): was mich am meisten überrascht hat | ich war fasziniert | ich freue mich riesig | ich bin stolz, verkünden zu dürfen | mit großer Begeisterung | hat mich sofort angesprochen | geht mir nicht mehr aus dem Kopf

### S15 · Endorsement closers
Tier P1.
- **Looks like:** a generic thumbs-up in place of a reason: "This one is worth your time:", "This one's a must-read", "I highly recommend giving this a read", "Do yourself a favor and read this", "You won't want to miss this one", "Save this for later", "Bookmark this", "Don't sleep on this one", "Trust me, you'll want to read this", "Thank me later"; the bare "worth reading / worth a look / worth exploring / worth checking out / worth paying attention to". DE: "Unbedingt lesenswert", "Absolute Leseempfehlung", "Lohnt sich!", "Speichern für später", "Klare Empfehlung".
- **Guard:** the source supplies the reason or audience; one such line in a DM (`casual` relaxed).
- **Fix:** use the source's reason and drop the call to action; if there is no reason, let the link stand alone. Do not invent an author, superlative, or audience.
- **From:** A-social-endorsement-closers, A-vague-endorsement ("worth [verb]ing").
Check (en): this one is worth your time | this one's worth | this one is a must | a must-read | highly recommend giving this | do yourself a favor and | you won't want to miss this | save this for later | bookmark this | don't sleep on this | thank me later | worth checking out | worth a look
Check (de): unbedingt lesenswert | absolute Leseempfehlung | lohnt sich! | speichern für später | klare Empfehlung

### S16 · Launch-copy introductions
Tier P1.
- **Looks like:** introducing a product like a game-show contestant: "Enter Flowdesk.", "Meet Flowdesk, your new favorite treasury dashboard", "Say hello to Flowdesk", "Think Notion meets Figma". DE: "Darf ich vorstellen: X", "Das ist X – Ihr neuer ...", "Hallo, X!", "Willkommen bei X, dem neuen ...".
- **Guard:** introducing a person ("Meet Sarah, your new account manager"); UI instructions ("Enter Password."); stage directions ("Enter Hamlet.").
- **Fix:** state what the source establishes ("Flowdesk is a treasury dashboard").
- **From:** A-launch-copy-dramatic-introductions.
Check (en): re:(?:^|[.!?]\s)Meet [A-Z][\w'-]{1,29}\s*,\s*(?:your new (?:favorite|go-to)\b|the new (?:home of|way to|standard (?:in|for))\b) | re:(?:^|[.!?]\s)[Tt]hink [A-Z][\w'-]{1,29} meets [A-Z][\w'-]{1,29}\b
Check (de): darf ich vorstellen: | re:\bdas ist [A-Z]\w+ – (?:Ihr|dein) neue[rs]?\b

### S17 · Fake-casual register
Tier P1.
- **Looks like:** the costume of an imposed casual voice: one-word verdict closers ("wild.", "insane.", "unhinged."); stage directions (*checks notes*, *chef's kiss*, *mic drop*, *takes a deep breath*, *sips coffee*, *nervous laughter*); wink asides ("(yes, really)", "(no, seriously)"); label openers ("hot take", "fun fact", "pro tip", "PSA", "unpopular opinion"); "because of course it does". Roleplay action markers in general (*nods*, *sighs*). DE: "(ja, wirklich)", "(kein Witz)", "Fun Fact:", "Pro-Tipp:", "Unpopuläre Meinung:".
- **Guard:** a writer whose established voice (sample) uses these props.
- **Fix:** delete the prop and keep the observation; do not invent a reaction.
- **From:** A-fake-casual-register, A-det-normflag (roleplay markers).
Check (en): *checks notes* | *chef's kiss* | *mic drop* | *takes a deep breath* | *nervous laughter* | re:\*sips (?:coffee|tea)\* | re:\(\s?(?:yes|no)\s?,\s?(?:really|seriously)\s?\) | ^hot take | ^fun fact | ^pro tip | ^unpopular opinion | because of course it does
Check (de): (ja, wirklich) | (kein Witz) | ^Fun Fact: | ^Pro-Tipp | ^Unpopuläre Meinung

### S18 · Self-labeling significance
Tier P2.
- **Looks like:** pointing back at one item and labeling it: "That last move is the contrarian one", "This is the interesting part", "That third bullet is the real story", "Here's where it gets clever". DE: "Der letzte Punkt ist der eigentlich spannende", "Hier wird es interessant".
- **Guard:** none beyond general guards.
- **Fix:** cut the label; let the item carry its weight.
- **From:** A-self-labeling-significance.
Check (en): is the contrarian one | this is the interesting part | is the real story | here's where it gets
Check (de): hier wird es interessant | der eigentlich spannende

### S19 · False agency and transformation crutch
Tier P2, judgment.
- **Looks like:** (a) a consequential choice attributed to an abstraction, hiding who decided: "The decision emerged after the offsite", "the complaint becomes a fix", "a bet lives or dies in days", "the conversation moves toward", "the market rewards"; (b) repeated unexplained relabeling: "the concern turns into panic", "a feature turns into a strategy", "the risk becomes real". DE: "Die Entscheidung fiel", "aus der Beschwerde wird eine Lösung", "Der Markt belohnt".
- **Guard:** conventional personification ("the data shows adoption is early"; "die Daten zeigen"); literal system behavior; collective shorthand; literal transformations ("water turns into ice"); changes explained in the passage.
- **Fix:** name the actor only if the source identifies them; otherwise ask. Ask what changed; never invent a mechanism or actor.
- **From:** A-false-agency, A-transformation-crutch, S-FalseAgency, S-Rule3 ("No inanimate objects performing human actions"), S-QuickChecks.

### S20 · Narrator from a distance
Tier P2, weak alone (stop-slop rule; `strict` raises it).
- **Looks like:** floating above the scene: "Nobody designed this.", "This happens because ...", "This is why ...", "People tend to ...". DE: "Niemand hat das so geplant.", "Das passiert, weil ...", "Menschen neigen dazu ...".
- **Guard:** explanatory and academic prose, documentation, CVs, science (off). A deliberate essayistic voice.
- **Fix:** put the reader in the room where the genre allows ("You don't sit down one day and decide to ..."). "You" beats "people"; specifics beat abstractions.
- **From:** S-NarratorFromADistance, S-Rule5.
Check (en): ^nobody designed this | ^people tend to
Check (de): ^Menschen neigen dazu | ^niemand hat das so geplant

### S21 · Slot-fill templates and false ranges
Tier P2.
- **Looks like:** constructions with a blank that any noun fits: "a [adjective] step towards [adjective] AI infrastructure", "a [adjective] step forward for [noun]", "Whether you're [X] or [Y]", "I recently had the pleasure of [verb]-ing", "By the time X, I was Y", "X that isn't Y"; false ranges that pair unrelated extremes ("from the Big Bang to dark matter", "from ancient civilizations to modern startups"). DE: "ein [adj] Schritt in Richtung [adj] ...", "Ob Sie X oder Y sind", "egal ob X oder Y", "Ich hatte kürzlich das Vergnügen", "von der Grundlagenforschung bis zur Marktreife".
- **Guard:** a real range with endpoints the source names; a real two-audience text.
- **Fix:** say what changed, only from the source; pick the audience you address; list the actual topics or pick the one that matters.
- **From:** A-template-phrases, A-false-ranges, S-FormulaicConstructions, M-11, M-13. (humanizer 3.0 dropped false ranges as a human habit; kept here at P2 because avoid-ai-writing keeps it.)
Check (en): re:\ba \w+ step (?:towards?|forward for)\b | re:\bwhether you'?re (?:a |an )?\w+ or\b | I recently had the pleasure of
Check (de): re:\bob Sie (?:ein |eine )?\w+ oder\b | ich hatte kürzlich das Vergnügen | von der Grundlagenforschung bis

### S22 · Slogans in place of properties
Tier P2.
- **Looks like:** stock simplicity claims: batteries included, it just works, zero config, sane defaults, small enough to fit in your head. DE: "funktioniert einfach", "ohne Konfiguration", "out of the box" (as a slogan).
- **Guard:** quoting a product's own tagline; discussing the phrase.
- **Fix:** name the concrete behavior the source supplies ("installs with no config file").
- **From:** A-dev-blog-boilerplate.
Check (en): it just works | zero config | zero-config | sane defaults | fit in your head | fits in your head
Check (de): funktioniert einfach

### S23 · Vague declaratives
Tier P1.
- **Looks like:** sentences that announce importance without naming the thing: "The reasons are structural", "The implications are significant", "This is the deepest problem", "The stakes are high", "The consequences are real"; consequence-free explanations: "This matters because it is important", "Here's why that matters" followed by a restatement. DE: "Die Gründe sind vielfältig", "Die Auswirkungen sind erheblich", "Es steht viel auf dem Spiel", "Das ist von großer Bedeutung".
- **Guard:** the specific thing follows at once ("This matters because retries can charge the customer twice").
- **Fix:** name the specific implication from the source, or cut.
- **From:** S-VagueDeclaratives, S-Rule4, A-consequence-free-explanation, S-EmphasisCrutches ("This matters because", "Here's why that matters").
Check (en): the reasons are structural | the implications are significant | the stakes are high | the consequences are real | this is the deepest problem | here's why that matters
Check (de): die Gründe sind vielfältig | die Auswirkungen sind erheblich | es steht viel auf dem Spiel

---

## R. Rhythm and structure

A person may do any one of these on purpose, so most are weak alone. Regularity alone never authorizes a rewrite or establishes authorship.

### R1 · Rule of three
Tier P2, weak alone.
- **Looks like:** ideas arriving in threes to sound complete, whether or not the meaning has three parts: a triad in one sentence ("innovation, inspiration, and insights"), three parallel examples, three short facts followed by a lesson, a colon opening onto exactly three items ("separate ports, processes, and local state"), always exactly three tips or arguments, the "benefits, opportunities, and challenges" triad, the three-adjective summary ("results-driven, detail-oriented, and passionate"). DE: "Teamfähigkeit, Belastbarkeit und Kommunikationsstärke", "Chancen, Potenziale und Herausforderungen", "menschlich, nachhaltig und zukunftsorientiert"; German Wikipedia names the tricolon.
- **Guard:** three real items; lists that are simply true (common in technical and scientific writing); deliberate rhetoric.
- **Fix:** check that each item adds a distinct idea; merge, develop the strongest, or vary the structure. Never add or remove an item to meet a rhythm quota. stop-slop's "two items beat three" applies under `strict`.
- **From:** A-rule-of-three, A-colon-into-a-triple, H-6, S-RhythmPatterns (three-item lists), S-Rule6 ("Two items beat three"), M-36a, W (Trikolon).
Density (model): 3 triads per 300 words.

### R2 · Hedging: padding and stacks
- **R2a Hedge padding** (P2, weak alone): empty softeners and single qualifiers that add no real uncertainty ("it could be argued", "to some extent", "in some cases it may"); stop-slop's "no softeners, no hedges"; German "kann"-density ("Dies kann dazu beitragen, ... zu ermöglichen", "kann hilfreich sein") and "gewissermaßen", "in gewisser Weise", "ein Stück weit". `off` in science (a single calibrated hedge is required there, `genre-science.md`, SCI-2).
- **R2b Stacked hedges** (P1): two or more qualifiers on one claim, each cancelling the next: could potentially, may eventually, might ultimately, might arguably, could possibly, potentially could, it's also possible that ... may, to be fair ... could. A hedge verb already carries the uncertainty, so a modal on top of it is a stack: may suggest, might indicate, could point to, may be consistent with. DE: könnte möglicherweise, könnte eventuell, eventuell vielleicht, unter Umständen ... könnte, ließe sich möglicherweise, möglicherweise vielleicht, würde gegebenenfalls; modal plus hedge verb: könnte darauf hindeuten, könnte nahelegen, legt nahe, dass ... könnte, deutet darauf hin, dass ... möglicherweise.
- **Guard:** qualifiers the source supports and the meaning needs; scope statements; legal and safety notices; real corrections; ordinary hedges ("perhaps", "tends to", "vermutlich") are human habits; hedges on different claims in one sentence are not a stack; "may not", "might never" (negators are not hedges).
- **Fix:** keep the one qualifier that carries the source's uncertainty, placed on the uncertain part. If the intended confidence is unclear and matters, leave it and ask rather than choosing a stronger claim (F2).
- **From:** A-hedging, A-hedge-stacked-predictions, H-9, S-Rule7 ("Skip softening"), S-Adverbs ("no hedges"), M-15, M-15a (corrected: Modalwörter, not Modalpartikeln).
Check (en): re:\b(?:could|may|might)\s+(?:(?!not\b|never\b|hardly\b|scarcely\b|barely\b)\w+\s+)?(?:potentially|eventually|ultimately|possibly|conceivably)\b | re:\b(?:potentially|eventually|ultimately)\s+(?:could|may|might)\b | might arguably | it could be argued | re:\b(?:may|might|could)\s+(?:suggest|indicate|point to|imply|be consistent with)\b
Check (de): könnte möglicherweise | könnte eventuell | eventuell vielleicht | möglicherweise vielleicht | ließe sich möglicherweise | würde gegebenenfalls | re:\bunter Umständen\b[^.]{0,40}\bkönnte\b | re:\bkönnten?\s+(?:darauf\s+hindeuten|nahelegen|darauf\s+hinweisen)\b | re:\b(?:legt|legen)\s+nahe,\s+dass\b[^.]{0,80}\bkönnten?\b | deutet darauf hin, dass … möglicherweise
Density (model): German "kann"/"können" hedges count at 4 per 100 words (the script counts this).

### R3 · Parenthetical hedging
Tier P2.
- **Looks like:** parenthetical asides that sound nuanced without committing: "(and, increasingly, Z)", "(or, more precisely, Y)", "(and perhaps more importantly, W)", "(though to be fair, ...)", "(at least in theory)". DE: "(und zunehmend auch Z)", "(oder genauer gesagt Y)", "(und vielleicht noch wichtiger: W)".
- **Guard:** parentheses that give examples, units, or references ("Tools (etwa X und Y)" is a normal German parenthetical listing, not a hedge).
- **Fix:** give a real aside its own sentence; cut the rest.
- **From:** A-parenthetical-hedging, M-14 (corrected).
Check (en): re:\(\s*(?:and,?\s+)?(?:increasingly|notably|importantly|crucially|interestingly|perhaps)[,]?\s+[^)]{3,60}\) | re:\(\s*or\s+more\s+(?:precisely|accurately|specifically)[,]?\s+[^)]{3,60}\) | re:\(\s*though\s+to\s+be\s+fair | re:\(\s*at\s+least\s+(?:in\s+)?(?:theory|principle|part)
Check (de): re:\(\s*und zunehmend | re:\(\s*oder genauer gesagt | re:\(\s*und vielleicht noch wichtiger

### R4 · Transition connectors
Tier P2, weak alone.
- **Looks like:** connectors that restate the obvious relation at the start of sentences, in density. EN: Moreover, Furthermore, Additionally, In addition, That said, That being said, Ultimately, paragraphs starting with "So". DE: Darüber hinaus, Des Weiteren, Zudem, Ferner, Nichtsdestotrotz, Letztendlich, Zum einen ... zum anderen, repeated "sowohl ... als auch".
- **Guard:** ordinary German connectors (Dabei, Gleichzeitig, Folglich, Außerdem, Allerdings) are never findings on their own; academic prose uses connectors (relaxed there); a "however" where the relation is a real contrast.
- **Fix:** restructure so the connection is obvious, or use "and", "also", "but"; "und", "auch", "aber". Do not overuse any single replacement.
- **From:** A-transitions, S-SentenceStarters ("So" paragraph starters), M-12 (corrected), M-25, W (Konjunktionen).
Check (en): ~^moreover | ~^furthermore | ~^additionally | ~^in addition, | ~^that said | ~^that being said | ~^ultimately,
Check (de): ~^darüber hinaus | ~^des Weiteren | ~^zudem | ~^ferner | ~^nichtsdestotrotz | ~^letztendlich | ~zum einen … zum anderen
Threshold: 2 per paragraph

### R5 · Filler, signposts, and importance markers
Tier P1 for "It is important to note"-type phrases; weak alone for the single words.
- **Looks like:** padding that tells the reader how to feel about a fact or that announces a summary. EN: It is important to note that, It's worth noting that, It's important to remember, Notably, Interestingly, Surprisingly, Importantly, Significantly (non-statistical), Certainly, Undoubtedly, Without a doubt, In terms of, When it comes to, At the end of the day, The reality is that, In conclusion, In summary, To summarize, It should be noted. DE: Es ist wichtig zu betonen, dass; Es ist wichtig zu beachten, dass; Es ist anzumerken, dass; Es sei darauf hingewiesen, dass; Bemerkenswert ist, dass; Interessanterweise; Zusammenfassend lässt sich sagen; Abschließend lässt sich festhalten; Es lässt sich festhalten; Insgesamt lässt sich sagen; Grundsätzlich (as a filler opener); Prinzipiell; Im Wesentlichen (opener); Es zeigt sich, dass / Es wird deutlich, dass (impersonal distancing openers); wenn es um ... geht.
- **Guard:** "In summary" opening a conclusion paragraph in science; German essay and thesis conclusions ("Zusammenfassend", "Abschließend", heading "Fazit"); "Es ist zu beachten, dass" in manuals; "Grundsätzlich" in legal text (as a rule, exceptions exist); one "notably" in a long piece (density: one per 2,000 words is fine, three in 500 is a finding).
- **Fix:** state the fact; let it carry its own weight.
- **From:** A-filler-phrases, A-confidence-calibration-phrases, A-transitions (In conclusion, When it comes to, At the end of the day, It's worth noting), S-FillerPhrases, M-16, M-30, M-31 (all corrected; see `lang-de.md`, DE-7), W (redaktionelle Kommentare, Zusammenfassungen), N (impersonal openers).
Check (en): it is important to note | it's important to note | it's worth noting | it is worth noting | it should be noted | the reality is that | when it comes to | at the end of the day | in terms of | ^in conclusion | ^to summarize | ~without a doubt | ~^interestingly | ~^notably | ~^importantly | ~^undoubtedly
Check (de): es ist wichtig zu betonen | es ist wichtig zu beachten | es ist anzumerken | es sei darauf hingewiesen | bemerkenswert ist, dass | ~^interessanterweise | zusammenfassend lässt sich sagen | abschließend lässt sich festhalten | es lässt sich festhalten | insgesamt lässt sich sagen | ^es zeigt sich, dass | ^es wird deutlich, dass | wenn es um
Threshold: 3 per 500 words

### R6 · Dashes as the universal connector
Tier P2, weak alone (one dash is weak; a text full of them is not).
- **Looks like:** em dashes (—) and double hyphens ( -- ) used to splice clauses instead of choosing how they relate; spaced en dashes used the same way in English. Target: zero in rewrites; ceiling one per 1,000 words; headings included. In German, the em dash is foreign typography and counts on sight; the spaced en dash ( – ) is the correct Gedankenstrich and counts only in density.
- **Guard:** ranges (2019–2022, pp. 10–12, 03/2021 – 06/2023) are en dashes by rule; the list separator after a bold lead term or a link ("- **Term** — description"); version headings in changelogs ("## 1.2.0 — 2026-09-01"); code, commands, paths, URLs; a voice sample that uses dashes (match its rate); a house style that uses them deliberately (the guide wins the mechanic, the habit is still noted). Dash rate is a writing-quality note, not an authorship signal: usage has varied by model generation.
- **Fix:** replace with a period, comma, colon, or parentheses, or rewrite the sentence. Never add dashes in a rewrite ("em-dash theatrics").
- **From:** A-em-dashes (with list-item carve-out), H-8, S-Rule6 ("No em dashes"), S-RhythmPatterns, S-QuickChecks, M-18 (corrected), W (corrected: the German en dash is correct).
Check (en): ~— | ~re:(?<=\s)--(?=\s)
Check (de): — | re:(?<=\s)--(?=\s) | ~~re:(?<=\s)–(?=\s)
Threshold (en): 1 per 1000 words
Threshold (de): 3 per 300 words

### R7 · Repeated openings and cloned skeletons
Tier P2, weak alone (`extra` for CV bullets).
- **Looks like:** three or more consecutive sentences opening with the same word ("Maybe nobody needed it. Maybe it solved the wrong problem. Maybe the timing was off."); several sentences in a row starting with the same subject ("She noted the door. She noted the lock. She filed both away."); consecutive sentences on the same skeleton ("A cart is an object in the system. A chat room is an object in the system."); CV bullets cloned from one template ("Spearheaded X, leveraging Y, resulting in Z%"); letters where every sentence opens with "I" or "Ich".
- **Guard:** deliberate anaphora doing persuasive work ("She came. She saw. She conquered."); ordinary pronoun narration (upstream treats pronoun runs as ordinary; flag them only when three or more short sentences could merge); consistent CV formatting (dates, tense) is not a cloned skeleton.
- **Fix:** keep the first; merge, change the subject, or begin with the action. Do not ban the word. For CVs, vary the bullet shape (`genre-cv.md`, CV-1, CV-3).
- **From:** A-same-opener-sentence-runs, H-7, N (CV skeletons, letters).

### R8 · Uniform rhythm
Tier P2, weak alone.
- **R8a Sentence length:** a run of similarly shaped sentences (script: five or more sentences with a coefficient of variation under 0.25 and an average above 10 words; stop-slop: three consecutive sentences of matching length).
- **R8b Paragraph length:** every paragraph the same size, boundaries not following the argument (script: four or more paragraphs, all within one sentence of the average, average at least 3).
- **R8c Cross-paragraph sameness:** the same internal rhythm or punctuation density in every paragraph (engine-only checks: punctuation distribution, function-word trigram entropy, cross-paragraph burstiness).
- **Read-aloud test:** if a text-to-speech engine could read it without sounding odd, it is probably too uniform.
- **Guard:** regular structure the genre calls for (bullets, reference docs, forms); second-language writing; never impose word-count bands, add questions, or chop sentences into fragments to create variation.
- **Fix:** vary by clarifying the source: combine a pair, split a long one at a real boundary, move a boundary to follow the argument.
- **From:** A-rhythm-and-uniformity (sentence, paragraph, read-aloud), A-uniform-paragraph-length, A-det-punct-distribution, A-det-fnword-entropy, A-det-cross-para, S-Rule6 ("Mix sentence lengths"), S-QuickChecks ("Three consecutive sentences match length?"), M-19, M-37.
