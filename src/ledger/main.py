"""Application entrypoint.

`app` is what uvicorn serves. `create_app()` exists so tests can build a fresh
instance pointed at a temporary database.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from ledger import db
from ledger.config import get_settings
from ledger.dependencies import PACKAGE_DIR
from ledger.routers import categories, pages, transactions


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Bring the schema up to date before serving the first request."""
    conn = db.connect(get_settings().database_path)
    try:
        db.migrate(conn)
    finally:
        conn.close()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Ledger", version="0.1.0", lifespan=lifespan)
    app.mount("/static", StaticFiles(directory=str(PACKAGE_DIR / "static")), name="static")

    # Every new resource adds one line here.
    app.include_router(pages.router)
    app.include_router(transactions.router)
    app.include_router(categories.router)

    return app


app = create_app()
