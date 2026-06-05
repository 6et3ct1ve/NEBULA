import sqlite3
from datetime import datetime

from db import queries


def create_transaction(
    conn: sqlite3.Connection,
    person_id: int,
    category_id: int,
    amount: float,
    date: str,
    currency_id: int = 1,
    note: str = "",
) -> int:
    # Check values before add transaction

    if (
        conn.execute("SELECT id FROM persons WHERE id = ?", (person_id,)).fetchone()
        is None
    ):
        raise ValueError(f"Person {person_id} does not exist")
    if (
        conn.execute(
            "SELECT id FROM categories WHERE id = ?", (category_id,)
        ).fetchone()
        is None
    ):
        raise ValueError(f"Category {category_id} does not exist")
    if not isinstance(amount, (int, float)):
        raise ValueError(f"Object {amount} is not number")
    if (
        conn.execute(
            "SELECT id FROM currencies WHERE id = ?", (currency_id,)
        ).fetchone()
        is None
    ):
        raise ValueError(f"Currence {currency_id} does not exist")

    fx_rate_snapshot = conn.execute(
        "SELECT rate_to_uah FROM currencies WHERE id = ?", (currency_id,)
    ).fetchone()

    try:
        datetime.strptime(date, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError(f"Invalid date format: {date}. Expected YYYY-MM-DD HH:MM")

    row = conn.execute(
        "SELECT is_income FROM categories WHERE id = ?", (category_id,)
    ).fetchone()
    type_ = "income" if row["is_income"] else "expense"

    return queries.add_transaction(
        conn,
        person_id,
        category_id,
        currency_id,
        amount,
        fx_rate_snapshot,
        type_,
        date,
        note,
    )


def delete_transaction(conn: sqlite3.Connection, transaction_id: int) -> None:
    row = conn.execute(
        "SELECT id, date FROM transactions WHERE id = ?", (transaction_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"Transaction {transaction_id} does not exist")

    date_now = datetime.now()
    date = datetime.strptime(row["date"], "%Y-%m-%d %H:%M")
    if (date_now - date).days > 30:
        raise ValueError(f"Transaction {transaction_id} is older than 30 days")

    return queries.delete_transaction(conn, transaction_id)
