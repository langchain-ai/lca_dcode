"""Categories: not built yet.

The table exists and transactions already reference it, but there is no way to
manage categories from the app. The routes below are placeholders so the gap is
visible in the UI instead of being a 404.

The contract is in repositories/categories.py.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from ledger.dependencies import templates

router = APIRouter(tags=["categories"])

NOT_BUILT_DETAIL = "Category management is not built yet."


@router.get("/categories", response_class=HTMLResponse)
def categories_page(request: Request):
    return templates.TemplateResponse(
        request,
        "not_built.html",
        {
            "title": "Categories",
            "heading": "No category management yet",
            "body": "Transactions can point at a category, but there's no way to "
            "create, rename, or delete one.",
        },
    )


@router.get("/api/categories")
def api_list_categories():
    raise HTTPException(status_code=501, detail=NOT_BUILT_DETAIL)


@router.post("/api/categories")
def api_create_category():
    raise HTTPException(status_code=501, detail=NOT_BUILT_DETAIL)
