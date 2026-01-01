# ====================================================
# utils/auth_middleware.py
# ====================================================

import functools
from flask import request, jsonify
import jwt
from config import SECRET_KEY


def require_role(allowed_roles):
    """
    Decorator untuk role-based authorization.
    Role diambil LANGSUNG dari JWT token (role_id).
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # ------------------------------------------------
            # 1. Ambil Authorization Header
            # ------------------------------------------------
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return jsonify({
                    "success": False,
                    "message": "Authorization token missing"
                }), 401

            # ------------------------------------------------
            # 2. Decode JWT Token
            # ------------------------------------------------
            try:
                token = auth_header.replace("Bearer ", "").strip()
                payload = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=["HS256"]
                )
            except jwt.ExpiredSignatureError:
                return jsonify({
                    "success": False,
                    "message": "Token expired"
                }), 401
            except jwt.InvalidTokenError:
                return jsonify({
                    "success": False,
                    "message": "Invalid token"
                }), 401

            # ------------------------------------------------
            # 3. Ambil Role dari Token
            # ------------------------------------------------
            role_id = payload.get("role_id")

            if role_id is None:
                return jsonify({
                    "success": False,
                    "message": "Role not found in token"
                }), 403

            # ------------------------------------------------
            # 4. Validasi Role
            # ------------------------------------------------
            if role_id not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "Access denied"
                }), 403

            # ------------------------------------------------
            # 5. Lolos Authorization
            # ------------------------------------------------
            return func(*args, **kwargs)

        return wrapper
    return decorator
