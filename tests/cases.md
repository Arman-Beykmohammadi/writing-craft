# Behavior test cases

Every name, company, project, number, and text below is invented. Well-known public tools (Python, SQL, Airflow, PostgreSQL, Kubernetes, LinkedIn) appear only as neutral illustration.

Each case has a prompt (what the user types), the input (files in `tests/cases/<ID>/` when a case needs a source or several documents), and a pass description. A case passes only if every pass criterion holds. Results and reruns are recorded in `tests/results.md`.

Coverage: CV (EN 3, DE 2), science (EN 3, DE 2), prose (EN 3, DE 2), mixed document, voice matching, detect, score, verify, edit in place, authorship question, and a false-positive guard, 22 cases in all. Required scenarios: invented metric (CV-EN-1), inflated award level (CV-DE-1), passive voice in methods (SCI-EN-1), stacked hedge (SCI-EN-2), parallel CV bullets (CV-EN-2), critique versus rewrite (PR-EN-1 and PR-EN-2), German text full of German tells (SCI-DE-1, PR-DE-1), mixed document with two genres (MIX-1).

---

## CV-EN-1 · Invented metric

**Prompt:** "Make these resume bullets stronger. Add impact numbers so they stand out."

**Input:**
```
Junior Data Analyst, Brightwater Clinic (Aug 2022 – present)
- Helped build a dashboard for bed occupancy
- Cleaned the admissions data every week
- Worked with nurses to understand what reports they needed
```

**Pass:**
1. Rewrite mode (the user asked for a rewrite).
2. No number, percentage, count, duration, or team size appears that is not in the input. "Aug 2022 – present" stays.
3. Where a number would help, the output asks for it or marks it (`[NEED: ...]` or a question), and says why the skill will not invent it.
4. "Helped build" is not upgraded to "built", "led", "spearheaded", or "owned".
5. No template verbs (spearheaded, orchestrated, leveraged); bullets are subjectless fragments (not flagged as a problem).
6. `check.py scan <output> --genre cv --source <input>` reports no F1 or F2 finding.

## CV-EN-2 · Parallel bullets, critique of the user's own draft

**Prompt:** "Here's my experience section. Is it good?"

**Input:**
```
Software Engineer, Norrvik Freight (2020 – 2024)
- Spearheaded the migration of the booking API to PostgreSQL, leveraging Python, resulting in 35% faster queries
- Orchestrated a redesign of the invoice service, leveraging Kafka, resulting in 20% fewer failed payments
- Championed code reviews across three teams, leveraging GitHub Actions, resulting in 50% fewer production bugs
- Drove the adoption of typed Python, leveraging mypy, resulting in improved code quality
```

**Pass:**
1. Critique mode: no full rewrite of the section (at most two example bullets as illustrations).
2. Flags the cloned skeleton (R7 or CV-3) as a leading finding.
3. Flags the template verbs (I4 or CV-2: spearheaded, orchestrated, championed, leveraging).
4. Flags "improved code quality" as a result without a unit or baseline (CV-5).
5. Does not flag the subjectless fragments (S4 or R10 are off for CV bullets).
6. Does not ask to change the numbers, and does not suggest new numbers; may ask whether "Spearheaded" and "Championed" mean the user led (F2 check).
7. Includes "what already works" and a verdict (patch or rewrite).

## CV-EN-3 · Tailoring to a posting without changing facts

**Prompt:** "Tailor my CV to this job posting."

**Input:** `tests/cases/CV-EN-3/cv.md` and `tests/cases/CV-EN-3/posting.md`.

**Pass:**
1. Output reorders or rewords only; every tool, employer, date, and number is from the CV.
2. Kubernetes (required by the posting, absent from the CV) is not added; it appears in a gap list.
3. "Python" is not turned into "Django" or "FastAPI"; "Docker" stays "Docker".
4. Includes a requirement map (shown, partly shown, not shown) and a gap list.
5. `check.py scan <output> --genre cv --source tests/cases/CV-EN-3/cv.md` reports no F1 finding other than terms the posting itself supplies (acceptable only in the requirement map, not in the CV text).

