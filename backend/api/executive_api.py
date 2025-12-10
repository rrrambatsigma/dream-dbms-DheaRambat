from flask import Blueprint, jsonify, request
from utils.auth_middleware import require_role
from utils.db_connection import get_connection, execute_query_all

executive_bp = Blueprint("executive", __name__)

# ===============================================================
# 1. KPI CARDS (TIDAK DIUBAH)
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
# 2. EXECUTIVE TABLE (Dropdown Table)
# ===============================================================
@executive_bp.route("/table", methods=["GET"])
@require_role([1])
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
# 3. SEARCH ENGINE TABEL EXECUTIVE
# ===============================================================
@executive_bp.route("/table/search", methods=["GET"])
@require_role([1])
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

        query = """
            EXEC UserExecutive.sp_SearchExecutiveTableData 
                @TableType = ?, 
                @Keyword = ?
        """

        rows = execute_query_all(query, (table_type, keyword))

        if len(rows) == 1 and "ErrorMessage" in rows[0]:
            return jsonify({"success": False, "error": rows[0]["ErrorMessage"]}), 400

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


# ===============================================================
# 4. 📊 BAR CHART — TOP 15
# ===============================================================
@executive_bp.route("/chart", methods=["GET"])
@require_role([1])   # executive only
def get_chart_data():
    try:
        chart_type = request.args.get("type")

        if not chart_type:
            return jsonify({"success": False, "error": "Missing chart type"}), 400

        allowed_types = ["country", "platform", "genre", "status"]

        if chart_type not in allowed_types:
            return jsonify({
                "success": False,
                "error": f"Invalid chart type. Must be one of: {allowed_types}"
            }), 400

        query = "EXEC UserExecutive.sp_GetBarChart @ChartType = ?"
        rows = execute_query_all(query, (chart_type,))

        if not rows:
            return jsonify({"success": False, "error": "No chart data found"}), 404

        labels = [row["Label"] for row in rows]
        totals = [row["Total"] for row in rows]

        return jsonify({
            "success": True,
            "chart_type": chart_type,
            "labels": labels,
            "totals": totals,
            "raw": rows
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 5. 🍩 PIE / DONUT CHART — STATUS, GENRE, LANGUAGE, COUNTRY
# ===============================================================
@executive_bp.route("/chart/pie", methods=["GET"])
@require_role([1])   # executive only
def get_pie_chart():
    try:
        chart_type = request.args.get("type")

        if not chart_type:
            return jsonify({"success": False, "error": "Missing chart type"}), 400

        allowed_types = ["status", "genre", "language", "country"]

        if chart_type not in allowed_types:
            return jsonify({
                "success": False,
                "error": f"Invalid chart type. Must be one of: {allowed_types}"
            }), 400

        query = "EXEC UserExecutive.sp_GetPieChart @ChartType = ?"
        rows = execute_query_all(query, (chart_type,))

        if not rows:
            return jsonify({"success": False, "error": "No pie chart data found"}), 404

        labels = [row["Label"] for row in rows]
        totals = [row["Total"] for row in rows]

        return jsonify({
            "success": True,
            "chart_type": chart_type,
            "labels": labels,
            "totals": totals,
            "raw": rows
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 6. 📊 STACKED BAR CHART — SHOW PER GENRE PER TYPE
# ===============================================================
@executive_bp.route("/chart/stacked", methods=["GET"])
@require_role([1])
def get_stacked_chart():
    try:
        # Call Stored Procedure
        rows = execute_query_all("EXEC UserExecutive.sp_GetStackedBarChart")

        if not rows:
            return jsonify({"success": False, "error": "No stacked chart data found"}), 404

        # rows example:
        # { "Genre": "Drama", "Type": "Scripted", "TotalShows": 120 }

        # Kumpulkan semua Genre (jadi labels X-axis)
        genres = sorted(list({row["Genre"] for row in rows}))

        # Kumpulkan semua Type (jadi setiap stack di bar)
        types = sorted(list({row["Type"] for row in rows}))

        # Bentuk datasets untuk Chart.js
        datasets = []
        for type_name in types:
            data_values = []
            for genre in genres:
                match = next(
                    (item for item in rows
                     if item["Genre"] == genre and item["Type"] == type_name),
                    None
                )
                data_values.append(match["TotalShows"] if match else 0)

            datasets.append({
                "label": type_name,
                "data": data_values
            })

        return jsonify({
            "success": True,
            "labels": genres,     # X-axis labels
            "datasets": datasets, # stacked data per type
            "raw": rows           # raw data kalau mau debug
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
