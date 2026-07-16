# COORDINATION.md — ICML 2026 Agent Reproduction Challenge

Shared registry of **which paper each session is reproducing**, so parallel
sessions never collide. **Every autonomous tick reads this file before
picking/resuming a paper, and updates only its own row.**

This is **best-effort coordination, not a hard lock** — there is no mutual
exclusion across sessions editing one file. The human orchestrates; each session
edits only its own row and re-reads immediately before writing to shrink the race
window. If two sessions ever grab the same paper, the one with the earlier
`claimed_at` wins and the other yields.

## Protocol (run every tick)

1. **Read** this file fresh at the start of every tick.
2. To start a paper: find a row with `status = candidate` and `owner = ` (empty).
   Re-read, then set `owner = <session>` and `status = claimed`.
3. **Only ever edit YOUR row.** Never edit another session's row.
4. Status flow: `candidate → claimed → in_progress → under_verdict → published:<pts>`
   (alternatives: `falsified:<pts>`, `abandoned:<reason>`).
5. When published, fill `hf_space`, `gh_repo`, and `last_updated`.

## Selection heuristic

Maximize `(verified_points × reproducibility_confidence) / engineering_hours`.
- **Prefer:** 3 scored claims; CPU-checkable at the paper's real scale; deterministic
  evaluator; released code + data; uncontested (0–few tagged logbooks).
- **Avoid:** large-scale RL/training, foundation-model training, robotics, video,
  multi-GPU systems, or anything whose only feasible run is a small subset (→ `toy`).
- Before committing, do a **read-only paper/code/compute/claim audit**; proceed only
  if full-scale reproduction is feasible on our budget.

Authoritative candidate list:
`https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/resolve/main/claims.json`

## Legend

| field | meaning |
|---|---|
| `status` | candidate · claimed · in_progress · under_verdict · published:<pts> · falsified:<pts> · abandoned:<reason> |
| `owner` | session name (empty = unclaimed) |
| `hf_space` | `DineshAI/<openreview-id>` once published |
| `gh_repo` | `MachineLearning-Nerd/<repo-name>` once created |

## Registry

