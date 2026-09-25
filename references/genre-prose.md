# Genre: general prose

Load this file for cover letters and German Anschreiben, motivation letters to research groups, application and outreach emails, LinkedIn posts, blog posts, technical blog posts, documentation, investor and press texts, casual messages, and any other prose that is not a CV or scientific text. It does not repeat any pattern from `patterns.md`. It holds the settings for each prose type and the rules that apply only here. Rule IDs start with `PR-`.

## Prose types

| Column | Covers | Detect by |
|---|---|---|
| `letter` | Cover letters, Anschreiben, motivation letters, Motivationsschreiben | Salutation plus application language ("position", "Stelle", "Bewerbung", "apply") |
| `email` | Application emails, outreach and cold emails, follow-ups, professional replies | Salutation or subject line, short, a request |
| `linkedin` | LinkedIn and other short social posts | Under about 300 words, hashtags or mentions, line-per-sentence layout |
| `blog` | Blog posts, essays, newsletters, opinion pieces, and any prose with no stronger signal | Long-form, headings optional, no code |
| `tech-blog` | Technical blog posts, engineering write-ups | Code blocks, API names, architecture |
| `investor` | Investor updates, fundraising emails, sponsor pitches | Salutation plus investor or funding language |
| `press` | Press releases, announcements, "Pressemitteilung" | Organization name, dateline, quotes from executives, boilerplate "About X" |
| `docs` | Documentation, READMEs, guides, how-tos | Step lists, parameter tables, README structure |
| `casual` | Slack or chat messages, internal notes, quick replies, very short social posts (three sentences or fewer) | Short, informal, no salutation needed |

When the signals are weak, use `blog` for coverage and keep borderline, context-dependent findings as judgment calls. When the chosen type changes a finding, say which type you used and why; the user can override it.

## Settings

An entry not listed is `on`. F1 to F5 are always on. Columns `linkedin`, `blog`, `tech-blog`, `investor`, `docs`, and `casual` carry over the avoid-ai-writing tolerance matrix unchanged; `letter`, `email`, and `press` are new.

| ID | letter | email | linkedin | blog | tech-blog | investor | press | docs | casual | Note |
|----|----|----|----|----|----|----|----|----|----|----|
| R6 | on | on | relaxed | on | on | on | on | relaxed | off | LinkedIn: up to two dashes per post pass. |
| M1 | on | on | relaxed | on | on | on | on | relaxed | off | LinkedIn: a bold hook passes. |
| M2a | on | on | relaxed | on | on | on | on | off | off | LinkedIn: one or two emoji at line ends pass; never mid-sentence. |
| M3a | relaxed | relaxed | off | on | relaxed | on | on | off | off | Lists work on LinkedIn and in docs; technical lists pass in tech-blog. A cover letter may carry two or three bullets. |
| R2a | on | on | on | on | relaxed | on | on | relaxed | off | "May" is often accurate in technical text. |
| I4 | extra | on | on | on | partial | on | on | relaxed | off | tech-blog: see the technical exceptions in I4. casual: only P0 entries apply. |
| I3 | on | on | relaxed | on | on | extra | extra | on | off | Some selling is expected on LinkedIn. |
| I1 | extra | on | on | on | on | extra | extra | relaxed | off | |
| I12 | on | on | off | on | relaxed | on | on | off | off | |
| R8b | relaxed | off | off | on | on | on | on | relaxed | off | Uniform paragraph length. |
| M3b | on | on | relaxed | on | relaxed | on | on | off | off | Numbered-list inflation. |
| S12 | on | on | relaxed | on | on | on | on | on | off | LinkedIn: one question as a hook passes. |
| R4 | on | on | off | on | on | on | on | relaxed | off | |
| I2a | extra | on | off | on | on | extra | extra | off | off | Generic conclusions. |
| M4 | off | off | on | on | on | extra | on | off | off | Hashtags: severity is P2 on blog and tech-blog, where a launch post may stack tags. |
| M3c | on | on | on | on | relaxed | on | on | relaxed | off | Bare noun-phrase bullets; option and parameter lists pass in tech-blog and docs. |
| I4d | on | on | on | on | on | extra | extra | relaxed | off | Tier-3 phrase clustering. |
| I2b | extra | on | on | on | on | extra | extra | off | off | Future-narrative closers. |
| S15 | on | on | on | on | on | on | on | off | relaxed | casual: one endorsement line in a DM passes. |
| R2b | on | on | on | on | relaxed | extra | on | relaxed | off | Hedge-stacked predictions; "could" is often hedged accuracy in tech-blog. |
| I9 | on | on | on | on | on | extra | extra | relaxed | off | |
| I10 | on | on | on | on | relaxed | on | on | relaxed | off | |
| S2 | on | on | on | on | relaxed | on | on | relaxed | off | |
| R10 | relaxed | relaxed | relaxed | on | relaxed | on | on | off | off | Short-form fragments are the LinkedIn register; fragment lists are docs. |
| R11 | relaxed | relaxed | relaxed | relaxed | relaxed | relaxed | relaxed | off | off | stop-slop's blanket adverb rule; `strict` raises it to on. |
| R12 | relaxed | relaxed | relaxed | relaxed | relaxed | relaxed | relaxed | off | off | stop-slop's Wh- and "So" opener rule. |
| S20 | off | off | relaxed | relaxed | relaxed | relaxed | relaxed | off | off | stop-slop's narrator-from-a-distance rule. |
| C1 | relaxed | relaxed | on | on | on | on | on | on | relaxed | Real letters and emails end with courtesy lines; see the C1 guard. |
| C2 | on | extra | on | on | on | on | on | on | relaxed | Cold emails are where flattery asks live. |
| R15 | off | on | off | off | off | on | off | off | on | Wall of text matters only in reply registers. |
| S14 | extra | on | relaxed | on | on | on | on | off | relaxed | "I am thrilled to apply" is the most common letter opener tell. |
| S13 | extra | on | on | on | on | on | on | on | off | "In today's competitive job market". |
| R7 | on | on | on | on | on | on | on | relaxed | off | In letters, a paragraph where every sentence opens with "I" or "Ich" counts. |
| R14 | extra | extra | on | on | on | extra | on | on | off | Letters and emails have no room for restatement. |

