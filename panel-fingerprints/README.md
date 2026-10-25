# Daily panel fingerprints

One line per daily AI answer-panel job run by Citant (citant.ai). Hashes and counts only: no question, answer, rival or client
name is published here.

- `job_sha1`: the first 16 hex characters of a SHA-1 over the job's question list (row, prompt number, prompt text, app). It
  proves which questions were asked. The same questions give the same value on every day.
- `runlog_sha1`: SHA-1 of the job's run log (what was asked, on which app, when, answer length, links, country).
- `answers_sha1`: SHA-1 over the sorted list `row:sha1(answer text)` of every saved answer. Changing one saved answer after the
  day it was committed changes this value.
- The proof of WHEN is the date of the git commit that added the line (GitHub shows it and it cannot be changed after the push).
- `rows_answered` / `rows_total`: answers captured of rows planned in the job that day.

Citant can show the underlying files to anyone who asks and the hashes will match them.
