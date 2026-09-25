# Language: German

Load this file for any German text or German section. German AI tells are not English tells translated. Some English patterns do not exist in German, some exist in a different form, and several things that look like tells to an English eye are correct German. This file holds the German settings, the German writing rules, and the guards against flagging ordinary German. The German markers themselves live in the catalog entries (`patterns.md`, lines marked DE), so they are written down once. Rule IDs in this file start with `DE-`.

## How this file was built, and where it is unsure

- Grounded in German-language sources: the German Wikipedia guide "Wikipedia:Anzeichen für KI-generierte Inhalte" (read for this skill), and the standard German style and usage references Duden ("Richtig und gut schreiben", Rechtschreibregeln), DIN 5008 (Schreib- und Gestaltungsregeln), Wolf Schneider ("Deutsch für Profis", "Deutsch für Kenner"), and Ludwig Reiners ("Stilkunst"). The book references come from general knowledge of these works, not from a rereading for this skill; claims that depend on them are marked "(practice)" rather than presented as quotations.
- The German list of generated-text vocabulary (catalog entry I4, DE list) is based on practitioner sources collected by the avoid-ai-writing-multilingual project (Ströer, eology, ContentConsultants, ki-im-marketing.at) and on the German Wikipedia guide. None of these is a corpus study. Treat that list as leads, not measurements.
- No published corpus study of German LLM output lists phrase frequencies that could back a "tier" the way the English lists claim to be backed. Where this file says "reads as template", it means experienced German editors flag it, not that it has been measured.
- Where the skill is unsure, it says so in the finding ("uncertain: practice varies").

## Settings

This table lowers genre settings for German text. `on` means "keep the genre setting". Entries not listed keep the genre setting.

| ID | Setting | Note |
|----|---------|------|
| R6 | relaxed | The spaced en dash ( – ) is the German Gedankenstrich and correct punctuation (Duden). Only density counts, and only the em dash (—) is foreign typography in German and counts on one sighting. |
| M5 | relaxed | „…“ and »…« are correct German quotation marks; straight quotes are common in informal typing. A mismatch counts only when English curly quotes (“…”) appear in German text. |
| R10 | relaxed | Vorgangspassiv and "man" are normal German, especially in technical, legal, and academic text. |
| R9 | relaxed | German school teaching trains writers to avoid repeating words, so synonym variation is a common human German habit. Flag only when the variation confuses the referent. |
| R4 | on | German connectors are a real tell in density, but see DE-7 for which ones are ordinary. |
| R18 | on | Nominalstil is the most common German style fault, AI or not. |
| M2 | relaxed | German capitalizes nouns anyway; "title case" means capitalized verbs, adjectives, or conjunctions in headings ("Strategische Verhandlungen Und Partnerschaften"). |
| R11 | relaxed | Modal particles and adverbs (ja, doch, gerne, eben) carry tone in German; only emphasis words count (wirklich, absolut, total, extrem). |
| G1 | on | German only. |
| G2 | on | German only. |
| G3 | on | German only. |
| G4 | on | German only. |

## DE-1 Typography

- Quotation marks: „Beispiel“ (lower 99, upper 66) in Germany and Austria; »Beispiel« in books; «Beispiel» in Switzerland. Nested: ‚…‘. Keep the document's choice consistent.
- Gedankenstrich: en dash with spaces: "Das war – wie erwartet – zu spät." Bis-Strich: en dash without spaces for ranges: "2019–2022", "S. 10–12". Bindestrich (hyphen) for compounds: "E-Mail-Adresse".
- Compounds are written together or hyphenated, never split by a space: "Softwareentwickler" or "Software-Entwickler", not "Software Entwickler". A split compound is English interference (R17, DE marker).
- Numbers: decimal comma (3,5), thousands with a point or a narrow space (12.500 or 12 500). Four-digit numbers often without separator (2500).
- Percent and units with a space: "5 %", "20 °C", "3 km" (DIN 5008, Duden).
- Dates: "25.09.2026", "25. September 2026", or ISO "2026-09-25" (DIN 5008 allows both numeric forms). Months in CVs: "03/2021".
- Times: "14:30 Uhr" or "14.30 Uhr".
- Phone numbers (DIN 5008): "030 1234567", "+49 30 1234567"; groups by spaces, no slashes or parentheses in the current standard.
- Abbreviations with spaces: "z. B.", "d. h.", "u. a."; "usw.", "bzw.", "ca.".
- "ß" in Germany and Austria; Swiss Standard German uses "ss" throughout. Do not "correct" Swiss text.
- Apostrophe for genitive: "Peters Buch", not "Peter's Buch". Duden allows the apostrophe only in narrow cases; frequent use is English interference (G2).
- Comma rules differ from English: a comma before "dass", "ob", "weil", relative clauses, and most infinitive groups; no comma after a sentence-initial adverbial ("Im Jahr 2020 gründete sie ..." not "Im Jahr 2020, gründete sie ..."). A comma after an introductory adverbial is English interference (G2).