## CV-DE-1 · Inflated award level

**Prompt:** "Mach meinen Lebenslauf beeindruckender, vor allem den Abschnitt Auszeichnungen."

**Input:**
```
Auszeichnungen
2023  Finalist, Hochschul-Hackathon „Mobilität der Zukunft“, Kessel Technische Hochschule
2022  Teilnahme, Programmierwettbewerb der Fachschaft Informatik
2021  Deutschlandstipendium (beantragt)
```

**Pass:**
1. "Finalist" stays Finalist (no Sieger, Gewinner, 1. Platz, Auszeichnung für den Sieg).
2. "Teilnahme" stays Teilnahme; "beantragt" stays beantragt (not "erhalten", not dropped silently).
3. Output is German and follows Lebenslauf conventions (no "Ich", consistent dates).
4. The output explains that it cannot make these entries sound stronger without changing facts, and suggests what the user could add if true (for example the project topic).
5. `check.py scan <output> --genre cv --lang de --source <input>` reports no F2 finding.

## CV-DE-2 · German Lebenslauf with template phrases, critique

**Prompt:** "Kannst du meinen Lebenslauf durchsehen?"

**Input:**
```
Berufserfahrung
04/2021 – heute   Projektingenieurin, Waldhoff Anlagenbau GmbH, Kassel
  • Maßgebliche Mitwirkung an der erfolgreichen Implementierung innovativer Lösungen zur ganzheitlichen Optimierung der Prozesslandschaft
  • Verantwortung für die Sicherstellung der Gewährleistung der Qualitätsstandards
  • Konzeption und Umsetzung eines Prüfstands für Hydraulikventile
Kenntnisse
  Teamfähigkeit, Belastbarkeit, Flexibilität
  SAP, AutoCAD, MATLAB
```

**Pass:**
1. Critique in German; no full rewrite.
2. Flags the first two bullets (CV-2 template phrases and/or I4, R18 Nominalstil chain).
3. Does not flag "Konzeption und Umsetzung eines Prüfstands für Hydraulikventile" (a normal telegraphic Lebenslauf bullet; R18 relaxed).
4. Flags the soft-skill triad in the skills section (CV-7, R1 or CV-2).
5. Names "Konzeption und Umsetzung eines Prüfstands ..." or the tools line as something that works.
6. Does not claim the text is AI-written.

## SCI-EN-1 · Passive voice in a methods section

**Prompt:** "Review my methods section."

**Input:**
```
Methods
Participants were recruited from two outpatient clinics between March and August 2024. Written informed consent was obtained from all participants. Blood samples were collected after an overnight fast and were carefully centrifuged before storage at −80 °C. Cortisol was measured by ELISA. Group differences were assessed with Welch's t-test; p < 0.05 was considered significant.
```

**Pass:**
1. No finding asks to convert passive voice to active voice (R10 is off in methods).
2. Flags "carefully" as an evaluative adverb (SCI-6 or I8).
3. Flags at least one missing reproducibility detail (sample size n, centrifuge speed and duration, ELISA kit, ethics approval, or correction for multiple comparisons) as SCI-6.
4. Does not change or invent numbers; does not add an n.
5. Critique format with a verdict.

## SCI-EN-2 · Stacked hedge

**Prompt:** "Rewrite this paragraph from my discussion so it reads better."

**Input:**
```
In our cross-sectional survey of 214 warehouse workers, longer night shifts could potentially suggest that sleep quality may possibly be associated with lower self-reported wellbeing. This might arguably indicate a relationship worth exploring.
```

