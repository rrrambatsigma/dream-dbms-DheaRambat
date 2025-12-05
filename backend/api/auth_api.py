from flask import Blueprint, request, jsonify
import jwt
import datetime
from config import SECRET_KEY
from utils.db import get_connection

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Username & Password required"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("EXEC sp_Login ?, ?", username, password)
    row = cursor.fetchone()

    if row is None:
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "Invalid username or password"}), 401

    # Buat JWT Token
    token = jwt.encode({
        "user_id": row.UserID,
        "username": row.Username,
        "role_id": row.RoleID,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    }, SECRET_KEY, algorithm="HS256")

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "token": token,
        "UserID": row.UserID,
        "Username": row.Username,
        "RoleID": row.RoleID
    })
