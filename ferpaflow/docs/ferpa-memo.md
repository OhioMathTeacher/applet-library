# FerpaFlow — FERPA framing (for counsel review)

**This is not legal advice and has not been reviewed by university counsel.** It
is the framing the project is built on, written so counsel can confirm, correct,
or reject it. If any of this is wrong, the architecture — not the conclusion —
should change.

## The short version (the two paragraphs to hand to counsel)

FerpaFlow is designed so that the data elements FERPA most clearly protects —
**grades and personally identifiable information from education records** — never
enter a system that lacks an institutional agreement to hold them. The
*grading* step runs on a local LLM on the faculty member's own machine, with no
internet route; the recommendation and its rationale are displayed locally and
written only to a local log; the faculty member then enters the grade of record
into Canvas by hand. No grade is ever produced, transmitted, or stored by any
cloud service in this pipeline. The one step that does use a cloud service
returns *qualitative, rubric-aligned comments only* — never a score — and
operates only on submission text that has been **de-identified and
human-reviewed first**, sent only to the institution's already-contracted model
(at Miami, Google Gemini / NotebookLM under the existing Workspace for Education
agreement). We are asking counsel to confirm three things: (1) that this
de-identify-then-comment cloud step is a permitted use under that agreement;
(2) what the institution's standard is for adequate de-identification of student
writing; and (3) whether returning AI-assisted feedback to students requires
disclosure to them, and in what form.

We want to be explicit about what we are **not** relying on. An earlier draft of
this project leaned on the idea that "student classwork is not a FERPA record,"
citing *Owasso Independent School District No. I-011 v. Falvo*, 534 U.S. 426
(2002). We no longer make that claim, and the architecture does not depend on
it. *Falvo* held narrowly that **peer-graded assignments, while they are being
handled by students before the teacher records the grade**, are not "education
records maintained by the institution." It did not hold that classwork is
categorically outside FERPA, and once a submission is collected by the
instructor and used in grading there is a strong argument it is part of an
education record. Rather than litigate that boundary, FerpaFlow treats student
submissions as sensitive by default and relies on **data minimization** (keep
grades and identifiers local) and **sanctioned endpoints** (use only systems the
institution has already vetted) — design choices that hold regardless of how the
classwork-vs-record question comes out.

## Element-by-element

| Element | Treatment in FerpaFlow | What we want counsel to confirm |
|---|---|---|
| Numeric / letter grades | Produced only by the local LLM (Zone 3); shown on the local terminal; written only to a local, git-ignored log; entered into Canvas manually by the faculty member. Never sent to any cloud service. | That this keeps grades out of scope for any third-party-disclosure concern. |
| Student names, IDs, and other PII in submissions | Must be removed before any cloud call. `anonymize.py` flags structured identifiers (emails, ID-shaped numbers, "my name is ___") but is explicitly a tripwire, not a guarantee; a human reviews the text before it goes to Zone 2. | The institution's actual standard for "de-identified" student writing — the FERPA test is that no one in the school community could reasonably identify the student, and reflective prose can defeat that even with names removed. |
| Submission text (de-identified) sent to the cloud model | Sent only to the institutionally contracted model (Miami: Gemini / NotebookLM, Workspace for Education DPA), only after de-identification + human review, only to obtain qualitative comments. Logged locally. | That "scrubbed classwork + rubric, to generate non-grade feedback" is within the permitted uses, data-retention terms, and (no-)training terms of that agreement. |
| Comments returned to the student | Qualitative, rubric-aligned; contain no score or grade by construction. | Whether disclosing to students that feedback is AI-assisted is required (syllabus statement, per-assignment notice, etc.). |
| The Zone-1 submission store | An institution-controlled git host (campus GitLab CE / Gitea, or department SSH) — no third-party processor. A private GitHub repo is treated as a pilot-only stopgap and, in that mode, carries minimal identifying content. | Whether a private GitHub repo is acceptable even for a limited single-faculty pilot, or whether intake must be on institutional infrastructure from day one. |
| Consumer AI accounts (ChatGPT, consumer Gemini, Claude, personal API keys) | Out of bounds everywhere in the pipeline. The whole project exists partly to give faculty a sanctioned alternative to this. | (No action — stated for completeness.) |

## Why the architecture is the safeguard

Even if some classwork turns out to be part of an education record, FerpaFlow's
posture doesn't change: the protected elements (grades, identifiers) stay on the
faculty machine; the only outbound flow is de-identified, grade-free text to a
vetted endpoint; nothing accepts inbound connections. The compliance argument
rests on *where the data is and what's in it*, not on a contested reading of
what counts as a record.

## Things that would change the design if counsel says so

- If de-identification of student writing can't be done to the institution's
  satisfaction → drop Zone 2 (the cloud-comments step) entirely; keep Zones 1
  and 3. The local grader still works.
- If the Workspace DPA doesn't cover this use → either get an addendum, or move
  Zone 2's comment generation onto the local LLM too (slower, but fully local).
- If a private GitHub repo isn't acceptable even for a pilot → Zone 1 starts on
  campus GitLab/Gitea from the first day.
