#!/usr/bin/env python3
"""Print a Markdown snapshot of the ICML 2026 reproduction challenge."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any
from urllib.request import Request, urlopen


SPACES_URL = (
    "https://huggingface.co/api/spaces?"
    "filter=icml2026-repro&full=true&limit=1000"
)
VERDICTS_URL = (
    "https://huggingface.co/datasets/ICML-2026-agent-repro/"
    "verdicts/resolve/main/verdicts.json"
)
CHALLENGE_BASE = (
    "https://huggingface.co/spaces/ICML-2026-agent-repro/"
    "challenge/resolve/main"
)

CANDIDATES = {
    "hCAEcqig2C": "Learning Randomized Reductions",
    "tI5CFbRhmV": "Rethinking Code Complexity Through the Lens of LLMs",
    "gc7Gg18ejz": "Stable Deep Reinforcement Learning via Isotropic Gaussian Representations",
    "WtgQOtmw9N": "What Characterizes Effective Reasoning?",
    "4M5Kj2UqaM": "AgentSelect",
    "vIZz7LvObC": "TokSuite",
    "3EcT46wsdc": "Efficient TTFS Spiking Neural Networks",
}


def fetch_json(url: str) -> Any:
    request = Request(url, headers={"User-Agent": "icml-repro-snapshot/1.0"})
    with urlopen(request, timeout=60) as response:
        return json.load(response)


def verdict_points(verdict: str) -> int:
    normalized = verdict.lower()
    if normalized in {"verified", "falsified"}:
        return 2
    if normalized == "toy":
        return 1
    return 0


def paper_tags(space: dict[str, Any]) -> set[str]:
    return {
        tag.removeprefix("paper-")
        for tag in space.get("tags", [])
        if tag.startswith("paper-")
    }


def main() -> None:
    spaces = fetch_json(SPACES_URL)
    verdicts = fetch_json(VERDICTS_URL)
    claims = fetch_json(f"{CHALLENGE_BASE}/claims.json")

    attempted: dict[str, list[str]] = defaultdict(list)
    rankings: dict[str, dict[str, int]] = defaultdict(
        lambda: {"points": 0, "maximum": 0, "logbooks": 0}
    )

    for space in spaces:
        space_id = space["id"]
        for paper_id in paper_tags(space):
            attempted[paper_id].append(space_id)

        judged = verdicts.get(space_id)
        if not judged:
            continue
        owner = space_id.split("/", 1)[0]
        claim_verdicts = judged.get("claims", [])
        rankings[owner]["points"] += sum(
            verdict_points(item.get("verdict", "")) for item in claim_verdicts
        )
        rankings[owner]["maximum"] += 2 * len(claim_verdicts)
        rankings[owner]["logbooks"] += 1

    ordered = sorted(
        rankings.items(),
        key=lambda item: (-item[1]["points"], item[0].lower()),
    )

    captured = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    print("# ICML 2026 reproduction challenge snapshot")
    print()
    print(f"Captured: `{captured}`")
    print()
    print(f"Public tagged Spaces: **{len(spaces)}**")
    print(f"Judged verdict records: **{len(verdicts)}**")
    print()
    print("## Leaderboard calculated from official verdicts")
    print()
    print("| Rank | Account | Points | Maximum | Judged logbooks | Efficiency |")
    print("|---:|---|---:|---:|---:|---:|")
    for rank, (owner, values) in enumerate(ordered[:20], start=1):
        maximum = values["maximum"]
        efficiency = 100 * values["points"] / maximum if maximum else 0
        print(
            f"| {rank} | `{owner}` | {values['points']} | {maximum} | "
            f"{values['logbooks']} | {efficiency:.1f}% |"
        )

    print()
    print("## Initial candidate status")
    print()
    print("| Paper | ID | Claims | Tagged logbooks |")
    print("|---|---|---:|---:|")
    for paper_id, title in CANDIDATES.items():
        print(
            f"| {title} | `{paper_id}` | {len(claims.get(paper_id, []))} | "
            f"{len(attempted.get(paper_id, []))} |"
        )

    print()
    print("## Sources")
    print()
    print(f"- Spaces: {SPACES_URL}")
    print(f"- Verdicts: {VERDICTS_URL}")
    print(f"- Claims: {CHALLENGE_BASE}/claims.json")


if __name__ == "__main__":
    main()
