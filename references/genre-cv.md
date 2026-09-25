# Genre: CVs, resumes, Lebenslauf

Load this file for English resumes and CVs, German Lebensläufe, academic CVs, single bullets, summary lines, skills sections, and tailoring a CV to a job posting. It does not repeat any pattern from `patterns.md`. It holds the settings table for this genre and the rules that only apply here. Rule IDs in this file start with `CV-`.

## Settings

Columns: `default` covers experience, education, and project entries (bullets and tabular lines). `summary` covers a summary, profile, or Kurzprofil line or paragraph. `academic` covers academic CVs (publication lists, talks, grants, teaching, service). An entry not listed here is `on`. Integrity entries (F1 to F5) are always on.

| ID | default | summary | academic | Note |
|----|---------|---------|----------|------|
| S4 | off | relaxed | off | Bullets are subjectless fragments by design. A row of dramatic fragments in a summary still counts. |
| R10 | off | relaxed | off | CV bullets drop the subject ("Built...", "Entwicklung von..."). Passive is fine when the actor is obviously the candidate. |
| R11 | relaxed | relaxed | relaxed | Only emphasis adverbs count (successfully, effectively, erfolgreich). Adverbs that carry scope stay (jointly, independently, eigenständig). |
| R12 | off | relaxed | off | Wh- and "So" openers do not occur in bullets. |
| S20 | off | off | off | Narrator-from-a-distance does not apply to CVs. |
| M1 | relaxed | on | relaxed | Bold for job titles, employers, and section headings is convention. Bold keywords inside bullets count. |
| M2 | relaxed | relaxed | relaxed | Standard section headings ("Experience", "Berufserfahrung") are correct, in title case or not. Emoji in headings still count. |
| M3 | off | on | off | Lists are the form of a CV. Bare noun-phrase bullets are standard German Lebenslauf style and standard for skills lines. |
| R1 | relaxed | extra | relaxed | Three-adjective summaries ("results-driven, detail-oriented, passionate") are the most common summary tell. |
| R4 | off | on | off | Connectors do not occur in bullets. |
| R6 | relaxed | on | relaxed | Date ranges take an en dash by rule (2019–2022, 03/2021 – 06/2023). A dash splicing a bullet into two claims still counts. |
| R7 | extra | on | on | Parallel skeletons across bullets are the strongest CV tell. See CV-3. |
| R8 | relaxed | on | relaxed | Bullets of similar length are normal. Every bullet at exactly two lines is not. |
| R9 | relaxed | on | relaxed | Varied verbs across bullets are fine; the entry targets one referent renamed ("team", "squad", "unit"). |
| R13 | off | on | off | No through-line is expected between bullets. |
| R14 | relaxed | extra | relaxed | A summary that restates the headline is a treadmill. |
| R15 | off | off | off | Not a reply register. |
| R18 | relaxed | on | relaxed | Telegraphic noun phrases are conventional ("Konzeption und Umsetzung eines Prüfstands"). Chains of three or more nominalizations still count. |
| I4 | extra | extra | on | Verb and adjective choice carry most of a CV's register. See CV-2. |
| I8 | on | extra | on | "Successfully", "erfolgreich", "highly" in front of every claim. |
| S14 | on | extra | on | "Passionate about", "leidenschaftlich", "I am thrilled" in a summary. |
| G3 | off | on | off | Satzklammer only matters in full sentences. |
| C3 | off | off | off | Not a reply register. |

## CV-1 Bullet structure

A bullet reports one piece of work in the order that makes its strongest element visible first. Use these shapes and mix them within a role:

1. **Action, object, method or scope.** "Rewrote the billing export in Go, replacing a nightly batch job." Use when there is no result in the source.
2. **Action, object, result.** "Cut report generation from 40 to 6 minutes by caching supplier lookups." Use only when the result is in the source, with the source's number and unit.
3. **Result first.** "Zero failed payroll runs in 2023 after moving validation into the import step." Use when the result is the strongest element and it is sourced.
4. **Scope first.** "For a 12-person support team, set up the on-call rota and runbook." Use when scope (team size, budget, users, sites) is the point and it is sourced.
5. **Plain fact.** "Maintained the internal component library (React, TypeScript)." A plain bullet is fine. Not every bullet needs a number or a result.

