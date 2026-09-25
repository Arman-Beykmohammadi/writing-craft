# Genre: scientific writing

Load this file for papers, abstracts, theses and dissertations, methods and results sections, related work, discussion and limitations, figure and table captions, grant proposals, peer reviews, and response-to-reviewer letters, in English or German. It does not repeat any pattern from `patterns.md`. It holds this genre's settings and rules. Rule IDs start with `SCI-`.

## Settings

Pick the column for the section being checked; split a whole paper by section first. `proposal` covers grant proposals and thesis exposés. `review` is a peer review the user writes. `response` is a response-to-reviewers letter. An entry not listed is `on`. F1 to F5 are always on.

| ID | abstract | intro | related | methods | results | discussion | caption | proposal | review | response | Note |
|----|----|----|----|----|----|----|----|----|----|----|----|
| R10 | relaxed | relaxed | relaxed | off | relaxed | relaxed | off | relaxed | relaxed | relaxed | Passive is the convention in methods and captions in many fields. "We" is also correct. Follow the field and the user's draft. |
| R11 | off | off | off | off | off | off | off | off | off | off | stop-slop's blanket adverb ban does not fit science: "approximately", "significantly" (statistical), "independently", "only" carry meaning. Emphasis adverbs are still caught by I8. |
| R2a | off | off | off | off | off | off | off | off | off | off | A single calibrated hedge is required, not a tell (SCI-2). |
| R2b | on | on | on | on | on | on | on | on | on | on | Stacked hedges stay on everywhere. |
| S7 | on | relaxed | on | on | on | on | on | relaxed | on | on | A one-sentence roadmap at the end of an introduction or in a thesis chapter is convention. |
| R4 | relaxed | relaxed | relaxed | relaxed | relaxed | relaxed | off | relaxed | relaxed | relaxed | Academic prose uses connectors; only density counts. |
| R5 | on | on | on | on | on | relaxed | on | on | on | on | "In summary" opening a conclusion paragraph is conventional; a stack of importance markers is not. |
| S4 | on | on | on | on | on | on | off | on | on | on | Captions open with a fragment title by convention. |
| M1 | on | on | on | on | on | on | on | relaxed | relaxed | relaxed | Bold aim labels in proposals and bold reviewer-comment labels in responses are convention. |
| M3a | on | on | on | relaxed | on | on | off | relaxed | off | off | Numbered points are expected in reviews and responses; step lists in methods can be right. |
| M3b | on | on | on | on | on | on | on | relaxed | off | off | |
| C2 | on | on | on | on | on | on | on | on | on | relaxed | One short thanks per reviewer is conventional; a thanks formula on every point is not (SCI-12). |
| C3 | on | on | on | on | on | on | on | on | on | off | Quoting the reviewer's comment before answering is the convention. |
| I1 | extra | extra | on | on | on | on | on | extra | on | on | |
| I7 | extra | extra | on | on | on | on | on | extra | on | on | "Novel", "first", "unprecedented" need support (SCI-1). |
| I13 | extra | extra | extra | extra | extra | extra | extra | extra | extra | extra | "Significant", "robust", "optimal", "proof", "novel" have technical senses here. |
| R1 | relaxed | relaxed | relaxed | relaxed | relaxed | relaxed | off | relaxed | relaxed | relaxed | Three items are often simply true in science. |
| R8 | relaxed | relaxed | relaxed | relaxed | relaxed | relaxed | off | relaxed | relaxed | relaxed | |
| R14 | extra | on | on | on | on | on | on | on | on | on | Abstracts have no room for restatement. |
| R15 | off | off | off | off | off | off | off | off | off | off | Not a reply register. |
| S10 | on | on | relaxed | on | on | relaxed | on | on | on | on | Positioning against prior work is legitimate when the prior work is cited. |
| S12 | on | relaxed | on | on | on | on | on | relaxed | on | on | A research question may be posed as a question. |
| S20 | off | off | off | off | off | off | off | off | off | off | |
| R12 | off | off | off | off | off | off | off | off | off | off | |
| G3 | relaxed | relaxed | relaxed | relaxed | relaxed | relaxed | off | relaxed | relaxed | relaxed | German academic prose tolerates longer sentences; very wide verb brackets still count. |

## SCI-1 Claim strength matched to evidence

