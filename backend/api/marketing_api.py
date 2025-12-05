from flask import Blueprint, jsonify
from utils.auth_middleware import require_role
from utils.db_connection import execute_query_single

marketing_bp = Blueprint("marketing", __name__)

@marketing_bp.get("/marketing/kpi")
@require_role(["MARKETING"])
def get_marketing_kpi():
    query = "SELECT * FROM v_kpi_marketing"
    result = execute_query_single(query)

    if result is None:
        return jsonify({"success": False, "message": "No KPI data found"}), 404

    return jsonify({
        "success": True,
        "data": result
    }), 200