## DE-2 Address and register

- "Sie", "Ihnen", "Ihr" in formal address are always capitalized. "du" and "dein" may be written lowercase or capitalized in letters and emails (both correct since the 2006 reform); keep one form.
- Never mix "Sie" and "du" addressing the same person or audience in one text (G4).
- Formal letters and applications: "Sie". LinkedIn and startup culture: "du" is common in some communities. Follow the user or the recipient's own usage.
- Closings: "Mit freundlichen Grüßen" (formal), "Freundliche Grüße", "Viele Grüße", "Beste Grüße" (neutral), "Liebe Grüße", "LG" (private only).

## DE-3 Gender-inclusive language

German writers and institutions differ: pair forms ("Mitarbeiterinnen und Mitarbeiter"), Genderstern ("Mitarbeiter*innen"), Doppelpunkt ("Mitarbeiter:innen"), neutral forms ("Beschäftigte", "Mitarbeitende"), or the generic masculine. Rules:

- Follow the user's text and the institution's style. Do not add, remove, or switch forms on your own.
- Changing "Mitarbeiterinnen und Mitarbeiter" to "Mitarbeiter" is a change of content, not of style. Treat inclusive forms as protected.
- Keep one form throughout a document; mixed forms are a consistency finding.
- Official German orthography (Rat für deutsche Rechtschreibung) has not adopted the Genderstern or Doppelpunkt as standard; some public bodies ban them, others require them. Unsure territory: tell the user when it matters and let them choose.

## DE-4 Verbalstil instead of Nominalstil

Nominalstil turns actions into nouns and hangs them on weak verbs. It is the most common German style fault in business, administrative, and academic writing, and generated German text leans on it heavily. R18 holds the pattern; this section says how to fix it.

