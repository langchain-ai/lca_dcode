# The course

Six lessons. Each one introduces a capability of the coding agent and gives you
a real piece of Ledger to build with it.

| Lesson | Capability | You build |
| --- | --- | --- |
| [01](lesson-01-orientation.md) | Reading a codebase, first task | A rounding bug in the amount field |
| [02](lesson-02-context-and-approvals.md) | Approval modes, context | Category management, then search |
| [03](lesson-03-goals.md) | `/goal` and `/rubric` | Monthly budgets |
| [04](lesson-04-skills.md) | Installing and tuning a skill | A design-system restyle of the whole app |
| [05](lesson-05-memory-and-subagents.md) | Memory and subagents | CSV import |
| [06](lesson-06-mcp.md) | Connecting MCP servers | Reports |

By the end, most of the app works and `make check` is still green.

## How the prompts work

Every lesson gives you the prompt to start from, in a block like this:

> Add a thing that does the thing, and here is exactly what the thing has to do.

Paste it and go. But read it first — the prompt *is* the specification. There's
no ticket system, no requirements doc, nothing else in the repo that describes
the work. If it isn't in what you typed, the agent doesn't know about it.

That's deliberate, and it's the habit worth building. Most of the time an agent
produces the wrong thing, it produced exactly what it was asked for.

Once you've done a couple, start changing the prompts. Cut a requirement and see
what the agent assumes. Add a constraint and see whether it holds. The supplied
wording is a starting point, not a script.

## Two things that apply to every lesson

**Verify, don't trust.** The agent will tell you it's finished. Run
`make check` yourself. When it reports a passing test suite, look at the output.
This gets more important, not less, as the lessons give the agent more autonomy.

**Read the diff.** Even in the lessons where you barely intervene, read what
changed before you commit. The point of the course is judgement about when to
loosen the reins, and you can't build that without seeing what happens when you
do.

## On tests

Category management is the only feature that ships with tests, in
`tests/test_categories_api.py`, currently skipped. Everything after lesson 2,
you specify yourself — deciding what "done" means is the work, which is exactly
what `/goal` and `/rubric` are for.
