# Lesson 6 — MCP

**You build:** the reports page, designed against real data.

---

## Why this feature needs it

Every feature so far could be built by reading code. Reports can't — not well.
Deciding what a useful report looks like means knowing what's in the data: which
categories are actually used, what the spread of amounts looks like, whether any
month is unusual, whether transactions are sitting uncategorised, and what last
lesson's import actually landed.

Make sure you have data:

```bash
make seed        # 228 transactions across eight months
```

## First, the honest objection

The agent already has `bash`. It could run `sqlite3 ledger.db "SELECT ..."` and
get the same answers. So what does an MCP server actually buy you?

Three things, in ascending order of importance:

1. **A described interface.** The server advertises its tools and the shape of
   their arguments. The agent doesn't have to guess at CLI flags or fight shell
   quoting.
2. **A constrained surface.** You choose which tools are exposed. `read_query`
   without `write_query` is a boundary you can actually enforce — unlike the
   subagent prompt in lesson 5, which was only a promise.
3. **Reach beyond the shell.** This is the real answer. A browser, a hosted API,
   an OAuth'd SaaS account — things no amount of `bash` gets you.

For a local SQLite file, MCP is a convenience. Knowing that, rather than
assuming every integration must be an MCP server, is part of the lesson.

## Connect it

`.mcp.json.example` is in the project root. Copy it:

```bash
cp .mcp.json.example .mcp.json
```

It configures:

- `ledger-db` — SQLite, pointed at `./ledger.db`, restricted via `allowedTools`
  to `read_query`, `list_tables`, and `describe_table`
- `docs-langchain` — the LangChain documentation, over HTTP
- `playwright` — a real browser, for the optional exercise at the end

`.mcp.json` is git-ignored, so this stays local to you.

Restart `dcode`. Two things happen.

**A trust prompt.** Project-level MCP config is default-deny. A committed
`.mcp.json` can name a stdio command that runs on your machine, so you're shown
each server's command or URL before anything connects. Read them. This is the
most consequential prompt in the course and the one people click through
fastest.

**A tool count**, something like `✓ Loaded 6 MCP tools`. Run `/mcp` for
per-server status and the tool list.

### On `allowedTools`

The database config is read-only by design. The agent gets `read_query`, not
`write_query`. Schema changes in this project go through migrations, and an
agent with write access to `ledger.db` would route around that entirely.

Narrow the surface to what the task needs. Ask what you'd have to trust if that
line weren't there.

---

## Look before you build

Fresh session. Before asking for any code:

> You have read access to the Ledger database now. Before we build anything,
> look at what's actually in there and tell me what's worth putting on a reports
> page. What's unusual, what's missing, what would surprise me? Show me the
> queries you ran.
>
> While you're in there: last session's CSV import wrote a batch of July
> transactions. Check they landed correctly and that nothing got duplicated.

Watch what it asks the database and whether its conclusions follow from the
answers. This is also a genuine verification pass on lesson 5's work — the first
time in the course the agent can check its own past output against ground truth
rather than against its tests.

## Then build

> Replace the `/reports` placeholder with real reports:
>
> - spending by category for a chosen month, biggest first
> - total in and total out per month for the last twelve months
> - the ten largest transactions in a selected period
> - average spend per category across the whole history, shown next to the
>   current month, so an unusual month reads as unusual
>
> The aggregation goes in repository functions with tests — not ad-hoc queries
> over MCP. The MCP connection is for exploring; shipped code goes through the
> normal layers like everything else.

Note what you didn't have to say: anything about how the page should look. The
design system from lesson 4 should fire on its own, and a reports page is the
easiest place in the app to spot if it didn't — it's almost entirely figures in
columns.

## Done when

- `/mcp` shows `ledger-db` as `ok`.
- `/reports` shows all four views with real numbers.
- The numbers are right — spot-check one against a query you write yourself.
- Tests exist and `make check` is green.

## Worth noticing

- Did the report design change after it looked at the data? Compare against what
  a cold ask would have produced.
- MCP results land in your context like anything else. A broad `SELECT *` over
  228 rows is expensive. Did it query narrowly, or dump the table?
- Check the aggregation really did end up in tested repository functions.
  Convenient tool access is a good way to end up with logic somewhere it can't
  be tested.

## The one bash can't do

Enable the `playwright` server and try:

> Open `/reports` and `/transactions` in a browser, look at them, and tell me
> what's visually wrong. Check the same pages at a phone-sized viewport.

This is the case where MCP isn't a convenience. The agent can now see rendered
output — layout that breaks at narrow widths, a table that overflows, a chart
with unreadable labels. Reports are the first feature in this course where being
*wrong* and being *unusable* are different failures, and only one of them shows
up in pytest.

---

## Finishing the course

You now have project memory, a design system as a skill, a subagent, and MCP
servers. Pick something below and build it with whichever of those the task
actually calls for — including none, when that's the right answer.

**Recurring transactions.** Rent and paychecks get typed in by hand every month.
Define a recurrence, generate the entries, and let one occurrence be edited
without disturbing the rest. Genuinely hard to specify, so a good second `/goal`.

**Tags.** Free-form labels — "reimbursable", "vacation", "tax" — many-to-many,
filterable. A good test of whether the design system generalises to a resource
it has never seen.

**A confirmation on delete.** One misclick on `/transactions` and the row is
gone, with no undo.

**Editing from the UI.** The JSON API has `PATCH`; the web pages have no way to
change a transaction after it's created.

**Export.** CSV and JSON, honouring whatever filters are currently applied.

**A better dashboard.** The all-time total stops being interesting after a few
months.

**`not_built.html`.** It's doing double duty for two different pages, and by now
it should be doing none at all.