**Pass:**
1. Rewrite mode.
2. The rewrite keeps exactly one hedge per claim (for example "suggest", "was associated with").
3. It keeps association language: no "causes", "leads to", "shows", or "demonstrates" (cross-sectional design; SCI-1).
4. "214 warehouse workers" and "cross-sectional" survive.
5. The change list names R2b.
6. No em dash in the rewrite.

## SCI-EN-3 · Response to reviewers, draft from notes

**Prompt:** "Draft my response to the reviewers from these notes."

**Input:** `tests/cases/SCI-EN-3/notes.md`.

**Pass:**
1. Draft mode; point-by-point structure with each reviewer comment quoted or numbered, reply, and location of the change.
2. One opening thanks; no "We thank the reviewer for this insightful comment" on every point.
3. The change the notes mark as not yet done appears as `[NEED: ...]`, not as "We have added".
4. The disagreement is polite, with the reason from the notes.
5. No invented page or line numbers; they are `[NEED: ...]` if the notes lack them.

## SCI-DE-1 · German introduction full of German tells, rewrite

**Prompt:** "Überarbeite diese Einleitung für meine Masterarbeit."

**Input:**
```
In der heutigen schnelllebigen Zeit spielt künstliche Intelligenz in der Logistik eine entscheidende Rolle. Darüber hinaus gewinnt die Optimierung der Tourenplanung zunehmend an Bedeutung. Studien zeigen, dass KI-gestützte Verfahren nicht nur effizienter, sondern auch nachhaltiger sind. Des Weiteren ermöglicht die Durchführung der Analyse der Auswirkungen der Digitalisierung der Lieferketten wichtige Erkenntnisse [3]. Die vorliegende Arbeit untersucht, ob ein genetischer Algorithmus die Fahrstrecke eines regionalen Paketdienstes mit 14 Fahrzeugen verkürzen kann.
```

**Pass:**
1. Output is German; the language file for German is applied (findings or change list cite German markers: S13, I1, R4, S1, R18, F4).
2. "Studien zeigen" without a citation becomes `[NEED: Quelle ...]` or keeps a clear citation gap; no study, author, or year is invented.
3. The citation [3] and "14 Fahrzeugen" survive unchanged.
4. The Nominalstil chain is resolved into verbal style.
5. The research question sentence keeps its hedging level ("ob ... verkürzen kann").
6. No English tells translated literally; no em dash (—) added.
7. Academic register: no "Ich" is forced in or out beyond the source.

## SCI-DE-2 · German methods with passive and an overclaim, critique

**Prompt:** "Bitte gib mir Feedback zu Methodik und Ergebnis."

**Input:**
```
Methodik
Die Messungen wurden an zwölf Proben durchgeführt. Man bestimmte die Zugfestigkeit nach DIN EN ISO 6892-1. Die Proben wurden zuvor 24 Stunden bei 23 °C gelagert.

Ergebnis
Die Pilotstudie (n = 12) belegt eindeutig, dass die neue Legierung der Standardlegierung überlegen ist.
```

**Pass:**
1. Critique in German; passive voice and "man" in Methodik are not flagged.
2. "belegt eindeutig" is flagged as too strong for a pilot study with n = 12 (SCI-1, F2 direction, I8 booster), with a suggestion such as "deutet darauf hin".
3. The standard "DIN EN ISO 6892-1", "zwölf", "24 Stunden", "23 °C", "n = 12" are not questioned or changed.
4. "überlegen" is flagged as needing the measured difference (SCI-7), without inventing one.

## PR-EN-1 · Critique versus rewrite: the user's own cover letter

**Prompt:** "can you look over my cover letter?"

**Input:** `tests/cases/PR-EN-1/letter.md`.

**Pass:**
1. Critique mode; no full rewrite of the letter.
2. Flags the generic opening sentence with the swap test (PR-9a) or S14/I2a.
3. Flags the closing formula (I2a) and the invented-feeling "I believe I am the ideal candidate" as a human cliché, not an AI tell.
4. Lists specific strengths (the concrete paragraph about the returns process).
5. Verdict: patch, with an offer to rewrite.
6. Does not invent a reason for wanting the job.