Rules:
- One claim per bullet. Split a bullet that joins two achievements with "and" or a dash.
- One to two lines at the document's font size. Three lines means two bullets or a cut.
- Past tense for finished roles and finished work; present tense for the current role's ongoing duties (English). Keep one tense per role.
- German Lebenslauf bullets are usually noun phrases ("Entwicklung eines Prüfstands für...") or short verb phrases without a subject ("Prüfstand für ... entwickelt"). Pick one style per document. Never write "Ich" in a Lebenslauf bullet.
- Name the tool, method, or domain when the source names it. "Using Python" is weaker than "in Python with pandas" only if the source says pandas.
- Numbers only from the source (F1). If a bullet would be stronger with a number the user has not given, say so in the findings and ask; in Draft mode write `[NEED: size of the dataset]`. Ask in words, without sample figures: "How many wards use the dashboard?", not "e.g., used daily by three wards". A sample figure in a question tends to come back as the answer.
- Numbers need a baseline or a unit to mean anything. "Improved performance by 30%" without "of what" is a finding (CV-5), not a reason to invent the baseline.

## CV-2 Verbs

### Plain, strong verbs

English: built, wrote, designed, ran, led (only when the person led), managed (only for people or budgets they managed), analysed/analyzed, measured, tested, fixed, cut, reduced, raised, migrated, replaced, automated, trained, taught, supervised, mentored, organised/organized, negotiated, sold, drafted, edited, published, presented, reviewed, audited, set up, launched, shipped, maintained, documented, coordinated, translated, interviewed, recruited.

German (as participle, infinitive-noun, or noun): entwickelt/Entwicklung, gebaut/Aufbau, geschrieben/Verfassen, geleitet/Leitung (nur bei echter Leitung), betreut/Betreuung, analysiert/Analyse, gemessen/Messung, getestet/Test, eingeführt/Einführung, umgestellt/Umstellung, automatisiert/Automatisierung, geschult/Schulung, unterrichtet/Unterricht, organisiert/Organisation, verhandelt/Verhandlung, veröffentlicht/Veröffentlichung, präsentiert/Vortrag, geprüft/Prüfung, dokumentiert/Dokumentation, koordiniert/Koordination, übersetzt/Übersetzung.

### Verbs and phrases that now read as template or AI-written

These are not wrong words. They are the words a CV generator reaches for, so a page full of them reads as generated and says little. One in a CV is not a finding; three or more, or one per role, is (I4 cluster rule). Replace with the plain verb that says what was done, or keep the word when it is literally accurate.

English: spearheaded, orchestrated, championed, leveraged, harnessed, pioneered (unless first), revolutionized, transformed (figurative), drove (without an object that can be driven), fostered, cultivated, elevated, empowered, streamlined (without what changed), synergized, architected, catalyzed, facilitated (fine for workshops, vague elsewhere), utilized, operationalized, "played a pivotal role in", "was instrumental in", "responsible for" (a human cliché: it names a duty, not an action), "results-driven", "proven track record", "dynamic", "passionate about", "detail-oriented", "self-starter", "team player", "go-getter", "thought leader".

German: "maßgeblich beteiligt an", "maßgebliche Mitgestaltung", "federführend" (only when true, otherwise F2), "Vorantreiben der ...", "Verantwortung für die ganzheitliche ...", "erfolgreiche Umsetzung" (erfolgreich as filler before every noun), "Implementierung innovativer Lösungen", "Optimierung von Prozessen" (without which process and how), "Sicherstellung", "Gewährleistung", "Begleitung der digitalen Transformation", "nachhaltige Steigerung", "zukunftsorientierte Weiterentwicklung", "leidenschaftlich", "hochmotiviert", "zielorientiert", "lösungsorientiert", "Teamfähigkeit, Belastbarkeit, Flexibilität" (the classic German soft-skill triad, a human cliché long before AI).

## CV-3 Parallel bullets

A CV where every bullet has the same skeleton reads as filled in, not written. The common generated skeleton is "[Strong verb]ed [object], leveraging [tool], resulting in [N]% [improvement]". R7 covers the pattern; in this genre it is set to `extra`.

- Three or more consecutive bullets with the same grammatical skeleton (same opening verb form, same connector, same position of the number) are a finding.
- Three or more bullets ending in "resulting in ...", "which led to ...", "was zu ... führte", or ", wodurch ..." are a finding.
- The fix is to vary the shape (CV-1), not to swap synonyms into the same skeleton.
- Consistent format is not the same as parallel skeletons. Dates, tense, and noun-versus-verb style should stay consistent; sentence shape should not be cloned.

## CV-4 Claim ladders

F2 forbids moving a claim up or down a ladder. These are the CV ladders, lowest first. Copy the rung the source gives.

