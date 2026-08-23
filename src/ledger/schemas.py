"""Pydantic request/response models for the JSON API."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator


class TransactionCreate(BaseModel):
    occurred_on: date
    description: str = Field(min_length=1, max_length=200)
    amount_cents: int
    category_id: int | None = None
    note: str | None = Field(default=None, max_length=1000)

    @field_validator("description")
    @classmethod
    def strip_description(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("description cannot be blank")
        return stripped


class TransactionUpdate(BaseModel):
    occurred_on: date | None = None
    description: str | None = Field(default=None, min_length=1, max_length=200)
    amount_cents: int | None = None
    category_id: int | None = None
    note: str | None = Field(default=None, max_length=1000)


class TransactionRead(BaseModel):
    id: int
    occurred_on: date
    description: str
    amount_cents: int
    category_id: int | None = None
    category_name: str | None = None
    note: str | None = None
    created_at: datetime
