# FerpaFlow

A split-architecture pipeline for using AI to help grade student work **without
putting grades or identifiable student records into a system that isn't cleared
to hold them.**

The idea in one breath: student classwork and instructor feedback flow through
institution-sanctioned tools (and never carry grades); the *grading* step runs
on a local LLM on the faculty machine, air-gapped from the internet; the faculty
member reads the recommendation and types the grade of record into Canvas
themselves. Grades never leave the local machine.

> **Status: early scaffold.** `grader.py` works against a local Ollama instance.
> `collector.py` and `feedback.py` are documented stubs (Phases 2). The legal
> framing in `docs/ferpa-memo.md` is written *for counsel to review*, not as
> cleared advice — see that file and `VISION.md`.

> **Not legal advice.** Nothing here has been reviewed by university counsel.
> Treat the FERPA discussion as a starting point for that conversation, not a
> substitute for it.

---

## The three zones

```
ZONE 1 — Submissions        institution-controlled git host (campus GitLab/Gitea,
                            or dept SSH; private GitHub repo only as a pilot stopgap)
        │  outbound poll only, no open ports
        ▼
ZONE 2 — Public feedback    institution-sanctioned cloud model (Miami: Google Gemini /
   (no grades, scrubbed)    NotebookLM, under the existing Workspace DPA)
        │  rubric-aligned comments returned to the student
        ▼
ZONE 3 — Grade rec          local LLM (Ollama), no internet, outbound-only
   (local only)             → recommendation + rationale printed to the terminal
                            → local JSONL audit log (stays on the machine)
                            → faculty enters the final grade in Canvas, by hand
```

Full data-flow detail, including exactly what crosses each boundary, is in
[`docs/architecture.md`](docs/architecture.md).

---

## Quick start (Zone 3 — the local grader)

You need Python 3.11+ and [Ollama](https://ollama.com) running locally.

```bash
# 1. install Ollama, then pull a model (Qwen 32B recommended for written work;
#    Llama 3 8B is fine for a quick demo on a laptop)
ollama pull qwen2.5:32b      # or: ollama pull llama3:8b
ollama serve                 # if it isn't already running as a service

# 2. python deps
cd ferpaflow
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. run the grader against the synthetic examples
python grader.py --rubric rubric/written-reflection.yaml --submissions submissions
#   smaller model:
python grader.py --rubric rubric/written-reflection.yaml --model llama3:8b
```

You'll get a rubric-by-rubric recommendation per submission on the terminal, and
a JSONL line per submission appended to `logs/grader.jsonl` (git-ignored — it
holds student work and stays on your machine).

Try the PII tripwire on its own:

```bash
python anonymize.py
```

---

## Files

| Path | What it is | Status |
|---|---|---|
| `grader.py` | Zone 3. Reads `submissions/`, calls local Ollama with the rubric, prints recommendation + rationale, appends to local audit log. | working |
| `anonymize.py` | Heuristic PII tripwire (emails, IDs, "my name is ___", …). A red-flag detector, **not** a de-identification guarantee — read its docstring. | working |
| `collector.py` | Zone 1. Poll an institution-controlled git host for new submissions. | stub (Phase 2) |
| `feedback.py` | Zone 2. Send *scrubbed* work + rubric to the sanctioned cloud model, return comments (no grades). | stub (Phase 2) |
| `rubric/*.yaml` | Faculty-defined, version-controlled rubrics. One per assignment type. | sample included |
| `submissions/` | Phase-1 intake: a folder of `.txt` files. Synthetic examples only in git. | sample included |
| `logs/` | Local audit log lands here. Git-ignored. | — |
| `docs/one-pager.md` | Colleague-facing one-page vision summary (Teacher Ed / CS). | draft |
| `docs/ferpaflow-onepager.html` | Same one-pager as a self-contained, print-to-PDF HTML page with the three-zone graphic. | draft |
| `docs/architecture.md` | Data-flow / trust-boundary writeup with a per-boundary table. For the CIO / IT conversation. | draft |
| `docs/ferpa-memo.md` | The legal framing, written for counsel to review. Includes the *Owasso* correction. | draft |
| `VISION.md` | The longer pitch / vision statement. | draft |

---

## What FerpaFlow is not

- Not automated grading — the faculty member reviews every recommendation and
  enters the grade themselves.
- Not a replacement for human judgment.
- Not a product — it's a reference architecture meant to be forked and adapted.
- Not cloud-dependent for the parts that carry risk (the grading step).
- Not cleared by anyone's legal office. Yet. That's the point of `ferpa-memo.md`.

## License

MIT.
