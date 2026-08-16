# Repository classification

## Identity

- Repository role: collection control plane
- Paper association: none
- Paper-level claims: none
- Current public URL: https://github.com/MachineLearning-Nerd/icml-2026-reproduction-challenge
- Default branch: main
- Name decision: retain icml-2026-reproduction-challenge

This repository coordinates a portfolio of independent paper reproductions.
It is not itself one of the paper repositories and should not be represented
as a reproduction of a particular paper.

## What belongs here

- competition findings and historical snapshots;
- paper-selection and compute-aware campaign strategy;
- shared quality and publication policy;
- workspace and repository architecture;
- links to paper repositories, Spaces, and artifact locations;
- utilities that refresh official challenge data.

## What does not belong here

- a paper's implementation or large experiment outputs;
- a paper-specific claim verdict;
- a paper citation presented as though it were the subject of this repository;
- an author thank-you note attributed to a paper's authors.

Each paper repository is responsible for its own paper title, authors,
version-pinned source, claims, evidence paths, branch purposes, citation, and
paper-author note. The central README links to the challenge's official guide,
FAQ, judge implementation, and verdict dataset instead.

## Evidence boundary

The leaderboard numbers in the README and snapshots are dated observations,
not live guarantees. Run scripts/challenge_snapshot.py against the official
Hugging Face endpoints to refresh them. The snapshot dated 2026-07-16 is
retained as historical evidence.

## Branch scope

The repository has one publication branch, main. There are no paper-specific
experiment branches to rename or interpret. A paper's descriptive branches
are documented in that paper's own repository.
