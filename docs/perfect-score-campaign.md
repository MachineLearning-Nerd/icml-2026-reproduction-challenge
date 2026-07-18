# Perfect-score campaign

Live snapshot: **2026-07-18 21:53 UTC** from the official verdict dataset.
DineshAI is at **245/290** across 56 judged logbooks. Twenty papers remain
non-perfect, with a 45-point gap. This expanded after the repaired judge
discovery loop saved a 243-verdict batch. Generate the authoritative current
inventory directly from verdict records, without the 1,000-Space API limit:

```bash
python3 scripts/perfect_score_inventory.py --owner DineshAI
```

## Current repair queue

| Priority | Paper | Score | Non-full claims | Judge-identified gap | Attempt state |
|---:|---|---:|---|---|---|
| done | `4vztmTrGhd` | **4/4** | none | Three-layer half was missing | **official high-quality perfect score** |
| done | `uG4IOdaAGk` | **6/6** | none | n=8192/timing/accuracy repair accepted | **official high-quality perfect score** |
| done | `ub9PwBtHqD` | **4/4** | none | Full-scale ImageNet/ViT + six-SOTA repair accepted | **official high-quality perfect score** |
| done | `QO82qIzEsP` | **4/4** | none | Full California Housing SOCP + complete baseline grids accepted | **official high-quality perfect score** |
| done | `vWQk8Kdlhy` | **6/6** | none | Full 60-row Markov grid and 60k/10k, 5,000-step Fashion-MNIST repair | **official high-quality perfect score at `b5b3258`** |
| active | `utTapVWtc7` | 5/6 | C1 toy | Prior correct ONNX accuracy run was only NASBench101 n=64 | exactly-10 repair: NASBench101 .4066 and ENAS .2495 complete at n=512; NASNet running |
| pending | `Cxdj2GYZ4c` | 2/6 | C1/C2 toy, C3 inconclusive | Small MAPF grids; Schrödinger bridge omitted | pending |
| pending | `qIOcJSCGn2` | 2/6 | C1/C3 inconclusive | Direct survival-distribution evidence and benchmarks omitted | pending |
| pending | `tibRKqUHcv` | 2/6 | C2/C3 inconclusive | Sample-complexity and bilevel cost-learning omitted | pending |
| pending | `VQt4w3lElX` | 3/6 | C1/C2/C3 toy | All evidence at n=8 | pending |
| pending | `gLRqqQOM9K` | 3/6 | C1/C2/C3 toy | Three-token, length-six model only | pending |
| pending | `qbe18sZPWS` | 3/6 | C1/C2/C3 toy | Exact tabular flows replace pre-trained neural GFlowNets | pending |
| pending | `1KRpajnd6u` | 4/6 | C3 inconclusive | Trained PDE rollout benchmarks omitted | pending |
| pending | `2jw5U060C4` | 2/4 | C2 inconclusive | No learnability/training experiment | pending |
| pending | `73YmKB7KpW` | 4/6 | C3 inconclusive | Real-world-data half missing | pending |
| pending | `A8AxU1GUUl` | 4/6 | C1/C2 toy | Three-outcome finite classes do not cover general/infinite classes | pending |
| pending | `C4JJrPSwpy` | 4/6 | C3 inconclusive | “First” is a priority claim; no prior-art audit | pending |
| pending | `HDoWJi2jlj` | 4/6 | C2/C3 toy | Oracle Gaussian evidence; NPE benchmarks omitted | pending |
| pending | `nBuL6HywFX` | 2/4 | C1/C2 toy | Finite expressivity instances only | pending |
| pending | `oUv02QKUxG` | 2/4 | C1/C2 toy | Two-to-four-state MDPs only | pending |
| pending | `potpaozpjv` | 2/4 | C1/C2 toy | Small tabular MDPs and incomplete theorem scope | pending |
| pending | `ry5HitnXzc` | 2/4 | C1/C2 toy | One binary model and one epsilon/delta point; lower bound untested | pending |
| pending | `G4D0YzzZEk` | 3/4 | C2 toy | Eight-point clouds only | pending |
| pending | `nf7JT1jCSy` | 3/4 | C1 toy | Formula checked without a real multimodal classifier/dataset | pending |
| pending | `vMcu1h3fOV` | 3/4 | C1 toy | n=80, d=8 synthetic ARD only | pending |

## `4vztmTrGhd` Claim 1 — ten approaches

All ten are implemented by `repro/src/run_three_layer_attempts.py`; the canonical
result is `outputs/three_layer_attempts.json` in the paper repository.

1. Dense recreation of all thirty clean Figure-2 theoretical curves.
2. Corollary 5.6 signed-curvature sweep across widths and exponents.
3. Symbolic constrained second derivative with SymPy.
4. Pinned authors' source-drift audit and landscape comparison.
5. Independent polynomial rewrite in `p=eta1+eta2`, `q=eta1*eta2`.
6. Eighty-digit arbitrary-precision curvature at perturbation `1e-20`.
7. Float64 automatic-differentiation Hessian.
8. Direct clean matrix GD at `h=d=n=1000`, five seeds.
9. Literal full-`X` autograd parity for the reduced full-scale implementation.
10. Direct `rho=0.01` noisy-label matrix GD at `h=d=n=1000`, five seeds.

The source audit found that the pinned three-layer plotting script omits the
paper's `2 eta1 eta2 / h^3` one-step term. This is disclosed explicitly; the
residual after accounting for it is `4.89e-16`, and both versions preserve the
claim on all thirty tested curves.

## Resume protocol

Work one paper per tick. For each non-full claim: read the paper and judge
rationale, preserve an **exactly 10 approach** ledger (never route 11), execute the strongest full-scale
routes, add independent verification and fail-closed controls, capture clean
relative Trackio commands, run the publish gate, sync/push, and confirm the new
official verdict before calling that paper perfect.