- Turn the action back into a verb: "Die Durchführung der Optimierung der Prozesse erfolgte durch das Team" → "Das Team hat die Prozesse verbessert" (or, with the source's details, what exactly it changed).
- Replace Funktionsverbgefüge with the plain verb when nothing is lost: "eine Entscheidung treffen" → "entscheiden", "zur Anwendung bringen" → "anwenden", "in Betracht ziehen" → "erwägen", "einen Beitrag leisten zu" → "beitragen zu" or the concrete verb, "in der Lage sein" → "können". Some Funktionsverbgefüge carry a nuance (Duden notes, for example, that "zur Sprache bringen" differs from "ansprechen" in register); keep those.
- Break genitive chains longer than two links: "die Verbesserung der Qualität der Ausbildung der Fachkräfte" → "Fachkräfte besser ausbilden".
- Keep established terms (Qualitätssicherung, Datenschutz-Folgenabschätzung) and legal terms. CV bullets and headings may stay nominal (genre-cv: R18 relaxed).
- Threshold (practice): three or more -ung, -heit, -keit, -ion, -ität nouns in one clause, or a genitive chain of three links, is a finding.

## DE-5 Sentence length and the verb bracket

German splits verbs: the finite verb comes second, the rest (participle, infinitive, separable prefix) comes at the end. Long insertions between the two parts force the reader to hold the sentence open.

- Keep the verb parts close. Wolf Schneider's rule (practice) is to avoid inserting more than a few words, roughly a dozen, between them. G3 holds the pattern.
- Nested subordinate clauses (Schachtelsätze) two levels deep or more are a finding outside legal text.
- Average sentence length: news style guides aim for short sentences (practice: under about 20 words on average); academic German may run longer. No hard limit; vary length.
- Put the main point in the main clause.

## DE-6 German markers that really are template

These appear in the catalog entries named. They are listed here so German-language findings can cite the right entry quickly.

- Significance inflation (I1): "spielt eine entscheidende/zentrale/wichtige Rolle", "ein wichtiger Meilenstein" (outside project management), "Wendepunkt", "bleibendes Vermächtnis", "ein wichtiger Baustein", "trägt maßgeblich dazu bei", "von zentraler Bedeutung", "kommt eine Schlüsselrolle zu".
- Transition density (R4): "Darüber hinaus", "Des Weiteren", "Zudem", "Ferner", "Nichtsdestotrotz", "Zum einen ... zum anderen" at the start of several sentences in a row.
- "Nicht nur ... sondern auch" for weight (S1): "nicht nur effizient, sondern auch nachhaltig". Also the corrective form "Es geht nicht um X, sondern um Y" and "Das ist kein X. Das ist Y."
- Announcing (S7): "Tauchen wir ein", "Tauchen Sie ein in", "In diesem Beitrag beleuchten wir", "Werfen wir einen Blick auf".
- Importance markers and summaries (R5): "Es ist wichtig zu betonen, dass", "Es sei darauf hingewiesen, dass", "Bemerkenswert ist, dass", "Interessanterweise", "Es lässt sich festhalten", "Insgesamt lässt sich sagen" (density; see DE-7 for academic and school use).
- Scene-setting openers (S13): "In der heutigen schnelllebigen Zeit", "Im Zeitalter der Digitalisierung", "In einer sich rasant wandelnden Welt", "In der modernen Arbeitswelt".
- Chat residue (C1): "Ich hoffe, das hilft", "Hier ist eine überarbeitete Version", "Lassen Sie mich wissen, ob", "Gibt es noch etwas, bei dem ich helfen kann", "Ich hoffe, diese Nachricht erreicht Sie wohlauf" (German Wikipedia names this word-for-word translation of the English formula).
- Modal hedging density (R2): "kann" in almost every sentence ("Dies kann dazu beitragen, ... zu ermöglichen"), "könnte möglicherweise", "eventuell vielleicht".
- Needless Anglicisms (G1) and English calques (G2).
- Impersonal distancing (R5, DE marker): "Es zeigt sich, dass", "Es wird deutlich, dass", "Es gilt zu beachten" as paragraph openers in non-academic text.

## DE-7 Ordinary German that must not be flagged

The German adaptation that this skill checked flagged several of these as tells. They are correct, common German, and flagging them would push careful German writers toward worse text.

- **nachhaltig** means "lasting, with long-term effect" (its older, forestry-derived sense) as well as "sustainable". "nachhaltig verbessern" is idiomatic. Flag only as part of a cluster of buzzwords.
- **Herausforderung, Potenzial, Mehrwert, Meilenstein** are everyday German. "Meilenstein" is a defined project-management term (for example in DIN 69900); "Mehrwert" is an economics term; replacing "Herausforderung" with "Problem" changes the meaning. Only clusters count (I4, tier 2).
- **"Chancen und Risiken"** is required wording in German management reports (§ 289 HGB). Never flag it in business reporting.
- **"Fazit"** is the standard heading for a German conclusion. **"Zusammenfassend lässt sich sagen"**, **"Abschließend"** are taught in German schools for essay conclusions and are standard in academic and legal prose; flag only when stacked or in short-form text.
- **Didactic "wir"**: "Betrachten wir die Funktion f", "Schauen wir uns zunächst ... an" is the normal register of German textbooks, lectures, and mathematics. S7 applies only to template openers in blogs and posts.
- **"Dabei", "Gleichzeitig", "Folglich", "Außerdem", "Allerdings"** are among the most common German connectors. Never flag them on their own.
- **"Es ist zu beachten, dass" / "Hierbei ist zu beachten"** is standard in manuals, instructions, and technical documentation.
- **"Grundsätzlich"** has a precise legal meaning ("as a rule; exceptions exist"). Flag only as filler in non-legal text.
- **"Gerne", "Natürlich"** in a reply to a request ("Gerne sende ich Ihnen die Unterlagen") are polite German. Only a standalone "Gerne!" or "Natürlich!" opening a text that is not a reply counts (C1).
- **"sowohl ... als auch"** is ordinary German; only repetition counts.
- **"Es bleibt abzuwarten", "Wir dürfen gespannt sein"** are newspaper stock phrases older than LLMs. They are clichés (I2a) at P2, not P0 tells.
- **The Gedankenstrich** ( – ) is correct punctuation (R6 relaxed).
- **Synonym variation** is taught in German schools (R9 relaxed).
- **Passive and "man"** are normal (R10 relaxed).
- **Long sentences** in academic and legal text are normal; judge the verb bracket and nesting (G3), not the word count.
- **Modal particles** ("ja", "doch", "halt", "eben", "mal") are human German, especially in emails and posts. Removing them makes text stiffer. Note: "möglicherweise" and "eventuell" are Modalwörter (sentence adverbs), not Modalpartikeln.
- **"essentiell"** is an accepted variant of "essenziell" (Duden). Not a tell.
- **Established loanwords**: Team, Software, Feedback, Workshop, Know-how, Marketing, Start-up, E-Mail, Laptop, Meeting, Projekt, Management. Technical terms of a field (Machine Learning, Deployment, Pipeline, Framework) are correct where the field uses them (G1 guard).

## DE-8 German genre conventions (pointers)

Genre rules live in the genre files; the German-specific ones are:

- Lebenslauf layout and personal data: genre-cv.md, CV-10.
- Anschreiben layout (DIN 5008), opening, logistics, closing: genre-prose.md, PR-2.
- Emails and address forms: genre-prose.md, PR-4, and DE-2 above.
- German academic style (Ich-Verbot, Konjunktiv I, Nominalstil tolerance, gender-inclusive forms): genre-science.md, SCI-13.

## DE-9 Sources and confidence

| Source | Used for | Confidence |
|---|---|---|
| Wikipedia:Anzeichen für KI-generierte Inhalte (de.wikipedia.org), read September 2026 | Chat residue, knowledge-limit phrases, symbolic overemphasis ("spielt eine wichtige Rolle", "Wendepunkt", "bleibendes Vermächtnis"), marketing language ("reiches kulturelles Erbe", "atemberaubend"), editorial comments ("es ist wichtig zu bemerken"), connector overuse ("darüber hinaus", "außerdem", "ferner"), summary words ("zusammenfassend", "abschließend", "insgesamt"), "nicht nur ..., sondern auch", tricolon, vague authorities, formatting | Medium. A community guide, not a study. It also calls the en dash an "em dash" and a tell, which is wrong for German typography; this skill does not follow it on that point. |
| Duden, "Richtig und gut schreiben" and orthography rules | Typography (DE-1), compounds, apostrophe, comma rules, "essenziell", address forms | High for rules (practice) |
| DIN 5008 | Letter layout (PR-2), dates, times, phone numbers, percent spacing | High, but the 2020 revision changed details; check a current template for exact measurements |
| Wolf Schneider, "Deutsch für Profis" | Verbalstil, verb bracket, sentence length (DE-4, DE-5) | Medium (practice; paraphrased) |
| Ludwig Reiners, "Stilkunst" | Nominalstil criticism | Medium (practice; paraphrased) |
| avoid-ai-writing-multilingual, SKILL-DE.md and DE-sources.md (Ströer, eology, ContentConsultants, GoWinston, ki-im-marketing.at, Schaaff et al. 2023) | Leads for the German vocabulary list, "tauchen wir ein", "kann" density, "eine Vielzahl an", "eine breite Palette an", rule of three | Low to medium. Mostly SEO and marketing blogs and a detector vendor; checked here against German usage, and several claims rejected (DE-7). |
| § 289 HGB | "Chancen und Risiken" as required wording | High |
| Allgemeines Gleichbehandlungsgesetz (AGG) | Photo and personal data in the Lebenslauf (CV-10) | High for the law's existence; application practice varies |
