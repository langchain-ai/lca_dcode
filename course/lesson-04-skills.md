# Lesson 4 — Skills

**You build:** nothing new. You install a design system as a skill and restyle
the entire application with one prompt.

---

## Memory versus skills

You've already been using memory. `.deepagents/AGENTS.md` loads into context at
the start of every session — every session, whether it's relevant or not. That's
why it's short.

A skill is different. `dcode` reads only the `name` and `description` from each
`SKILL.md` at startup. The body is read when a task matches the description. So
a skill can be long and detailed without costing you anything on the tasks where
it doesn't apply.

|  | Memory (`AGENTS.md`) | Skill |
| --- | --- | --- |
| Loaded | Always | On match |
| Should be | Short | As long as it needs to be |
| Good for | Facts true of every task | Specifications and procedures for one kind of task |

That "as long as it needs to be" is the part worth internalising. The skill
you're about to install is roughly 300 lines. It would be absurd in
`AGENTS.md` — every backend task would pay for it. As a skill it costs two lines
until something visual comes along.

## Why a design system is the ideal skill

Look at Ledger. It's legible, and it has no visual identity at all: system
fonts, a couple of greys, whatever the previous agent run happened to do. The
budgets page you built last lesson probably doesn't match the transaction list.

A design system is the textbook case for a skill:

- **It's long.** Real specifications are — tokens, type scale, component specs,
  accessibility rules. Far too long to keep in memory.
- **It's pure reference.** The agent doesn't need to reason about it, just apply
  it. Exactly the kind of content that survives being written down.
- **It's not inferable.** No amount of reading the existing CSS tells you the
  brand colour is `#14503C`, or that headings are set in a serif.
- **It applies to a recognisable class of task and nothing else.** Which is what
  the `description` field is for.

If a rule is short and applies to every task, it's memory. If it's a
specification for a recognisable kind of work, it's a skill.

---

## Install it

The skill is written for you at `course/skills/ui-styling/SKILL.md`.

```bash
mkdir -p .deepagents/skills
cp -r course/skills/ui-styling .deepagents/skills/
```

Then `/reload` in a running session, or restart `dcode`.

## Read it first

Open `.deepagents/skills/ui-styling/SKILL.md`. It's the artefact this lesson is
about — spend a few minutes on it before you use it.

**The frontmatter** is the only part loaded at startup, and it's the entire
triggering mechanism. Note that the description names concrete surfaces, says
what the body contains, covers the case where styling is the last step of a
backend feature, and states an exclusion. Compare with the first draft most
people write:

```yaml
description: Helps with styling.
```

That matches everything and nothing.

**The body** is a specification, not advice. Look at the shape:

- Concrete values. `--brand: #14503C`, not "a deep green". A skill full of
  adjectives produces a different result every run.
- Rationale where a value looks like a mistake. `--brand` and `--credit` are the
  same colour on purpose, and the skill says so — otherwise a diligent agent
  "fixes" it.
- Exact class names, because renaming classes would turn a styling change into a
  markup change.
- Prohibitions. No gradients, no animation, one shadow. Specifications earn a
  lot of their value from ruling things out.
- Fallbacks and failure modes: the font stack degrades, and the checklist says
  to test with the font link removed.
- A checklist at the end. Long instructions get partially applied; a list gives
  the agent something to verify against when it thinks it's finished.

---

## Use it

Fresh session. One prompt, whole app:

> Restyle the entire application to match our design system. Every page —
> dashboard, transactions, categories, budgets, and the not-built reports
> placeholder. Rewrite `app.css` from scratch rather than patching it.
>
> This is presentation only. Don't change any behaviour, any route, or anything
> in the repository layer.

That's the whole prompt. No colours, no fonts, no class names, no accessibility
requirements, no mention of `app.css` structure — all of it lives in the skill
now. If you find yourself adding any of that back, the skill isn't carrying its
weight.

Doing the whole app at once is deliberate. It's a large change, but it's a
*shallow* one, and consistency is easier to achieve in a single pass than page
by page. It also means the result is unmissable: reload the browser and either
the app looks like a different product or it doesn't.

If the skill doesn't trigger on its own, that's information — the description
isn't matching. Fix it and retry before falling back to `/skill:ui-styling`.

## Check the work

Open every page.

- Serif headings, sans interface text, monospaced figures?
- Do the numbers line up vertically down each column? That's `tabular-nums`
  doing its job.
- Active nav link in brand green with an underline?
- Search the diff for `#` — any raw hex outside the `:root` block is a miss.
- **How is an over-budget category shown?** If it's a red number and nothing
  else, the skill wasn't applied. It calls for a `.badge-warn` containing an
  actual word, and it says explicitly that colour alone is never a status. This
  is the most likely thing to have been missed.
- Comment out the Google Fonts link and reload. Still deliberate, or does it
  fall apart?
- `make check` — behaviour should be untouched.

## Done when

- Every page uses the design system.
- Over-budget status is communicated by something other than colour.
- No raw colour values outside `:root`.
- The app degrades sensibly without the font link.
- `make check` is green.

---

## Make it yours

A skill you didn't write is a skill you don't trust yet.

**Break the description.** Change it to `description: Helps with styling.`,
`/reload`, and give the same prompt in a fresh session. Watch it not fire. Put
it back.

This is the single most useful thing to know about how skills work. The
description is the whole triggering mechanism, and it's the part people spend
the least time on — they write a careful 300-line body and one careless line
above it, then wonder why the skill never runs.

**Add the rule it broke.** Whatever you corrected by hand is a line the skill is
missing. Add it now, while you remember why. If the agent used `--debit` for a
delete button, say so explicitly. If it invented a panel style instead of using
`.card`, name the component it should have reached for.

**Change a token and rerun.** Set `--brand` to something else, `/reload`, and
give the same prompt in a fresh session on a clean checkout. The app should come
out consistently rebranded. If it doesn't — if the old green survives somewhere —
you've found a gap between the specification and what the agent actually did.

`/remember` will also offer to update memory and skills from the conversation.
Try it after a correction and see what it proposes, then decide whether the
suggestion belongs in the skill or in `AGENTS.md`, and be able to say why.
