# Campaign execution plan

## Phase 0: campaign infrastructure

Use `ReproduceICML` as the local parent workspace. Keep the campaign repository, template repository, and independent paper repositories beneath that parent as described in [Repository and workspace architecture](repository-architecture.md).

Build one reusable reproduction harness that every paper can copy:

- deterministic configuration and seed recording;
- command capture through Trackio;
- raw CSV/JSON result writers;
- figure generation from raw data;
- environment and hardware capture;
- SHA-256 artifact manifest generation;
- unit and numerical-consistency tests;
- a compact claim evidence table;
- a final verification command that fails if required artifacts are absent.

Create each paper repository from the shared template, then register its GitHub, Trackio Space, and Hugging Face Bucket URLs in the central campaign repository.

## Phase 1: flagship

Run *Learning Randomized Reductions* end to end.

1. Reproduce Vanilla Bitween locally across all 80 functions.
2. Establish exact inference token and cost budgets.
3. Run agentic and pure-neural conditions with the same backend and budget.
4. Verify identities independently.
5. Add negative controls and failure taxonomy.
6. Publish a full Trackio bundle and obtain the first verdict.
7. Address genuine experimental gaps identified by the judge.

## Phase 2: CPU production line

While hosted inference is running, process theory and classical-ML papers:

1. Read the paper and source material.
2. Copy the exact claims used by `claims.json`.
3. Design one decisive experiment per claim.
4. Reproduce the paper-default setup before extending it.
5. Run several seeds and a claim-relevant parameter sweep.
6. Compare with an independent direct implementation where possible.
7. Publish only after tests and artifact verification pass.

Target cadence after stabilization: two complete full-scale CPU papers each day.

## Required logbook order

1. `00 - Scored claim evidence`: compact table with exact claims, configurations, headline numbers, and artifact links.
2. One page per scored claim.
3. Methods, environment, provenance, and executable commands.
4. Negative controls, limitations, and falsification attempts.
5. Pinned conclusion and complete artifact bundle.

The decisive evidence goes first because the public judge limits the amount of rendered Markdown it reads. Large raw tables belong in linked artifacts, not before the claim summaries.

## Verdict loop

For every publication:

1. Record the submitted commit SHA.
2. Wait for the automated verdict.
3. Save the per-claim evidence explanation.
4. If the result is `toy` or `inconclusive`, determine whether a missing full-scale experiment can be added.
5. Revise only with new evidence, rerun verification, republish, and record the new SHA.
6. Stop investing when the remaining claim needs prohibited compute or would require misrepresenting a proxy as full scale.

## Daily controls

- Refresh the leaderboard and attempted-paper set.
- Re-estimate the points required to finish in the top group.
- Do not start a new paper while an existing result lacks reproducibility artifacts.
- Track verified points per engineering hour and inconclusive causes.
- Reserve hosted inference credit for papers where backend substitution remains full-scale.
- Preserve one daily block for flagship depth and manual-review quality.
