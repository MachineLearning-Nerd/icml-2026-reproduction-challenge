# Competition findings

Snapshot date: **2026-07-16**. Live values will drift; use `scripts/challenge_snapshot.py` before making scheduling decisions.

## 1. Scoring mechanics

The public leaderboard sums verdicts across all judged logbooks owned by a Hugging Face username:

| Verdict | Points | Required evidence |
|---|---:|---|
| `verified` | 2 | Concrete, non-toy experimental evidence supporting the claim |
| `falsified` | 2 | Concrete, non-toy experimental evidence contradicting the claim |
| `toy` | 1 | Real results on reduced data, a smaller model, or a proxy task |
| `inconclusive` | 0 | Missing, assertion-only, weak, or unrelated evidence |

The organizers state that leaderboard points are only the starting point. They manually verify the top finishers before awarding prizes.

## 2. Live competitive position

The official Spaces and verdict feeds produced the following leading accounts at capture time:

| Rank | Account | Points | Maximum | Judged logbooks | Efficiency |
|---:|---|---:|---:|---:|---:|
| 1 | `neonforestmist` | 111 | 114 | 20 | 97.4% |
| 2 | `rdubwiley` | 96 | 114 | 20 | 84.2% |
| 3 | `nkapila6` | 39 | 92 | 18 | 42.4% |
| 4 | `abidlabs` | 25 | 72 | 13 | 34.7% |

The important signal is not merely the number of logbooks. First place converted nearly every available claim into a full verification or falsification.

## 3. What the strongest entries do

The highest-scoring CPU logbooks consistently make each judge claim easy to audit:

- an evidence scorecard appears before lengthy detail;
- each official claim has its own experiment and page;
- the paper-default configuration is tested first;
- sweeps cover the parameter dependence stated by the paper;
- several seeds are used when sampling or initialization matters;
- theoretical inequalities are checked numerically across a declared grid;
- a direct implementation test guards optimized or closed-form evaluators;
- limitations distinguish finite empirical evidence from universal theorems;
- raw CSV/JSON, figures, source, tests, environments, and hashes are published.

This is good scientific communication, not a substitute for genuine evidence. The judge explicitly ignores self-assigned verdicts and independently evaluates the runs and numbers.

## 4. Important judge behavior

The public judge implementation establishes several operational facts:

1. It scores the claims in the challenge's `claims.json` file, which may differ from a longer claim list shown elsewhere.
2. It reads at most 120,000 characters of rendered logbook Markdown. Decisive evidence must therefore appear early and compactly.
3. A similar-class open model may replace a proprietary model when the backbone is not the paper's contribution, provided the substitution and expected effects are documented.
4. Smaller data subsets, proxy tasks, and models far below the paper's class remain toy-scale.
5. Updating a published Space changes its commit SHA and queues it for a new judgment. Revisions must add missing experiments or evidence, not merely stronger wording.

## 5. Consequences for paper selection

Use this gate before beginning a reproduction:

- Prefer three-claim papers (six possible points); consider four-claim papers only when inference cost is controlled.
- Every scored claim must map to a decisive experiment.
- The complete original-scale run should fit within two CPU hours or one ordinary T4 session.
- Favor exact equations, released code, public data, and deterministic evaluators.
- Avoid papers whose only feasible result would use a small subset or unrelated proxy.
- Avoid large video, robotics, foundation-model training, large-scale RL, and multi-GPU systems work.
- Prefer unattempted papers, although independent attempts on the same paper are permitted.

## 6. Competitive target

The challenge closes on 2026-08-02. Because the current leader can continue adding points, merely exceeding 111 is not a winning target.

The campaign target is:

- **200-240 total points**;
- **35-40 mostly three-claim papers**;
- **at least 90% verified/falsified claim verdicts**;
- **one flagship reproduction** designed for manual organizer review;
- approximately **two completed full reproductions per day** after the reusable harness is stable.

This target is intentionally aggressive. It will be reduced only if early verdicts show that quality cannot be maintained.
