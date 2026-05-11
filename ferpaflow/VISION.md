# FerpaFlow: A FERPA-Aware AI Grading Pipeline for Higher Education

> *Built for educators who want to use AI responsibly — not just to claim they're compliant.*

> **Revision note (May 2026):** this version corrects two things from the first
> draft. (1) The legal framing no longer leans on "classwork isn't a FERPA
> record" — that overreads *Owasso v. Falvo*; see [Legal foundation](#legal-foundation)
> and [`docs/ferpa-memo.md`](docs/ferpa-memo.md). (2) Zone 1 now specifies an
> *institution-controlled* git host, with a private GitHub repo named only as a
> single-faculty pilot stopgap. Nothing here is legal advice or has been
> reviewed by counsel.

---

## The problem

Faculty increasingly want generative AI to help with grading and feedback. The
tools exist; the desire is real. But most educators are left choosing between
two bad options:

1. **Paste student work into a consumer AI tool** (ChatGPT, Gemini, Claude) and
   hope — putting potentially protected records into a system with no
   institutional agreement and no idea where the data goes.
2. **Avoid AI entirely** and keep grading 150 reflections by hand.

There's a third option, and it's mostly about *where the data lives*, not about
finding a loophole.

---

## The solution: a split-architecture pipeline

FerpaFlow splits the workflow into three zones, each with its own data
classification and tooling:

```
┌─────────────────────────────────────────────────────────────────┐
│ ZONE 1 — STUDENT SUBMISSIONS                                    │
│ Institution-controlled git host (campus GitLab CE / Gitea, or   │
│ bare repos over SSH on a department server, behind campus SSO).  │
│ A private GitHub repo is a stopgap for a one-faculty pilot only. │
│ → No third-party processor in the loop when self-hosted.        │
└───────────────────────────┬─────────────────────────────────────┘
                            │ outbound poll only — no open ports
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ ZONE 2 — RUBRIC-BASED FEEDBACK (no grades, scrubbed input)      │
│ Institution-sanctioned cloud model — at Miami, Google Gemini /  │
│ NotebookLM under the existing Workspace for Education agreement. │
│ → Qualitative, rubric-aligned comments. No scores. No grades.   │
│ → Input de-identified AND human-reviewed before it's sent.      │
└───────────────────────────┬─────────────────────────────────────┘
                            │ comments returned to the student
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ ZONE 3 — GRADE RECOMMENDATIONS (local only)                     │
│ Local LLM (Ollama), air-gapped from the internet.               │
│ → Outbound-only; no listening service.                          │
│ → Recommendation + rationale printed to the faculty terminal.   │
│ → Local JSONL audit log; never leaves the machine.              │
│ → Faculty enters the grade of record in Canvas, by hand.        │
└─────────────────────────────────────────────────────────────────┘
```

**The key design move:** the step that produces a *grade* runs entirely on the
faculty member's own hardware, and the step that touches a cloud service
produces only *comments*, on *de-identified* text, through a *sanctioned*
endpoint. Risk is concentrated where it can be contained — and contained there.

---

## Legal foundation

This is the part most worth getting right before the CIO meeting, because
counsel will go straight here.

| Element | Honest status | Notes |
|---|---|---|
| Student classwork generally | ⚠️ **Often part of an education record once submitted to and used by the instructor.** | *Owasso v. Falvo*, 534 U.S. 426 (2002), held only that **peer-graded papers, while being passed among students before the teacher records the grade,** aren't "education records." It does **not** establish that classwork is categorically unprotected. Do not build on the broad reading. |
| The pipeline's actual safeguard | ✅ **Data minimization + sanctioned endpoints.** | Grades and identifiers stay on the local machine; the only cloud hop carries de-identified, grade-free comments through a system already under an institutional agreement. |
| Numerical / letter grades | 🔒 FERPA-protected. **Kept local, full stop.** | Never produced, transmitted, or stored outside Zone 3 + Canvas. |
| Names / IDs / self-identifying detail in submissions | 🔒 Must be removed before any cloud call — and `anonymize.py` is a *tripwire*, not a guarantee. | FERPA de-identification has a real standard (no reasonable person in the school community could identify the student). Reflective writing leaks identity in prose ("my hometown of ___") that regexes miss. Human review is part of the design. |
| The Zone-1 git host | ✅ if institution-controlled; ⚠️ if it's `github.com`. | A self-hosted host means no third-party processor for intake. A private GitHub repo is still a third-party service that may not be covered by an existing agreement — acceptable only as a pilot, with minimal identifying content. |

