# Perfect-score campaign

Initial live snapshot: **2026-07-18 08:48 UTC** from the official Spaces, claims,
and verdict datasets. After the `uG4IOdaAGk` re-verdict at 09:50 UTC, DineshAI is
at **194/216** across 40 judged logbooks. Eleven papers remain non-perfect,
covering eighteen non-full claims and a 22-point gap. Re-run the snapshot before
relying on these numbers.

## Current repair queue

| Priority | Paper | Score | Non-full claims | Judge-identified gap | Attempt state |
|---:|---|---:|---|---|---|
| done | `4vztmTrGhd` | **4/4** | none | Three-layer half was missing | **official high-quality perfect score** |
| done | `uG4IOdaAGk` | **6/6** | none | n=8192/timing/accuracy repair accepted | **official high-quality perfect score** |
| 3 | `ub9PwBtHqD` | 3/4 | C2 toy | Random-only baseline; tiny synthetic problems; observed MSE often worse | pending |
| 4 | `QO82qIzEsP` | 3/4 | C2 toy | No SOCP; single newsvendor proxy rather than released benchmarks | pending |
| 5 | `vWQk8Kdlhy` | 5/6 | C3 toy | Inconsistent Markov-blanket settings and reduced Fashion-MNIST SSL | pending |
| 6 | `utTapVWtc7` | 5/6 | C1 toy | NAS accuracy proxy is not code accuracy | pending |
| 7 | `73YmKB7KpW` | 4/6 | C3 inconclusive | Real-world-data half missing | pending |
| 8 | `C4JJrPSwpy` | 4/6 | C3 inconclusive | “First” is a priority claim; no prior-art audit | pending |
| 9 | `A8AxU1GUUl` | 4/6 | C1/C2 toy | Three-outcome finite classes do not cover general/infinite classes | pending |
| 10 | `VQt4w3lElX` | 3/6 | C1/C2/C3 toy | All evidence at n=8 | pending |
| 11 | `qbe18sZPWS` | 3/6 | C1/C2/C3 toy | Exact tabular flows replace pre-trained neural GFlowNets | pending |
| 12 | `ry5HitnXzc` | 2/4 | C1/C2 toy | One binary model and one epsilon/delta point; lower bound untested | pending |
| 13 | `qIOcJSCGn2` | 2/6 | C1/C3 inconclusive | No direct survival-distribution evidence; benchmarks omitted | pending |

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
rationale, preserve a ten-approach ledger, execute the strongest full-scale
routes, add independent verification and fail-closed controls, capture clean
relative Trackio commands, run the publish gate, sync/push, and confirm the new
official verdict before calling that paper perfect.
