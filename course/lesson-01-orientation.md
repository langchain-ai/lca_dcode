# Lesson 1 — Orientation

**You build:** a fix for a rounding bug in the amount field.

---

## Before you start

```bash
make install
make seed
make test        # green
make dev         # look around at http://127.0.0.1:8000
```

Then start the agent from the project root:

```bash
dcode
```

## Get oriented

Ask the agent to explain the codebase before you ask it to change anything:

> Walk me through how a transaction gets from the web form into the database.
> Which files are involved, and in what order?

Compare its answer against the files yourself. You're checking two things: that
the answer is right, and that `.deepagents/AGENTS.md` gave it enough to work
from. If the agent got something wrong that the project notes should have
covered, that's a gap in the notes, not a failure of the agent.

## The bug

Add a few transactions through the form at `/transactions` — try `4.35`,
`129.95`, `12.45`. Then look at what actually landed:

```bash
sqlite3 ledger.db "SELECT description, amount_cents FROM transactions ORDER BY id DESC LIMIT 5"
```

Some of those are a cent off. Here's your prompt:

> When I add a transaction through the web form, the amount is sometimes stored
> one cent low. Entering 4.35 gives me 434 in the database instead of 435.
> 129.95 becomes 12994. 1050.10 becomes 105009. Other amounts are fine — 12.45
> and 56.11 both come through correctly, which is why I didn't notice for a
> while. Adding the same amounts through the JSON API works properly; it's only
> the form.
>
> Reproduce this with a failing test before you change any code. I want to see
> the test fail, then see it pass.

That last paragraph is the important half of the prompt. A fix without a test
can silently come undone later, and an agent asked only to "fix it" will
usually just fix it.

## Done when

- A test exists that fails against the old code and passes against the new.
- `make check` is green.

## Worth noticing

- How much of the codebase did the agent read to answer your first question?
- Did it actually run the test to confirm the failure, or did it assert the
  failure and move on? Those are very different things, and the second one looks
  exactly like the first in a transcript.
- The JSON API doesn't have this bug. Ask the agent why not — the answer is
  about where validation lives, and it's the reason for the layer rules in
  `.deepagents/AGENTS.md`.

## Try changing the prompt

Start a fresh session and ask for the fix without the reproduction requirement:

> Amounts entered in the web form are sometimes a cent low. Fix it.

Compare the two runs. Same bug, same codebase, different quality of outcome — and
the only variable was what you typed.
