# ICMLPapers Agent Instructions

Before any campaign action, read [AGENTS_SCORE.md](AGENTS_SCORE.md). It is the
authoritative release, claims, Hugging Face, Git-parity, paper-source, and
score-ledger runbook.

In addition:

- Read the paper's current files and live ledger row before editing.
- Keep work scoped to an existing recorded paper/process; preserve unrelated
  user changes and protected jobs.
- Use ar5iv HTML first for exact paper claims.
- Publish HF evidence only through the text-only commit API, then verify the
  exact new revision and mirror it to GitHub `main`/`master`.
- The live judge scores the Hugging Face Space only. GitHub `main`/`master`
  parity is bookkeeping: it never affects the score and must never block,
  precede, or substitute for the HF publish. Publish and verify on HF first,
  then mirror.
- Never permit a claim update to remove or weaken an already-earned claim.
- Do not commit unless the user has authorized it; stage only scoped files.

## Known failure modes — prevent recurrence

### Hugging Face client and auth

- Do **not** use bare `python3` for Hub work in this repository. It may not
  have `huggingface_hub` installed or may use a different cache. Use the
  dedicated YPXD venv documented in `AGENTS_SCORE.md`.
- `HfApi().token` can be empty even when `hf auth whoami` is logged in. Use
  `get_token()` and pass `token=token` explicitly to `whoami`, downloads,
  `repo_info`, and uploads. Never print the token.
- A metadata GET/`whoami` with write role does **not** prove the LFS/Xet bucket
  write route works. A 401 from preupload/bucket/Trackio artifact publishing is
  a separate binary-write-path failure, not evidence that text commits cannot
  work.
- Avoid Trackio publishing for this evidence path when it attempts artifact or
  bucket writes. Use `snapshot_download` followed by `upload_folder` with an
  explicit text-only allowlist and `HF_HUB_DISABLE_XET=1`.
- `HF_HUB_DISABLE_IMPLICIT_TOKEN=1` is set here, so bare CLIs (`hf jobs list`,
  `hf ...`) send **no** token and return 401 ("Invalid username or password") —
  that is a missing-token error, not a credential or scope failure. For
  read-only queries use the venv Python API with an explicit token, e.g.
  `HfApi().list_jobs(namespace="DineshAI", status=["RUNNING","SCHEDULING"], token=get_token())`.
  If the CLI is unavoidable, prefix `env -u HF_HUB_DISABLE_IMPLICIT_TOKEN` and
  call the **venv** `hf` binary; never pass `--token` (it leaks into shell
  history).

### Claims and logbooks

- Never overwrite the Space root `logbook.json` with a generated
  `.trackio/logbook/logbook.json` without a structural comparison. It can have
  a different page tree and silently un-link prior judged evidence.
- Before each claim publication, compare the candidate with the last judged HF
  revision: prior page-tree nodes/files must be a subset of the new revision;
  existing claims and evidence paths must remain reachable; additions must be
  additive only.
- Verify the final revision, not an intermediate commit. Download the exact
  final `logbook.json`, evidence Markdown, and verifiers by revision, then
  check that the old Space file set is a subset of the final file set.
- If a regression is found before judging, restore the judged logbook tree and
  append the new page node; upload only the repaired `logbook.json`.

### Score and Git release state

- A new HF HEAD is **not** a new score. Keep the last judged score as the
  baseline, mark the paper `awaiting judge`, and never promise an estimate.
- When reading `verdicts.json`, filter entries by `space_id` starting with
  `DineshAI/` **before** keying by `orid`. Orids collide across agents, so an
  orid-only lookup returns another agent's score. Regenerate with
  `refresh_ledger.py`, which filters and de-dupes by orid. Never create a
  second Space for an existing orid (a duplicate double-counts the board).
- Mirror every exact HF text path to GitHub `main`/`master`, including
  `logbook.json` and any `pages/<slug>/page.md`. Confirm the remote SHA with
  `git ls-remote`; do not rely only on local push output.
- Do not stage untracked directories merely to make a worktree look clean.
  Inspect and preserve them unless they are explicitly in scope.