See [`docs/ferpa-memo.md`](docs/ferpa-memo.md) for the two-paragraph version to
hand to counsel.

---

## Why a local LLM for the grading step

- **No vendor data agreement needed** for the one step that handles grades.
- **No outbound student data** in that step — ever.
- **Full local auditability** — every prompt and response logged on the machine.
- **Works offline** — no dependence on internet or API availability while grading.
- **No per-grade API cost.**

Models worth trying: Llama 3, Mistral 7B, Qwen 32B. Qwen 32B has handled
nuanced written-work evaluation best in informal testing; Llama 3 8B is fine for
a laptop demo.

---

## How this scales to Miami

The single-faculty setup and the campus setup are the *same architecture* with
one box swapped:

- **Today (one faculty member):** Zone 1 = a repo; Zone 3 = Ollama on the
  professor's workstation.
- **At campus scale:** Zone 1 = a campus-run GitLab/Gitea behind SSO; Zone 3 =
  an IT-managed local-inference appliance (the kind of thing Miami's NVIDIA-grant
  exploration points at). The faculty workstation becomes a managed campus
  service. Zone 2 stays exactly as is — the existing Google Workspace tooling.

That's the pitch to the CIO: locally-hosted inference and the institutional
Google tools aren't competitors — they're two halves of one compliant workflow,
and FerpaFlow is a working sketch of the seam between them. The ask is a **pilot
plus a legal review**, not a launch.

---

## What this is not

- ❌ Not automated grading — faculty review every recommendation.
- ❌ Not a replacement for human judgment.
- ❌ Not a product — open infrastructure, fork it.
- ❌ Not cloud-dependent for the parts that carry risk.
- ❌ Not cleared by any legal office yet — see the memo.

---

## Roadmap

### Phase 1 — MVP (target: this week)
- [x] `grader.py` — Ollama local inference with a rubric prompt
- [x] Sample rubric (YAML) for a written-reflection assignment
- [x] Local JSONL audit log
- [x] Heuristic PII tripwire (`anonymize.py`)
- [x] README + setup instructions
- [x] `docs/architecture.md` (data-flow one-pager) + `docs/ferpa-memo.md` (legal framing for counsel)
- [ ] One run-through of the demo on real faculty hardware

### Phase 2 — feedback integration
- [ ] `feedback.py` — sanctioned-cloud-model integration (Miami: Gemini)
- [ ] Return comments to students via the git host (file or MR/PR comment)
- [ ] Strengthen the anonymization step; bake human review into the flow
- [ ] Get the Workspace-DPA scope questions answered in writing

### Phase 3 — FERPA literacy layer
- [ ] Interactive FERPA explainer (the *Owasso* facts, what is / isn't a record)
- [ ] "What gets you fired" scenario guide for preservice teachers
- [ ] "Design your own compliant pipeline" worksheet
- [ ] Integration with the TCE/CSE AI-bridge coursework

### Phase 4 — broader sharing
- [ ] Clean public release
- [ ] Documentation site
- [ ] TEA network demo
- [ ] Teacher-education journal write-up

---

## Built with

- Python 3.11+
- [Ollama](https://ollama.com) — local LLM inference
- [PyYAML](https://pyyaml.org), [Requests](https://requests.readthedocs.io)
- *(Phase 2)* an institution-controlled git host; the sanctioned cloud model's API; Canvas (manual, faculty-initiated grade entry)

---

## Contact

OhioMathTeacher @ GitHub — Technology Educator Alliance (TEA).
*(Confirm author attribution before this circulates publicly.)*

## License

MIT. Fork it, adapt it, share it. Leave something back.