## PR-1 Cover letters (English)

Structure, for about 250 to 400 words on one page:

1. **Opening (2 to 3 sentences).** The role, and one specific reason this person wants this job at this organization. The reason comes from the user. If the user has not given one, write `[NEED: why this role and this organization, in your words]` in Draft and Rewrite mode, or flag its absence in Critique. Never invent enthusiasm for a product, mission, or person, and never build a reason out of CV facts ("because it combines my studies with my practice").
2. **Evidence (1 or 2 paragraphs).** Two or three of the posting's requirements, each matched to something the user has done (from the CV or source). One concrete example beats a list of adjectives.
3. **Logistics (1 to 2 sentences, only what applies).** Start date, notice period, relocation, work authorization, salary expectation when the posting asks for it. All from the user.
4. **Closing (1 to 2 sentences).** The next step, stated plainly. No pleading, no over-thanking.
5. Sign-off and name.

If the user has not supplied a reason, the opening is exactly: `[NEED: why this role and this organization, in your words]` plus one plain sentence naming the role. No sentence about what sparked or drew the writer's interest.

Openings to avoid:
- Human clichés (flag as filler, not as AI tells): "I am writing to express my interest in", "Please accept this letter as my application for", "I believe I am the ideal candidate".
- Template openings: "I am thrilled to submit my application for the esteemed position of", "Your company's commitment to innovation resonates deeply with me", "As a passionate and results-driven professional" (S14, I4, I3).

Closings to avoid: "I am confident that I would be a valuable asset to your team" (I2a), "Thank you for considering my application. I look forward to the opportunity to discuss how my skills align with your needs" (a stack of formulas; one plain line is enough).

## PR-2 Anschreiben (German)

Layout follows DIN 5008 in most German applications. Details below reflect common practice; the 2020 revision of the standard changed some spacing and field rules, so for exact measurements the user should check a current template.

