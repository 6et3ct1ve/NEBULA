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
            is_income BOOLEAN CHECK(is_income IN (0, 1))
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
        (1, "Salary", 1),
        (2, "Freelance", 1),
        (3, "Other income", 1),
        # Housing
        (4, "Rent", 0),
        (5, "Utilities", 0),
        (6, "Internet/Phone", 0),
        (7, "Home insurance", 0),
        # Food
        (8, "Groceries", 0),
        (9, "Restaurants/Cafes", 0),
        # Transport
        (10, "Fuel", 0),
        (11, "Parking", 0),
        (12, "Taxi/Transit", 0),
        # Health
        (13, "Medical", 0),
        (14, "Insurance", 0),
        (15, "Gym", 0),
        # Entertainment
        (16, "Streaming", 0),
        (17, "Games", 0),
        (18, "Hobbies", 0),
        # Shopping
        (19, "Clothing", 0),
        (20, "Electronics", 0),
        # Personal
        (21, "Beauty/Care", 0),
        (22, "Education", 0),
        # Finance
        (23, "Savings", 0),
        (24, "Debt/Credit", 0),
        # Other
        (25, "Unexpected", 0),
    ]

    currencies = [
        (1, "UAH", 1.0, "2026-06-03"),
        (2, "USD", 44.29, "2026-06-03"),
        (3, "EUR", 51.56, "2026-06-03"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO categories (id, name, is_income)\
        VALUES (?, ?, ?)",
        categories,
    )

    conn.executemany(
        "INSERT OR IGNORE INTO currencies (id, code, rate_to_uah, updated_at)\
        VALUES (?, ?, ?, ?)",
        currencies,
    )

    conn.commit()
