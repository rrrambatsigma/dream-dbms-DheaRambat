from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime

# ==== CONFIG ====
from config import SECRET_KEY

# ==== DB UTIL ====
from utils.db_connection import execute_query_single

# ==== BLUEPRINTS ====
# Native API (pencarian, detail, discover)
from api.native_api import native_api

# Executive API (KPI + Table Dropdown + Search Engine)
from api.executive_api import executive_bp

# Marketing API
from api.marketing_api import marketing_bp


# ====================================================
# FLASK APP INITIALIZATION
# ====================================================
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


# ====================================================
# GLOBAL CORS SETTINGS
# ====================================================
CORS(
    app,
    origins=["http://localhost:5173"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    supports_credentials=True,
)


# ====================================================
# HANDLE PREFLIGHT (OPTIONS) REQUESTS
# ====================================================
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return "", 200


# ====================================================
# LOGIN ROUTE
# ====================================================
@app.post("/login")
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # Call SQL Server stored procedure
        query = "EXEC sp_Login ?, ?"
        user = execute_query_single(query, (username, password))

        if user is None:
            return jsonify({"error": "Invalid username or password"}), 401

        # Generate JWT token
        token = jwt.encode(
            {
                "user_id": user["UserID"],
                "username": user["Username"],
                "role_id": user["RoleID"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6),
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        return jsonify(
            {
                "success": True,
                "token": token,
                "role_id": user["RoleID"],
                "username": user["Username"],
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ====================================================
# ROOT TEST ROUTE
# ====================================================
@app.get("/")
def index():
    return jsonify({"status": "Backend OK", "message": "Flask Running"})


# ====================================================
# BLUEPRINT ROUTES REGISTRATION
# ====================================================
# Native User Endpoints
app.register_blueprint(native_api, url_prefix="")

# Executive Endpoints (KPI + Table + Search Engine)
app.register_blueprint(executive_bp, url_prefix="/api/executive")

# Marketing Endpoints
app.register_blueprint(marketing_bp, url_prefix="/api/marketing")


# ====================================================
# RUN SERVER
# ====================================================
if __name__ == "__main__":
    print("🚀 Flask Running at: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
