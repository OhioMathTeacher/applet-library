#!/usr/bin/env python3
"""feedback.py — public rubric-feedback generator for FerpaFlow.  *** STUB — Phase 2 ***

Status: not implemented. Documented here so the data-flow boundaries are explicit.

INTENDED BEHAVIOR
-----------------
Take an *already scrubbed* student submission plus the rubric, send it to the
institution's sanctioned cloud model (at Miami: Google Gemini / NotebookLM,
covered by the existing Google Workspace for Education agreement), and return
rubric-aligned qualitative comments — strengths, gaps, suggestions tied to
specific criteria. Post those comments back to the student (a file in their repo
or a PR/MR comment on the self-hosted git host).

HARD CONSTRAINTS — these are the whole point of the split architecture
----------------------------------------------------------------------
1. NO GRADES. This zone never produces, transmits, or stores a numeric score or
   letter grade. Comments only. Grades live exclusively in grader.py's local
   path and, ultimately, in Canvas (entered by the instructor).
2. SCRUBBED INPUT ONLY. Before anything is sent here it must pass through the
   anonymization step, AND a human must review it. anonymize.find_likely_pii is
   a tripwire for structured identifiers (emails, IDs); it does not catch
   self-identifying narrative detail ("my hometown of ___"). A clean tripwire
   result is necessary, not sufficient. If in doubt, don't send it.
3. SANCTIONED ENDPOINT ONLY. The cloud call goes to the institutionally
   contracted model and nowhere else. No personal API keys, no consumer
   ChatGPT/Claude/Gemini accounts — those are not covered by an agreement and
   are exactly the failure mode FerpaFlow exists to prevent.
4. LOG WHAT LEFT. Record (locally) what text was sent to the cloud and what
   came back, so the instructor can audit the boundary.

OPEN QUESTIONS TO RESOLVE WITH IT / COUNSEL BEFORE THIS SHIPS
-------------------------------------------------------------
- Which Gemini surface is in scope under Miami's DPA, and with what data-use /
  retention / training terms? (Workspace core services vs. the public AI Studio
  API are not the same contract.)
- Is "scrubbed classwork + rubric, no grade" inside or outside the agreement's
  permitted uses? Get that in writing.
- Does returning AI-generated feedback to students require disclosure to them
  (syllabus statement, per-assignment notice)? Likely yes; design for it.

LIKELY DEPENDENCIES (when implemented): google-generativeai (or the Workspace
API), plus the git host client shared with collector.py.
"""
from __future__ import annotations

import sys


def main() -> int:
    print(__doc__)
    print("feedback.py is a stub. Not wired up until the DPA questions above are answered.")
    print("See ../docs/architecture.md and ../docs/ferpa-memo.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
