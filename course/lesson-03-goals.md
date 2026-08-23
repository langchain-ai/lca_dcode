# Lesson 3 — Goals and rubrics

**You build:** monthly budgets.

The last two lessons handed you a specification. This one hands you a sentence.
That's the point — budgets are underspecified on purpose, and closing that gap
is what `/goal` is for.

---

## Goal or rubric?

- `/goal <objective>` — you have one measurable objective and want the agent to
  draft acceptance criteria before it starts. You review the criteria, then it
  works against them until they're met. The goal survives across turns.
- `/rubric set <criteria>` — you already know the criteria and want them applied
  as a standing quality gate.

Useful commands: `/goal show`, `/goal amend <feedback>`, `/goal pause`,
`/goal resume`, `/rubric next <criteria>` for a one-turn gate.

Budgets are a goal. You know roughly what you want and you'd rather argue about
the criteria than write them out.

---

## Set the goal

```bash
dcode
```

Then, deliberately thin:

> /goal Add monthly per-category budgets to Ledger, with progress against the
> limit visible on the dashboard.

The agent drafts acceptance criteria. **This is the part of the lesson that
matters.** Read them properly before accepting.

Here's what you actually want, so you can tell what the draft is missing:

- A monthly spending limit can be set for each category.
- The current month shows, per category: spent, remaining, and percentage used.
- Categories over their limit are visibly flagged, not merely calculated.
- A budget carries forward month to month until it's changed. Setting a budget
  in March means April has one too.
- A category with no budget is not the same as a category with a budget of zero.
- The dashboard shows a summary; a dedicated page shows the full detail.
- Tests exist and `make check` passes.

Carry-forward and the no-budget-vs-zero distinction are the two a first draft
almost always misses. Vague criteria — "budgets work correctly" — are worse than
missing ones, because they read as covered. If you can't check it, it isn't a
criterion.

Sharpen the draft with `/goal amend` rather than accepting and correcting later:

> /goal amend Budgets need to carry forward — if I set one in March, April
> should have the same budget until I change it. And a category with no budget
> set should display differently from one budgeted at zero, not just show 0%.

Then let it work. `/goal show` tells you where it thinks it is.

## Done when

The criteria you accepted are met — that's the exercise. Check a couple by hand
rather than taking the agent's word for it.

## Worth noticing

- Compare the accepted criteria against what actually got built. Where they
  differ, was the criterion too loose, or did the agent drift?
- Did having a goal reduce how often you needed to intervene mid-task, compared
  with lesson 2?
- A goal doesn't verify itself. The agent grades its own work against the
  criteria, and it's capable of being generous.

## The contrast: rubrics

Do something small with `/rubric set` instead, so you can feel the difference.
The transaction list stops at 200 rows with no pagination — try that:

> /rubric set tests pass; ruff is clean; no files outside src/ and tests/ are
> touched; the JSON API and the HTML pages stay consistent with each other

Then:

> The transaction list is capped at 200 rows and there's no way to see past
> that. Add pagination to both `/transactions` and `/api/transactions`, and keep
> the page position in the URL so it survives a refresh.

A goal drives the work. A rubric gates it. The rubric above says nothing about
pagination and would apply just as well to the next five tasks — which is
exactly when to reach for one.
