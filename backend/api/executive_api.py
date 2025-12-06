from flask import Blueprint, jsonify
from utils.auth_middleware import require_role
from utils.db_connection import get_connection

executive_bp = Blueprint("executive", __name__)

# GET KPI EXECUTIVE
@executive_bp.route("/kpi", methods=["GET"])
@require_role(["EXECUTIVE"])           # <-- FIXED (role pakai nama)
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
