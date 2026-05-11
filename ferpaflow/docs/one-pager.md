# FerpaFlow — one page

*A FERPA-aware way to let AI help with grading, without putting grades or
identifiable student records into a system that isn't cleared to hold them.*

For: colleagues in Teacher Education and Computer Science. (Not legal advice;
not yet reviewed by counsel — see [`ferpa-memo.md`](ferpa-memo.md).)

---

## The problem

Faculty want AI help with feedback and grading. Right now the realistic choices
are: **(a)** paste student work into consumer ChatGPT/Gemini/Claude and hope —
no institutional agreement, no idea where the data goes, a real FERPA exposure;
or **(b)** don't use AI at all and grade everything by hand. FerpaFlow is a
third path, and it's mostly about *where the data lives*, not a loophole.

## The idea: split the workflow into three zones

| Zone | Where it runs | What moves through it |
|---|---|---|
| **1 — Submissions** | An institution-controlled git host (a campus GitLab/Gitea, or a department server). A private GitHub repo only as a one-person pilot stopgap. | Student classwork. *No grades.* |
| **2 — Feedback** | The institution's *sanctioned* cloud model — at Miami, Google Gemini / NotebookLM, under the Workspace agreement we already have. | **De-identified** student work + a rubric → rubric-aligned *comments*. *No scores, ever.* Text is scrubbed **and human-reviewed** before it's sent. |
| **3 — Grades** | A local LLM (Ollama) on the faculty member's own computer, with no internet connection. | Student work + rubric → a grade *recommendation* + rationale, shown on the faculty member's screen and saved to a local log. **The faculty member reads it and types the grade into Canvas by hand. The grade never leaves the machine.** |

```
 [Zone 1]  campus git host ──poll──► [Zone 3]  local LLM on faculty PC
  student work                         grade recommendation → faculty → Canvas
      │                                       (never leaves the machine)
      └─scrub + human review─► [Zone 2]  sanctioned cloud model (Gemini)
                                          comments only, no grades ──► back to student
```

The move that makes it work: the step that produces a **grade** runs only on
the faculty member's hardware; the step that touches the **cloud** produces only
**comments**, on **de-identified** text, through an **already-vetted** tool.
Risk is concentrated where it can be contained.

## What's honest about the legal side

We are **not** claiming "student classwork isn't a FERPA record." An earlier
draft leaned on *Owasso v. Falvo* (2002) for that; we've dropped it — *Falvo*
only says peer-graded papers being passed among students before the teacher
records the grade aren't "education records," not that classwork is categorically
unprotected. FerpaFlow instead relies on **data minimization** (grades and
identifiers stay local) and **sanctioned endpoints** (only tools the institution
has vetted) — which hold regardless. The open questions for counsel: is the
"scrubbed work → comments" cloud step inside our Google agreement; what counts
as adequate de-identification of student *writing*; and do students need to be
told feedback is AI-assisted. Details in [`ferpa-memo.md`](ferpa-memo.md).

## Why this matters for our department

- **A model for preservice teachers.** "Design a compliant AI workflow" beats
  "don't get caught." The planned FERPA-literacy layer (the *Owasso* facts, a
  "what gets you fired" scenario guide, a build-your-own-pipeline worksheet)
  drops straight into the TCE/CSE AI-bridge coursework.
- **A bridge between tools Miami already has.** Google Workspace (Gemini,
  NotebookLM), Canvas, and faculty interest all exist; what's missing is a
  principled workflow connecting them. FerpaFlow is a working sketch of that
  seam — and it shows locally-hosted AI and the institutional Google tools are
  *complementary*, not competing (relevant to the NVIDIA-grant exploration).
- **It scales without redesign.** Same architecture, one box swapped: Zone 1 → a
  campus git host behind SSO; Zone 3 → an IT-managed local-inference appliance;
  Zone 2 unchanged. The faculty workstation becomes a managed campus service.

## Status (as of May 2026)

Working: the local grader (`grader.py` → Ollama, a sample YAML rubric, a local
audit log) and a heuristic PII tripwire. Documented but not built: the git-host
collector and the cloud-feedback step (deliberately — the Google-agreement
questions come first). Repo to be created; this scaffold is ready to drop in.

## The ask

Not "adopt this." **A small pilot + a legal review.** One assignment, one
section, one faculty machine — then take what we learn to IT and counsel.

---

*Technology Educator Alliance (TEA) · MIT-licensed · contact: OhioMathTeacher @ GitHub*
*(Confirm author attribution before circulating publicly.)*
