"""Transactions: HTML pages under /transactions, JSON under /api/transactions.

This is the reference router — new resources should look like this one.
Routers validate input, call a repository, and shape the response. They never
write SQL.
"""

from __future__ import annotations

import sqlite3

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from ledger.dependencies import get_conn, templates
from ledger.money import parse_amount_to_cents
from ledger.repositories import transactions as repo
from ledger.schemas import TransactionCreate, TransactionRead, TransactionUpdate

router = APIRouter(tags=["transactions"])


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------


@router.get("/transactions", response_class=HTMLResponse)
def transactions_page(request: Request, conn: sqlite3.Connection = Depends(get_conn)):
    return templates.TemplateResponse(
        request,
        "transactions/list.html",
        {
            "title": "Transactions",
            "transactions": repo.list_transactions(conn, limit=200),
        },
    )


@router.post("/transactions")
def create_transaction_form(
    occurred_on: str = Form(...),
    description: str = Form(...),
    amount: str = Form(...),
    note: str = Form(""),
    conn: sqlite3.Connection = Depends(get_conn),
):
    repo.create_transaction(
        conn,
        occurred_on=occurred_on,
        description=description,
        amount_cents=parse_amount_to_cents(amount),
        note=note or None,
    )
    return RedirectResponse("/transactions", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/transactions/{transaction_id}/delete")
def delete_transaction_form(
    transaction_id: int,
    conn: sqlite3.Connection = Depends(get_conn),
):
    repo.delete_transaction(conn, transaction_id)
    return RedirectResponse("/transactions", status_code=status.HTTP_303_SEE_OTHER)


# --------------------------------------------------------------------------
# JSON API
# --------------------------------------------------------------------------


@router.get("/api/transactions", response_model=list[TransactionRead])
def api_list_transactions(
    limit: int = 100,
    offset: int = 0,
    conn: sqlite3.Connection = Depends(get_conn),
):
    return repo.list_transactions(conn, limit=limit, offset=offset)


@router.post("/api/transactions", response_model=TransactionRead, status_code=201)
def api_create_transaction(
    payload: TransactionCreate,
    conn: sqlite3.Connection = Depends(get_conn),
):
    return repo.create_transaction(
        conn,
        occurred_on=payload.occurred_on.isoformat(),
        description=payload.description,
        amount_cents=payload.amount_cents,
        category_id=payload.category_id,
        note=payload.note,
    )


@router.get("/api/transactions/{transaction_id}", response_model=TransactionRead)
def api_get_transaction(
    transaction_id: int,
    conn: sqlite3.Connection = Depends(get_conn),
):
    found = repo.get_transaction(conn, transaction_id)
    if found is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return found


@router.patch("/api/transactions/{transaction_id}", response_model=TransactionRead)
def api_update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    conn: sqlite3.Connection = Depends(get_conn),
):
    changes = payload.model_dump(exclude_unset=True)
    if changes.get("occurred_on") is not None:
        changes["occurred_on"] = changes["occurred_on"].isoformat()

    updated = repo.update_transaction(conn, transaction_id, **changes)
    if updated is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated


@router.delete("/api/transactions/{transaction_id}", status_code=204)
def api_delete_transaction(
    transaction_id: int,
    conn: sqlite3.Connection = Depends(get_conn),
):
    if not repo.delete_transaction(conn, transaction_id):
        raise HTTPException(status_code=404, detail="Transaction not found")