F2 forbids changing a claim's strength. When the user asks for help choosing, or when a draft's claim does not match its evidence, use this table. The row is decided by the design and the data, not by how exciting the result is.

| Evidence | English verbs and phrases | German verbs and phrases |
|---|---|---|
| Formal proof, derivation | proves, shows, it follows that | beweist, zeigt, daraus folgt |
| Controlled experiment or randomized trial, adequately powered, replicated | shows, demonstrates, establishes, causes (for the tested intervention) | zeigt, belegt, weist nach, bewirkt |
| Single controlled study, or strong effect with limits | indicates, provides evidence that, supports | deutet darauf hin, spricht dafür, stützt die Annahme |
| Observational or correlational data | is associated with, correlates with, predicts (statistical sense), co-occurs with | geht einher mit, korreliert mit, hängt zusammen mit, sagt ... vorher (statistisch) |
| Small sample, pilot, qualitative, exploratory | suggests, is consistent with, points to, we observed | legt nahe, ist vereinbar mit, weist auf ... hin, wir beobachteten |
| Hypothesis, interpretation, speculation | may, might, could, we hypothesize, one possible explanation is, we speculate | könnte, möglicherweise, vermutlich, wir vermuten, eine mögliche Erklärung ist |
| Null result | did not detect, found no evidence of, was not significantly different (with the test) | konnte nicht nachgewiesen werden, kein signifikanter Unterschied (mit Test) |

Rules:
- Causal words (causes, leads to, drives, improves, bewirkt, führt zu, verbessert) need a causal design. Observational data gets association verbs.
- "Significant" and "signifikant" mean statistical significance. Use them only with a test and a threshold. For importance, write "large", "substantial", "wichtig", "deutlich" (with the number).
- "Novel", "first", "for the first time", "erstmals" only when the source makes the claim and the user confirms it. Otherwise flag (I7).
- "No effect" from a null result is an upgrade of absence of evidence into evidence of absence. Write "did not detect".
- Scope stays attached: population, species, setting, dataset, time period. "In mice" does not drop out of the abstract.
- Generalization claims ("in general", "universally", "in allen Fällen") need matching evidence.
- A reported statistic is copied exactly: estimate, interval, test, degrees of freedom, p-value, n, units. No rounding, no conversion.

Upgrade words (en): shows | demonstrates | proves | establishes | confirms | causes | leads to | drives | significant | novel | first | for the first time | unprecedented | always | universally
Upgrade words (de): zeigt | belegt | beweist | bestätigt | weist nach | bewirkt | führt zu | signifikant | neuartig | erstmals | erstmalig | beispiellos | immer | stets

## SCI-2 Hedging

Calibrated hedging is part of scientific honesty. The task is to put the right amount of uncertainty in the right place.

- One hedge per claim, placed on the uncertain part. "These results suggest that X contributes to Y" hedges once. "These results could potentially suggest that X may contribute to Y" hedges three times (R2b). A hedge verb (suggests, indicates, points to, is consistent with; legt nahe, deutet darauf hin) is already the hedge: "may suggest" and "legt nahe, dass ... könnte" hedge twice. Choose the hedge verb or the modal, not both.
- Do not hedge facts about your own methods and data. "We may have used 40 samples" is wrong; "we used 40 samples" is right.
- Do not hedge and boost the same claim ("may clearly show", "could definitely", "könnte eindeutig").
- Do not remove a hedge the source has. Deleting "may" is an upgrade (F2). Adding a hedge to a claim the source states plainly is a downgrade (F2), unless the user asks for a more cautious claim.
- Boosters need evidence: clearly, undoubtedly, remarkably, strikingly, eindeutig, zweifellos, bemerkenswert. One in a paper can be earned; several are a finding (I8).
- Limitations are specific: "The sample came from one hospital; results may not transfer to rural clinics" instead of "This study has several limitations".
- German hedging uses modal verbs, Konjunktiv II, and particles: "könnte", "dürfte", "scheint", "möglicherweise", "vermutlich", "wahrscheinlich". "Dürfte" expresses a probable assumption and is often the most precise single hedge in German.

## SCI-3 Abstract

