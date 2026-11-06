import os
import sqlite3

# -----------------------------
# Database Connection
# -----------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "records.db")
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


# -----------------------------
# Tables Creation
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS document_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT UNIQUE,
    hash_value TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS verification_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT,
    result TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# -----------------------------
# Save / Update Original Hash
# (IMPORTANT FIX: prevents old hash conflict)
# -----------------------------
def save_hash(file_name, hash_value):

    # Remove old entry if exists
    cursor.execute(
        "DELETE FROM document_records WHERE file_name = ?",
        (file_name,)
    )

    # Insert fresh hash (latest version only)
    cursor.execute(
        "INSERT INTO document_records (file_name, hash_value) VALUES (?, ?)",
        (file_name, hash_value)
    )

    conn.commit()


# -----------------------------
# Get Stored Hash
# -----------------------------
def get_hash(file_name):

    cursor.execute(
        "SELECT hash_value FROM document_records WHERE file_name = ?",
        (file_name,)
    )

    result = cursor.fetchone()

    return result[0] if result else None


# -----------------------------
# Save Verification History
# -----------------------------
def save_history(file_name, result):

    cursor.execute(
        "INSERT INTO verification_history (file_name, result) VALUES (?, ?)",
        (file_name, result)
    )

    conn.commit()


# -----------------------------
# Get Verification History
# -----------------------------
def get_history():

    cursor.execute("""
        SELECT file_name, result, timestamp
        FROM verification_history
        ORDER BY timestamp DESC
    """)

    return cursor.fetchall()


# -----------------------------
# Clear History
# -----------------------------
def clear_history():

    cursor.execute("DELETE FROM verification_history")
    conn.commit()