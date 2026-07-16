# Repository and workspace architecture

## Local parent workspace

The complete campaign will live beneath a local parent folder named exactly:

```text
ReproduceICML/
```

The intended layout is:

```text
ReproduceICML/
├── icml-2026-reproduction-challenge/       # Central campaign repository
├── icml-2026-repro-template/                # Reusable paper template repository
└── papers/                                  # Independent paper repositories
    ├── icml26-repro-hcaecqig2c-bitween/
    ├── icml26-repro-ti5cfbrhmv-lm-cc/
    ├── icml26-repro-gc7gg18ejz-sigreg/
    └── icml26-repro-<paper-id>-<slug>/
```

The paper directories are sibling Git repositories under `ReproduceICML/papers/`. They are not ordinary nested repositories inside `icml-2026-reproduction-challenge`.

## GitHub repositories

All repositories will be owned by the same GitHub account:

```text
MachineLearning-Nerd/
├── icml-2026-reproduction-challenge
├── icml-2026-repro-template
├── icml26-repro-hcaecqig2c-bitween
├── icml26-repro-ti5cfbrhmv-lm-cc
└── icml26-repro-<paper-id>-<slug>
```

Use this naming rule for paper repositories:

```text
icml26-repro-<lowercase-openreview-id>-<short-paper-slug>
```

Including the OpenReview ID prevents collisions between papers with similar titles and provides a stable connection to the challenge's `paper-<openreview-id>` tag.

## Repository responsibilities

### Central campaign repository

`icml-2026-reproduction-challenge` remains the control plane. It contains:

- competition findings and leaderboard snapshots;
- the paper-selection queue;
- campaign status and awarded points;
- links to each paper repository, Trackio Space, and artifact bucket;
- shared policies and quality requirements;
- scripts that refresh challenge state.

It should not contain copies of each paper's implementation or large outputs.

### Template repository

`icml-2026-repro-template` will define the standard structure and verification tooling copied into every new paper repository:

```text
README.md
paper/
  metadata.yaml
  claims.md
  sources.md
reproduction/
  src/
  configs/
  tests/
scripts/
outputs/
  figures/
  tables/
  metrics/
docs/
  methodology.md
  limitations.md
.trackio/
.env.example
.gitignore
pyproject.toml
```

### Paper repositories

Each paper repository owns exactly one reproduction:

- source and adapted author code;
- paper-specific dependencies and configuration;
- exact scored claims;
- executed tests and experimental results;
- figures and compact raw data;
- Trackio logbook sources;
- environment details and artifact manifests;
- judge verdict history and evidence-driven revisions.

## GitHub and Hugging Face mapping

Each reproduction has three public locations:

| Responsibility | Location |
|---|---|
| Code, tests, and configurations | GitHub paper repository |
| Human-readable experimental record | Trackio Hugging Face Space |
| Large datasets, checkpoints, and outputs | Hugging Face Bucket |

For Bitween, the intended mapping is:

```text
GitHub:  MachineLearning-Nerd/icml26-repro-hcaecqig2c-bitween
Space:   MachineLearning-Nerd/hCAEcqig2C
Bucket:  MachineLearning-Nerd/hCAEcqig2C-artifacts
```

The GitHub README, Trackio logbook, and central registry must link to each other.

## Central registry

The central repository will eventually contain a machine-readable `papers.yaml` registry. Each entry will record:

- OpenReview and arXiv identifiers;
- paper title and short slug;
- GitHub repository URL;
- Trackio Space and artifact Bucket URLs;
- selection and reproduction status;
- expected and awarded points;
- compute type, duration, and cost;
- current judge verdicts;
- last verified commit SHA.

The registry will be the source of truth for generating the campaign dashboard. The paper repositories remain the source of truth for experimental evidence.

## Paper lifecycle

1. Greenlight the paper after a claim, code, data, and compute audit.
2. Add a `selected` entry to the central registry.
3. Create its GitHub repository from the template.
4. Clone it beneath `ReproduceICML/papers/`.
5. Implement and verify the full reproduction.
6. Publish the Trackio Space and artifact Bucket.
7. Record links, commit SHA, compute, and verdicts centrally.
8. Revise the paper repository only when new evidence addresses a genuine experimental gap.

Git submodules are intentionally excluded from the initial design. Central links and a registry are simpler to clone, automate, and maintain across dozens of paper repositories.
