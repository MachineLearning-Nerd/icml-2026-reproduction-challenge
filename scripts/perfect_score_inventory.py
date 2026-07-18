#!/usr/bin/env python3
"""Build an owner-scoped perfect-score inventory directly from official verdicts."""
from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone


VERDICTS_URL = (
    "https://huggingface.co/datasets/ICML-2026-agent-repro/verdicts/"
    "resolve/main/verdicts.json"
)
FULL = {"verified", "falsified"}


def points(verdict: str) -> int:
    verdict = verdict.lower()
    if verdict in FULL:
        return 2
    if verdict == "toy":
        return 1
    return 0


def fetch_verdicts() -> dict:
    request = urllib.request.Request(
        VERDICTS_URL,
        headers={"User-Agent": "icml-perfect-score-inventory/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def one_line(value: str, limit: int = 240) -> str:
    rendered = " ".join(str(value).split()).replace("|", "\\|")
    return rendered if len(rendered) <= limit else rendered[: limit - 1].rstrip() + "…"


def build(owner: str, verdicts: dict) -> str:
    prefix = owner + "/"
    records = []
    score = maximum = 0
    for space_id, record in verdicts.items():
        if not space_id.startswith(prefix):
            continue
        claims = record.get("claims", [])
        paper_score = sum(points(row.get("verdict", "")) for row in claims)
        paper_maximum = 2 * len(claims)
        score += paper_score
        maximum += paper_maximum
        deficient = [
            (index, row)
            for index, row in enumerate(claims, 1)
            if row.get("verdict", "").lower() not in FULL
        ]
        records.append((space_id, record, paper_score, paper_maximum, deficient))

    nonperfect = [row for row in records if row[2] < row[3]]
    nonperfect.sort(key=lambda row: (-(row[3] - row[2]), row[0].lower()))
    captured = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    lines = [
        f"# {owner} perfect-score inventory",
        "",
        f"Captured from the [official verdict dataset]({VERDICTS_URL}) at `{captured}`.",
        "",
        f"- Official direct-verdict score: **{score}/{maximum}**.",
        f"- Judged logbooks: **{len(records)}**.",
        f"- Non-perfect papers: **{len(nonperfect)}**.",
        f"- Remaining point gap: **{maximum - score}**.",
        "",
        "A claim is full only when the official verdict is `verified` or `falsified`. "
        "Every deficient claim must use exactly 10 evidence approaches—never route 11—before republishing.",
        "",
        "| Paper | Score | Deficient claims | Official SHA | Judged at |",
        "|---|---:|---|---|---|",
    ]
    for space_id, record, paper_score, paper_maximum, deficient in nonperfect:
        gaps = ", ".join(
            f"C{index} `{row.get('verdict', '')}`" for index, row in deficient
        )
        lines.append(
            f"| `{space_id.removeprefix(prefix)}` | {paper_score}/{paper_maximum} | {gaps} | "
            f"`{record.get('sha', '')[:12]}` | `{record.get('judged_at', '')}` |"
        )
    lines.extend(["", "## Judge-identified gaps", ""])
    for space_id, record, paper_score, paper_maximum, deficient in nonperfect:
        paper = space_id.removeprefix(prefix)
        lines.extend([
            f"### `{paper}` — {one_line(record.get('paper_title', ''))}",
            "",
        ])
        for index, row in deficient:
            lines.append(
                f"- **C{index} `{row.get('verdict', '')}`:** {one_line(row.get('evidence', ''))}"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="DineshAI")
    args = parser.parse_args()
    print(build(args.owner, fetch_verdicts()))


if __name__ == "__main__":
    main()
