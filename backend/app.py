# ====================================================
# app.py
# ====================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime

# ====================================================
# CONFIG
# ====================================================
from config import SECRET_KEY

# ====================================================
# DATABASE UTIL
# ====================================================
from utils.db_connection import execute_query_single

# ====================================================
# BLUEPRINTS
# ====================================================
from api.native_api import native_api
from api.executive_api import executive_bp
from api.marketing_api import marketing_bp


# ====================================================
# FLASK APP INITIALIZATION
# ====================================================
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


# ====================================================
# GLOBAL CORS CONFIGURATION
# ====================================================
CORS(
    app,
    origins=["http://localhost:5173"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)


# ====================================================
# HANDLE PREFLIGHT (OPTIONS)
# ====================================================
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return jsonify({"success": True}), 200


# ====================================================
# AUTHENTICATION - LOGIN
# ====================================================
@app.post("/login")
def login():
    """
    Login endpoint
    - Validate user via SQL Server (sp_Login)
    - Generate JWT token
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Request body is required"
            }), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({
                "success": False,
                "message": "Username and password are required"
            }), 400

        # Call SQL Server Stored Procedure
        user = execute_query_single(
            "EXEC sp_Login ?, ?",
            (username, password)
        )

        if not user:
            return jsonify({
                "success": False,
                "message": "Invalid username or password"
            }), 401

        # Generate JWT
        token = jwt.encode(
            {
                "user_id": user["UserID"],
                "username": user["Username"],
                "role_id": user["RoleID"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "success": True,
            "token": token,
            "user": {
                "user_id": user["UserID"],
                "username": user["Username"],
                "role_id": user["RoleID"]
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ====================================================
# ROOT / HEALTH CHECK
# ====================================================
@app.get("/")
def health_check():
    return jsonify({
        "status": "OK",
        "service": "Flask Backend",
        "message": "Backend is running"
    }), 200


# ====================================================
# BLUEPRINT REGISTRATION
# ====================================================

# Native user endpoints (public / basic access)
app.register_blueprint(
    native_api,
    url_prefix="/api/native"
)

# Executive endpoints (role-based)
app.register_blueprint(
    executive_bp,
    url_prefix="/api/executive"
)

# Marketing endpoints (role-based)
app.register_blueprint(
    marketing_bp,
    url_prefix="/api/marketing"
)


# ====================================================
# GLOBAL ERROR HANDLERS (OPTIONAL BUT GOOD PRACTICE)
# ====================================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500


# ====================================================
# RUN SERVER
# ====================================================
if __name__ == "__main__":
    print("🚀 Flask Backend Running")
    print("📍 URL: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