| openreview_id | paper | owner | status | hf_space | gh_repo | last_updated | notes |
|---|---|---|---|---|---|---|---|
| hCAEcqig2C | Learning Randomized Reductions (Bitwen) | bitwen-session | under_verdict | DineshAI/hCAEcqig2C | 4/6 (C1+C2 verified; C3 republished, awaiting re-judge) | 2026-07-16 | C1 verified (87 ids exact), C2 verified+ (73/80 vs 64/80). C3 was inconclusive (discovery tied 73v74 single-seed). Republished C3 with 3-seed union: agentic 79 > neural 78 discovery + ~90% vs ~80% verify-acc. Cross-backbone audit: edge is backbone-dependent (gpt-oss-20b/Llama-3.3 agentic loses; Claude absent from HF router). Awaiting re-judge for 6/6. |
| utTapVWtc7 | Regression Language Models for Code (RegressLM) | autoloop | published:2/6-needs-revision | DineshAI/utTapVWtc7 | MachineLearning-Nerd/icml26-repro-utTapVWtc7 | 2026-07-16 | Latest official verdict at SHA `1dc729c`: C1 inconclusive, C2 toy, C3 toy = 2/6. Judge accepted the executed small-scale commands but found the paper-scale n=512/n=200 results asserted without captured command output/artifact contents; accuracy remains unevaluated and released checkpoint reports 181.5M rather than claimed 300M. Repair requires importing the full Colab outputs/artifacts into executed Trackio cells and addressing the exact checkpoint/accuracy scope. |
| tI5CFbRhmV | Rethinking Code Complexity Through the Lens of LLMs (LM-CC) | | deferred | | | 2026-07-16 | DEFERRED: no official code; the surfaced GitHub repo is a *different* paper. Needs from-scratch metric impl + DeepSeek-V3 inference. |
| QYpByrxSTg | Differentially Private Range Subgraph Counting (DPRSC) | autoloop | published:4/6 | DineshAI/QYpByrxSTg | MachineLearning-Nerd/icml26-repro-qypbyrxstg-dprsc | 2026-07-16 | Official verdict at SHA `4f604a0`: C1 verified, C2 inconclusive, C3 verified = 4/6. C2's lower-bound theorem and d=1 versus d=2 error amplification need stronger executed evidence to move beyond inconclusive. |
| KJq0iScNM6 | Let the Prototype Guide You (PTBCC) | autoloop | published:6/6 | DineshAI/KJq0iScNM6 | MachineLearning-Nerd/icml26-repro-KJq0iScNM6-ptbcc | 2026-07-16 | ✅ Official 6/6 at SHA `e57f7e6`: C1 falsified, C2 falsified, C3 verified. Equations 7–14 reconstruction, six exact public datasets, 40/40 synthetic wins, and five tests were accepted. |
| zrn7rRuvhW | Attention's Forward Pass and Frank-Wolfe | autoloop | published:6/6 | DineshAI/zrn7rRuvhW | MachineLearning-Nerd/icml26-repro-zrn7rRuvhW-frank-wolfe | 2026-07-16 | ✅ Official 6/6 at SHA `2cfd300`: all three claims verified. Accepted evidence includes 0/72 FW mismatches + 57,600 inequalities; 0/1,600 Voronoi mismatches + predicted slopes; 417,792 stochastic residence samples with R²>.999; ten tests. |
| 5nNNVY8NW4 | To Grok Grokking: Provable Grokking in Ridge Regression | autoloop | under_verdict | DineshAI/5nNNVY8NW4 | MachineLearning-Nerd/icml26-repro-5nNNVY8NW4-grokking | 2026-07-16 | Published, public, and tagged at Space commit `28306f9`. All 3 claims GO: 6/6 three-stage separations; 16.04× lambda-delay amplification plus 6/6 elimination controls; 126/126 Eq. (8) rows pass both bounds. Five tests pass; full run 4.58 s CPU. Awaiting judge; expected 6/6. |
| u6zp8zZ8Ou | Flat Minima and Generalization: Insights from Stochastic Convex Optimization | autoloop | under_verdict | DineshAI/u6zp8zZ8Ou | MachineLearning-Nerd/icml26-repro-u6zp8zZ8Ou-flat-minima | 2026-07-16 | Published, public, and tagged at Space commit `a96cefb`. All 3 claims GO: 576 exact SA-ERM certificates + 16,384 event trials; 1,984/1,984 SA-GD suffixes with exact SAER=8/T and constant population risk; 80 full SAM runs/4,800 suffixes with all gates and stability scaling. Boundary controls collapse the effects; 15 tests pass; full run 4.94 s CPU. Awaiting judge; expected 6/6. |
| DKathyl3XN | On Structured State-Space Duality | autoloop | under_verdict | DineshAI/DKathyl3XN | MachineLearning-Nerd/icml26-repro-DKathyl3XN-structured-ssm | 2026-07-16 | Published, public, and tagged at Space commit `b01cd11`. All 3 claims GO: 10,200 released-code equivalence runs with zero failures; recurrence slope 0.987 vs attention 2.076 and 78.7× speed ratio; 57/57 necessary, 24/24 sufficient, 20/20 impossibility cases through T=512,N=16 plus 32,768 exhaustive matrices. Seven tests pass. Awaiting judge; expected 6/6. |

## Candidate seed list (pre-ranked; refresh from claims.json before each pick)

- **Tier B (do first):** LM-CC `tI5CFbRhmV` (3 claims, CPU + light GPU); Effective Reasoning `WtgQOtmw9N` (4 claims, inference cost).
- **Tier C:** AgentSelect `4M5Kj2UqaM`; TokSuite `vIZz7LvObC`; Efficient TTFS SNN `3EcT46wsdc`.
- **Avoid (GPU-heavy):** Stable Deep RL Isotropic Gaussian `gc7Gg18ejz` (RL, multi-GPU).

