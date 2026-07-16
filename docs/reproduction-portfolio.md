# Initial reproduction portfolio

Status and claim counts reflect the official `claims.json` and public Space tags checked on **2026-07-16**.

## Tier A: begin here

### Learning Randomized Reductions (`hCAEcqig2C`)

**Maximum:** 6 points from 3 claims
**Compute:** CPU for Vanilla Bitween; hosted inference for agentic comparisons
**Public tagged logbook at snapshot:** none found
**Code:** [ferhaterata/learning-randomized-reductions](https://github.com/ferhaterata/learning-randomized-reductions)

Scored claims:

1. Vanilla Bitween discovers RSRs for 43 of 80 functions, including a sigmoid reduction.
2. Agentic Bitween discovers RSRs for 64 of 80 functions.
3. Agentic Bitween outperforms pure-neural baselines in discovery and verification accuracy.

Required full reproduction:

- execute all 80 RSR-Bench functions;
- reproduce Vanilla coverage using the released linear-regression backend;
- run the agentic and pure-neural conditions using the same comparable-class hosted model;
- independently verify every returned identity with SymPy;
- report coverage, verified properties, unverified properties, false positives, runtime, and failures per function;
- repeat critical comparisons with controlled seeds and identical budgets;
- publish raw outputs, code, environment, tests, figures, and a manifest.

Why it is the flagship: it offers exact executable claims, formal verification, a full released benchmark, low CPU requirements, and a substantive neuro-symbolic story for manual review.

## Tier B: promising after a paper-level audit

### Rethinking Code Complexity Through the Lens of LLMs (`tI5CFbRhmV`)

**Maximum:** 6 points from 3 claims
**Compute:** CPU analysis plus a quantized 7B code model on a T4
**Public tagged logbook at snapshot:** none found
**Code:** [xchen121/lm-cc](https://github.com/xchen121/lm-cc)

The strongest path is to reproduce the traditional-metric and LM-CC partial correlations on the full released result set, recompute LM-CC on a declared full benchmark partition, and run the semantics-preserving rewrite comparison. Quantization can change entropy values and must be validated against a small full-precision reference before it is accepted as faithful.

### Stable Deep Reinforcement Learning via Isotropic Gaussian Representations (`gc7Gg18ejz`)

**Maximum:** 6 points from 3 claims
**Compute:** CPU theory checks plus one T4 for non-stationary CIFAR-10; full RL scope requires audit
**Public tagged logbook at snapshot:** none found

The non-stationary CIFAR-10 experiment can test stability, feature rank, and dormant-neuron claims across the reported optimizers. This paper is greenlit only if the released code and full claim scope can be run without reducing datasets or environments.

### What Characterizes Effective Reasoning? (`WtgQOtmw9N`)

**Maximum:** 8 points from 4 claims
**Compute:** hosted inference; no training
**Public tagged logbook at snapshot:** none found

This is unusually valuable but potentially expensive. A full reproduction must compare length, review ratio, and Failed-Step Fraction; rerank candidate chains; and perform failed-branch editing at the real benchmark scale. It should start only after an inference-token budget is calculated.

## Tier C: feasible but poor early-game value

### AgentSelect (`4M5Kj2UqaM`)

Only two scored claims are present. The marketplace-transfer claim is substantially harder than auditing dataset counts, and the repository notes ongoing reproducibility cleanup. Keep it as a later diversification paper.

### TokSuite (`vIZz7LvObC`)

Only two scored claims are present, and both focus on released assets rather than the richer performance findings. Evaluating fourteen 1B models sequentially remains feasible on a T4, but its points-per-hour is weaker than the Tier A/B queue.

### Efficient TTFS Spiking Neural Networks (`3EcT46wsdc`)

Only one broad scored claim combines results across five datasets. Matching that claim fully without released code is high-risk; a Fashion-MNIST-only result would probably be toy-scale.

## Continuous screening queue

The wider conference list contains thousands of theory and classical-ML papers. Candidates should be ranked by:

```text
expected_value = expected_verified_points
                 * reproducibility_confidence
                 * manual_review_value
                 / estimated_engineering_hours
```

No paper enters implementation based on title alone. It must first receive a paper, code, dataset, compute, and claim-to-experiment audit.