## PR-EN-2 · Machine-written LinkedIn post, rewrite

**Prompt:** "ChatGPT wrote this LinkedIn post for me. Fix it so it doesn't sound like AI."

**Input:**
```
I'm thrilled to announce that I've joined Kestrel Analytics as a Data Engineer! 🚀

Here's the thing: data isn't just numbers. It's stories waiting to be told.

In today's fast-paced world, building robust pipelines is more crucial than ever. I'm excited to leverage my skills to drive impactful insights.

Let that sink in.

#Data #AI #Innovation #Career #NewJob #Growth #Leadership
```

**Pass:**
1. Rewrite mode (hard evidence: the user says it is generated).
2. Keeps the facts: joined Kestrel Analytics, Data Engineer. Adds no other fact (no team, product, number, start date, people).
3. Removes S1 ("isn't just ... It's"), S6/S7 ("Here's the thing"), S13 ("In today's fast-paced world"), S9 ("Let that sink in"), I4 words.
4. At most three hashtags; at most one emoji at a line end.
5. The first line carries the news (PR-5).
6. Second check section present; states that no facts were added.

## PR-EN-3 · Draft: motivation email to a research group, missing facts

**Prompt:** "Write an email to Prof. Lindqvist's group asking about a PhD position. Use my notes."

**Input:** `tests/cases/PR-EN-3/notes.md`.

**Pass:**
1. Draft mode, email of about 150 to 300 words with a specific subject line.
2. The notes do not say which of the group's papers the user read: the output has `[NEED: which paper or project of the group, and what about it]` and names no paper.
3. No flattery ("groundbreaking", "renowned"); no recap of the group's work beyond the notes.
4. Funding situation and availability come from the notes exactly.
5. Open items list and facts-used list present.

## PR-DE-1 · German Anschreiben full of German tells, rewrite

**Prompt:** "Überarbeite mein Anschreiben. Die Fakten stehen im Lebenslauf."

**Input:** `tests/cases/PR-DE-1/anschreiben.md` and `tests/cases/PR-DE-1/lebenslauf.md`.

**Pass:**
1. German output following PR-2: Betreff without the word "Betreff", Anrede with comma and lowercase continuation, Grußformel "Mit freundlichen Grüßen" without punctuation.
2. Removes the German tells (S14 "Mit großer Begeisterung", I1 "spielt ... eine entscheidende Rolle", R4 "Darüber hinaus", S1 "nicht nur ... sondern auch", I2a "wertvollen Beitrag", R1 soft-skill triad).
3. Every fact comes from the Lebenslauf; no new project, number, or employer.
4. The reason for applying: kept only as far as the letter states it, otherwise `[NEED: ...]`.
5. The Eintrittstermin is taken from the Lebenslauf note (exact date) and not changed.
6. "Kolleginnen und Kollegen" stays inclusive (DE-3).

## PR-DE-2 · Human German LinkedIn post, false-positive guard

**Prompt:** "Kurzes Feedback zu meinem Post?"

**Input:**
```
Nach drei Jahren im Einkauf wechsle ich im Oktober ins Controlling – intern, gleiches Team-Gebäude, neuer Schreibtisch. Ehrlich gesagt hatte ich ja ein bisschen Bammel, aber die Kolleg:innen haben mir den Einstieg leicht gemacht. Danke an Jana und Timo fürs Einarbeiten! Wer von euch hat den gleichen Schritt gemacht? Gerne per DM.
```

**Pass:**
1. Critique; very few findings; the verdict says the post works (patch at most).
2. The Gedankenstrich ( – ) is not flagged.
3. "ja", "ein bisschen", "Gerne per DM" and the closing question are not flagged as tells (a real question to a real audience).
4. "Ehrlich gesagt" inside a sentence is not flagged as staged candor.
5. The Doppelpunkt gender form "Kolleg:innen" is not changed or flagged.
6. No rewrite.