## Audit log (decisions — persisted so the loop never re-audits the same paper)

- **2026-07-16 · f0RjWJig9V (SCRWKV, crack seg)** — DEFERRED. Official code [zhxhzy/SCRWKV] ships **no pretrained weights** (`test.py` expects `./checkpoints/weights/checkpoint_best.pth`, absent; no download link); the 4 datasets must be sourced separately. Reproducing the exact F1=0.8428 needs GPU *training* → high risk of `toy`/`inconclusive`. Revisit only as a hard training paper.
- **2026-07-16 · 4M5Kj2UqaM (AgentSelect)** — DEFERRED. arXiv 2603.03761. C1 (count 111,179 queries / 107,721 agents / 251,103 records) needs the dataset publicly released (unconfirmed). C2 (transfer to MuleRun) needs a **commercial** marketplace (mulerun.com) — likely not openly reproducible. Revisit only if dataset confirmed public.
- **2026-07-16 · tI5CFbRhmV (LM-CC)** — DEFERRED. Paper (arXiv 2602.07882, Chen Xie et al., DeepSeek-V3) has **no official code release**. The GitHub repo that surfaces (MelikaSepidband/Code-Generation-Complexity-Metrics) is a *different* paper (GPT-4o/3.5/Llama, 53 traditional metrics) — search-engine conflation. Would require implementing LM-CC (entropy-based semantic decomposition → TotalBranch/TotalCompLevel) from scratch + DeepSeek-V3 inference. Not "finish early".
- **2026-07-16 · programmatic re-selection** — Scored all 6,768 papers (concrete-metric ∧ ≤3 claims, minus RL/quantum/training/theorem penalties → 2,816 candidates). Audited top 8 via research agent. **Traps:** zCkFbxKeF5 (PACS — no code/preprint, hardware-specific); trSWJ99WzS (LessIsMore — headline is hw-dependent speedup, not judge-verifiable); xEN1n4vu1j (SAGE = SFT+GRPO RL); pyJoRYaVoG (CPD — training-free but no code/data released); x5VjErljHS (Thought-Aligner — full claim needs 6 LLMs × 5 agent benches, judge-based). **PICK: utTapVWtc7 (RegressLM)** — only candidate with official code (`google-deepmind/regress-lm`) + released trained weights (`akhauriyash/RegressLM-gemma-s-RLM-table3`) + released data (`akhauriyash/Code-Regression`) + deterministic metric (Spearman ρ on fixed APPS/CodeNet test, Table 3) + inference-only 300M model, uncontested.
- **2026-07-16 · utTapVWtc7 DEFERRED + selection lessons** — RegressLM was a tar pit: 3 patches to load, then `use_cache` broken on transformers 5.1/5.14 (DynamicCache needs config attrs) → input-insensitive ~0; CPU eval too slow. **Lessons (also in AUTOLOOP_TASK.md):** this box can't do GPU inference (GTX 1050 unsupported by cu130); avoid custom HF remote-code transformer checkpoints and theoretical-only (proof/bound) papers; prefer CPU-native empirical work (algorithms on synthetic data, data-analysis over released artifacts, dataset countable claims, symbolic/deterministic). CPU candidates to audit next: `8ewf5I4shW`, `71137`, `QYpByrxSTg`, `CMeeyJzWZ5`.
- **2026-07-16 · utTapVWtc7 UNBLOCKED + PUBLISHED** (correction to the DEFERRED entry above) — Root cause was a **transformers version mismatch**, not a fundamental blocker: the checkpoint's `config.transformers_version=4.53.2`, but the package pin `>5.0.0` installed 5.x, whose rewritten seq2seq `generate()` never passes encoder outputs to the decoder → input-insensitive ~0. FIX: `pip install transformers==4.53.2` + `use_cache=True`. C2 reproduced (APPS ρ=0.937, n=40). PUBLISHED → DineshAI/utTapVWtc7 + GitHub. Lesson update: before deferring a custom-remote-code HF model, **check `config.transformers_version` and pin it**.
- **2026-07-16 · 71137 (Auxiliary-MCMC) AUDITED → DEFERRED.** arXiv 2406.05242 / OpenReview `dDkl5ZcyTl`, "MCMC without Evaluating the Target: an Auxiliary Variable Approach" (Yuan & Wang, Rutgers). Official code [ywwes26/Auxiliary-MCMC] exists (replicates simulations) BUT: **Julia v1.10** toolchain (not Python; needs Julia install + `Pkg.instantiate()`); README admits runs "may be slow" and recommends **SLURM HPC job arrays (4h × 30)**; 2 of 3 claims (framework-unification, theory-extension) are **theoretical** (only C2 = "new algorithms better on synthetic+real" is empirical). Theory-heavy + slow CPU + non-Python → poor fit, defer.
- **2026-07-16 · CMeeyJzWZ5 (1B-vertex road-network dataset) → AVOID.** Claims are planetary-scale OSM data processing (1B vertices, 31-city + 6-city benchmarks). Not reproducible at full scale on this box; data-engineering, not an ML-result claim.
- **2026-07-16 · remaining-candidate sweep (Tier B/C + shortlist exhausted).** `8ewf5I4shW` (RGPO causal identifiability) → DEFERRED (theory: identifiability *characterization* + *cardinality of feasible set* = math claims; no findable code). `vIZz7LvObC` (TokSuite, 14 models × multilingual bench) → AVOID (14-model GPU inference). `3EcT46wsdc` (TTFS SNN 99.48% MNIST etc.) → AVOID (training). `gc7Gg18ejz` (Isotropic-Gaussian RL) → AVOID (RL/training, already flagged). **`WtgQOtmw9N` ("What Characterizes Effective Reasoning?", arXiv 2509.19284, FSF) = only viable remaining candidate** but HEAVY: **no released code/data** (HF papers page confirms) → must generate ~10 reasoning-model CoTs on math/science via HF router AND implement the FSF (Failed-Step Fraction) graph-view method from scratch; 4 empirical claims. Doable at reduced scale (2–3 LRMs × subset) for a qualitative reproduction (risk: `toy`), multi-tick lift. **Pool status: RegressLM + DPRSC published, Bitwen under_verdict (bitwen-session); no other clearly-doable full-scale CPU/GPU-free paper remains.** Next-paper options after RegressLM C3 finalizes: (a) commit to WtgQOtmw9N as a dedicated multi-tick effort, or (b) re-run the 6,768-paper programmatic scorer for fresh CPU candidates.
- **2026-07-16 · hE0n8gS7Ru (Graph Label Selection) → DEFERRED (theory claims).** arXiv 2605.18623 (John, Meierhans, Probst Gutenberg); pure-Python code [josia-john/icml2026-graph-label-selection] @ `342aa2f7` runs + `ours` Ψ > baselines on SNAP (verified by a research agent). BUT the claims are C1 "first **O(log^1.5 n)-approximation**" + C2 "prior work lacks **provable guarantees**" — an asymptotic Big-O bound + positioning, NOT exact-instance theorems like Grokking/Frank-Wolfe/Flat-Minima (so the theorem-instance pattern gives only *suggestive* empirical verification, not decisive). (A research agent mis-id'd this as `62371` — a poster number; real forum id is `hE0n8gS7Ru`.) Folder scaffolded at `papers/icml26-repro-hE0n8gS7Ru-graph-label-selection` (cloned + venv + metis-import patched) for reuse if revisited (brute-force Ψ_optimal on small graphs vs ours).
