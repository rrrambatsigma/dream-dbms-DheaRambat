from flask import Blueprint, jsonify, request
from utils.auth_middleware import require_role
from utils.db_connection import get_connection, execute_query_all

executive_bp = Blueprint("executive", __name__)

# ===============================================================
# 1. KPI CARDS (JANGAN DIUBAH - SESUAI PUNYA KAMU)
# ===============================================================
@executive_bp.route("/kpi", methods=["GET"])
@require_role([1])            # Role EXECUTIVE = 1
def get_kpi_executive():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("EXEC UserExecutive.sp_KPIExecutive")
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        result = {
            "TotalShows": row[0],
            "AverageRating": float(row[1]),
            "TotalVotes": row[2],
            "TotalProductionCompanies": row[3],
            "TotalProductionCountries": row[4],
            "TotalNetworks": row[5]
        }

        return jsonify({"success": True, "data": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# ===============================================================
# 2. EXECUTIVE TABLE (TAMPILKAN SEMUA DATA SESUAI DROPDOWN)
# GET /api/executive/table?type=overview
# ===============================================================
@executive_bp.route("/table", methods=["GET"])
@require_role([1])  # Only Executive role
def get_executive_table():
    try:
        table_type = request.args.get("type")

        if not table_type:
            return jsonify({"success": False, "error": "Missing table type"}), 400

        allowed_types = [
            "overview",
            "genres",
            "languages",
            "production",
            "networks",
            "performance"
        ]

        if table_type not in allowed_types:
            return jsonify({"success": False, "error": "Invalid table type"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("EXEC UserExecutive.sp_GetExecutiveTableData @TableType = ?", table_type)

        columns = [column[0] for column in cursor.description]
        rows = [
            {columns[i]: row[i] for i in range(len(columns))}
            for row in cursor.fetchall()
        ]

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "columns": columns,
            "rows": rows
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# ===============================================================
# 3. SEARCH ENGINE EXECUTIVE TABLE
# GET /api/executive/table/search?type=overview&keyword=crime
# ===============================================================
@executive_bp.route("/table/search", methods=["GET"])
@require_role([1])  # Executive only
def search_executive_table():
    try:
        table_type = request.args.get("type")
        keyword = request.args.get("keyword", "")

        if not table_type:
            return jsonify({"success": False, "error": "Missing table type"}), 400

        allowed_types = [
            "overview",
            "genres",
            "languages",
            "production",
            "networks",
            "performance"
        ]

        if table_type not in allowed_types:
            return jsonify({"success": False, "error": "Invalid table type"}), 400

        # Jalankan SP Search
        query = """
            EXEC UserExecutive.sp_SearchExecutiveTableData 
                @TableType = ?, 
                @Keyword = ?
        """

        rows = execute_query_all(query, (table_type, keyword))

        # Jika SP mengembalikan error
        if len(rows) == 1 and "ErrorMessage" in rows[0]:
            return jsonify({"success": False, "error": rows[0]["ErrorMessage"]}), 400

        # Ambil kolom
        columns = list(rows[0].keys()) if rows else []

        return jsonify({
            "success": True,
            "table": table_type,
            "keyword": keyword,
            "columns": columns,
            "rows": rows,
            "count": len(rows)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