- Role in work: supported, assisted < contributed to, worked on, was part of the team that < co-developed, co-led, shared responsibility for < led, headed, owned, managed.
- German: unterstützt, mitgearbeitet an, beteiligt an < mitentwickelt, mitverantwortlich für < verantwortlich für < geleitet, federführend, leitend.
- Competitions and awards: participant < nominated, shortlisted < finalist < honourable mention < third, second place < winner, first place. German: Teilnahme < Nominierung < Finale, Finalist:in < Auszeichnung, lobende Erwähnung < 3., 2. Platz < Sieg, 1. Platz, Gewinner:in.
- Publications: in preparation < submitted < under review < revise and resubmit < accepted < in press < published. German: in Vorbereitung < eingereicht < in Begutachtung < angenommen < im Druck < veröffentlicht. A preprint is a preprint.
- Talks: attended < poster < contributed talk < invited talk < keynote. German: Teilnahme < Poster < Vortrag < eingeladener Vortrag < Hauptvortrag.
- Degrees: enrolled < expected (month year) < completed. "M.Sc. (expected 2027)" never becomes "M.Sc.". German: "voraussichtlicher Abschluss 09/2027".
- Funding: applied for < shortlisted < awarded. The amount only when the source gives it.
- Languages: copy the CEFR level (A1 to C2) or the user's own label exactly. "Fließend" does not become "verhandlungssicher"; "B2" does not become "fluent".
- Job titles: copy exactly. "Werkstudent Softwareentwicklung" does not become "Software Engineer"; "Junior" and "Intern" stay.

Upgrade words (en): led | headed | owned | spearheaded | managed | directed | founded | winner | won | first place | published | accepted | invited talk | keynote | awarded | fluent | native | expert | senior | lead | proficient | advanced | extensive | deep expertise
Upgrade words (de): geleitet | leitete | Leitung | federführend | verantwortete | gegründet | Gewinner | Gewinnerin | gewonnen | Sieg | 1. Platz | veröffentlicht | angenommen | eingeladener Vortrag | ausgezeichnet | verhandlungssicher | muttersprachlich | Experte | Expertin | Senior | sicher | fundierte | sehr gute | umfassende

The script flags any of these words that appear in the output but not in the source. The model applies the ladders directly.

## CV-5 Metrics

- A metric needs a unit and a baseline or a comparison, or it means nothing: "40% faster" (than what?), "handled 200 tickets" (per what period?). Flag a metric that lacks one; ask for the missing part.
- Do not round or "improve" numbers. "37%" stays "37%", not "nearly 40%". "Around 300" stays approximate.
- Do not convert units or currencies unless the user asks.
- A range stays a range.
- Vague quantities ("several", "numerous", "zahlreiche") are acceptable when that is all the source knows; do not replace them with numbers.
- A result with no measure at all ("resulting in improved code quality", "enhanced performance", "increased efficiency", "verbesserte Codequalität", "gesteigerte Effizienz") is a claim without evidence. Flag it and ask what changed and how the user knows; offer to cut the result clause if there is no answer.

## CV-6 Summary lines

A summary is optional. Early-career CVs, academic CVs, and most German Lebensläufe do without one. When present:

- One to three lines. Role or field, the level the source supports (years only if given), the domain, and one or two specific proofs from the CV below.
- No adjective stacks (R1), no stock passion (S14), no first-person "I am a..." in English resumes (drop the pronoun), no "Ich bin ..." in German Kurzprofile (write in noun phrases or without subject).
- Test: delete the adjectives. If nothing specific remains, the summary is empty.
- Test: would the summary fit a thousand other applicants? Then it is not doing its job.
- A tailored summary mirrors the posting's top two requirements only where the CV proves them (CV-8).

Example (invented):
- Weak: "Results-driven and passionate data professional with a proven track record of leveraging cutting-edge tools to drive impactful insights."
- Better, if the CV supports it: "Data analyst, four years in hospital logistics. Built the bed-occupancy forecast used by three wards; SQL, Python, Power BI."

## CV-7 Skills section

- Group by kind: languages (spoken), programming languages, tools and platforms, methods, certifications. Keep each group short.
- Name tools exactly as the user does, including versions if given. Do not add a tool the user did not list, even if it is "obviously" used alongside one they did.
- Proficiency: use one scale for the whole section. CEFR for spoken languages; plain words (basic, working, advanced) or years of use for tools. No star ratings, percentage bars, or pie charts: they invite the question "80% of what?" and many applicant tracking systems cannot read graphics.
- Soft skills do not belong in a skills list. Show them in bullets ("ran weekly client calls") or leave them out.
- In German: "Kenntnisse" or "IT-Kenntnisse", "Sprachkenntnisse" with CEFR (Deutsch C2, Englisch C1) or "Muttersprache". "Grundkenntnisse", "gute Kenntnisse", "sehr gute Kenntnisse", "verhandlungssicher", "fließend", "Muttersprache" are the common scale. Copy the user's level.

## CV-8 Tailoring to a posting

Tailoring changes selection, order, and wording. It never changes facts.

