#!/usr/bin/env python3
"""grader.py — FerpaFlow local grade recommender.

Reads anonymized student submissions from a local folder, sends each one
together with a YAML rubric to a locally-running Ollama instance, prints a
grade recommendation + justification to the terminal, and appends every
prompt/response pair to a local JSONL audit log.

Design constraint: nothing in this script makes an outbound network call.
The only socket it opens is to http://localhost:11434 (Ollama on the same
machine). No grades, no submissions, and no logs ever leave the workstation.

Usage:
    python grader.py --rubric rubric/written-reflection.yaml
    python grader.py --rubric rubric/written-reflection.yaml --model llama3:8b
    python grader.py --rubric r.yaml --submissions ./submissions --glob '*.txt'
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import textwrap
from pathlib import Path

import requests
import yaml

from anonymize import find_likely_pii

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "qwen2.5:32b"

SYSTEM_PROMPT = textwrap.dedent(
    """\
    You are a grading assistant for a university instructor. You are given a
    grading rubric and one anonymized student submission. Apply the rubric
    criterion by criterion. For each criterion: name it, state the points you
    would award out of its maximum, and give a one- or two-sentence rationale
    grounded in specific evidence from the submission. Then give a total and a
    short overall comment.

    This is a *recommendation* for the instructor, who will review it and is
    solely responsible for the grade of record. Be specific, be fair, and do
    not invent content that is not in the submission. If the submission is too
    short or off-topic to evaluate against a criterion, say so rather than
    guessing.
    """
)


def load_rubric(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict) or "criteria" not in data:
        raise ValueError(
            f"{path}: expected a mapping with a 'criteria' list "
            "(see rubric/written-reflection.yaml for the shape)."
        )
    return data


def render_rubric(rubric: dict) -> str:
    lines = [f"ASSIGNMENT: {rubric.get('assignment', '(unnamed)')}"]
    total = 0
    for c in rubric["criteria"]:
        pts = c.get("max_points", 0)
        total += pts
        lines.append(f"\n- {c['name']} ({pts} pts)")
        if c.get("description"):
            lines.append(f"    {c['description']}")
        for level in c.get("levels", []) or []:
            lines.append(f"    [{level.get('points', '?')}] {level.get('label', '')}: {level.get('description', '')}")
    lines.append(f"\nTOTAL POSSIBLE: {total} pts")
    if rubric.get("notes"):
        lines.append(f"\nINSTRUCTOR NOTES: {rubric['notes']}")
    return "\n".join(lines)


def build_user_prompt(rubric: dict, submission_text: str) -> str:
    return (
        "Here is the rubric:\n\n"
        f"{render_rubric(rubric)}\n\n"
        "----------\n"
        "Here is the anonymized student submission:\n\n"
        f"{submission_text.strip()}\n\n"
        "----------\n"
        "Now produce the rubric-by-rubric grade recommendation."
    )


def grade_submission(model: str, rubric: dict, submission_text: str, timeout: int) -> str:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(rubric, submission_text)},
        ],
        "stream": False,
        "options": {"temperature": 0.2},
    }
    resp = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()["message"]["content"].strip()


def append_audit_log(log_path: Path, record: dict) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rubric", required=True, type=Path, help="Path to the YAML rubric.")
    ap.add_argument("--submissions", type=Path, default=Path("submissions"), help="Folder of submission files.")
    ap.add_argument("--glob", default="*.txt", help="Glob for submission files within --submissions (default: *.txt).")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"Ollama model tag (default: {DEFAULT_MODEL}).")
    ap.add_argument("--log", type=Path, default=Path("logs/grader.jsonl"), help="Local audit log (JSONL).")
    ap.add_argument("--timeout", type=int, default=600, help="Per-request timeout in seconds (default: 600).")
    ap.add_argument("--skip-pii-check", action="store_true", help="Skip the heuristic PII warning (not recommended).")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        rubric = load_rubric(args.rubric)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Could not load rubric: {exc}", file=sys.stderr)
        return 2

    if not args.submissions.is_dir():
        print(f"Submissions folder not found: {args.submissions}", file=sys.stderr)
        return 2

    files = sorted(p for p in args.submissions.glob(args.glob) if p.is_file())
    if not files:
        print(f"No files matching {args.glob!r} in {args.submissions}", file=sys.stderr)
        return 1

    print(f"FerpaFlow grader — model={args.model}  rubric={args.rubric}  submissions={len(files)}")
    print("Grades and submissions stay on this machine. Audit log: " + str(args.log))

    failures = 0
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        print("\n" + "=" * 72)
        print(f"Submission: {path.name}")
        print("=" * 72)

        if not args.skip_pii_check:
            hits = find_likely_pii(text)
            if hits:
                print("  ⚠ heuristic PII check flagged this submission BEFORE grading:")
                for kind, sample in hits:
                    print(f"      - {kind}: {sample}")
                print("    The local grader will still run (it never leaves this machine),")
                print("    but DO NOT send this text to the cloud feedback step un-scrubbed.")

        try:
            result = grade_submission(args.model, rubric, text, args.timeout)
        except requests.exceptions.ConnectionError:
            print("  ! Could not reach Ollama at http://localhost:11434.", file=sys.stderr)
            print("    Start it with `ollama serve`, then `ollama pull " + args.model + "`.", file=sys.stderr)
            return 3
        except requests.RequestException as exc:
            print(f"  ! Ollama request failed for {path.name}: {exc}", file=sys.stderr)
            failures += 1
            continue

        print(result)
        append_audit_log(
            args.log,
            {
                "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
                "submission_file": path.name,
                "model": args.model,
                "rubric_file": str(args.rubric),
                "assignment": rubric.get("assignment"),
                "response": result,
            },
        )

    if failures:
        print(f"\nDone, with {failures} failed submission(s).", file=sys.stderr)
        return 1
    print("\nDone. Review each recommendation; you enter the grade of record yourself.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
