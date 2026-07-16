# ICML 2026 Reproduction Challenge Campaign

An evidence-driven campaign for competing in the [ICML 2026 Agent Reproduction Challenge](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge) without relying on A100-class hardware.

This repository tracks:

- the live competitive position;
- how the automated judge actually scores evidence;
- a compute-aware paper-selection strategy;
- the initial paper portfolio;
- the protocol every reproduction must satisfy before publication.

## Current finding

The competition is not likely to be won by submitting a few toy reproductions. In the snapshot taken on **2026-07-16**, the leading public account had **111/114 points across 20 judged logbooks**, while second place had **96/114 across 20**. Both leaders concentrated on mathematical, statistical, and classical-ML papers whose claims could be tested at the paper's real scale on CPU.

Our campaign therefore has two tracks:

1. **Flagship quality:** a complete reproduction of *Learning Randomized Reductions* (Bitween), including all 80 benchmark functions, agentic and non-agentic baselines, formal verification, runtime evidence, and falsification checks.
2. **High-confidence throughput:** original-scale CPU reproductions of theory, optimization, sampling, tabular RL, kernel, and classical-ML papers with three experimentally testable claims.

The working target is **200-240 points**, at least **90% verified/falsified verdicts**, and one reproduction strong enough to stand out during the organizers' manual winner verification.

## Repository map

- [Competition findings](docs/competition-findings.md)
- [Initial reproduction portfolio](docs/reproduction-portfolio.md)
- [Campaign execution plan](docs/campaign-plan.md)
- [Live snapshot utility](scripts/challenge_snapshot.py)
- [2026-07-16 snapshot](snapshots/2026-07-16.md)

## Refresh the live data

The leaderboard changes frequently. Generate a fresh Markdown report without installing dependencies:

```bash
python3 scripts/challenge_snapshot.py > snapshot.md
```

The utility reads only official Hugging Face challenge endpoints and reports the leaderboard, judged efficiency, paper claim counts, and whether the initial candidates already have tagged logbooks.

## Scientific standard

Leaderboard points are a selection signal, not permission to lower scientific standards. Every published result must contain executed commands, raw outputs, deterministic checks, multiple seeds where stochasticity matters, paper-scale evidence, explicit deviations, negative controls, and a complete artifact bundle. A falsification is as valuable as a verification when the evidence genuinely supports it.

## Sources

- [Challenge guide](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/PROMPT.md)
- [Scoring FAQ](https://huggingface.co/spaces/ICML-2026-agent-repro/challenge/blob/main/faq.html)
- [Public judge implementation](https://huggingface.co/spaces/ICML-2026-agent-repro/logbook-judge/blob/main/app.py)
- [Official verdict dataset](https://huggingface.co/datasets/ICML-2026-agent-repro/verdicts/blob/main/verdicts.json)