- Structure (unless the venue prescribes headings): context in one sentence, the gap, what was done, main results with the numbers from the source, the implication at the strength the evidence allows.
- Tense: present for established knowledge and for what the paper does ("We present"); past for what was done and found ("We measured", "Accuracy was 91%").
- No citations, undefined abbreviations, or references to figures, unless the venue allows them.
- Respect the word limit the user gives. Cut restatement (R14) before cutting results.
- No opener of the "has attracted increasing attention" or "In recent years" type (S13). Start with the specific context.
- No closing sentence of the "paves the way for future research" type (I2). End on the implication or the main result.

## SCI-4 Introduction and the research gap

- Move from what is known, to what is not known (the gap), to the question, to what this paper contributes. Each step cites where citations are needed.
- The gap must be specific: "no study has measured X under condition Y" or "existing methods require Z, which is unavailable in setting W". "Little is known about X" is only acceptable when it is followed by what exactly is unknown.
- A gap claim that depends on the literature needs citations the user supplies. Without them, write `[NEED: citation for the claim that ...]`. Never invent a reference, author, year, or DOI (F1).
- Contributions may be a short list. Each item is a claim the results section supports.
- A roadmap sentence ("Section 2 reviews ...") is optional and conventional in long papers and theses (S7 relaxed here).

## SCI-5 Related work

- Group by approach, question, or method, not by paper. A paragraph per group; each paragraph ends by saying how this work differs.
- Avoid the list form "A et al. did X. B et al. did Y. C et al. did Z." (R7 applies: same skeleton, three times).
- Be fair and specific about prior work. "Unlike [12], which assumes a fixed vocabulary, our method ..." is fair. "Existing approaches fail to capture the complexity of ..." is S10 with no one named.
- Use only the references the user supplies; keep citation keys and numbers exactly.

## SCI-6 Methods

- Enough detail to reproduce: design, participants or samples (n, inclusion and exclusion criteria), materials with versions, procedures in order, parameters, analysis (tests, software and version, thresholds, corrections for multiple comparisons), ethics approval if the user gives it.
- Past tense. Passive or "we": both are correct; follow the field, the venue, and the user's draft (R10 is off here). Do not convert passive to active in a methods section because a general rule says so.
- No evaluative adjectives ("carefully", "rigorous", "meticulously", "sorgfältig"): they describe the authors' self-image, not the method.
- Every number (n, concentrations, durations, hyperparameters, seeds) is copied exactly (F1). A missing one in Draft mode is `[NEED: ...]`.

## SCI-7 Results

- Report before interpreting. Interpretation belongs in the discussion, apart from the minimum needed to read a result.
- Numbers with units, variability (SD, SE, CI), test, and n. Same order as the methods.
- Refer to figures and tables by number; say what the reader should see in them.
- No "interestingly", "notably", "remarkably" (R5). If a result matters, say why in the discussion.
- Negative and null results are reported with the same care.

## SCI-8 Discussion

- Open with the answer to the research question, at the strength of SCI-1.
- Compare with prior work the user cites: agree, disagree, and why.
- Mechanisms and explanations are hedged once (SCI-2).
- Implications stay within the evidence and the scope.
- No "future work will" filler; name the specific next study if the user gives one.

## SCI-9 Limitations

- Specific, with consequences: what the limitation is, which result it affects, in which direction, and what would address it.
- Not ritual: "Like all studies, ours has limitations" adds nothing.
- Not self-sabotage: list real limits, not every conceivable one.

## SCI-10 Figure and table captions

- Self-contained: a reader should understand the figure from the caption alone.
- Start with a title fragment ("Figure 3. Error rate by noise level."), then what is shown, conditions, n, what error bars or shading mean, statistical annotations, and abbreviations.
- Minimal interpretation. "Error rate rises above noise level 0.4" is description; "demonstrating the superiority of our method" is not.
- In German: "Abbildung 3: ..." or "Abb. 3.", "Tabelle 2: ..."; the same content rules apply.

## SCI-11 Grant proposals

- Aims are concrete and testable; each has a method and a measurable outcome.
- Feasibility rests on preliminary results and resources the user supplies. Never invent preliminary data, collaborators, letters of support, or budget figures (F1).
- Impact is bounded by the evidence and plausible; I1 and I7 are set to `extra`.
- Use the funder's structure and headings when the user provides the call or template. German funders (for example the DFG) prescribe section structures and page limits that change between calls; follow the user's template and say so when you are unsure of the current rules.
- Work plan: work packages, milestones, and timeline only from the user's material.

