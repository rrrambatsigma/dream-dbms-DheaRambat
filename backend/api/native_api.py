# ============================================================
# api/native_api.py
# ============================================================

from flask import Blueprint, jsonify, request
import pandas as pd
from utils.db_connection import get_connection

native_api = Blueprint("native_api", __name__)

# ============================================================
# 1️⃣ HEALTH CHECK
# GET /api/native/health
# ============================================================
@native_api.route("/health", methods=["GET"])
def health_check():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()

        return jsonify({
            "success": True,
            "status": "healthy",
            "message": "Native API aktif & koneksi database OK"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "status": "unhealthy",
            "error": str(e)
        }), 500


# ============================================================
# 2️⃣ TOP TRENDING
# GET /api/native/top-trending
# ============================================================
@native_api.route("/top-trending", methods=["GET"])
def get_top_trending():
    try:
        conn = get_connection()
        query = "SELECT * FROM userNative.vw_Native_TopTrending"
        df = pd.read_sql(query, conn)
        conn.close()

        return jsonify({
            "success": True,
            "count": len(df),
            "data": df.to_dict(orient="records")
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================
# 3️⃣ SEARCH SHOWS
# GET /api/native/search
# ============================================================
@native_api.route("/search", methods=["GET"])
def search_shows():
    try:
        keyword = request.args.get("keyword")
        genre = request.args.get("genre")
        language = request.args.get("language")
        start_year_from = request.args.get("start_year_from", type=int)
        start_year_to = request.args.get("start_year_to", type=int)
        sort_by = request.args.get("sort_by", "popularity")
        sort_order = request.args.get("sort_order", "DESC")
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("page_size", 20, type=int)

        page = max(page, 1)
        page_size = 20 if page_size < 1 or page_size > 100 else page_size

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            EXEC userNative.sp_SearchShows
                @SearchKeyword = ?,
                @GenreFilter = ?,
                @LanguageFilter = ?,
                @StartYearFrom = ?,
                @StartYearTo = ?,
                @SortBy = ?,
                @SortOrder = ?,
                @PageNumber = ?,
                @PageSize = ?;
        """, (
            keyword, genre, language,
            start_year_from, start_year_to,
            sort_by, sort_order,
            page, page_size
        ))

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({
                "success": True,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_rows": 0,
                    "total_pages": 0
                },
                "results": []
            }), 200

        results = [dict(zip(columns, row)) for row in rows]

        total_rows = results[0].get("TotalResults", 0)
        total_pages = (total_rows + page_size - 1) // page_size

        return jsonify({
            "success": True,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_rows": total_rows,
                "total_pages": total_pages
            },
            "results": results
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================
# 4️⃣ SHOW DETAIL
# GET /api/native/detail/<show_id>
# ============================================================
@native_api.route("/detail/<int:show_id>", methods=["GET"])
def get_show_detail(show_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("EXEC userNative.sp_GetShowDetail ?", show_id)

        results = []
        while True:
            rows = cursor.fetchall()
            if not rows:
                break
            columns = [col[0] for col in cursor.description]
            results.append([dict(zip(columns, row)) for row in rows])
            if not cursor.nextset():
                break

        conn.close()

        return jsonify({
            "success": True,
            "data": {
                "show_info": results[0] if len(results) > 0 else [],
                "links": results[1] if len(results) > 1 else []
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================
# 5️⃣ DISCOVER CATEGORIES
# GET /api/native/discover/<category_type>
# ============================================================
@native_api.route("/discover/<category_type>", methods=["GET"])
def discover_categories(category_type):
    view_map = {
        "networks": "userNative.vw_DiscoverByNetwork",
        "countries": "userNative.vw_DiscoverByCountry",
        "types": "userNative.vw_DiscoverByType",
        "statuses": "userNative.vw_DiscoverByStatus"
    }

    if category_type not in view_map:
        return jsonify({
            "success": False,
            "error": "Invalid category type"
        }), 400

    try:
        conn = get_connection()
        df = pd.read_sql(
            f"SELECT * FROM {view_map[category_type]} ORDER BY TotalShows DESC",
            conn
        )
        conn.close()

        return jsonify({
            "success": True,
            "category": category_type,
            "count": len(df),
            "data": df.to_dict(orient="records")
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================
# 6️⃣ SHOWS BY CATEGORY
# GET /api/native/discover/<type>/<id>
# ============================================================
@native_api.route("/discover/<category_type>/<int:category_id>", methods=["GET"])
def shows_by_category(category_type, category_id):
    valid_types = ["network", "country", "type", "status"]
    if category_type not in valid_types:
        return jsonify({"success": False, "error": "Invalid category type"}), 400

    try:
        sort_by = request.args.get("sort_by", "popularity")
        sort_order = request.args.get("sort_order", "DESC")
        page = request.args.get("page", 1, type=int)
        page_size = request.args.get("page_size", 20, type=int)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            EXEC userNative.sp_GetShowsByCategory
                @CategoryType = ?,
                @CategoryID = ?,
                @SortBy = ?,
                @SortOrder = ?,
                @PageNumber = ?,
                @PageSize = ?
        """, (
            category_type, category_id,
            sort_by, sort_order,
            page, page_size
        ))

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return jsonify({
                "success": True,
                "results": [],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_rows": 0,
                    "total_pages": 0
                }
            }), 200

        results = [dict(zip(columns, row)) for row in rows]

        total_rows = results[0].get("TotalRows", 0)
        for r in results:
            r.pop("TotalRows", None)

        total_pages = (total_rows + page_size - 1) // page_size

        return jsonify({
            "success": True,
            "results": results,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_rows": total_rows,
                "total_pages": total_pages
            }
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# 7️⃣ GENRES
# GET /api/native/genres
# ============================================================
@native_api.route("/genres", methods=["GET"])
def get_genres():
    try:
        conn = get_connection()
        df = pd.read_sql("""
            SELECT DISTINCT GenreName
            FROM userNative.vw_ShowGenres
            WHERE GenreName IS NOT NULL
            ORDER BY GenreName
        """, conn)
        conn.close()

        return jsonify({
            "success": True,
            "count": len(df),
            "data": df["GenreName"].tolist()
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# 8️⃣ LANGUAGES
# GET /api/native/languages
# ============================================================
@native_api.route("/languages", methods=["GET"])
def get_languages():
    try:
        conn = get_connection()
        df = pd.read_sql("""
            SELECT DISTINCT LanguageCode, LanguageName
            FROM userNative.vw_ShowLanguages
            WHERE LanguageCode IS NOT NULL
            ORDER BY LanguageName
        """, conn)
        conn.close()

        return jsonify({
            "success": True,
            "count": len(df),
            "data": df.to_dict(orient="records")
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
