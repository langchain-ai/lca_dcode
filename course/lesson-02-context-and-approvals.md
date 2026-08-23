# Lesson 2 — Approval modes and context

**You build:** category management in Manual mode, then transaction search in
Auto mode.

This is the lesson where you feel the tradeoff rather than being told about it.
Same codebase, comparable tasks, two different levels of supervision.

---

## The three modes

| Mode | How | What it does |
| --- | --- | --- |
| Manual | default | Asks before every gated action |
| Auto | `-y` / `--auto-approve`, or `Shift+Tab` | A classifier approves the safe ones |
| YOLO | `--yolo` | No review at all |

`Shift+Tab` toggles Manual and Auto mid-session, so you don't have to restart to
change your mind.

---

## Part 1 — Categories, in Manual mode

Start in the default mode:

```bash
dcode
```

Your prompt:

> Transactions can be filed under a category — the table exists and the foreign
> key is already there — but there's no way to manage categories from the app.
> `/categories` is a placeholder and `/api/categories` returns 501.
>
> Build it out:
>
> - list, create, rename, and delete categories
> - a category has a name and a kind, where kind is either "expense" or "income"
> - names are unique; a duplicate should come back as a 409, not a 500
> - deleting a category must not delete its transactions — they just become
>   uncategorised
> - once this works, the add-transaction form on `/transactions` needs a
>   category picker
>
> `src/ledger/repositories/categories.py` has stubs with the contract in the
> docstrings. `tests/test_categories_api.py` has the tests already written and
> skipped — remove the skip marks and make them pass.

Now do the thing this lesson is actually about: **count your approvals.** Don't
batch-approve on autopilot. For each one, ask yourself whether you'd have caught
a mistake in it.

This touches eight files. The migration is already done, but there's a
repository, schemas, a router, registration in `main.py`, a template, a nav
link, the transaction form, and tests. You'll approve a lot.

### Then look at your context

Check how much of the window this consumed. Note the number.

Two things drove it up: the files the agent read to find the pattern, and the
back-and-forth of the approval loop itself. The second one is the surprise —
supervision isn't free.

If a compaction happened partway through, notice what the agent forgot. That's
usually where a project convention should have been in `AGENTS.md` instead of
discovered mid-session.

---

## Part 2 — Search, in Auto mode

Fresh session, auto-approve on:

```bash
dcode -y
```

Your prompt:

> `/transactions` shows the 200 most recent rows and there's no way to find
> anything older than that. I want to be able to answer "what was that hardware
> store thing back in April?"
>
> Add search and filtering to the transaction list:
>
> - free-text search across both description and note
> - filter by category
> - filter by date range, either bound optional
> - the filters combine — category *and* date range *and* text at once
>
> Two constraints. Filtering happens in the SQL query, not in Python after
> fetching the rows. And the filter state lives in the URL, so a filtered view
> can be bookmarked and shared.
>
> Write the tests as you go.

Then let it run. Don't intervene unless it's clearly going sideways.

Those two constraints are in the prompt because they're the ones an
unsupervised agent gets wrong. Notice that you had to know that in advance.

## Compare

Answer these honestly:

- Which run was faster in wall-clock time?
- Which used more context, and why?
- Did Auto mode do anything you would have rejected in Manual?
- Of all the approvals you gave in Part 1, how many were load-bearing?
- Which mode would you pick for a task in code you didn't write?

The useful answer usually isn't "Auto is better." It's a rule about *when*.

## Done when

- `tests/test_categories_api.py` has no skip marks and passes.
- The transaction form has a working category picker.
- Search and filtering work, with tests, and the filtering is in the SQL.
- A filtered view is a linkable URL.
- `make check` is green.

## Worth noticing

The category picker was one bullet in a long prompt. Did it get built, or did
the feature ship half-wired? Requirements buried in the middle of a list are the
ones that go missing — worth knowing about yourself as much as about the agent.
