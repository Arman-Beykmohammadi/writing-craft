# Activation tests

The skill's `description` field decides whether Claude loads the skill. These prompts check that it loads for writing work in its three genres, in both languages and all modes, including casual phrasings that never mention AI, and that it stays out of unrelated work.

How they were run, and the limits of that run, are in `tests/results.md`. Real activation happens inside Claude chat, Claude Code, and the desktop app, and depends on which other skills a user has installed; a simulation cannot prove it.

## Should activate

| # | Prompt | Genre · language · mode |
|---|---|---|
| A1 | can you look over my cover letter? | prose · en · critique |
| A2 | make this abstract tighter | science · en · rewrite |
| A3 | Kannst du mein Anschreiben überarbeiten? | prose · de · rewrite |
| A4 | Here's my resume, what would you change? | cv · en · critique |
| A5 | Tailor my CV to this job ad | cv · en · tailoring (draft) |
| A6 | Schreib mir einen Lebenslauf aus diesen Stichpunkten | cv · de · draft |
| A7 | Does this LinkedIn post sound like it was written by AI? | prose · en · critique |
| A8 | Help me respond to reviewer 2's comments | science · en · draft |
| A9 | Write the related work section from these paper notes | science · en · draft |
| A10 | Check my methods section for clarity | science · en · critique |
| A11 | Bitte prüfe die Einleitung meiner Bachelorarbeit | science · de · critique |
| A12 | Kannst du meinen Lebenslauf in einen amerikanischen Resume umbauen? | cv · de→en · rewrite |
| A13 | Draft an email to a professor asking about PhD openings, here are my notes | prose · en · draft |
| A14 | Humanize this blog post | prose · en · rewrite |
| A15 | Just flag the AI tells in this paragraph, don't change it | prose · en · detect |
| A16 | Score this draft on directness and rhythm | prose · en · score |
| A17 | Clean up the prose in docs/intro.md in place | prose · en · edit in place |
| A18 | Did my edit change any numbers or links compared to the original? | any · verify |
| A19 | Improve the summary line at the top of my CV | cv · en · rewrite |
| A20 | Mein LinkedIn-Post klingt so steif – was kann ich besser machen? | prose · de · critique |
| A21 | Write a figure caption for this plot description | science · en · draft |
| A22 | Can you make the aims in my grant proposal more concrete? | science · en · rewrite |
| A23 | I'm reviewing a manuscript for a journal, help me structure my review comments | science · en · draft |
| A24 | Rewrite this in my voice, here are three of my old emails | prose · en · rewrite with voice sample |
| A25 | Formuliere aus diesen Stichpunkten ein Motivationsschreiben für ein Stipendium | prose · de · draft |

## Should not activate

| # | Prompt | Why not |
|---|---|---|
| N1 | Fix this Python error: TypeError: 'NoneType' object is not subscriptable | code |
| N2 | Summarize this article in three bullet points | summarizing |
| N3 | Translate this sentence into German: The meeting is at 3. | plain translation |
| N4 | What's the capital of Australia? | general knowledge |
| N5 | Write a SQL query that counts orders per customer | code |
| N6 | Refactor this TypeScript function | code |
| N7 | Convert this CSV to JSON | data |
| N8 | Explain how transformers work in machine learning | explanation |
| N9 | Check this contract for legal risks | legal review |
| N10 | Is this statistic right? 40% of Germans work from home | fact-checking |
| N11 | Make a slide deck about our Q3 results | slides |
| N12 | Wie spät ist es gerade in Tokio? | general knowledge |
| N13 | Write a poem about autumn | poetry, not in the skill's genres |
| N14 | Generate a regex that matches email addresses | code |
