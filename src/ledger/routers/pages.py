"""Top-level pages: the dashboard and the (empty) reports page."""

from __future__ import annotations

import sqlite3

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from ledger.dependencies import get_conn, templates
from ledger.repositories import transactions as repo

router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, conn: sqlite3.Connection = Depends(get_conn)):
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "title": "Dashboard",
            "net_total_cents": repo.total_cents(conn),
            "transaction_count": repo.count_transactions(conn),
            "recent": repo.list_transactions(conn, limit=5),
        },
    )


@router.get("/reports", response_class=HTMLResponse)
def reports(request: Request):
    """Reports don't exist yet."""
    return templates.TemplateResponse(
        request,
        "not_built.html",
        {
            "title": "Reports",
            "heading": "No reports yet",
            "body": "Spending by category, month-over-month trends, and a running "
            "balance all belong here.",
        },
        status_code=200,
    )
