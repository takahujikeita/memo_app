import sqlite3

DATABASE='database.db'

def init_db():
    connection=sqlite3.connect(DATABASE)

    connection.execute("""
            CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            content TEXT NOT NULL,
            category TEXT NOT NULL
                    )
                    """)
    connection.commit()
    connection.close()