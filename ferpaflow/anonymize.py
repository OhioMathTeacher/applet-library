#!/usr/bin/env python3
"""anonymize.py — heuristic PII detection / scrubbing for FerpaFlow.

IMPORTANT — read this before relying on it:

This module is a *tripwire*, not a guarantee. It catches obvious, structured
identifiers (emails, phone numbers, "my name is ___", student-ID-looking
numbers) and a few common give-aways. It will NOT catch the kind of
self-identifying narrative detail that reflective student writing is full of:
"in my hometown of Defiance", "my mother, who teaches third grade at the same
district", "as a transfer student from Sinclair". FERPA de-identification has a
real legal standard (a reasonable person in the school community could not
identify the student), and a regex does not meet it.

Treat a clean result here as "no red flags found", never as "safe to send to
the cloud". Human review of anything bound for the public-feedback (Gemini)
zone is part of the design, not an optional extra.

Functions:
    find_likely_pii(text) -> list[(kind, sample)]   # detect, don't modify
    redact(text)          -> (clean_text, report)   # best-effort masking
"""
from __future__ import annotations

import re

_EMAIL = re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")
# North-American-ish phone numbers; deliberately loose.
_PHONE = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)")
# "Banner"-style 8-9 digit student IDs, optionally prefixed.
_STUDENT_ID = re.compile(r"\b(?:student\s*id|banner\s*id|id\s*#?)\s*[:#]?\s*(\d{6,9})\b", re.IGNORECASE)
_BARE_LONG_NUM = re.compile(r"(?<!\d)\d{8,9}(?!\d)")
# Case-sensitive on purpose: the anchor allows a couple of casings, but the
# captured name must start uppercase, so "I am tired" doesn't get flagged.
# Name words exclude "." so we stop at a sentence boundary ("Jordan Alvarez. Reach...").
_SELF_NAME = re.compile(
    r"\b(?:[Mm]y name is|[Nn]ame:|[Ss]ubmitted by|[Ww]ritten by|[Bb]y:|[Ii] am|[Ii]'m)\s+"
    r"([A-Z][a-z'’-]+(?:\s+[A-Z][a-z'’-]+){0,2})"
)
_URL = re.compile(r"\bhttps?://\S+", re.IGNORECASE)


def _trim(s: str, n: int = 60) -> str:
    s = s.strip().replace("\n", " ")
    return s if len(s) <= n else s[: n - 1] + "…"


def find_likely_pii(text: str) -> list[tuple[str, str]]:
    """Return a list of (kind, sample) pairs for likely identifiers in *text*.

    Empty list means "no obvious structured PII" — see the module docstring for
    why that is not the same as "this text is de-identified".
    """
    hits: list[tuple[str, str]] = []
    for m in _EMAIL.finditer(text):
        hits.append(("email", m.group(0)))
    for m in _PHONE.finditer(text):
        hits.append(("phone-like", m.group(0)))
    for m in _STUDENT_ID.finditer(text):
        hits.append(("student-id", m.group(0)))
    for m in _BARE_LONG_NUM.finditer(text):
        hits.append(("8-9 digit number", m.group(0)))
    for m in _SELF_NAME.finditer(text):
        hits.append(("self-identified name", _trim(m.group(0))))
    for m in _URL.finditer(text):
        hits.append(("url", _trim(m.group(0))))
    # De-dupe while preserving order.
    seen = set()
    deduped = []
    for kind, sample in hits:
        key = (kind, sample)
        if key not in seen:
            seen.add(key)
            deduped.append((kind, sample))
    return deduped


def redact(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Best-effort masking of structured identifiers.

    Returns (redacted_text, report) where report is the same shape as
    find_likely_pii() applied to the *original* text. This is a convenience for
    the (stubbed) feedback pipeline; it is NOT a substitute for human review.
    """
    report = find_likely_pii(text)
    out = text
    out = _EMAIL.sub("[EMAIL]", out)
    out = _URL.sub("[URL]", out)
    out = _STUDENT_ID.sub("student id: [ID]", out)
    out = _PHONE.sub("[PHONE]", out)
    out = _BARE_LONG_NUM.sub("[NUMBER]", out)
    out = _SELF_NAME.sub(lambda m: m.group(0)[: m.start(1) - m.start(0)] + "[NAME]", out)
    return out, report


if __name__ == "__main__":  # tiny smoke test
    sample = (
        "My name is Jordan Alvarez. Reach me at jordan.alvarez@miamioh.edu or 513-529-1809. "
        "Student ID: 90213847. In my hometown of Piqua we never talked about this."
    )
    cleaned, found = redact(sample)
    print("FOUND:")
    for k, v in found:
        print(f"  {k}: {v}")
    print("\nREDACTED:\n" + cleaned)
    print("\nNote: 'hometown of Piqua' survived — that's the point of the docstring warning.")
