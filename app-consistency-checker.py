#!/usr/bin/env python3
"""Consistency checks for applet-library publishing.

Usage:
  python app-consistency-checker.py
  python app-consistency-checker.py --strict-warnings

What it checks:
- README applet entries have unique emojis
- README links point to folder roots (not specific HTML files)
- Listed applet folders exist
- Each listed applet has index.html
- If index.html redirects to pedagogical-notes.html, ensure that file exists
- Pedagogical notes include launch and feedback conventions
- Launch target referenced from pedagogical notes exists
- Main app page contains a link back to pedagogical-notes.html (warning)
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


README_ENTRY_RE = re.compile(
    r"^###\s+(.+?)\s+\[(.+?)\]\((https://ohiomathteacher\.github\.io/applet-library/[^)]+)\)\s*$",
    re.MULTILINE,
)

ROOT_LINK_RE = re.compile(r"^https://ohiomathteacher\.github\.io/applet-library/([^/]+)/$")
LAUNCH_LINK_RE = re.compile(r"Launch Applet[^\\n]*", re.IGNORECASE)
HREF_RE = re.compile(r"href=\"([^\"]+)\"")
DOCS_LINK_RE = re.compile(r'https://docs\.google\.com/document/[^"\s]+')


@dataclass
class Finding:
    level: str
    scope: str
    message: str


class Checker:
    def __init__(self, repo_root: Path, strict_warnings: bool = False) -> None:
        self.repo_root = repo_root
        self.strict_warnings = strict_warnings
        self.findings: list[Finding] = []

    def add(self, level: str, scope: str, message: str) -> None:
        self.findings.append(Finding(level=level, scope=scope, message=message))

    def run(self) -> int:
        readme_path = self.repo_root / "README.md"
        if not readme_path.exists():
            self.add("ERROR", "README", "Missing README.md at repository root")
            return self._finish()

        readme_text = readme_path.read_text(encoding="utf-8", errors="replace")
        entries = list(README_ENTRY_RE.finditer(readme_text))

        if not entries:
            self.add("ERROR", "README", "No applet entries found in README")
            return self._finish()

        self._check_unique_emojis(entries)

        for entry in entries:
            emoji = entry.group(1).strip()
            name = entry.group(2).strip()
            url = entry.group(3).strip()
            scope = f"{name} ({emoji})"

            slug = self._check_readme_url(scope, url)
            if not slug:
                continue

            app_dir = self.repo_root / slug
            if not app_dir.exists() or not app_dir.is_dir():
                self.add("ERROR", scope, f"Listed folder '{slug}' does not exist")
                continue

            self._check_applet_folder(scope, app_dir)

        return self._finish()

    def _check_unique_emojis(self, entries: Iterable[re.Match[str]]) -> None:
        by_emoji: dict[str, list[str]] = {}
        for entry in entries:
            emoji = entry.group(1).strip()
            name = entry.group(2).strip()
            by_emoji.setdefault(emoji, []).append(name)

        for emoji, names in by_emoji.items():
            if len(names) > 1:
                self.add(
                    "ERROR",
                    "README",
                    f"Emoji '{emoji}' is reused across applets: {', '.join(names)}",
                )

    def _check_readme_url(self, scope: str, url: str) -> str | None:
        match = ROOT_LINK_RE.match(url)
        if match:
            return match.group(1)

        self.add(
            "ERROR",
            scope,
            "README link should target folder root format: "
            "https://ohiomathteacher.github.io/applet-library/<folder>/",
        )
        return None

    def _check_applet_folder(self, scope: str, app_dir: Path) -> None:
        index_path = app_dir / "index.html"
        if not index_path.exists():
            self.add("ERROR", scope, "Missing index.html")
            return

        index_text = index_path.read_text(encoding="utf-8", errors="replace")
        has_notes_redirect = "pedagogical-notes.html" in index_text and "http-equiv=\"refresh\"" in index_text

        notes_path = app_dir / "pedagogical-notes.html"
        if has_notes_redirect and not notes_path.exists():
            self.add(
                "ERROR",
                scope,
                "index.html redirects to pedagogical-notes.html, but that file is missing",
            )

        if notes_path.exists():
            self._check_pedagogical_notes(scope, app_dir, notes_path)
        else:
            self.add(
                "WARN",
                scope,
                "No pedagogical-notes.html found (legacy applet style or incomplete landing flow)",
            )

    def _check_pedagogical_notes(self, scope: str, app_dir: Path, notes_path: Path) -> None:
        notes_text = notes_path.read_text(encoding="utf-8", errors="replace")

        if "Launch Applet" not in notes_text:
            self.add("ERROR", scope, "pedagogical-notes.html is missing a 'Launch Applet' link")

        if "Add Your Feedback (Google Doc)" not in notes_text:
            self.add(
                "ERROR",
                scope,
                "pedagogical-notes.html is missing the standard feedback button text",
            )

        if not DOCS_LINK_RE.search(notes_text):
            self.add(
                "ERROR",
                scope,
                "pedagogical-notes.html has no Google Doc feedback URL",
            )

        launch_target = self._extract_launch_target(notes_text)
        if launch_target is None:
            self.add("WARN", scope, "Could not detect launch target href in pedagogical notes")
            return

        launch_path = (app_dir / launch_target).resolve()
        try:
            launch_path.relative_to(app_dir.resolve())
        except ValueError:
            self.add("ERROR", scope, f"Launch target escapes applet folder: {launch_target}")
            return

        if not launch_path.exists():
            self.add("ERROR", scope, f"Launch target does not exist: {launch_target}")
            return

        if launch_path.suffix.lower() == ".html":
            app_text = launch_path.read_text(encoding="utf-8", errors="replace")
            if "href=\"pedagogical-notes.html\"" not in app_text:
                self.add(
                    "WARN",
                    scope,
                    f"Launch page '{launch_target}' has no obvious link back to pedagogical-notes.html",
                )

    def _extract_launch_target(self, notes_text: str) -> str | None:
        launch_line_match = LAUNCH_LINK_RE.search(notes_text)
        if not launch_line_match:
            return None

        line_start = notes_text.rfind("\n", 0, launch_line_match.start()) + 1
        line_end = notes_text.find("\n", launch_line_match.end())
        if line_end == -1:
            line_end = len(notes_text)
        launch_line = notes_text[line_start:line_end]

        href_match = HREF_RE.search(launch_line)
        if not href_match:
            return None

        href = href_match.group(1).strip()
        if href.startswith("http://") or href.startswith("https://"):
            return None
        return href

    def _finish(self) -> int:
        if not self.findings:
            print("PASS: No consistency issues found.")
            return 0

        errors = [f for f in self.findings if f.level == "ERROR"]
        warns = [f for f in self.findings if f.level == "WARN"]

        ordered = errors + warns
        for finding in ordered:
            print(f"[{finding.level}] {finding.scope}: {finding.message}")

        print()
        print(f"Summary: {len(errors)} error(s), {len(warns)} warning(s)")

        if errors:
            return 1
        if self.strict_warnings and warns:
            return 2
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check applet-library consistency before publishing.")
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to applet-library repository (default: current directory)",
    )
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Treat warnings as non-zero exit (exit code 2)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo).resolve()
    checker = Checker(repo_root=repo_root, strict_warnings=args.strict_warnings)
    return checker.run()


if __name__ == "__main__":
    sys.exit(main())
