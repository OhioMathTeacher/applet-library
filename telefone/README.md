# Telefone

Telephone, except the machine is every player. Hand it a page, ask it to
revise, and watch what it corrects away — round after round. It stops
itself when there is nothing left to correct.

**Live**: https://ohiomathteacher.github.io/applet-library/telefone/

This is the Generation Loss lab from
[Journaler](https://github.com/OhioMathTeacher/journaler), pulled out to
stand on its own. Same experiment, same round math, no course attached.

## How it is played

Round 0 is your page. Every **AI Revise** hands the *latest* round to the
model — not round 0 — and files the reply as the next round. The
compounding is the whole point: each round corrects a page that was
already corrected.

Three things can be asked of it, in any combination:

- clean it up & correct it
- fix grammar, spelling, punctuation
- rewrite in clear, standard English

The prompt is fixed and dull on purpose. The point isn't the prompt; it's
watching what each round erases.

## Reading a round

Each tab wears the share of your words still standing, so the tab strip
*is* the chart — there is no separate graph. Any round past 0 can be read
three ways:

- **What's left** — the machine's text as it stands
- **What this round changed** — this round against the one before it
- **What's lost** — your original page with everything gone by this round
  struck through

**Figures** gives the round's word count, sentence count, words per
sentence, share of your words remaining, and how many words this round
cut and added.

## It ends itself

Nobody decides to stop; the game does, whichever comes first:

- **Floor** — under a fifth of your words are left
- **Settled** — the percentage hasn't moved for three rounds running; the
  machine has stopped changing it
- **Cap** — 20 rounds, as a backstop

Round 0 and the ending round both stay in the tabs, side by side. That
comparison is the finding.

## Bring your own model

Telefone needs a model — the machine is the other player. **AI Setup**
takes a key you supply:

- **Groq** — free tier, no Google account needed
- **Google Gemini** — free tier
- **Anthropic Claude** — paid
- **A model on this computer** — Ollama or LM Studio; press *Find models*
  and it probes the usual ports. Nothing leaves the machine.
- **Other** — any OpenAI-compatible endpoint

No key ships with this app and none is baked in. What you type is kept in
your own browser, under storage names belonging to Telefone alone — it
will not pick up a key set in another applet on this domain, and no other
applet can read the one you set here.

Free tiers meter tokens per minute. A 500-word page spends roughly 1,400
of them per round, so a rate limit is an ordinary event here rather than a
failure: Telefone waits the time the provider names, says so on screen,
and goes again.

## What leaves your computer

The text you put in round 0 goes to whichever provider you chose, so it
can revise it — to that company, and nowhere else. Pick a local model and
not even that. Nothing is submitted, nothing is graded, and the rounds
live in your browser only. **Save rounds** writes every round and its
figures to one plain text file; the key is never written to it.
