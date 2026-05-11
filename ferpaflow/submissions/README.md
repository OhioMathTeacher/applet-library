# submissions/

Phase-1 intake for FerpaFlow is just this folder: drop one plain-text file per
student submission in here, then run `grader.py`.

```
python ../grader.py --rubric ../rubric/written-reflection.yaml --submissions .
```

## Rules

- **Synthetic examples only in version control.** The repo ships `example-01.txt`
  and `example-02.txt` so the demo runs out of the box. Everything else in this
  folder is git-ignored on purpose (see `../.gitignore`). Do not commit real
  student work — not here, not anywhere in this repo.
- **One submission per file.** Plain `.txt`. Filenames should be non-identifying
  (`submission-04.txt`, not `jane_doe_essay.txt`).
- **Scrub before the cloud step.** The local grader never leaves your machine, so
  it tolerates whatever's in here. The (future) `feedback.py` cloud step does
  not — anything bound for that path must be de-identified and human-reviewed
  first. `../anonymize.py` is a tripwire, not a guarantee.

## When `collector.py` lands (Phase 2)

It will populate this folder automatically by polling an institution-controlled
git host, and run the PII tripwire over each new file. Until then, this is a
manual drop folder — which is also exactly what you want for the CIO demo:
nothing magic, every step inspectable.
