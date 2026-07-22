# ICMLPapers Campaign Instructions

Read `AGENTS.md` and `AGENTS_SCORE.md` before working on the ICML reproduction
campaign. Follow the text-only Hugging Face publication flow, claim-regression
gate, live-ledger refresh, and GitHub `main`/`master` parity requirement in
those files.

Never expose HF tokens, upload binary artifacts by default, overwrite
unrelated changes, duplicate protected jobs, or state an estimated score as a
judged result.

The live judge scores the Hugging Face Space only; GitHub parity is bookkeeping
and must never block or replace the HF publish. When reading `verdicts.json`,
filter by `space_id` starting with `DineshAI/` before keying by `orid` (orids
collide across agents).
