-- Initial schema.
--
-- Amounts are integer cents. Negative is money out, positive is money in.
-- Dates are ISO strings (YYYY-MM-DD) so lexical sort == chronological sort.

CREATE TABLE categories (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL UNIQUE,
    kind       TEXT NOT NULL CHECK (kind IN ('expense', 'income')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE transactions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    occurred_on  TEXT NOT NULL,
    description  TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    category_id  INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    note         TEXT,
    created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_transactions_occurred_on ON transactions (occurred_on);
CREATE INDEX idx_transactions_category_id ON transactions (category_id);
