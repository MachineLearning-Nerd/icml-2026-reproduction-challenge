#!/usr/bin/env bash
#
# Publish every project whose coordination row is marked `publication_queued`.
#
# This script is deliberately inert unless invoked with --publish.  It locates
# project directories by OpenReview ID rather than by the GitHub repository
# slug, which also handles projects whose local directory has a legacy name.

set -euo pipefail

usage() {
  printf 'Usage: %s --check | --publish\n' "${0##*/}"
  printf '  --check    Validate the queued publication handoff without writing.\n'
  printf '  --publish  Create/push each queued Trackio Space sequentially.\n'
}

if [[ ${1:-} != '--check' && ${1:-} != '--publish' ]]; then
  usage >&2
  exit 2
fi

mode=$1
root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
papers_dir=$(cd "$root_dir/../papers" && pwd)
coordination_file="$root_dir/COORDINATION.md"

if ! command -v jq >/dev/null || ! command -v trackio >/dev/null; then
  printf 'Both jq and trackio must be available on PATH.\n' >&2
  exit 1
fi

while IFS=$'\t' read -r paper_id github_repo; do
  project_dir=$(find "$papers_dir" -mindepth 1 -maxdepth 1 -type d -iname "*${paper_id}*" -print -quit)
  if [[ -z $project_dir ]]; then
    printf '%s: no local project directory found\n' "$paper_id" >&2
    exit 1
  fi

  expected_origin="https://github.com/${github_repo}.git"
  actual_origin=$(git -C "$project_dir" remote get-url origin)
  if [[ $actual_origin != "$expected_origin" ]]; then
    printf '%s: origin mismatch (%s)\n' "$paper_id" "$actual_origin" >&2
    exit 1
  fi

  if ! sync_delta=$(git -C "$project_dir" rev-list --left-right --count '@{upstream}...HEAD' 2>/dev/null); then
    printf '%s: no GitHub tracking branch is configured\n' "$paper_id" >&2
    exit 1
  fi
  if [[ $sync_delta != $'0\t0' ]]; then
    printf '%s: committed branch is not synchronized with GitHub (%s)\n' "$paper_id" "$sync_delta" >&2
    exit 1
  fi

  if ! jq -e --arg tag "paper-${paper_id}" \
    '(.tags // []) | index("icml2026-repro") != null and index($tag) != null' \
    "$project_dir/.trackio/metadata.json" >/dev/null; then
    printf '%s: required Trackio tags are missing\n' "$paper_id" >&2
    exit 1
  fi

  if rg -q '/home/dineshai' "$project_dir/.trackio" -g '!logbook/assets/**'; then
    printf '%s: Trackio metadata contains a local path\n' "$paper_id" >&2
    exit 1
  fi

  printf '%s  %s\n' "$paper_id" "${project_dir##*/}"
  if [[ $mode == '--publish' ]]; then
    if [[ ! -f $project_dir/.venv/bin/activate ]]; then
      printf '%s: project virtual environment is unavailable\n' "$paper_id" >&2
      exit 1
    fi
    (
      cd "$project_dir"
      # shellcheck disable=SC1091
      source .venv/bin/activate
      trackio logbook publish "DineshAI/${paper_id}"
    )
    printf '  published: https://huggingface.co/spaces/DineshAI/%s\n' "$paper_id"
  fi
done < <(
  awk -F'|' '
    $5 ~ /publication_queued/ {
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", $2)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", $7)
      print $2 "\t" $7
    }
  ' "$coordination_file" | sort -u
)

if [[ $mode == '--check' ]]; then
  printf 'Preflight passed. Re-run with --publish after the Space quota resets.\n'
else
  printf 'Publish commands completed. Verify each public Space and update its row to under_verdict.\n'
fi
