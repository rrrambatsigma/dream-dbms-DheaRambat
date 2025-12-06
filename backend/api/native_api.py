# api/native_api.py
from flask import Blueprint, jsonify, request
import pandas as pd
from utils.db_connection import get_connection

native_api = Blueprint('native_api', __name__)

# ============================================================
# 1️⃣ Health Check
# ============================================================
@native_api.route('/api/native/health', methods=['GET'])
def health_check():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return jsonify({
            "success": True,
            "status": "healthy",
            "message": "✅ Native API berjalan dan koneksi ke SQL Server aktif"
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "status": "unhealthy",
            "error": str(e)
        }), 500


# ============================================================
# 2️⃣ Top Trending (opsional, view tambahan)
# ============================================================
@native_api.route('/api/native/top-trending', methods=['GET'])
def get_top_trending():
    """Ambil data dari view userNative.vw_Native_TopTrending (jika ada)"""
    try:
        conn = get_connection()
        query = "SELECT * FROM userNative.vw_Native_TopTrending"
        df = pd.read_sql(query, conn)
        conn.close()
        return jsonify(df.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================
# 3️⃣ SEARCH SHOWS (sp_SearchShows) - DIPERBAIKI (Konsistensi)
# ============================================================
@native_api.route('/api/native/search', methods=['GET'])
def search_shows():
    """Pencarian show berdasarkan keyword, genre, bahasa, tahun, dan sort"""
    try:
        # Ambil parameter dari frontend
        keyword = request.args.get('keyword', '')
        genre = request.args.get('genre', '')
        language = request.args.get('language', '')
        start_year_from = request.args.get('start_year_from', type=int)
        start_year_to = request.args.get('start_year_to', type=int)
        sort_by = request.args.get('sort_by', 'popularity')
        sort_order = request.args.get('sort_order', 'DESC')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)

        # Validasi parameter
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 20

        # Koneksi ke database
        conn = get_connection()
        cursor = conn.cursor()

        # Execute Stored Procedure dengan parameter yang benar
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
        """, (keyword or None, genre or None, language or None, 
              start_year_from, start_year_to, sort_by, sort_order, 
              page, page_size))

        # Ambil hasil dari SQL
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        # Handle case ketika tidak ada results
        if not rows:
            conn.close()
            return jsonify({
                "success": True,
                "filters": {
                    "keyword": keyword,
                    "genre": genre,
                    "language": language,
                    "year_range": [start_year_from, start_year_to],
                    "sort_by": sort_by,
                    "order": sort_order
                },
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_rows": 0,
                    "total_pages": 0
                },
                "results": []
            }), 200

        results = [dict(zip(columns, row)) for row in rows]

        # PERBAIKAN KONSISTENSI
        total_rows = 0
        if results:
            total_rows = results[0].get("TotalResults", 0)

        # Hitung total pages
        total_pages = (total_rows + page_size - 1) // page_size if total_rows > 0 else 0

        conn.close()

        # Return full pagination data
        return jsonify({
            "success": True,
            "filters": {
                "keyword": keyword,
                "genre": genre,
                "language": language,
                "year_range": [start_year_from, start_year_to],
                "sort_by": sort_by,
                "order": sort_order
            },
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
# 4️⃣ SHOW DETAIL (sp_GetShowDetail)
# ============================================================
@native_api.route('/api/native/detail/<int:show_id>', methods=['GET'])
def get_show_detail(show_id):
    """Ambil detail lengkap show berdasarkan ShowID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("EXEC userNative.sp_GetShowDetail @ShowID = ?", show_id)

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
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# 5️⃣ DETAIL SHOW DARI SEARCH BASE (sp_ShowDetailBySearchBase)
# ============================================================
@native_api.route('/api/native/search/detail/<int:show_id>', methods=['GET'])
def get_show_detail_from_search_base(show_id):
    """
    Ambil detail show (fitur cabang dari Search Base)
    Menggunakan stored procedure: userNative.sp_ShowDetailBySearchBase
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("EXEC userNative.sp_ShowDetailBySearchBase @ShowID = ?", show_id)

        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        if not rows:
            conn.close()
            return jsonify({
                "success": False,
                "message": f"Show dengan ID {show_id} tidak ditemukan."
            }), 404

        results = [dict(zip(columns, row)) for row in rows]
        conn.close()

        return jsonify({
            "success": True,
            "show_id": show_id,
            "detail": results[0]
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================
# 6️⃣ DISCOVER - GET CATEGORIES LIST (DYNAMIC)
# ============================================================
@native_api.route('/api/native/discover/<category_type>', methods=['GET'])
def get_discover_categories(category_type):
    """
    Mendapatkan daftar kategori untuk Discover
    
    category_type: 'networks', 'countries', 'types', 'statuses'
    
    Contoh:
    - GET /api/native/discover/networks
    - GET /api/native/discover/countries
    - GET /api/native/discover/types
    - GET /api/native/discover/statuses
    """
    try:
        # Mapping category_type ke VIEW yang sesuai
        view_map = {
            'networks': 'userNative.vw_DiscoverByNetwork',
            'countries': 'userNative.vw_DiscoverByCountry',
            'types': 'userNative.vw_DiscoverByType',
            'statuses': 'userNative.vw_DiscoverByStatus'
        }
        
        # Validasi category_type
        if category_type not in view_map:
            return jsonify({
                "success": False,
                "error": f"Invalid category type. Must be one of: {', '.join(view_map.keys())}"
            }), 400
        
        # Query ke database
        conn = get_connection()
        query = f"SELECT * FROM {view_map[category_type]} ORDER BY TotalShows DESC"
        df = pd.read_sql(query, conn)
        conn.close()
        
        return jsonify({
            "success": True,
            "category": category_type,
            "count": len(df),
            "data": df.to_dict(orient='records')
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e)
        }), 500


# ============================================================
# 7️⃣ DISCOVER - GET SHOWS BY CATEGORY (DYNAMIC) - DIPERBAIKI
# ============================================================
@native_api.route('/api/native/discover/<category_type>/<int:category_id>', methods=['GET'])
def get_shows_by_category(category_type, category_id):
    """
    Mendapatkan daftar shows berdasarkan kategori tertentu
    
    category_type: 'network', 'country', 'type', 'status' (SINGULAR!)
    category_id: ID dari kategori
    
    Query Parameters:
    - sort_by: 'popularity', 'rating', 'name' (default: 'popularity')
    - sort_order: 'ASC', 'DESC' (default: 'DESC')
    - page: nomor halaman (default: 1)
    - page_size: jumlah per halaman (default: 20)
    
    Contoh:
    - GET /api/native/discover/network/213
    - GET /api/native/discover/country/1?sort_by=rating
    - GET /api/native/discover/type/1?page=2&page_size=10
    - GET /api/native/discover/status/2
    """
    try:
        # Ambil query parameters
        sort_by = request.args.get('sort_by', 'popularity')
        sort_order = request.args.get('sort_order', 'DESC')
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        
        # Validasi parameter
        if page < 1:
            page = 1
        if page_size < 1 or page_size > 100:
            page_size = 20
        
        # Validasi category_type (harus singular)
        valid_types = ['network', 'country', 'type', 'status']
        if category_type not in valid_types:
            return jsonify({
                "success": False,
                "error": f"Invalid category type. Must be one of: {', '.join(valid_types)}"
            }), 400
        
        # Execute stored procedure
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
        """, (category_type, category_id, sort_by, sort_order, page, page_size))
        
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        if not rows:
            conn.close()
            return jsonify({
                "success": True,
                "category_type": category_type,
                "category_id": category_id,
                "filters": {
                    "sort_by": sort_by,
                    "sort_order": sort_order,
                    "page": page,
                    "page_size": page_size
                },
                "count": 0,
                "results": []
            }), 200
        
        results = [dict(zip(columns, row)) for row in rows]
        
        # ================================================
        # PERBAIKAN: AMBIL TOTAL ROWS DARI KOLOM YANG BENAR
        # ================================================
        total_rows = 0
        if results:
            # SQL mengembalikan "TotalRows", bukan "TotalResults"
            total_rows = results[0].get("TotalRows", 0)
            
            # Hapus TotalRows dari setiap hasil agar tidak tampil sebagai data show
            for result in results:
                result.pop("TotalRows", None)
        
        total_pages = (total_rows + page_size - 1) // page_size if total_rows > 0 else 0
        # ================================================
        
        conn.close()
        
        return jsonify({
            "success": True,
            "category_type": category_type,
            "category_id": category_id,
            "filters": {
                "sort_by": sort_by,
                "sort_order": sort_order,
                "page": page,
                "page_size": page_size
            },
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_rows": total_rows,
                "total_pages": total_pages
            },
            "count": len(results),
            "results": results
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
# ============================================================
# 8️⃣ GET ALL GENRES - ENDPOINT BARU
# ============================================================
@native_api.route('/api/native/genres', methods=['GET'])
def get_all_genres():
    """Mendapatkan daftar semua genre yang tersedia"""
    try:
        conn = get_connection()
        query = """
            SELECT DISTINCT GenreName 
            FROM userNative.vw_ShowGenres 
            WHERE GenreName IS NOT NULL 
            ORDER BY GenreName
        """
        df = pd.read_sql(query, conn)
        conn.close()
        
        genres = df['GenreName'].tolist() if not df.empty else []
        
        return jsonify({
            "success": True,
            "count": len(genres),
            "genres": genres
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================
# 9️⃣ GET ALL LANGUAGES - ENDPOINT BARU
# ============================================================
@native_api.route('/api/native/languages', methods=['GET'])
def get_all_languages():
    """Mendapatkan daftar semua bahasa yang tersedia"""
    try:
        conn = get_connection()
        query = """
            SELECT DISTINCT LanguageCode, LanguageName 
            FROM userNative.vw_ShowLanguages 
            WHERE LanguageCode IS NOT NULL 
            ORDER BY LanguageName
        """
        df = pd.read_sql(query, conn)
        conn.close()
        
        languages = df.to_dict(orient='records') if not df.empty else []
        
        return jsonify({
            "success": True,
            "count": len(languages),
            "languages": languages
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500