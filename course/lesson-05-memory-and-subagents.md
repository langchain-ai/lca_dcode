# Lesson 5 — Memory and subagents

**You build:** CSV import, then try to break it.

---

## Part 1 — Memory

Three things load into a session, and it's worth knowing which is which.

| What | Where | Scope |
| --- | --- | --- |
| Global memory | `~/.deepagents/<agent_name>/AGENTS.md` | Every project |
| Project memory | `.deepagents/AGENTS.md` at a git root | Only in that project |
| Learned memories | `~/.deepagents/<agent_name>/memories/*.md` | Every project |

The first two are appended to the system prompt at session start. You've been
editing the project one all course.

The third is different: `dcode` writes those files itself, organised by topic
with descriptive filenames. It searches them before starting a task, checks them
when uncertain mid-task, and saves new information as it goes.

`/remember` tells it to update memory and skills from the current conversation
now, rather than waiting for it to infer what's worth keeping. Run it after
you've corrected something, then go look at what it actually wrote:

```bash
ls ~/.deepagents/*/memories/
```

Two things to check: is it true, and is it in the right scope? A Ledger-specific
convention that landed in global memory will follow you into every unrelated
project you open. Move it to `.deepagents/AGENTS.md`.

That's the habit — `/remember`, then verify. Memory that accumulates unread is
memory you'll eventually have to debug.

---

## Part 2 — Build the import

Before we can break something, we need something to break.

```
dcode
```

> Add CSV import for bank exports. There's a realistic example at
> `data/sample_bank_export.csv` and it's deliberately messy — three different
> date formats, debit and credit in separate columns rather than one signed
> amount, thousands separators inside quoted fields, at least one negative
> written in accounting parentheses, a duplicated row, a blank line, trailing
> whitespace, a row missing its description, and a row missing its amount.
>
> Requirements:
>
> - upload a file and see a preview of what would be imported before anything is
>   written
> - nothing is committed until I confirm — no silent partial imports
> - importing the same file twice doesn't create duplicates
> - rows that can't be imported are reported individually, each with the reason
>
> Write tests as you go.

Get it green. `make check` should pass and the sample file should import.

Now notice what you're about to do: hand working, tested code to something whose
only job is to prove it isn't finished.

---

## Part 3 — Why a subagent

In `dcode`, a subagent gets you three things:

**Context isolation.** It burns its own window and returns one message. Work
that reads enormously and concludes briefly costs the main agent almost nothing.

**A different model**, via the optional `model` field.

**A fresh context.** It never saw the main agent's reasoning — only the
artifacts. This is the one that matters here. The agent that wrote the parser
tests the cases it thought of while writing the parser. It can't easily test the
cases it never imagined, because those are exactly the ones its assumptions rule
out. A separate agent with no memory of that reasoning has no such blind spot.

What `dcode` does *not* give you, since docs for other tools imply otherwise:
`tools`, `middleware`, `interrupt_on`, and `skills` aren't configurable in
frontmatter, so a subagent inherits the main agent's tools. A subagent that
promises not to edit files is making a promise, not respecting a boundary.

## Install the adversary

```bash
mkdir -p .deepagents/agents
cp -r course/agents/adversary .deepagents/agents/
```

**Then open it and set the `model` field**, which ships commented out. Pick a
model from a *different provider* than your main agent — if you're running
Anthropic, point the adversary at OpenAI or Google.

That's the opposite of the usual advice about this field. The common use is a
cheaper, faster model for simple delegation, and that's real. But adversarial
thinking is the capability-heavy part of testing, so a small model is the wrong
choice here. What you want is *different* — different training, different
habits, different blind spots. A model from another provider will go after
things yours is systematically bad at noticing.

Restart `dcode`, or `/reload`.

### Read the prompt first

The load-bearing part is the hard rule: **every finding must include a
reproduction** — exact input, exact command, observed output. No repro, no
finding.

Without that rule, an adversarial agent produces a confident list of plausible
vulnerabilities it never triggered, which is worse than an empty report because
you can't separate guesses from evidence. Same discipline as lesson 1, where you
made the agent reproduce the rounding bug before fixing it.

Note the mandatory **"Attacked and held"** section too. That's what makes a
clean result legible — without it, "nothing is wrong here" and "I didn't look
hard" produce identical output.

## Part 4 — Attack it

Delegate once, to see the plain mechanic:

> Hand the CSV importer to the adversary subagent. Give it the requirements and
> tell it where the code is.

Read what comes back, and check each repro yourself before believing it. That's
the entire reason for requiring one.

## Part 5 — Fan out

Now the interesting part. `dcode` runs **dynamic subagents** when you ask for a
*workflow*: rather than doing the work itself, the agent writes an orchestration
script that calls `task()` and runs it in the code interpreter. Spawned
subagents show up live in the dynamic subagents panel, grouped into phases.

> Run a workflow that uses the adversary subagent to attack every path that
> writes a transaction to the database — the JSON API, the HTML form, and the
> CSV importer — one subagent per path.

Watch the panel. Three attackers, three isolated contexts, three independent
sets of assumptions, and your main context stays clean because each returns only
its report.

This is where the shape pays off. One adversary reading everything would exhaust
its window and blur the surfaces together. Three, each looking at one path,
won't.

## Part 6 — Fix

The adversary reports; it doesn't repair. Separating who breaks it from who
fixes it is the same principle as separating who writes it from who certifies it.

> For each confirmed finding, write a failing regression test first, then fix
> it. If you think a finding isn't worth fixing, say so and why rather than
> quietly skipping it.

That last clause matters. Some findings won't be worth fixing, and "we
considered this and accepted it" is a legitimate outcome — but it should be a
decision, not an omission.

## Done when

- `.deepagents/agents/adversary/AGENTS.md` is installed with a cross-provider
  `model` set.
- The sample file imports; re-importing it doesn't duplicate.
- Every finding is either fixed with a regression test, or explicitly accepted
  with a stated reason.
- `make check` is green.

There's no target number of findings. What you get depends on how the import was
built and which model you pointed at it, and comparing across the room is more
interesting than any particular count.

## Worth noticing

- Could you reproduce every finding yourself? Any you couldn't means the hard
  rule isn't holding, and the prompt needs tightening.
- Did it find anything in code from *earlier* lessons? It's attacking write
  paths, and two of the three predate this lesson.
- Look at `update_transaction` in `src/ledger/repositories/transactions.py`. It
  builds a SQL `SET` clause by string interpolation. Did the adversary flag it?
  Is it actually exploitable? Work that out yourself before judging whether a
  report that missed it — or one that flagged it without checking the mitigation
  — was doing its job.
- Did it stay in its lane, or start editing files? Nothing stopped it.

## Make it yours

**Rerun with a small fast model** in the `model` field and compare findings.
Clearest demonstration in the course that model choice is an engineering
decision rather than a default to accept.

**Rerun with the field removed entirely**, so the adversary inherits your main
agent's model. Same model, same blind spots — so how much does the fresh context
buy you on its own, separate from the different model? That's the experiment
that isolates the two variables.

**Point it at something else.** The budgets page, the search filters, the
category endpoints. Each was built at a different level of supervision, and it
shows.
