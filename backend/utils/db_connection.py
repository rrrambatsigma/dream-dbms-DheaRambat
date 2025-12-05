# utils/db_connection.py

import pyodbc

# ===============================
# FUNGSI UTAMA KONEKSI
# ===============================

def get_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=RAMBATUNGU25;"
            "DATABASE=FINAL_PROJECT;"
            "Trusted_Connection=yes;",
            timeout=5
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None


# ===============================
# GET 1 RECORD
# ===============================
def execute_query_single(query, params=()):
    conn = get_connection()
    if conn is None:
        return {"error": "Cannot connect to database"}

    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        row = cursor.fetchone()

        if not row:
            return None

        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))

    except Exception as e:
        print("Query error:", e)
        return None

    finally:
        cursor.close()
        conn.close()


# ===============================
# GET MANY RECORDS
# ===============================
def execute_query_all(query, params=()):
    conn = get_connection()
    if conn is None:
        return {"error": "Cannot connect to database"}

    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print("Query error:", e)
        return []

    finally:
        cursor.close()
        conn.close()


# ===============================
# INSERT / UPDATE / DELETE
# ===============================
def execute_query_commit(query, params=()):
    conn = get_connection()
    if conn is None:
        return {"error": "Cannot connect to database"}

    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        conn.commit()
        return {"success": True}

    except Exception as e:
        print("Commit error:", e)
        return {"success": False, "error": str(e)}

    finally:
        cursor.close()
        conn.close()
