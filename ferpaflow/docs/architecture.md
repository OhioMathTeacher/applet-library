# FerpaFlow — architecture & trust boundaries

Audience: IT / CIO / anyone who needs to see exactly what data crosses which
line. One page. Companion to [`ferpa-memo.md`](ferpa-memo.md) (legal framing)
and [`one-pager.md`](one-pager.md) (the colleague-facing pitch).

## The three zones and what crosses each boundary

```
                         FACULTY WORKSTATION (or, at scale, IT-managed campus services)
                         ┌───────────────────────────────────────────────────────────┐
  ZONE 1                 │   ZONE 3                                                   │
  Submissions            │   Local grade recommender                                  │
  ┌──────────────────┐   │   ┌───────────────────────────────────────────────────┐    │
  │ institution-     │   │   │ grader.py  ──►  Ollama (localhost:11434)           │    │
  │ controlled git   │   │   │   in : anonymized submission + rubric YAML         │    │
  │ host (GitLab CE/ │   │   │   out: grade rec + rationale  ──► terminal         │    │
  │ Gitea / dept SSH)│   │   │                               ──► logs/*.jsonl     │    │
  │                  │   │   │ Ollama: no internet. No listening port. Outbound   │    │
  │ private GitHub   │   │   │ only. Model weights + inference 100% local.        │    │
  │ repo = pilot     │   │   └───────────────────────────────────────────────────┘    │
  │ stopgap only     │   │            │ faculty reads recommendation                  │
  └────────┬─────────┘   │            ▼                                               │
           │             │   Canvas  ◄── faculty types the grade of record, by hand   │
           │ collector.py│                                                            │
           │ polls OUT;  └───────────────────────────────────────────────────────────┘
           │ no inbound
           ▼
  (anonymize + human review)
           │
           ▼  scrubbed submission + rubric  — NO grade, NO score
  ZONE 2
  ┌──────────────────────────────────────────────┐
  │ institution-sanctioned cloud model           │
  │ (Miami: Google Gemini / NotebookLM,          │
  │  under the existing Workspace DPA)           │
  │   in : de-identified text + rubric           │
  │   out: rubric-aligned COMMENTS (no scores)   │
  └────────┬─────────────────────────────────────┘
           │ comments returned to the student via the git host
           ▼
        student
```

## Boundary table

| # | Boundary crossed | What goes across | What must NOT | Control |
|---|---|---|---|---|
| B1 | git host → faculty machine (`collector.py`) | student submission text | — | outbound poll only; no service listening on the faculty machine |
| B2 | faculty machine → cloud model (`feedback.py`, Zone 2) | **de-identified** submission + rubric | any grade or score; any name/ID/self-identifying detail | runs only after `anonymize.py` **and** a human review; sanctioned endpoint only; what-was-sent logged locally |
| B3 | cloud model → student (via git host) | rubric-aligned qualitative comments | scores, grades | comments only by construction (Zone 2 never computes a grade) |
| B4 | faculty machine → Ollama (`grader.py`, Zone 3) | anonymized submission + rubric | — | `localhost` only; Ollama has no internet route |
| B5 | Zone 3 → terminal / `logs/*.jsonl` | grade recommendation + rationale | leaving the machine (log is git-ignored) | local disk only; faculty re-keys the grade into Canvas manually |
| B6 | faculty → Canvas | the final grade of record | — | normal Canvas workflow; a human decision, not an API write from this pipeline |

## Properties this buys

- **Grades are confined to the workstation and Canvas.** No grade is ever
  produced, transmitted, or stored in Zone 1 or Zone 2.
- **The only cloud hop carries de-identified, grade-free text through a system
  already under an institutional agreement.** No personal API keys, no consumer
  AI accounts.
- **No inbound network surface.** `collector.py` polls outward; Ollama listens
  only on loopback. Nothing accepts connections from the campus network or the
  internet.
- **Auditable.** Every Zone-3 prompt/response is logged locally; the (future)
  Zone-2 step logs what text left the machine.

## Failure modes this is built to prevent

1. Faculty pasting a student essay *with the name on it* into consumer ChatGPT/
   Gemini/Claude — no agreement, unknown data handling. (FerpaFlow gives them a
   sanctioned path for comments and a local path for grades.)
2. Grades landing in a tool not cleared to hold them. (They never leave Zone 3.)
3. "Anonymized" text that still identifies the student in prose. (Tripwire +
   *mandatory human review* before B2; see `anonymize.py` docstring for why the
   tripwire alone is not enough.)

## Open items before Zone 2 is wired up

- Confirm with IT/counsel which Gemini surface is in scope under Miami's DPA and
  with what retention / training terms.
- Confirm "scrubbed classwork + rubric, no grade" is a permitted use under that
  agreement — in writing.
- Decide the student-disclosure mechanism (syllabus statement / per-assignment
  notice) for AI-generated feedback.

## Scaling note (the CIO version)

Single-faculty and campus deployments are the same architecture with one box
swapped: Zone 1 becomes a campus-run GitLab/Gitea behind SSO; Zone 3 becomes an
IT-managed local-inference appliance (cf. the NVIDIA-grant exploration); Zone 2
is unchanged (existing Google Workspace tooling). The faculty workstation
becomes a managed service. Locally-hosted inference and the institutional Google
tools are complementary halves of one compliant workflow — not competitors.
