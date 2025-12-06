import functools
from flask import request, jsonify
import jwt
from config import SECRET_KEY
from utils.db_connection import execute_query_single

def require_role(allowed_roles):

    def wrapper(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):

            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"error": "Authorization header missing"}), 401

            try:
                token = auth_header.replace("Bearer ", "").strip()
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            username = payload.get("username")

            if not username:
                return jsonify({"error": "Invalid token payload"}), 401

            # ⬅⬅ AMBIL ROLE_ID, BUKAN ROLENAME
            sql = """
                SELECT u.RoleID
                FROM Users u
                WHERE u.Username = ?
            """
            result = execute_query_single(sql, (username,))

            if not result:
                return jsonify({"error": "User not found"}), 404

            user_role = result["RoleID"]   # ⬅ ROLE ANGKA

            # ⬅ CEK ROLE ANGKA
            if user_role not in allowed_roles:
                return jsonify({
                    "error": f"Access denied for role_id {user_role}"
                }), 403

            return func(*args, **kwargs)

        return decorated
    return wrapper