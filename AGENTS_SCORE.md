# ICML Reproduction Campaign Runbook

This file is the durable operating guide for score-improvement work in this
repository. Read it before selecting a paper, changing a claim, or publishing
to Hugging Face.

## Non-negotiable release gates

1. Work only on papers already recorded in the campaign control plane. Do not
   intake a new paper, duplicate a protected process/job, or cancel a running
   job without explicit user direction.
2. Preserve the current judged score. Before publishing, compare the candidate
   logbook/claims with the last judged revision. Every already-earned claim
   must still be present and supported. A new claim must be additive, exact,
   and backed by a deterministic verifier.
3. Record each paper in `DINESHAI_SCORE_LEDGER.md` with work status, estimated
   new score, Git sync SHA, and whether the judge has finished. Refresh live
   verdict data instead of relying on historical totals. When refreshing, filter
   `verdicts.json` by `space_id` starting with `DineshAI/` before keying by
   `orid` — orids collide across agents — and de-dupe by orid. Use
   `refresh_ledger.py`, which does this.
4. Every successful Hugging Face publication must be mirrored in GitHub on
   `main` or `master` in a normal, non-force push. Stage only the evidence and
   status files within scope; never add unrelated dirty or untracked files. The
   live judge scores the HF Space only; GitHub parity is bookkeeping and must
   never block, precede, or substitute for the HF publish.
5. Do not claim a score increase until the live judge has evaluated the new
   HF HEAD. Until then, say `awaiting judge` and retain the old judged score as
   the baseline.

## Reading source papers

- Prefer ar5iv HTML: `https://ar5iv.org/abs/<arxiv_id>` (or
  `https://ar5iv.labs.arxiv.org/html/<arxiv_id>`). It preserves theorem
  numbering, inline mathematics, and exact claim wording.
- Next use native arXiv HTML: `https://arxiv.org/html/<arxiv_id>`. The abstract
  page is `https://arxiv.org/abs/<arxiv_id>`.
- Use PDF only when needed: `https://arxiv.org/pdf/<arxiv_id>`, parsed with
  `pdftotext`, `pypdf`, or `pdfplumber`.
- Fetching arXiv/ar5iv is an outbound request. Record the source URL/scope used
  for each claim audit.

## Hugging Face publication: text-only commit API

Do not use raw Git, Git LFS, or binary artifact uploads for a reproduction
publication. The reliable path is a small text-only Hub commit:

```python
from huggingface_hub import HfApi, snapshot_download, get_token

repo = "DineshAI/<orid>"
token = get_token()
api = HfApi()
snapshot_download(repo, repo_type="space", local_dir=work_dir, token=token)

# Write/update only deterministic text evidence in work_dir.
api.upload_folder(
    repo_id=repo,
    repo_type="space",
    folder_path=work_dir,
    allow_patterns=[
        "logbook.json",
        "repro/src/<script>.py",
        "pages/<slug>/page.md",
    ],
    token=token,
    commit_message="...",
)
```

Use this interpreter for HF work (it has `huggingface_hub==1.24.0` and the
correct cached login):

```bash
VENV=/Users/dineshjinjala/Documents/AllCode/ICMLPapers/papers/icml26-repro-YPXDQkU7XW-nd-rope/.venv/bin/python3
"$VENV" -c 'import huggingface_hub; print(huggingface_hub.__version__)'
```

Pass the cached token explicitly with `get_token()` or `token=...`; never print
or write the token to a file, shell history, remote URL, or log. Keep
`HF_HUB_DISABLE_IMPLICIT_TOKEN=1` when using an explicit token. For a
text-only commit, set `HF_HUB_DISABLE_XET=1` as a defensive safeguard.

Large/binary files can trigger preupload, LFS, Xet, or bucket-token flows and
may return 401 even when metadata reads and `whoami` show `write`. Do not use
that route for reproducibility evidence: upload the deterministic Python
regenerator, Markdown explanation, and logbook instead. If binaries are
unavoidably required, obtain explicit direction before trying a classic LFS
fallback or changing token scope.

## HF release verification

After every Hub commit:

1. Confirm `HfApi().whoami(token=token)` identifies `DineshAI` with write role.
2. Record `HfApi().repo_info(..., repo_type="space", token=token).sha`.
3. Download every published path from that exact revision using
   `hf_hub_download(..., revision=sha, force_download=True)` and compare bytes
   or SHA-256 with the staged file.
4. Re-refresh the score ledger. The new HF SHA should differ from the judged
   SHA and the paper should read `awaiting judge` until verdict completion.
5. Mirror the exact published text paths and their source/status record to the
   paper's GitHub repository, then verify `git ls-remote` for `main`/`master`.

## Claim and score-regression check

Before publish, make a machine-readable comparison between the prior judged
revision and candidate revision:

- claim IDs, labels, statuses, and evidence references;
- all existing awarded claims remain unchanged or are strengthened;
- any new claim is scoped to the actual benchmark and does not overstate a
  failed or guarded experiment;
- verifier inputs, expected result, and source hashes are documented;
- logbook JSON remains valid and its rendered page references the evidence.

If a comparison is incomplete, do not publish a claim change. Keep the paper
at its current scored baseline, state the unknown explicitly, and repair the
evidence first.

## Git discipline

- Read status/diff before changing anything; preserve unrelated user changes.
- Commit only when the user explicitly asks to commit/push. For this campaign,
  an explicit instruction to keep HF and Git in sync authorizes the matching
  scoped Git commit and push.
- Check the branch for a Jira key and include it in the commit message when
  present. Never add vendor/tool signatures or co-author lines.
- Do not force-push, reset hard, or modify the campaign control-plane checkout
  merely to publish one paper's evidence.

