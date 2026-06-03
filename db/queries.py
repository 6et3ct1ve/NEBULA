def add_transaction(
    conn,
    person_id,
    category_id,
    currency_id,
    amount,
    fx_rate_snapshot,
    type_,
    date,
    note,
):
    # Add a new transaction to the database

    if type_ not in ("income", "expense"):
        raise ValueError(f"Invalid transaction type: {type_}")

    conn.execute(
        """
        INSERT INTO transactions (
            person_id,
            category_id, currency_id,
            amount, fx_rate_snapshot, type, date, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            person_id,
            category_id,
            currency_id,
            amount,
            fx_rate_snapshot,
            type_,
            date,
            note,
        ),
    )
    conn.commit()

    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def add_person(conn, name):
    # Add a new person to the database

    conn.execute(
        "INSERT INTO persons (name, created_at) "
        "VALUES (?, datetime('now', 'localtime'))",
        (name,),
    )
    conn.commit()

    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def get_all_transactions(conn):
    # Retrieve all transactions from the database

    return conn.execute(
        """
        SELECT t.id, p.name, c.name, cu.code, t.amount, t.fx_rate_snapshot,
               t.type, t.date, t.note
        FROM transactions t
        JOIN persons p ON t.person_id = p.id
        JOIN categories c ON t.category_id = c.id
        JOIN currencies cu ON t.currency_id = cu.id
        ORDER BY t.date DESC
    """
    ).fetchall()


def get_by_person(conn, person_id):
    # Retrieve transactions for a specific person

    return conn.execute(
        """
        SELECT t.id, p.name, c.name, cu.code, t.amount, t.fx_rate_snapshot,
               t.type, t.date, t.note
        FROM transactions t
        JOIN persons p ON t.person_id = p.id
        JOIN categories c ON t.category_id = c.id
        JOIN currencies cu ON t.currency_id = cu.id
        WHERE p.id = ?
        ORDER BY t.date DESC
    """,
        (person_id,),
    ).fetchall()


def get_by_category(conn, category_id):
    # Retrieve transactions for a specific category

    return conn.execute(
        """
        SELECT t.id, p.name, c.name, cu.code, t.amount, t.fx_rate_snapshot,
               t.type, t.date, t.note
        FROM transactions t
        JOIN persons p ON t.person_id = p.id
        JOIN categories c ON t.category_id = c.id
        JOIN currencies cu ON t.currency_id = cu.id
        WHERE c.id = ?
        ORDER BY t.date DESC
    """,
        (category_id,),
    ).fetchall()


def get_by_month(conn, month):
    # Retrieve transactions for a specific month

    return conn.execute(
        """
        SELECT t.id, p.name, c.name, cu.code, t.amount, t.fx_rate_snapshot,
               t.type, t.date, t.note
        FROM transactions t
        JOIN persons p ON t.person_id = p.id
        JOIN categories c ON t.category_id = c.id
        JOIN currencies cu ON t.currency_id = cu.id
        WHERE strftime('%Y-%m', t.date) = ?
        ORDER BY t.date DESC
    """,
        (month,),
    ).fetchall()


def get_by_quarter(conn, year, quarter):
    # Retrieve transactions for a specific quarter

    return conn.execute(
        """
        SELECT t.id, p.name, c.name, cu.code, t.amount, t.fx_rate_snapshot,
               t.type, t.date, t.note
        FROM transactions t
        JOIN persons p ON t.person_id = p.id
        JOIN categories c ON t.category_id = c.id
        JOIN currencies cu ON t.currency_id = cu.id
        WHERE (
            (strftime('%m', t.date) IN ('01', '02', '03') AND ? = 'Q1') OR
            (strftime('%m', t.date) IN ('04', '05', '06') AND ? = 'Q2') OR
            (strftime('%m', t.date) IN ('07', '08', '09') AND ? = 'Q3') OR
            (strftime('%m', t.date) IN ('10', '11', '12') AND ? = 'Q4')
        )
        AND strftime('%Y', t.date) = ?
        ORDER BY t.date DESC
    """,
        (quarter, quarter, quarter, quarter, year),
    ).fetchall()


def get_by_year(conn, year):
    # Retrieve transactions for a specific year

    return conn.execute(
        """
        SELECT t.id, p.name, c.name, cu.code, t.amount, t.fx_rate_snapshot,
               t.type, t.date, t.note
        FROM transactions t
        JOIN persons p ON t.person_id = p.id
        JOIN categories c ON t.category_id = c.id
        JOIN currencies cu ON t.currency_id = cu.id
        WHERE strftime('%Y', t.date) = ?
        ORDER BY t.date DESC
    """,
        (year,),
    ).fetchall()


def get_person_monthly_balance(conn, person_id, month):
    # Calculate the monthly balance for a specific person

    result = conn.execute(
        """
        SELECT
            SUM(CASE WHEN t.type = 'income'
                THEN t.amount * t.fx_rate_snapshot ELSE 0 END) AS total_income,
            SUM(CASE WHEN t.type = 'expense'
                THEN t.amount * t.fx_rate_snapshot ELSE 0 END) AS total_expense
        FROM transactions t
        WHERE t.person_id = ? AND strftime('%Y-%m', t.date) = ?
    """,
        (person_id, month),
    ).fetchone()

    total_income = result["total_income"] or 0
    total_expense = result["total_expense"] or 0

    return total_income - total_expense


def update_currency_rate(conn, currency_id, new_rate):
    # Update the exchange rate for a specific currency

    conn.execute(
        """
        UPDATE currencies
        SET rate_to_uah = ?, updated_at = datetime('now', 'localtime')
        WHERE id = ?
    """,
        (new_rate, currency_id),
    )
    conn.commit()


def delete_transaction(conn, transaction_id):
    # Delete a transaction from the database

    conn.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,),
    )
    conn.commit()


def delete_person(conn, person_id):
    # Delete a person from the database
    conn.execute(
        "DELETE FROM persons WHERE id = ?",
        (person_id,),
    )
    conn.commit()
