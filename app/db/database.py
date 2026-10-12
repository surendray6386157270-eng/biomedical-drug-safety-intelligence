from pathlib import Path
import sqlite3


DATABASE_PATH = Path("data/evidence.db")


def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS evidence (
            evidence_id TEXT PRIMARY KEY,
            drug_name TEXT NOT NULL,
            drug_identifier TEXT,
            reaction TEXT,
            evidence_type TEXT NOT NULL,
            event_date TEXT,
            source TEXT NOT NULL,
            source_record_id TEXT NOT NULL,
            retrieved_at TEXT NOT NULL,
            source_reference TEXT NOT NULL,
            schema_version TEXT NOT NULL,
            transformation TEXT NOT NULL,
            raw_record_reference TEXT
        )
        """
    )

    connection.commit()
    connection.close()