1. **Absender:** Name, address, phone, email (often as a header matching the CV).
2. **Empfänger:** Organization, person if known, address. "z. Hd." is outdated.
3. **Ort und Datum**, right-aligned: "Berlin, 25. September 2026" or "25.09.2026".
4. **Betreff** without the word "Betreff", often bold: "Bewerbung als Datenanalyst (Kennziffer 26-114)". The reference number only from the user or the posting.
5. **Anrede:** "Sehr geehrte Frau Dr. Keller," or "Sehr geehrter Herr Yilmaz,". Keep academic titles. If no name is known: "Sehr geehrte Damen und Herren," still works, but a name is better; "Guten Tag Alex Keller," is a neutral form when the gender is unknown. After the comma the first sentence starts with a lowercase letter unless it begins with a noun.
6. **Einleitung:** Why this position and this organization, specifically, in the user's words. If the user has not supplied a reason, the Einleitung is exactly two parts: `[NEED: was Sie an dieser Stelle oder an <Organisation> konkret anspricht]` and one plain application sentence ("Ich bewerbe mich um die Stelle als ... (Kennziffer ...)."). No sentence about interest, motivation, or what "geweckt" the interest. Avoid "hiermit bewerbe ich mich" and "mit großem Interesse habe ich Ihre Stellenanzeige gelesen": career advisors have discouraged these human clichés for decades. They are filler, not AI tells, and the critique should say so.
7. **Hauptteil:** Two or three requirements from the posting, each matched to evidence from the Lebenslauf. Not every sentence starts with "Ich" (R7), but do not contort sentences to avoid it.
8. **Schluss:** Eintrittstermin or Kündigungsfrist, Gehaltsvorstellung if the posting asks (as Bruttojahresgehalt, number only from the user), and the wish for an interview. "Ich freue mich auf ein persönliches Gespräch." and "Über eine Einladung zu einem Vorstellungsgespräch würde ich mich freuen." are both acceptable. Some advisors call the Konjunktiv hesitant; this is a matter of taste, not a finding.
9. **Grußformel:** "Mit freundlichen Grüßen", with no comma or period after it, then the signature and printed name.
10. **Anlagen** line: optional; often omitted in online applications.

One page. Same font and header as the Lebenslauf. Many employers now accept or prefer applications without an Anschreiben, or a short cover email instead; if the posting says so, follow it.

German template phrases in Anschreiben (flag under the entries named): "Mit großer Begeisterung habe ich ..." (S14), "Ihre Stellenausschreibung hat mich sofort angesprochen" (S14), "passt perfekt zu meinem Profil" (I1), "Ich bin fest davon überzeugt, dass ich mit meiner Expertise einen wertvollen Beitrag leisten kann" (I2a, R18), "Darüber hinaus ..." at the start of every paragraph (R4), "Teamfähigkeit, Belastbarkeit und Kommunikationsstärke" (R1, CV-2), "eine spannende Herausforderung in einem dynamischen Umfeld" (I4), "nicht nur fachlich, sondern auch menschlich" (S1).

## PR-3 Motivation letters to research groups

Usually an email of 150 to 300 words with a CV attached; sometimes a formal letter for a scholarship or graduate program (then use PR-1 or PR-2 structure).

- **Who you are:** degree, institution, status (for example "finishing my M.Sc. in September 2026"). From the user.
- **Why this group:** one specific piece of the group's work (a paper, dataset, method, project) and what about it connects to the user's interest or question. This must come from the user. Without it, write `[NEED: which of the group's papers or projects, and what about it]`. Never pick a paper yourself and never describe its content beyond what the user says.
- **What you bring:** one or two concrete things the user has done that relate.
- **What you ask:** an open position, a PhD place, a research stay, a conversation; and the funding situation (own scholarship, applying to an advertised position, looking for funding). From the user.
- **Attachments and availability.**

Avoid: "your groundbreaking work" (I3), summarizing the group's paper back to them at length (C2, recap flattery), "I have always been fascinated by" (S14), claims to have read "all" of the group's work.

German address forms: "Sehr geehrte Frau Professorin Keller," or "Sehr geehrte Frau Prof. Dr. Keller," are both used. Many German PhD positions are funded posts advertised with a pay grade; name the grade only if the user gives it.

## PR-4 Emails

- **Subject line:** specific: "Application: research assistant, ref. 24-17", "Question about your 2025 dataset license". Not "Hello" or "Inquiry".
- **First two lines carry the ask.** Context after, and only as much as the reader needs.
- **One ask per email.** A second ask goes in a second email or a clearly separate line.
- **Short.** Most professional emails fit in 150 words. Long context goes in an attachment.
- **Attachments named** in the text.
- **Closing:** the next step and a plain sign-off.
- **Follow-ups:** after about a week, two or three lines, referencing the first email.
- **Cold outreach:** why this person, why now, what exactly you want, and how small the ask is. A flattery ask ("I'd love your perspective") with no question is C2.
- German register: "Sehr geehrte Frau ..." for first contact in formal settings; "Hallo Frau ..." is accepted in many industries and startups; "Liebe Frau ..." once a relationship exists. "Mit freundlichen Grüßen" (formal), "Viele Grüße" or "Beste Grüße" (neutral). "LG" and "Liebe Grüße" never in applications. "Gerne sende ich Ihnen weitere Unterlagen" is normal polite German, not chat residue.
- "I hope this email finds you well" and "Ich hoffe, diese Nachricht erreicht Sie wohlauf" are clichés. The German one is also listed by German Wikipedia as a sign of generated text, because it is a word-for-word translation of the English formula. In a warm email between people who know each other, the English one can pass.

