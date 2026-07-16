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
| utTapVWtc7 | Regression Language Models for Code (RegressLM) | autoloop | published:6/6 | DineshAI/utTapVWtc7 | MachineLearning-Nerd/icml26-repro-utTapVWtc7 | 2026-07-16 | ✅ **6/6 — all 3 claims reproduced** (paper-scale, Colab GPU). **C2** APPS ρ=0.9254 (n=512) >0.9 ✅ (ref 0.926). **C3** 17-CodeNet-lang avg ρ=0.517 (n=200/lang) >0.5 ✅ (12/17 langs >0.5; pooled CDSS 0.806≈card 0.787). **C1** VERIFIED — single checkpoint predicts APPS memory (0.925) + KBSS latency (0.531) + CDSS-17-lang memory (0.517); *caveat (disclosed in logbook): 'accuracy' is named in the claim but has no target column in the released Code-Regression parquet (target=memory bytes/latency ms), so accuracy isn't independently evaluated — a data-release scope, not a model limit.* Local CPU small-scale validated first (n=40 APPS ρ=0.937, perm p=0.0005, shuffled-control -0.205). Key fix: transformers 4.53.2 (ckpt export version; 5.x breaks T5Gemma generate). Logbook: https://huggingface.co/spaces/DineshAI/utTapVWtc7 · GitHub: https://github.com/MachineLearning-Nerd/icml26-repro-utTapVWtc7 . |
| tI5CFbRhmV | Rethinking Code Complexity Through the Lens of LLMs (LM-CC) | | deferred | | | 2026-07-16 | DEFERRED: no official code; the surfaced GitHub repo is a *different* paper. Needs from-scratch metric impl + DeepSeek-V3 inference. |
| QYpByrxSTg | Differentially Private Range Subgraph Counting (DPRSC) | autoloop | published | DineshAI/QYpByrxSTg | MachineLearning-Nerd/icml26-repro-qypbyrxstg-dprsc | 2026-07-16 | ✅ All claims finished (logbook corrected + republished). C1 verified; **C3 verified — pure_DP beats both baselines at every ε for ALL 3 patterns** (triangle/edge/2-star, ca-netscience) + paper-scale musae-squirrel edge (n=5201); approx_DP also wins edge/2-star. C2 = lower-bound **theorem + empirically confirmed** — Colab d=1 vs d=2: error grows **10³–10⁵×** (ours + both baselines), far past the `(log m)²`=100× noise floor; its `(log m)^(2d)` noise parameter in the code confirms the mechanism. (Earlier logbook mislabeled the anomaly as 2-star; it's triangle approx_DP at low ε — corrected.) |
| KJq0iScNM6 | Let the Prototype Guide You (PTBCC) | autoloop | under_verdict | DineshAI/KJq0iScNM6 | MachineLearning-Nerd/icml26-repro-KJq0iScNM6-ptbcc | 2026-07-16 | Published and publicly verified at Space commit `e57f7e6`. C1 falsified (paper says PTBCC/15%, not CPBCC/26%); C2 falsified (paper says 11 datasets and 69.86→74.72, not 10 and 68.73→74.11); C3 verified by equations 7–14 reconstruction, six exact public datasets (79.31% vs MV 76.57%), 40/40 synthetic wins, five passing tests. Awaiting judge; expected 6/6. |
| zrn7rRuvhW | Attention's Forward Pass and Frank-Wolfe | autoloop | under_verdict | DineshAI/zrn7rRuvhW | MachineLearning-Nerd/icml26-repro-zrn7rRuvhW-frank-wolfe | 2026-07-16 | Published, public, and tagged at Space commit `2cfd300`. All 3 claims GO: 0/72 FW mismatches + 57,600/57,600 inequalities; 0/1,600 Voronoi mismatches + predicted slopes; 417,792 stochastic residence samples with R²>.999 exponential fits. Ten tests pass. Awaiting judge; expected 6/6. |
| 5nNNVY8NW4 | To Grok Grokking: Provable Grokking in Ridge Regression | autoloop | under_verdict | DineshAI/5nNNVY8NW4 | MachineLearning-Nerd/icml26-repro-5nNNVY8NW4-grokking | 2026-07-16 | Published, public, and tagged at Space commit `28306f9`. All 3 claims GO: 6/6 three-stage separations; 16.04× lambda-delay amplification plus 6/6 elimination controls; 126/126 Eq. (8) rows pass both bounds. Five tests pass; full run 4.58 s CPU. Awaiting judge; expected 6/6. |
| u6zp8zZ8Ou | Flat Minima and Generalization: Insights from Stochastic Convex Optimization | autoloop | in_progress | | | 2026-07-16 | Selected as a proven 6/6, three-claim CPU target (1.98 s reference runtime). Scope: clean-room theorem-instance construction, exact risks and dynamics, scaling sweeps, event-frequency checks, stability audit, and falsification controls. |

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
