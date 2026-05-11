#!/usr/bin/env python3
"""collector.py — submission intake for FerpaFlow.  *** STUB — Phase 2 ***

Status: not implemented. For the Phase-1 MVP and the CIO demo, intake is just a
local folder of .txt files that the instructor drops submissions into (see
submissions/README.md). `grader.py` reads that folder directly. This file
exists to pin down the intended design so the architecture conversation has
something concrete to point at.

INTENDED BEHAVIOR
-----------------
Run locally on the faculty machine (cron job or small daemon). Poll an
institution-controlled git host for new student submissions, normalize each one
to a plain-text file in ./submissions/, and run the heuristic PII tripwire
(anonymize.find_likely_pii) over it, surfacing warnings to the instructor.

Outbound-only: it makes requests *out* to the git host; it never listens on a
port. No inbound connections, no exposed service.

HOSTING — DELIBERATE CHOICE
---------------------------
The submission store should be a git host the institution controls — a campus
GitLab CE / Gitea instance, or bare repos over SSH on a department server,
ideally behind institutional SSO. In that configuration student work never
touches a third-party processor at all, which is the cleanest answer to "is the
intake layer covered by an agreement?" — there is no third party.

A private repo on github.com is acceptable only as a stopgap for a single-
faculty pilot, and even then submissions should carry as little identifying
information as the assignment allows. Do not treat "it's a private repo" as
equivalent to "it's on institutional infrastructure" — it isn't.

WHAT THIS MODULE MUST NOT DO
----------------------------
- Must not call any cloud LLM. That's feedback.py's job, and only on scrubbed text.
- Must not write grades anywhere. That's grader.py, local terminal + local log.
- Must not open a listening socket.

LIKELY DEPENDENCIES (when implemented): PyGitHub or python-gitlab, or just the
`git` CLI via subprocess for the self-hosted-SSH case.
"""
from __future__ import annotations

import sys


def main() -> int:
    print(__doc__)
    print("collector.py is a stub. Phase-1 intake = a local folder of .txt files.")
    print("See submissions/README.md and ../docs/architecture.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