1. List the posting's requirements (must-have, nice-to-have) and its terms.
2. Map each requirement to evidence in the user's CV. Mark each as: shown, partly shown, not shown.
3. Reorder: put the most relevant role, project, or bullet first within its section. Reverse-chronological order of roles stays.
4. Select: cut or shorten bullets that support nothing in the posting, if space is tight.
5. Reword to the posting's terms only when the thing is the same thing. "Customer support" may become the posting's "client services" if the work matches. "Python" does not become "Django"; "used Excel" does not become "financial modelling". When unsure, ask.
6. Summary (if any): lead with the two requirements the CV proves best, in the CV's own terms. A summary may not generalize a fact into the posting's wording: "on call for the order system" does not become "on call for production systems", and "moved three services into Docker" does not become "runs containerized services".
7. Report gaps to the user: requirements marked "not shown". Never add them. Suggest what the user could add if it is true ("If you have used Terraform, add where").
8. Keywords appear naturally where true. No keyword blocks, no hidden text, no white-on-white lists. Applicant tracking systems parse plain layouts best: standard headings, one column, text rather than images, dates in one consistent format.

Output of a tailoring request: the tailored CV text or a list of edits, plus the requirement map and the gap list.

## CV-9 Academic CVs

- Longer and complete rather than selective. Two pages is not a limit.
- Usual order (fields vary): contact; current position; education (degree, institution, year, thesis title, advisor if the user lists one); positions; publications; grants and funding; awards and honours; talks and presentations; teaching; supervision; service (reviewing, committees); skills and languages.
- Publications: copy each citation exactly as supplied, in one consistent style. Mark the user's name the way they do (bold is common). Keep the status on the ladder (CV-4). Separate peer-reviewed articles, conference papers, preprints, and other work if the user's list mixes them.
- Talks: keep "invited" only where the source says invited.
- Grants: role (PI, co-PI, participant) and amount only from the source.
- Teaching: course, level, role (lecturer, teaching assistant, tutor), term.
- No achievement bullets with invented impact; academic CVs list facts. A one-line description under a position is fine.
- German academic CVs (wissenschaftlicher Lebenslauf) follow the same logic, usually with a separate Publikationsverzeichnis. Funders and appointment committees often prescribe a format (for example a page limit or a narrative section); use their template when the user names one. Unsure: formats change between funding calls, so tell the user to check the current call text.

## CV-10 English resume, English CV, German Lebenslauf

| Point | US resume | UK and international CV | German Lebenslauf |
|---|---|---|---|
| Length | 1 page early career, 2 pages experienced | 2 pages usual | 1 to 2 pages; up to 3 for long careers |
| Order | Reverse chronological | Reverse chronological | Reverse chronological (tabellarisch, "amerikanisch") is the norm today |
| Photo | No | No | Optional. Many applicants still include one; employers may not require it (the Allgemeines Gleichbehandlungsgesetz, AGG, discourages discriminatory selection). The user decides. |
| Personal data | Name, city, phone, email, links | Same | Name, address or city, phone, email. Date and place of birth, nationality, and marital status are optional and increasingly left out; nationality can matter for work permits. |
| Summary | Common | Common ("personal profile") | Optional ("Kurzprofil"), less common |
| Dates | "Mar 2021 – Jun 2023" or "2021–2023" | Same | "03/2021 – 06/2023" or "seit 10/2023" |
| Headings | Experience, Education, Skills | Same, plus Interests sometimes | Berufserfahrung, Ausbildung or Bildungsweg, Praktika, Kenntnisse, Sprachen, Ehrenamt, Interessen (optional) |
| Pronouns | None | None | None |
| Signature | No | No | Traditionally place, date, signature at the end; now optional and often omitted, especially in online applications |
| School | Omit high school once you have a degree | Same | Schulabschluss (Abitur) usually still listed, briefly |
| References | "Available on request" is outdated; omit | Often omitted | Omit; Arbeitszeugnisse are attached separately if requested |

Where unsure: photo and signature practice varies by industry and region, and advice changed quickly after 2015. Say so, give the options, and let the user choose.

## CV-11 Critique checklist

Run this after the pattern pass. Each "no" is a finding with the CV rule ID.

1. Every number, date, title, employer, degree, grade, and award in the output is in the source, unchanged (F1, CV-5).
2. No claim moved up or down a ladder (F2, CV-4).
3. Each bullet makes one claim and fits in two lines (CV-1).
4. Bullet shapes vary; no cloned skeletons; no run of "resulting in" (CV-3, R7).
5. Verbs are plain and accurate; template verbs appear at most once or twice (CV-2, I4).
6. Metrics have units and baselines, or the gap is flagged (CV-5).
7. The summary, if any, is specific enough that it fits only this person (CV-6).
8. Skills are grouped, use one proficiency scale, and list nothing the user did not (CV-7).
9. Tailoring changed order, selection, and wording only; gaps are reported (CV-8).
10. The document follows the conventions of its type (CV-9, CV-10): length, order, dates, personal data, headings.
11. Date formats, tense, and bullet style are consistent throughout.
12. No placeholders or chat residue remain (F3, C1).