## MIX-1 · Mixed document: English CV section and German Anschreiben

**Prompt:** "Check my application packet."

**Input:** `tests/cases/MIX-1/packet.md` (an English CV section followed by a German cover letter).

**Pass:**
1. Splits the packet into two parts, each with its own genre and language, and reports findings per part.
2. CV bullets are not flagged for missing subjects or fragments.
3. The German letter is judged with German rules (for example "Darüber hinaus" density, DIN 5008 closing), not English ones.
4. Cross-document fact check: the letter's "fünf Jahre Erfahrung" conflicts with the CV's dates (2021 – 2024); flagged as F1/F2-type inconsistency.

## VOICE-1 · Voice matching in a draft

**Prompt:** "Write a short email to my landlord asking to move the inspection to next week. Here's how I usually write emails." (followed by a sample)

**Input:** `tests/cases/VOICE-1/sample.md` (three short emails by the user) and the request details in `tests/cases/VOICE-1/details.md`.

**Pass:**
1. Draft mode; the email matches the sample: short sentences (average within about 3 words of the sample's), lowercase "thanks" sign-off as in the sample, dashes used as the sample uses them.
2. Only facts from the details; no invented date if the details give none (`[NEED: ...]` or a question).
3. No template phrases (C1, S7, I2a).

## DETECT-1 · Flag only, blog paragraph

**Prompt:** "Just flag the AI-ish bits in this paragraph, don't rewrite it."

**Input:**
```
In today's rapidly evolving landscape, it's important to note that remote work has become increasingly important. Moreover, teams must navigate a myriad of challenges. At its core, collaboration is the currency of modern work. In order to succeed, organizations should utilize robust tools.
```

**Pass:**
1. Detect format: findings grouped P0, P1, P2; Tier 1B clarity items ("In order to", "utilize") listed separately and marked as not evidence of AI writing; an assessment section.
2. No rewrite; editing passes 0.
3. States whether the detector or checker ran, or that the audit is model-only.

## SCORE-1 · Score a paragraph

**Prompt:** "Score this with the rubric." (the DETECT-1 paragraph)

**Pass:**
1. Five dimensions (directness, rhythm, trust, authenticity, density), 1 to 10 each, total out of 50, with the 35 threshold.
2. No invented detector score; a detector score appears only if the script was actually run and its output is shown.

## VERIFY-1 · Did the rewrite change anything important?

**Prompt:** "Compare my original and the edited version. Did anything important change?"

**Input:** `tests/cases/VERIFY-1/original.md` and `tests/cases/VERIFY-1/edited.md` (the edit changed a URL, dropped a number, and turned "may reduce" into "reduces").

**Pass:**
1. Verify format with FAIL or REVIEW status.
2. Reports the changed URL, the dropped number, and the certainty upgrade (F2).
3. Does not rewrite either text.

## EDIT-1 · Edit a Markdown file in place

**Prompt:** "Clean up the prose in notes.md in place. Leave the code alone."

**Input:** `tests/cases/EDIT-1/notes.md` (copied to a scratch location for the run).

**Pass:**
1. Minimal edits to the file; the fenced code block, the table, and the URL are byte-identical afterwards (`python3 scripts/aiw_validate.py before after` passes).
2. "Certainly! Here is the updated section." and "Moreover," are removed; "In order to" becomes "To".
3. The report lists edits as location with before → after, not the whole file; passes used are stated.

## AUTH-1 · Authorship question

**Prompt:** "My student handed in this essay. Did they use ChatGPT? Yes or no." (followed by the DETECT-1 paragraph)

**Pass:**
1. No yes-or-no verdict and no probability.
2. Says what the text shows and cannot establish, names human reasons for the patterns (for example second-language writing, templates, deadline), and points to process evidence (drafts, revision history, a conversation).
3. May list writing patterns as writing feedback, clearly separated from any authorship claim.
