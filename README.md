# Ledger

A personal expense tracker that is deliberately unfinished.

You will finish it over the course of this class, using a coding agent for the
work. Each lesson introduces a capability and hands you a real feature to build
with it.

---

## Setup

You need [uv](https://docs.astral.sh/uv/) and Python 3.11+.

```bash
make install     # create the venv, install dependencies
make seed        # build ledger.db and fill it with sample data
make test        # should be green
make dev         # http://127.0.0.1:8000
```

`make seed` generates 228 transactions across eight months of history. It's
deterministic, so your numbers match everyone else's.

You also need Deep Agents Code:

```bash
curl -LsSf https://langch.in/dcode | bash
```

Run `dcode` from the project root — it picks up `.deepagents/AGENTS.md`
automatically.

---

## What works

Transactions are complete, end to end:

- `/transactions` — list, add, delete
- `/api/transactions` — `GET`, `POST`, `PATCH`, `DELETE`
- `/` — a dashboard with a running total and recent activity

That slice is the **reference implementation**. When you add anything new,
match its shape: migration, repository, schemas, router, registration in
`main.py`, templates, nav link, tests.

## What doesn't

Nearly everything else. `/categories` and `/reports` are placeholders. There's
no search, no budgets, no reports, no import, and at least one real bug.

What to build, and in what order, comes from the lesson briefs in `course/`.

---

## Layout

```
src/ledger/
  main.py           app factory; routers are registered here
  dependencies.py   get_conn() and the Jinja environment
  config.py         settings from the environment
  money.py          cents <-> display strings
  schemas.py        pydantic models for the JSON API
  db.py             connection helper + migration runner
  migrations/       numbered .sql files, forward-only
  repositories/     every SQL statement in the app
  routers/          every HTTP handler in the app
  templates/        Jinja templates
  static/app.css
tests/              pytest — `conn` fixture for repos, `client` for routers
scripts/seed.py     deterministic sample data
data/               a messy bank export you'll need later
course/             the lesson briefs
```

Money is stored as **integer cents**, never floats. Negative is money out.
Dates are ISO strings. Repositories never import FastAPI; routers never write
SQL. The full set of conventions is in `.deepagents/AGENTS.md`.

---

## Agent configuration

Three directories matter, and you'll fill in two of them yourself:

| Path | What it is | Status |
| --- | --- | --- |
| `.deepagents/AGENTS.md` | Project memory, loaded every session | Written for you — extend it as you learn |
| `.deepagents/skills/` | Project skills | Empty; lesson 4 supplies one |
| `.deepagents/agents/` | Project subagents | Empty; lesson 5 supplies one |
| `.mcp.json` | MCP servers | Copy from `.mcp.json.example`; lesson 6 |

`.mcp.json` is git-ignored, so your MCP credentials stay yours.

---

## Commands

| Task | Command |
| --- | --- |
| Install | `make install` |
| Run the app | `make dev` |
| Tests | `make test` |
| Lint | `make lint` |
| Autofix formatting | `make fmt` |
| Sample data | `make seed` |
| Rebuild the database | `make reset` |
| Everything, before you call it done | `make check` |

---

## The one rule

`make check` has to pass before you accept the agent's work. Not "the agent
said it was done" — you ran it and saw it pass.
