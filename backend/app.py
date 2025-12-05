# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
import datetime

# ==== CONFIG ====
from config import SECRET_KEY

# ==== DB UTIL ====
from utils.db_connection import execute_query_single

# ==== BLUEPRINTS ====
from api.native_api import native_api
from api.executive_api import executive_bp
from api.marketing_api import marketing_bp

# ================================
# FLASK APP
# ================================
app = Flask(__name__)
CORS(app)   # ← FIX

# ================================
# LOGIN ROUTE
# ================================
@app.post("/login")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Stored Procedure
    query = "EXEC sp_Login ?, ?"

    user = execute_query_single(query, (username, password))

    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401

    token = jwt.encode({
        "user_id": user["UserID"],
        "username": user["Username"],
        "role_id": user["RoleID"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "success": True,
        "token": token,
        "role_id": user["RoleID"],
        "username": user["Username"]
    })

# ================================
# MAIN TEST ENDPOINT
# ================================
@app.get("/")
def index():
    return {"message": "Backend Flask is running!"}

# ================================
# BLUEPRINT ROUTES
# ================================
app.register_blueprint(native_api, url_prefix="/native")
app.register_blueprint(executive_bp, url_prefix="/executive")  # <── INI YANG BENAR
app.register_blueprint(marketing_bp, url_prefix="/marketing")

# ================================
# RUN SERVER
# ================================
if __name__ == '__main__':
    print("🚀 Flask Running at http://127.0.0.1:5000")
    app.run(debug=True)