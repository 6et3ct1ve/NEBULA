import sqlite3


def init_db(db_name):
    # Initiation of database

    if not db_name.endswith(".db"):
        raise ValueError(f"Invalid database name: {db_name}")

    db = sqlite3.connect(db_name)
    db.row_factory = sqlite3.Row

    db.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT CHECK(type IN ('income', 'expense', 'transfer'))
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS currencies (
            id INTEGER PRIMARY KEY,
            code TEXT,
            rate_to_uah REAL,
            updated_at TEXT
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            category_id INTEGER,
            currency_id INTEGER,
            amount REAL,
            fx_rate_snapshot REAL,
            type TEXT CHECK(type IN ('income','expense')),
            date TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (currency_id) REFERENCES currencies(id)
        )
    """)

    db.commit()

    return db


def seed(conn):
    # Create default categories and money value

    categories = [
        # Income
        (1, "Salary", "income"),
        (2, "Freelance", "income"),
        (3, "Other income", "income"),
        # Housing
        (4, "Rent", "expense"),
        (5, "Utilities", "expense"),
        (6, "Internet/Phone", "expense"),
        (7, "Home insurance", "expense"),
        # Food
        (8, "Groceries", "expense"),
        (9, "Restaurants/Cafes", "expense"),
        # Transport
        (10, "Fuel", "expense"),
        (11, "Parking", "expense"),
        (12, "Taxi/Transit", "expense"),
        # Health
        (13, "Medical", "expense"),
        (14, "Insurance", "expense"),
        (15, "Gym", "expense"),
        # Entertainment
        (16, "Streaming", "expense"),
        (17, "Games", "expense"),
        (18, "Hobbies", "expense"),
        # Shopping
        (19, "Clothing", "expense"),
        (20, "Electronics", "expense"),
        # Personal
        (21, "Beauty/Care", "expense"),
        (22, "Education", "expense"),
        # Finance
        (23, "Savings", "transfer"),
        (24, "Debt/Credit", "transfer"),
        # Other
        (25, "Unexpected", "expense"),
    ]

    currencies = [
        (1, "UAH", 1.0, "2026-06-03"),
        (2, "USD", 44.29, "2026-06-03"),
        (3, "EUR", 51.56, "2026-06-03"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO categories (id, name, type) VALUES (?, ?, ?)", categories
    )

    conn.executemany(
        "INSERT OR IGNORE INTO currencies (id, code, rate_to_uah, updated_at) VALUES (?, ?, ?, ?)",
        currencies,
    )

    conn.commit()
