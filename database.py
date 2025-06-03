"""Simple SQLite database utilities for storing DIBBS solicitations."""

import sqlite3
import json
from typing import Dict, List

DB_PATH = "solicitations.db"


def init_db() -> None:
    """Initialize the SQLite database and create table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS solicitations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            solicitation TEXT UNIQUE,
            description TEXT,
            deadline TEXT,
            buyer TEXT,
            nsn TEXT,
            fsc TEXT,
            posted TEXT,
            raw_data TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def insert_solicitation(data: Dict) -> None:
    """Insert a solicitation into the database if it doesn't already exist."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        INSERT OR IGNORE INTO solicitations (
            solicitation, description, deadline, buyer, nsn, fsc, posted, raw_data
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("solicitation"),
            data.get("description"),
            data.get("deadline"),
            data.get("buyer"),
            data.get("nsn"),
            data.get("fsc"),
            data.get("posted"),
            json.dumps(data),
        ),
    )
    conn.commit()
    conn.close()


def fetch_all() -> List[Dict]:
    """Return all solicitations stored in the database."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT solicitation, description, deadline, buyer, nsn, fsc, posted, raw_data FROM solicitations"
    ).fetchall()
    conn.close()
    result = []
    for solicitation, description, deadline, buyer, nsn, fsc, posted, raw_json in rows:
        item = json.loads(raw_json)
        item.update(
            {
                "solicitation": solicitation,
                "description": description,
                "deadline": deadline,
                "buyer": buyer,
                "nsn": nsn,
                "fsc": fsc,
                "posted": posted,
            }
        )
        result.append(item)
    return result