## SCI-12 Peer reviews and responses to reviewers

### Writing a peer review

- Open with a short summary of the paper's claims in your own words, to show what you understood.
- Then major issues (those that affect the conclusions), then minor issues. Number them.
- Each issue: where (section, line, figure), what the problem is, why it matters, and a concrete suggestion.
- Judge the claims against the evidence (SCI-1); say where a claim is stronger than the data.
- Tone: direct and respectful. Criticize the work, not the authors. No sarcasm, no speculation about who the authors are.
- Do not ask authors to cite your own work unless it is necessary, and say so if you do.
- Do not reproduce confidential manuscript content outside the review.
- End with a recommendation only if the venue asks for one in the review text.

### Writing a response to reviewers

- One opening thanks to the editor and reviewers. Not a thanks formula on every point ("We thank the reviewer for this insightful comment" twelve times is C2).
- Point by point: quote or number each comment, then the reply, then what changed and where (page, line, section, figure).
- State changes as done only if the user says they are done. If the user has not yet made a change, write "[NEED: confirm whether the new analysis was added]" rather than "We have added" (F1).
- Disagree politely with reasons and evidence. "We respectfully disagree because ..." is fine once per disagreement.
- Keep the reviewer's numbering. Use the same terms as the reviewer where possible.
- In German responses ("Stellungnahme zu den Gutachten"), the same structure applies.

## SCI-13 English and German academic style

| Point | English | German |
|---|---|---|
| Person | "We" common in most fields, also for single authors in some; "I" in humanities and theses | The traditional "Ich-Verbot" is weakening: many current guides accept "ich" for the author's own decisions in theses, while others and some supervisors still prefer impersonal forms ("es wurde", "man", "die vorliegende Arbeit"). Follow the user's draft and institution. Unsure territory: practice varies by discipline and department. |
| Passive | Accepted in methods; active preferred elsewhere by many journals | Vorgangspassiv is normal in methods and descriptions; "man" is acceptable but sparingly |
| Sentence length | Short to medium preferred | Longer sentences are tolerated, but readability guides (for example Wolf Schneider) warn against wide verb brackets and nested clauses (G3) |
| Nominal style | Zombie nouns discouraged | Nominalstil is common in German academic prose but heavy chains are a style fault (R18) |
| Reported speech | Past tense reporting verbs | Indirect speech in Konjunktiv I ("X argumentiert, dies sei ...") marks another author's claim |
| Tense for literature | Present or past, consistent | Präsens for current claims, Präteritum or Perfekt for completed studies |
| Numbers | 1,234.5; 5% | 1.234,5 (or thin space); 5 % with a space |
| Citations | Per style guide | Per style guide; "vgl." for indirect references in humanities styles |
| Anglicisms | n/a | Technical English terms are normal where the field uses them; general-language Anglicisms are not (G1) |
| Gender-inclusive language | Singular "they" and neutral nouns are common | Institutions differ (Doppelnennung, Genderstern, Doppelpunkt, neutral forms); follow the user and institution; do not add or remove on your own |

## SCI-14 Critique checklist

1. Every number, statistic, citation, name, and date matches the source exactly (F1).
2. Every claim sits at the right rung of SCI-1; no upgrade or downgrade from the source (F2).
3. Each claim has at most one hedge, on the uncertain part (SCI-2, R2b).
4. The abstract has context, gap, method, result with numbers, bounded implication (SCI-3).
5. The research gap is specific and cited, or marked `[NEED: citation]` (SCI-4).
6. Related work is grouped and contrasted, not listed (SCI-5).
7. Methods are reproducible, with passive or active as the field prefers (SCI-6).
8. Results report before interpreting, with units, variability, tests, and n (SCI-7).
9. Discussion answers the question first and stays within scope (SCI-8).
10. Limitations are specific with consequences (SCI-9).
11. Captions are self-contained (SCI-10).
12. Reviews are numbered, specific, and fair; responses quote, reply, and locate each change (SCI-12).
13. "Significant", "novel", "robust", "optimal", "proof" are used in their technical sense (I13).
14. No chat residue, placeholders, or invented references (C1, F3, F1).