## PR-5 LinkedIn and short social posts

- **The first line carries the news or the point.** Not "I'm thrilled to announce", "Ich freue mich riesig, ...", or a question hook. Those openers are human clichés on LinkedIn and also generated defaults (S14). Relax them only if the user's voice sample uses them.
- **One point per post.** A second point is a second post.
- **Specifics from the user:** what happened, who (only people the user names), what number (only from the user).
- Line breaks between thoughts are the register; fragments are relaxed here.
- Hashtags: three or fewer, specific (M4).
- No engagement bait at the end ("Agree?", "What do you think? 👇", "Thoughts?"); a real question to a real audience can stay (S12).
- Tag or thank people only as the user says.
- German LinkedIn: "du" is common in some communities, "Sie" in others; match the user. "Spannend" is overused; one per post is enough.
- Share posts: say why the linked item matters, from the user's reason; no endorsement closer (S15).

## PR-6 Blog posts and essays

- The title makes the claim or names the topic plainly.
- The point arrives by the second paragraph.
- Examples are specific and from the user's material.
- Headings in sentence case (English), and only when the post is long enough to need them (M2, M3).
- Paragraphs build: each one should need the one before it (R13).
- End on the last useful point. No "In conclusion", no send-off (R5, I2).
- Link or name sources for factual claims when the user supplies them.
- Keep the writer's opinions, uncertainty, humor, asides, and specific odd details (R16). Removing tells is half the job; the result must still sound like the person.

## PR-7 Technical blog posts and documentation

- Clarity over voice. Plain copulas ("X is Y"). Imperative mood for instructions.
- Technical terms stay when accurate: "robust", "comprehensive", "seamless", "ecosystem", "leverage" (for real platform leverage), "facilitate", "underpin", "streamline", and "harness" in "test harness" have technical senses (I4 exceptions).
- Lists, tables, and code blocks where the content is list-shaped.
- Describe the current behavior, not the change history, except in changelogs, release notes, and migration guides (C7).

## PR-8 Investor updates and press releases

- Tighten everything. Promotional language and significance inflation are the biggest risks (I3, I1 `extra`).
- Numbers only from the user, with period and comparison ("MRR rose from 41k to 48k EUR between June and August").
- One unsupported "thriving ecosystem" can undermine an investor email.
- Press releases: dateline, what happened, who, when, where, one quote only if the user supplies it (never write a quote for a real person), boilerplate from the user.

## PR-9 Tests for any prose

Run the tests that fit the type. Each failure is a finding with the test's ID.

- **PR-9a Swap test:** replace the organization's name with a competitor's. If the paragraph still works, it is generic.
- **PR-9b Applicant swap:** replace the writer's name with another applicant's. If the paragraph is still true, it says nothing about this writer.
- **PR-9c Delete test:** delete the adjectives and adverbs. If no claim remains, there was none.
- **PR-9d Evidence test:** every claim the writer makes about themselves points to something in the CV or source.
- **PR-9e So-what test:** after each paragraph, the reader can say what they learned.
- **PR-9f Read-aloud test:** would the writer say this to the recipient in person? Text that could be read by a text-to-speech engine without sounding odd is probably too uniform (R8).
- **PR-9g Reshuffle test:** if two body paragraphs can swap places without loss, the piece is a list, not an argument (R13).
- **PR-9h Ten-second test (emails):** the recipient can tell in ten seconds what is being asked.
- **PR-9i First-line test (posts):** the first line carries the news.

## PR-10 Critique checklist

1. Every name, number, date, title, and experience is in the source (F1); no claim moved up or down (F2).
2. The type's structure is present: PR-1 or PR-2 for letters, PR-3 for research-group letters, PR-4 for emails, PR-5 to PR-8 for the rest.
3. The opening is specific to this recipient (PR-9a) and this writer (PR-9b).
4. Each claim about the writer has evidence (PR-9d).
5. Logistics the posting asks for are present, from the user, or flagged as `[NEED: ...]`.
6. The closing states the next step without formulas.
7. Register and address forms are consistent (G4 for German).
8. The German Anschreiben follows DIN 5008 conventions, or the user has chosen otherwise: no "Betreff:" label, comma after the Anrede and lowercase continuation, no comma or period after "Mit freundlichen Grüßen" (G4). Check the input's closing, not only the rewrite's.
9. No chat residue, placeholders, or invented quotes (C1, F3, F1).
10. The writer's voice survives: sentence length, word choice, punctuation, and any voice sample.
