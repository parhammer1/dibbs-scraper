import os
import sqlite3
from typing import List, Dict, Optional

DATA_DIR = "data"
DB_PATH = os.path.join(DATA_DIR, "solicitations.db")


def fetch_solicitations(fsc: str = "", nsn: str = "", start_date: str = "", end_date: str = "") -> List[Dict]:
    """Return solicitations filtered by FSC, NSN, and optional posted date range."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    query = "SELECT solicitation, description, deadline, buyer, nsn, fsc, posted FROM solicitations WHERE 1=1"
    params = []
    if fsc:
        query += " AND fsc LIKE ?"
        params.append(f"%{fsc}%")
    if nsn:
        query += " AND nsn LIKE ?"
        params.append(f"%{nsn}%")
    if start_date:
        query += " AND posted >= ?"
        params.append(start_date)
    if end_date:
        query += " AND posted <= ?"
        params.append(end_date)
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_solicitation_details(solicitation: str) -> Optional[Dict]:
    """Return the full record for a specific solicitation."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT solicitation, description, deadline, buyer, nsn, fsc, posted FROM solicitations WHERE solicitation = ?",
        (solicitation,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None
