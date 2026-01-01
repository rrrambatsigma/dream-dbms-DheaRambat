from flask import Blueprint, jsonify, request
from utils.auth_middleware import require_role
from utils.db_connection import get_connection, execute_query_all
import datetime

executive_bp = Blueprint("executive", __name__)

# ===============================================================
# 1. KPI CARDS (TETAP SAMA)
# ===============================================================
@executive_bp.route("/kpi", methods=["GET"])
@require_role([1])
def get_kpi_executive():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC UserExecutive.sp_KPIExecutive")
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if len(row) == 8:
            result = {
                "TotalShows": row[0],
                "TotalVotes": row[1],
                "TotalProductionCompanies": row[2],
                "TotalProductionCountries": row[3],
                "TopProductionCompany": row[4],
                "ShowsFromTopCompany": row[5],
                "TopGenre": row[6],
                "TopMovie": row[7]
            }
        elif len(row) == 6:
            result = {
                "TotalShows": row[0],
                "AverageRating": float(row[1]) if row[1] is not None else 0.0,
                "TotalVotes": row[2],
                "TotalProductionCompanies": row[3],
                "TotalProductionCountries": row[4],
                "TotalNetworks": row[5]
            }
        else:
            columns = ["TotalShows", "TotalVotes", "TotalProductionCompanies", 
                      "TotalProductionCountries", "TopProductionCompany", 
                      "ShowsFromTopCompany", "TopGenre", "TopMovie"]
            result = {}
            for i, col in enumerate(columns):
                if i < len(row):
                    result[col] = row[i]
                else:
                    result[col] = None

        return jsonify({"success": True, "data": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 2. EXECUTIVE TABLE (TETAP SAMA)
# ===============================================================
@executive_bp.route("/table", methods=["GET"])
@require_role([1])
def get_executive_table():
    try:
        table_type = request.args.get("type")
        if not table_type:
            return jsonify({"success": False, "error": "Missing table type"}), 400

        allowed_types = ["overview", "genres", "languages", "production", "networks", "performance"]
        if table_type not in allowed_types:
            return jsonify({"success": False, "error": "Invalid table type"}), 400

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC UserExecutive.sp_GetExecutiveTableData @TableType = ?", table_type)
        columns = [column[0] for column in cursor.description]
        rows = [{columns[i]: row[i] for i in range(len(columns))} for row in cursor.fetchall()]
        cursor.close()
        conn.close()

        return jsonify({"success": True, "columns": columns, "rows": rows})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 3. SEARCH ENGINE TABEL EXECUTIVE (TETAP SAMA)
# ===============================================================
@executive_bp.route("/table/search", methods=["GET"])
@require_role([1])
def search_executive_table():
    try:
        table_type = request.args.get("type")
        keyword = request.args.get("keyword", "")

        if not table_type:
            return jsonify({"success": False, "error": "Missing table type"}), 400

        allowed_types = ["overview", "genres", "languages", "production", "networks", "performance"]
        if table_type not in allowed_types:
            return jsonify({"success": False, "error": "Invalid table type"}), 400

        query = "EXEC UserExecutive.sp_SearchExecutiveTableData @TableType = ?, @Keyword = ?"
        rows = execute_query_all(query, (table_type, keyword))

        if len(rows) == 1 and "ErrorMessage" in rows[0]:
            return jsonify({"success": False, "error": rows[0]["ErrorMessage"]}), 400

        columns = list(rows[0].keys()) if rows else []
        return jsonify({
            "success": True,
            "table": table_type,
            "keyword": keyword,
            "columns": columns,
            "rows": rows,
            "count": len(rows)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 4. BAR CHART — TOP 15 (TETAP SAMA)
# ===============================================================
@executive_bp.route("/chart", methods=["GET"])
@require_role([1])
def get_chart_data():
    try:
        chart_type = request.args.get("type")
        if not chart_type:
            return jsonify({"success": False, "error": "Missing chart type"}), 400

        allowed_types = ["country", "platform", "genre", "status"]
        if chart_type not in allowed_types:
            return jsonify({"success": False, "error": f"Invalid chart type. Must be one of: {allowed_types}"}), 400

        query = "EXEC UserExecutive.sp_GetBarChart @ChartType = ?"
        rows = execute_query_all(query, (chart_type,))

        if not rows:
            return jsonify({"success": False, "error": "No chart data found"}), 404

        labels = [row["Label"] for row in rows]
        totals = [row["Total"] for row in rows]

        return jsonify({
            "success": True,
            "chart_type": chart_type,
            "labels": labels,
            "totals": totals,
            "raw": rows
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 5. PIE / DONUT CHART (TETAP SAMA)
# ===============================================================
@executive_bp.route("/chart/pie", methods=["GET"])
@require_role([1])
def get_pie_chart():
    try:
        chart_type = request.args.get("type")
        if not chart_type:
            return jsonify({"success": False, "error": "Missing chart type"}), 400

        allowed_types = ["status", "genre", "language", "country"]
        if chart_type not in allowed_types:
            return jsonify({"success": False, "error": f"Invalid chart type. Must be one of: {allowed_types}"}), 400

        query = "EXEC UserExecutive.sp_GetPieChart @ChartType = ?"
        rows = execute_query_all(query, (chart_type,))

        if not rows:
            return jsonify({"success": False, "error": "No pie chart data found"}), 404

        labels = [row["Label"] for row in rows]
        totals = [row["Total"] for row in rows]

        return jsonify({
            "success": True,
            "chart_type": chart_type,
            "labels": labels,
            "totals": totals,
            "raw": rows
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 6. STACKED BAR CHART - BY COUNTRIES (TETAP SAMA)
# ===============================================================
@executive_bp.route("/stacked/countries", methods=["GET"])
@require_role([1])
def get_stacked_countries():
    try:
        rows = execute_query_all("EXEC UserExecutive.sp_Top10CompaniesByCountries_Improved", ())
        
        if not rows:
            return jsonify({"success": False, "error": "No data found"}), 404
        
        companies = []
        company_data = {}
        
        for row in rows:
            company = row["ProductionCompanyName"]
            country = row["ProductionCountryName"]
            count = row["ShowsCount"]
            
            if company not in companies:
                companies.append(company)
                company_data[company] = {}
            
            company_data[company][country] = count
        
        all_countries = []
        for row in rows:
            country = row["ProductionCountryName"]
            if country not in all_countries:
                all_countries.append(country)
        
        companies_sorted = sorted(companies, 
            key=lambda c: sum(company_data[c].values()), 
            reverse=True
        )[:10]
        
        datasets = []
        for country in all_countries:
            country_counts = []
            for company in companies_sorted:
                count = company_data.get(company, {}).get(country, 0)
                country_counts.append(count)
            
            datasets.append({
                "label": country,
                "data": country_counts
            })
        
        return jsonify({
            "success": True,
            "chart_type": "stacked_countries",
            "labels": companies_sorted,
            "datasets": datasets,
            "raw_data": rows
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 7. STACKED BAR CHART - BY STATUS (TETAP SAMA)
# ===============================================================
@executive_bp.route("/stacked/status", methods=["GET"])
@require_role([1])
def get_stacked_status():
    try:
        rows = execute_query_all("EXEC UserExecutive.sp_Top10CompaniesByStatus", ())
        
        if not rows:
            return jsonify({"success": False, "error": "No data found"}), 404
        
        companies = []
        company_data = {}
        
        for row in rows:
            company = row["ProductionCompanyName"]
            status = row["StatusName"]
            count = row["ShowsWithStatus"]
            
            if company not in companies:
                companies.append(company)
                company_data[company] = {}
            
            company_data[company][status] = count
        
        all_statuses = []
        for row in rows:
            status = row["StatusName"]
            if status not in all_statuses:
                all_statuses.append(status)
        
        companies_sorted = sorted(companies,
            key=lambda c: sum(company_data[c].values()),
            reverse=True
        )[:10]
        
        datasets = []
        for status in all_statuses:
            status_counts = []
            for company in companies_sorted:
                count = company_data.get(company, {}).get(status, 0)
                status_counts.append(count)
            
            datasets.append({
                "label": status,
                "data": status_counts
            })
        
        return jsonify({
            "success": True,
            "chart_type": "stacked_status",
            "labels": companies_sorted,
            "datasets": datasets,
            "raw_data": rows
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 8. STACKED BAR CHART - BY GENRES (TETAP SAMA)
# ===============================================================
@executive_bp.route("/stacked/genres", methods=["GET"])
@require_role([1])
def get_stacked_genres():
    try:
        rows = execute_query_all("EXEC UserExecutive.sp_Top10CompaniesByGenres", ())
        
        if not rows:
            return jsonify({"success": False, "error": "No data found"}), 404
        
        companies = []
        company_data = {}
        
        for row in rows:
            company = row["ProductionCompanyName"]
            genre = row["GenreGroup"]
            count = row["UniqueShowCount"]
            
            if company not in companies:
                companies.append(company)
                company_data[company] = {}
            
            company_data[company][genre] = count
        
        all_genres = []
        for row in rows:
            genre = row["GenreGroup"]
            if genre not in all_genres:
                all_genres.append(genre)
        
        if 'Others' in all_genres:
            all_genres.remove('Others')
            all_genres.append('Others')
        
        companies_sorted = sorted(companies,
            key=lambda c: sum(company_data[c].values()),
            reverse=True
        )[:10]
        
        datasets = []
        for genre in all_genres:
            genre_counts = []
            for company in companies_sorted:
                count = company_data.get(company, {}).get(genre, 0)
                genre_counts.append(count)
            
            datasets.append({
                "label": genre,
                "data": genre_counts
            })
        
        return jsonify({
            "success": True,
            "chart_type": "stacked_genres",
            "labels": companies_sorted,
            "datasets": datasets,
            "raw_data": rows
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 9. UNIVERSAL STACKED BAR CHART (TETAP SAMA)
# ===============================================================
@executive_bp.route("/stacked/universal", methods=["GET"])
@require_role([1])
def get_universal_stacked():
    try:
        chart_type = request.args.get("type", "genres")
        sort_by = request.args.get("sort", "total")
        top_n = request.args.get("top", 10, type=int)
        
        if chart_type not in ["countries", "status", "genres"]:
            return jsonify({"success": False, "error": "Invalid chart type. Use: countries, status, or genres"}), 400
        
        if sort_by not in ["total", "name", "percentage"]:
            return jsonify({"success": False, "error": "Invalid sort. Use: total, name, or percentage"}), 400
        
        if top_n < 1 or top_n > 20:
            top_n = 10
        
        query = "EXEC UserExecutive.sp_UniversalStackedBarChart @ChartType = ?, @SortBy = ?, @TopN = ?"
        params = (chart_type, sort_by, top_n)
        rows = execute_query_all(query, params)
        
        if not rows:
            return jsonify({"success": False, "error": "No data found"}), 404
        
        companies = []
        company_data = {}
        company_totals = {}
        
        for row in rows:
            company = row["Company"]
            category = row["CategoryName"]
            value = row["Value"]
            total = row.get("CompanyTotal", 0)
            
            if company not in companies:
                companies.append(company)
                company_data[company] = {}
                company_totals[company] = total
            
            company_data[company][category] = value
        
        all_categories = []
        for row in rows:
            category = row["CategoryName"]
            if category not in all_categories:
                all_categories.append(category)
        
        if sort_by == "total":
            companies_sorted = sorted(companies,
                key=lambda c: company_totals.get(c, 0),
                reverse=True
            )[:top_n]
        elif sort_by == "name":
            companies_sorted = sorted(companies)[:top_n]
        else:
            companies_sorted = companies[:top_n]
        
        datasets = []
        for category in all_categories:
            category_data = []
            for company in companies_sorted:
                value = company_data.get(company, {}).get(category, 0)
                category_data.append(value)
            
            datasets.append({
                "label": category,
                "data": category_data
            })
        
        return jsonify({
            "success": True,
            "chart_type": chart_type,
            "sort_by": sort_by,
            "top_n": top_n,
            "labels": companies_sorted,
            "datasets": datasets,
            "raw_data": rows
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 10. MAP ENDPOINT - WORLD MAP DATA (REVISI UTAMA)
# ===============================================================
@executive_bp.route("/map", methods=["GET"])
@require_role([1])
def get_world_map_data():
    """
    NEW: Endpoint untuk mengambil data World Map dari VIEW v_WorldMap_CountryOverview
    Data sudah lengkap dalam satu View, tidak perlu filter atau parameter
    """
    try:
        query = """
            SELECT 
                CountryName,
                TotalShows,
                Top3Genres,
                Top3ProductionCompanies
            FROM UserExecutive.v_WorldMap_CountryOverview
            ORDER BY TotalShows DESC
        """
        
        rows = execute_query_all(query)
        
        if not rows:
            return jsonify({
                "success": True,
                "data": [],
                "summary": {
                    "total_countries": 0,
                    "total_shows": 0,
                    "message": "No data available"
                }
            })
        
        # Format data untuk frontend
        map_data = []
        total_shows = 0
        
        for row in rows:
            country_name = row.get("CountryName", "").strip()
            if not country_name:
                continue
            
            # Format untuk frontend
            country_data = {
                "country": country_name,
                "total_shows": row.get("TotalShows", 0),
                "top_genres": row.get("Top3Genres", "No genre data"),
                "top_companies": row.get("Top3ProductionCompanies", "No company data"),
                "genre_count": row.get("Top3Genres", "").count('(') if row.get("Top3Genres") else 0,
                "company_count": row.get("Top3ProductionCompanies", "").count('(') if row.get("Top3ProductionCompanies") else 0
            }
            
            map_data.append(country_data)
            total_shows += row.get("TotalShows", 0)
        
        # Summary statistics
        total_countries = len(map_data)
        avg_shows = total_shows / total_countries if total_countries > 0 else 0
        
        # Find top country
        top_country = max(map_data, key=lambda x: x["total_shows"]) if map_data else None
        
        return jsonify({
            "success": True,
            "data": map_data,
            "summary": {
                "total_countries": total_countries,
                "total_shows": total_shows,
                "avg_shows": round(avg_shows, 2),
                "top_country": {
                    "name": top_country["country"] if top_country else "N/A",
                    "shows": top_country["total_shows"] if top_country else 0
                } if top_country else None
            },
            "view_name": "v_WorldMap_CountryOverview",
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 11. MAP ENDPOINT - COUNTRY DETAIL (REVISI UTAMA)
# ===============================================================
@executive_bp.route("/map/<country_name>", methods=["GET"])
@require_role([1])
def get_country_map_details(country_name):
    """
    NEW: Endpoint untuk mengambil detail satu negara dari VIEW v_WorldMap_CountryOverview
    """
    try:
        if not country_name or len(country_name) > 100:
            return jsonify({"success": False, "error": "Invalid country name"}), 400
        
        query = """
            SELECT 
                CountryName,
                TotalShows,
                Top3Genres,
                Top3ProductionCompanies
            FROM UserExecutive.v_WorldMap_CountryOverview
            WHERE LOWER(CountryName) = LOWER(?)
        """
        
        rows = execute_query_all(query, (country_name,))
        
        if not rows:
            return jsonify({
                "success": False,
                "error": f"No data found for country: {country_name}"
            }), 404
        
        row = rows[0]
        
        # Parse genre data (format: "1. Drama (450 shows), 2. Comedy (320 shows), ...")
        genres_text = row.get("Top3Genres", "")
        genres_list = []
        if genres_text != "No genre data":
            parts = genres_text.split(', ')
            for part in parts:
                if '. ' in part and '(' in part and ')' in part:
                    # Format: "1. Drama (450 shows)"
                    try:
                        rank_part, rest = part.split('. ', 1)
                        genre_part = rest.split(' (')[0]
                        count_part = rest.split(' (')[1].replace(' shows)', '')
                        genres_list.append({
                            "rank": int(rank_part),
                            "genre": genre_part,
                            "shows": int(count_part)
                        })
                    except:
                        genres_list.append({"raw": part})
        
        # Parse company data (format: "1. Warner Bros. (180 shows), 2. Netflix (150 shows), ...")
        companies_text = row.get("Top3ProductionCompanies", "")
        companies_list = []
        if companies_text != "No company data":
            parts = companies_text.split(', ')
            for part in parts:
                if '. ' in part and '(' in part and ')' in part:
                    # Format: "1. Warner Bros. (180 shows)"
                    try:
                        rank_part, rest = part.split('. ', 1)
                        company_part = rest.split(' (')[0]
                        count_part = rest.split(' (')[1].replace(' shows)', '')
                        companies_list.append({
                            "rank": int(rank_part),
                            "company": company_part,
                            "shows": int(count_part)
                        })
                    except:
                        companies_list.append({"raw": part})
        
        return jsonify({
            "success": True,
            "country": row.get("CountryName"),
            "total_shows": row.get("TotalShows", 0),
            "genres": {
                "text": row.get("Top3Genres"),
                "parsed": genres_list
            },
            "production_companies": {
                "text": row.get("Top3ProductionCompanies"),
                "parsed": companies_list
            },
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 12. MAP ENDPOINT - COUNTRY LIST (REVISI UTAMA)
# ===============================================================
@executive_bp.route("/map/countries", methods=["GET"])
@require_role([1])
def get_country_list():
    """
    NEW: Endpoint untuk mengambil daftar negara yang tersedia (untuk dropdown)
    """
    try:
        query = """
            SELECT DISTINCT CountryName
            FROM UserExecutive.v_WorldMap_CountryOverview
            WHERE CountryName IS NOT NULL
            ORDER BY CountryName
        """
        
        rows = execute_query_all(query)
        
        countries = [row.get("CountryName") for row in rows if row.get("CountryName")]
        
        return jsonify({
            "success": True,
            "countries": countries,
            "count": len(countries),
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 13. MAP ENDPOINT - QUICK STATS (REVISI UTAMA)
# ===============================================================
@executive_bp.route("/map/stats", methods=["GET"])
@require_role([1])
def get_map_stats():
    """
    NEW: Endpoint untuk statistik cepat dari data map
    """
    try:
        query = """
            SELECT 
                COUNT(*) as country_count,
                SUM(TotalShows) as total_shows,
                AVG(TotalShows) as avg_shows,
                MAX(TotalShows) as max_shows,
                MIN(TotalShows) as min_shows
            FROM UserExecutive.v_WorldMap_CountryOverview
            WHERE TotalShows > 0
        """
        
        rows = execute_query_all(query)
        
        if not rows:
            return jsonify({
                "success": True,
                "stats": {
                    "country_count": 0,
                    "total_shows": 0,
                    "avg_shows": 0,
                    "max_shows": 0,
                    "min_shows": 0
                }
            })
        
        row = rows[0]
        
        return jsonify({
            "success": True,
            "stats": {
                "country_count": row.get("country_count", 0),
                "total_shows": row.get("total_shows", 0),
                "avg_shows": round(row.get("avg_shows", 0), 2),
                "max_shows": row.get("max_shows", 0),
                "min_shows": row.get("min_shows", 0)
            },
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 14. TEST ENDPOINT UNTUK MAP (REVISI UTAMA)
# ===============================================================
@executive_bp.route("/test/map", methods=["GET"])
@require_role([1])
def test_map_endpoint():
    """
    NEW: Test endpoint untuk verifikasi data map
    """
    try:
        # Test 1: Check if view exists and has data
        test_query = "SELECT TOP 5 * FROM UserExecutive.v_WorldMap_CountryOverview"
        rows = execute_query_all(test_query)
        
        # Test 2: Check total countries
        count_query = "SELECT COUNT(*) as count FROM UserExecutive.v_WorldMap_CountryOverview"
        count_result = execute_query_all(count_query)
        
        # Test 3: Check sample data structure
        sample_countries = []
        if rows:
            for row in rows[:3]:
                sample_countries.append({
                    "country": row.get("CountryName"),
                    "shows": row.get("TotalShows"),
                    "has_genres": row.get("Top3Genres") != "No genre data",
                    "has_companies": row.get("Top3ProductionCompanies") != "No company data"
                })
        
        return jsonify({
            "success": True,
            "view_exists": True,
            "total_countries": count_result[0].get("count", 0) if count_result else 0,
            "sample_data": sample_countries,
            "sample_count": len(sample_countries),
            "message": "Map data is working properly",
            "timestamp": datetime.datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "message": "Map data test failed"
        }), 500


# ===============================================================
# 15. ENDPOINT UNTUK MELIHAT DAFTAR ENDPOINT YANG TERSEDIA (TETAP SAMA)
# ===============================================================
@executive_bp.route("/endpoints", methods=["GET"])
@require_role([1])
def get_available_endpoints():
    endpoints = {
        "kpi": {
            "method": "GET",
            "url": "/api/executive/kpi",
            "description": "Mengambil data KPI cards untuk dashboard executive",
            "parameters": "Tidak ada"
        },
        "table": {
            "method": "GET",
            "url": "/api/executive/table?type=<table_type>",
            "description": "Mengambil data tabel executive",
            "parameters": {"type": "overview|genres|languages|production|networks|performance"}
        },
        "table_search": {
            "method": "GET",
            "url": "/api/executive/table/search?type=<table_type>&keyword=<keyword>",
            "description": "Mencari data dalam tabel executive",
            "parameters": {"type": "sama seperti table", "keyword": "opsional"}
        },
        "bar_chart": {
            "method": "GET",
            "url": "/api/executive/chart?type=<chart_type>",
            "description": "Mengambil data bar chart (Top 15)",
            "parameters": {"type": "country|platform|genre|status"}
        },
        "pie_chart": {
            "method": "GET",
            "url": "/api/executive/chart/pie?type=<chart_type>",
            "description": "Mengambil data pie/donut chart",
            "parameters": {"type": "status|genre|language|country"}
        },
        "stacked_countries": {
            "method": "GET",
            "url": "/api/executive/stacked/countries",
            "description": "Stacked bar chart: Top 10 Companies by Countries",
            "parameters": "Tidak ada"
        },
        "stacked_status": {
            "method": "GET",
            "url": "/api/executive/stacked/status",
            "description": "Stacked bar chart: Top 10 Companies by Status",
            "parameters": "Tidak ada"
        },
        "stacked_genres": {
            "method": "GET",
            "url": "/api/executive/stacked/genres",
            "description": "Stacked bar chart: Top 10 Companies by Genres (Top 3 + Others)",
            "parameters": "Tidak ada"
        },
        "stacked_universal": {
            "method": "GET",
            "url": "/api/executive/stacked/universal?type=<chart_type>&sort=<sort_by>&top=<top_n>",
            "description": "Universal stacked bar chart dengan parameter",
            "parameters": {
                "type": "countries|status|genres",
                "sort": "total|name|percentage",
                "top": "1-20 (default: 10)"
            }
        },
        # MAP ENDPOINTS YANG BARU
        "map_all": {
            "method": "GET",
            "url": "/api/executive/map",
            "description": "Mengambil semua data world map dari VIEW v_WorldMap_CountryOverview",
            "parameters": "Tidak ada"
        },
        "map_country_detail": {
            "method": "GET",
            "url": "/api/executive/map/<country_name>",
            "description": "Mengambil detail satu negara dari VIEW",
            "parameters": "country_name: nama negara (contoh: 'United States')"
        },
        "map_countries_list": {
            "method": "GET",
            "url": "/api/executive/map/countries",
            "description": "Mengambil daftar negara yang tersedia (untuk dropdown)",
            "parameters": "Tidak ada"
        },
        "map_stats": {
            "method": "GET",
            "url": "/api/executive/map/stats",
            "description": "Statistik cepat dari data world map",
            "parameters": "Tidak ada"
        },
        "map_test": {
            "method": "GET",
            "url": "/api/executive/test/map",
            "description": "Test endpoint untuk verifikasi data map",
            "parameters": "Tidak ada"
        }
    }
    
    return jsonify({
        "success": True,
        "message": "Executive API endpoints (dengan revisi map)",
        "endpoints": endpoints,
        "total_endpoints": len(endpoints),
        "map_endpoints": 5  # Jumlah endpoint map yang baru
    })


# ===============================================================
# 16. TEST ALL ENDPOINTS (TETAP SAMA)
# ===============================================================
@executive_bp.route("/test/all", methods=["GET"])
@require_role([1])
def test_all_endpoints():
    try:
        test_results = {}
        
        # Test KPI
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("EXEC UserExecutive.sp_KPIExecutive")
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            test_results["kpi"] = {
                "success": True,
                "data": bool(row)
            }
        except Exception as e:
            test_results["kpi"] = {
                "success": False,
                "error": str(e)
            }
        
        # Test Bar Chart
        try:
            rows = execute_query_all("EXEC UserExecutive.sp_GetBarChart @ChartType = 'country'", ())
            test_results["bar_chart"] = {
                "success": True,
                "count": len(rows) if rows else 0
            }
        except Exception as e:
            test_results["bar_chart"] = {
                "success": False,
                "error": str(e)
            }
        
        # Test Stacked Chart
        try:
            rows = execute_query_all("EXEC UserExecutive.sp_Top10CompaniesByCountries_Improved", ())
            test_results["stacked_chart"] = {
                "success": True,
                "count": len(rows) if rows else 0
            }
        except Exception as e:
            test_results["stacked_chart"] = {
                "success": False,
                "error": str(e)
            }
        
        # Test Map Data (NEW)
        try:
            rows = execute_query_all("SELECT TOP 5 * FROM UserExecutive.v_WorldMap_CountryOverview", ())
            test_results["map_data"] = {
                "success": True,
                "count": len(rows) if rows else 0,
                "sample": rows[:2] if rows else []
            }
        except Exception as e:
            test_results["map_data"] = {
                "success": False,
                "error": str(e)
            }
        
        all_passed = all(item.get("success", False) for item in test_results.values())
        
        return jsonify({
            "success": True,
            "message": "All endpoints test completed (with map revision)",
            "results": test_results,
            "status": "All tests passed" if all_passed else "Some tests failed",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===============================================================
# 17. HEALTH CHECK (TETAP SAMA dengan tambahan map check)
# ===============================================================
@executive_bp.route("/health", methods=["GET"])
@require_role([1])
def check_executive_health():
    try:
        # Test database connection
        test_query = "SELECT 1 AS status"
        rows = execute_query_all(test_query)
        
        # Test map view
        map_ok = False
        try:
            map_test = execute_query_all("SELECT TOP 1 CountryName FROM UserExecutive.v_WorldMap_CountryOverview", ())
            map_ok = len(map_test) > 0
        except Exception as e:
            map_ok = False
        
        return jsonify({
            "success": True,
            "status": "healthy",
            "database": "connected" if rows else "disconnected",
            "map_system": "operational" if map_ok else "degraded",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "message": "Executive API dengan World Map View v_WorldMap_CountryOverview"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "status": "unhealthy",
            "error": str(e)
        }), 500


# ===============================================================
# HELPER FUNCTIONS (TETAP SAMA)
# ===============================================================

def get_color_by_value(value, max_value):
    """
    Helper function to get color based on value intensity
    """
    if not max_value or value == 0:
        return "#f5f5f5"  # Light gray for zero/low values
    
    intensity = value / max_value
    
    if intensity > 0.8:
        return "#e53935"  # Red for high values
    elif intensity > 0.6:
        return "#fb8c00"  # Orange
    elif intensity > 0.4:
        return "#fdd835"  # Yellow
    elif intensity > 0.2:
        return "#43a047"  # Green
    else:
        return "#1e88e5"  # Blue for low values