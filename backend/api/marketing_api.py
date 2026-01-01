# =========================================================
# api/marketing_api.py - VERSI RAPI & LENGKAP
# =========================================================

from flask import Blueprint, jsonify, request
from utils.auth_middleware import require_role
from utils.db_connection import execute_query_single, execute_query_all
import traceback
import pycountry

# =========================================================
# BLUEPRINT
# =========================================================
marketing_bp = Blueprint("marketing", __name__)

# =========================================================
# HELPER FUNCTIONS
# =========================================================
def get_year_params():
    """Extract start_year and end_year from request arguments"""
    start_year = request.args.get('start_year', type=int)
    end_year = request.args.get('end_year', type=int)
    
    # Validasi
    if start_year is not None and end_year is not None:
        # Pastikan start_year <= end_year
        if start_year > end_year:
            start_year, end_year = end_year, start_year
    else:
        # Jika tidak ada parameter tahun, ambil dari database
        try:
            years_result = execute_query_all("""
                SELECT MIN(YEAR(AirDate)) as min_year, 
                       MAX(YEAR(AirDate)) as max_year
                FROM AirDates 
                WHERE IsFirst = 1 AND AirDate IS NOT NULL
            """) or []
            
            if years_result and years_result[0].get('min_year') and years_result[0].get('max_year'):
                start_year = years_result[0]['min_year']
                end_year = years_result[0]['max_year']
            else:
                # Default fallback
                start_year = 1900
                end_year = 2025
        except Exception as e:
            print(f"Error getting year range: {e}")
            start_year = 1900
            end_year = 2025
    
    return start_year, end_year

# =========================================================
# TEST / PUBLIC ENDPOINTS
# =========================================================
@marketing_bp.get("/test-cors")
def test_cors():
    return jsonify({
        "success": True,
        "message": "CORS test successful (marketing)"
    }), 200

@marketing_bp.get("/public-test")
def public_test():
    return jsonify({
        "success": True,
        "message": "Public marketing endpoint",
        "auth": "not required"
    }), 200

# =========================================================
# MARKETING CORE ENDPOINTS
# =========================================================

# ---------------------------------------------------------
# 1. WELCOME
# ---------------------------------------------------------
@marketing_bp.get("/welcome")
@require_role([2])  # RoleID 2 = MARKETING
def marketing_welcome():
    return jsonify({
        "success": True,
        "role": "MARKETING",
        "message": "Welcome Marketing Team"
    }), 200

# ---------------------------------------------------------
# 2. KPI DASHBOARD (with year filtering)
# ---------------------------------------------------------
@marketing_bp.get("/kpi")
@require_role([2])
def get_marketing_kpi():
    try:
        start_year, end_year = get_year_params()
        
        # Debug info
        print(f"📊 KPI Request - start_year: {start_year}, end_year: {end_year}")
        
        query = f"""
            SELECT * 
            FROM fn_get_marketing_kpi({start_year}, {end_year})
        """
        
        print(f"📋 Executing KPI query: {query}")
        result = execute_query_single(query)
        print(f"📦 KPI Result: {result}")

        if not result:
            return jsonify({
                "success": False,
                "message": "No KPI data found for the selected year range",
                "year_range": {
                    "start_year": start_year,
                    "end_year": end_year
                }
            }), 404

        data = {
            "year_range": {
                "start_year": start_year,
                "end_year": end_year,
                "year_span": end_year - start_year + 1
            },
            "total_movies": result.get("TotalMovies", 0) or 0,
            "top_film": {
                "name": result.get("TopFilm_Name") or "-",
                "total_votes": result.get("TopFilm_TotalVotes", 0) or 0
            },
            "top_rating": {
                "name": result.get("TopRating_Name") or "-",
                "average_rating": float(result.get("TopRating_Average", 0)) if result.get("TopRating_Average") else 0
            },
            "top_platform": result.get("TopPlatform") or "-",
            "top_country": result.get("TopCountry") or "-",
            "top_genre": result.get("TopGenre") or "-"
        }

        return jsonify({
            "success": True,
            "data": data
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e),
            "error_details": traceback.format_exc()
        }), 500

# Alias dashboard → KPI
@marketing_bp.get("/dashboard")
@require_role([2])
def marketing_dashboard():
    return get_marketing_kpi()

# ---------------------------------------------------------
# 2.5 AVAILABLE YEARS (NEW)
# ---------------------------------------------------------
@marketing_bp.get("/available-years")
@require_role([2])
def get_available_years():
    try:
        # Pakai query langsung ke database
        data = execute_query_all("""
            SELECT DISTINCT YEAR(AirDate) AS Year
            FROM AirDates
            WHERE IsFirst = 1 
              AND AirDate IS NOT NULL
              AND YEAR(AirDate) IS NOT NULL
            ORDER BY Year ASC
        """) or []
        
        print(f"📅 Available years query result: {data}")
        
        years = [row['Year'] for row in data if row['Year'] is not None]
        
        response = {
            "success": True,
            "data": years,
            "min_year": min(years) if years else None,
            "max_year": max(years) if years else None,
            "total_years": len(years)
        }
        
        print(f"📅 Available years response: {response}")
        return jsonify(response), 200
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e),
            "error_details": traceback.format_exc(),
            "data": []
        }), 500

# =========================================================
# CHART ENDPOINTS (all with year filtering)
# =========================================================

# ---------------------------------------------------------
# 3. Movies Growth per Year (LINE CHART) - FIXED
# ---------------------------------------------------------
@marketing_bp.get("/charts/movies-growth-year")
@require_role([2])
def chart_movies_growth_year():
    try:
        start_year, end_year = get_year_params()
        
        # GANTI dengan query yang PASTI menggunakan parameter tahun
        query = f"""
            SELECT * 
            FROM fn_get_movies_growth({start_year}, {end_year})
            ORDER BY Year ASC
        """
        
        print(f"📈 Query movies growth: {query}")
        data = execute_query_all(query) or []
        print(f"📈 Data result: {len(data)} rows")
        
        # DEBUG: Print data untuk verifikasi
        for item in data:
            print(f"📊 Year: {item.get('Year')}, TotalShows: {item.get('TotalShows')}")
        
        return jsonify({
            "success": True,
            "data": data,
            "year_range": {
                "start_year": start_year,
                "end_year": end_year
            }
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e),
            "data": []
        }), 500

# ---------------------------------------------------------
# 4. Genre Distribution (PIE / DONUT)
# ---------------------------------------------------------
@marketing_bp.get("/charts/genre-distribution")
@require_role([2])
def chart_genre_distribution():
    try:
        start_year, end_year = get_year_params()
        
        # DEBUG: Print tahun yang digunakan
        print(f"🎭 GENRE DISTRIBUTION - Year Range: {start_year} to {end_year}")
        
        # Pakai fungsi dengan parameter tahun
        query = f"""
            SELECT GenreName, TotalMovies
            FROM fn_get_genre_distribution({start_year}, {end_year})
            ORDER BY TotalMovies DESC
        """
        
        print(f"🎭 Query: {query}")
        
        all_genres = execute_query_all(query) or []
        
        # DEBUG: Print hasil query
        print(f"🎭 Raw data count: {len(all_genres)}")
        for i, genre in enumerate(all_genres[:5]):
            print(f"🎭 {i+1}. {genre.get('GenreName')}: {genre.get('TotalMovies')}")
        
        # Ambil top 5 dan group lainnya
        top_5 = all_genres[:5]
        others_total = sum(row['TotalMovies'] for row in all_genres[5:])
        
        data = top_5
        if others_total > 0:
            data.append({
                "GenreName": "Others",
                "TotalMovies": others_total
            })
        
        return jsonify({
            "success": True,
            "data": data,
            "year_range": {
                "start_year": start_year,
                "end_year": end_year
            }
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e),
            "data": []
        }), 500

# ---------------------------------------------------------
# 5. Country Distribution (MAP) - SIMPLE VERSION
# ---------------------------------------------------------
@marketing_bp.get("/charts/country-distribution-map")
@require_role([2])
def chart_country_distribution_map():
    try:
        start_year, end_year = get_year_params()
        
        # Pakai fungsi dengan parameter tahun
        query = f"""
            SELECT CountryRegion, TotalTitles, CountryName
            FROM fn_get_country_distribution({start_year}, {end_year})
            WHERE TotalTitles > 0
        """
        
        raw_data = execute_query_all(query) or []

        mapped = []
        special_codes = {
            "XWW": "Worldwide",
            "XWG": "Global",
            "XEU": "Europe"
        }

        for row in raw_data:
            code = (row.get("CountryRegion") or row.get("CountryName") or "").upper()
            if not code:
                continue
                
            name = special_codes.get(code, code)
            iso3 = code

            try:
                country = (
                    pycountry.countries.get(alpha_2=code)
                    or pycountry.countries.get(alpha_3=code)
                )
                if country:
                    name = country.name
                    iso3 = country.alpha_3
            except:
                pass

            mapped.append({
                "name": name,
                "code": iso3,
                "value": row.get("TotalTitles", 0)
            })

        return jsonify({
            "success": True,
            "data": mapped,
            "year_range": {
                "start_year": start_year,
                "end_year": end_year
            }
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e),
            "data": []
        }), 500

# ---------------------------------------------------------
# 6. Top 10 Platforms (BAR)
# ---------------------------------------------------------
@marketing_bp.get("/charts/top-platforms")
@require_role([2])
def chart_top_platforms():
    try:
        start_year, end_year = get_year_params()
        
        # Pakai fungsi dengan parameter tahun
        query = f"""
            SELECT Platform, TotalMovies
            FROM fn_get_top_platforms({start_year}, {end_year})
        """
        
        data = execute_query_all(query) or []

        return jsonify({
            "success": True,
            "data": data,
            "year_range": {
                "start_year": start_year,
                "end_year": end_year
            }
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e),
            "data": []
        }), 500

# ---------------------------------------------------------
# 7. Top 10 Most Rated Movies
# ---------------------------------------------------------
@marketing_bp.get("/charts/top-most-rated")
@require_role([2])
def chart_top_most_rated():
    try:
        start_year, end_year = get_year_params()
        
        # Pakai fungsi dengan parameter tahun
        query = f"""
            SELECT Movie, VoteCount
            FROM fn_get_most_rated_movies({start_year}, {end_year})
        """
        
        data = execute_query_all(query) or []

        return jsonify({
            "success": True,
            "data": data,
            "year_range": {
                "start_year": start_year,
                "end_year": end_year
            }
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e),
            "data": []
        }), 500

# ---------------------------------------------------------
# 8. Top Production Companies (HORIZONTAL BAR)
# ---------------------------------------------------------
@marketing_bp.get("/charts/top-production-companies")
@require_role([2])
def chart_top_production_companies():
    try:
        start_year, end_year = get_year_params()
        
        # DEBUG: Print tahun yang digunakan
        print(f"🏢 PRODUCTION COMPANIES - Year Range: {start_year} to {end_year}")
        
        # Pakai fungsi dengan parameter tahun
        query = f"""
            SELECT Company, TotalMovies, AvgRating, TotalVotes
            FROM fn_get_production_companies({start_year}, {end_year})
            ORDER BY TotalMovies DESC
        """
        
        print(f"🏢 Query: {query}")
        
        data = execute_query_all(query) or []
        
        # DEBUG: Print hasil query
        print(f"🏢 Raw data count: {len(data)}")
        for i, company in enumerate(data[:3]):
            print(f"🏢 {i+1}. {company.get('Company')}: {company.get('TotalMovies')} movies")
        
        formatted = [
            {
                "Company": row["Company"],
                "TotalMovies": row["TotalMovies"],
                "AvgRating": float(row["AvgRating"]) if row["AvgRating"] is not None else 0,
                "TotalVotes": row["TotalVotes"]
            }
            for row in data
        ]

        return jsonify({
            "success": True,
            "data": formatted,
            "year_range": {
                "start_year": start_year,
                "end_year": end_year
            }
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e),
            "data": []
        }), 500

# ---------------------------------------------------------
# 9. Highest Rated Movies
# ---------------------------------------------------------
@marketing_bp.get("/charts/top-highest-rated")
@require_role([2])
def chart_top_highest_rated():
    try:
        start_year, end_year = get_year_params()
        
        # Pakai fungsi dengan parameter tahun
        query = f"""
            SELECT TOP 10
                s.Name AS Movie,
                sv.VoteAverage,
                sv.VoteCount,
                (sv.VoteAverage * sv.VoteCount) AS RankingScore
            FROM Shows s
            JOIN ShowVotes sv ON s.ShowID = sv.ShowID
            JOIN AirDates ad ON s.ShowID = ad.ShowID
            WHERE ad.IsFirst = 1 
              AND YEAR(ad.AirDate) BETWEEN {start_year} AND {end_year}
              AND sv.VoteCount > 100
            ORDER BY sv.VoteAverage DESC, sv.VoteCount DESC
        """
        
        data = execute_query_all(query) or []

        return jsonify({
            "success": True,
            "data": data,
            "year_range": {
                "start_year": start_year,
                "end_year": end_year
            }
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": True,
            "data": [],
            "message": str(e)
        }), 200

# ---------------------------------------------------------
# 10. Country Category Map (NEW) - dengan top 3 dan others
# ---------------------------------------------------------
# =========================================================
# api/marketing_api.py - PERBAIKAN ERROR 500
# =========================================================

# ... (kode sebelumnya tetap) ...

# =========================================================
# HELPER FUNCTION UNTUK KONVERSI OTOMATIS
# =========================================================

def get_full_country_name(original_name, country_code):
    """
    OTOMATIS konversi nama/kode negara ke nama lengkap
    """
    try:
        # Jika original_name sudah nama lengkap, langsung return
        if not original_name:
            return original_name
        
        # Coba berdasarkan code dulu
        if country_code:
            try:
                if len(country_code) == 2:
                    country = pycountry.countries.get(alpha_2=country_code.upper())
                    if country:
                        return country.name
                elif len(country_code) == 3:
                    country = pycountry.countries.get(alpha_3=country_code.upper())
                    if country:
                        return country.name
            except Exception:
                pass
        
        # Coba berdasarkan nama original dengan fuzzy search
        try:
            results = pycountry.countries.search_fuzzy(str(original_name))
            if results and len(results) > 0:
                return results[0].name
        except (LookupError, AttributeError):
            pass
        
        # Jika tidak ditemukan, return original
        return str(original_name)
        
    except Exception as e:
        print(f"⚠️ Error in get_full_country_name: {e}")
        return str(original_name)

def get_iso3_code(original_name, country_code):
    """
    OTOMATIS dapatkan ISO3 code
    """
    try:
        if not original_name and not country_code:
            return "XXX"
        
        # Coba berdasarkan code dulu
        if country_code:
            try:
                if len(country_code) == 2:
                    country = pycountry.countries.get(alpha_2=country_code.upper())
                    if country:
                        return country.alpha_3
                elif len(country_code) == 3:
                    # Cek apakah valid ISO3 code
                    country = pycountry.countries.get(alpha_3=country_code.upper())
                    if country:
                        return country.alpha_3
                    else:
                        # Jika tidak valid, tetap pakai
                        return country_code.upper()
            except Exception:
                pass
        
        # Coba berdasarkan nama
        try:
            results = pycountry.countries.search_fuzzy(str(original_name))
            if results and len(results) > 0:
                return results[0].alpha_3
        except (LookupError, AttributeError):
            pass
        
        # Fallback: buat code dari 3 huruf pertama
        if original_name:
            return original_name[:3].upper() if len(original_name) >= 3 else original_name.upper()
        
        return "XXX"
        
    except Exception as e:
        print(f"⚠️ Error in get_iso3_code: {e}")
        return "XXX"

# ---------------------------------------------------------
# 10. Country Category Map (NEW) - dengan error handling
# ---------------------------------------------------------
@marketing_bp.get("/charts/country-category-map")
@require_role([2])
def chart_country_category_map():
    try:
        start_year, end_year = get_year_params()
        
        # Get category parameter
        category_type = request.args.get('category_type', 'genre').lower()
        
        # Validate category type
        valid_categories = ['genre', 'network', 'status']
        if category_type not in valid_categories:
            return jsonify({
                "success": False,
                "message": f"Invalid category type. Must be one of: {', '.join(valid_categories)}",
                "data": []
            }), 400
        
        print(f"🗺️ MAP REQUEST: start_year={start_year}, end_year={end_year}, category_type={category_type}")
        
        # Build query - dengan try-catch untuk SQL error
        try:
            query = f"""
                SELECT 
                    CountryName,
                    CountryCode,
                    TotalMovies,
                    CategoryName,
                    CategoryValue,
                    CategoryCount,
                    CategoryRank
                FROM fn_get_country_category_data(
                    {start_year}, 
                    {end_year}, 
                    '{category_type}'
                )
                ORDER BY CountryName, CategoryRank
            """
            
            print(f"🗺️ SQL QUERY: {query}")
            
            raw_data = execute_query_all(query) or []
            print(f"🗺️ RAW DATA COUNT: {len(raw_data)}")
            
        except Exception as sql_error:
            print(f"❌ SQL ERROR: {sql_error}")
            return jsonify({
                "success": False,
                "message": f"Database error: {str(sql_error)}",
                "data": []
            }), 500
        
        if not raw_data:
            print("⚠️ No data returned from database")
            return jsonify({
                "success": True,
                "data": [],
                "message": "No data found for the selected parameters",
                "year_range": {
                    "start_year": start_year,
                    "end_year": end_year
                }
            }), 200
        
        # Dictionary untuk menyimpan data per negara
        country_data_dict = {}
        
        # PROCESS SETIAP BARIS DATA
        for row in raw_data:
            try:
                original_name = row.get("CountryName") or ""
                country_code = row.get("CountryCode") or ""
                
                print(f"📄 Processing: {original_name} ({country_code})")
                
                # Cari nama lengkap negara OTOMATIS
                full_country_name = get_full_country_name(original_name, country_code)
                iso3_code = get_iso3_code(original_name, country_code)
                
                print(f"   → Converted to: {full_country_name} ({iso3_code})")
                
                # Gunakan nama lengkap sebagai key
                if full_country_name not in country_data_dict:
                    country_data_dict[full_country_name] = {
                        "name": full_country_name,
                        "code": iso3_code,
                        "total_movies": row.get("TotalMovies", 0),
                        "top_categories": [],
                        "others_count": 0,
                        "has_data": False
                    }
                
                category_info = {
                    "name": row.get("CategoryName", ""),
                    "value": row.get("CategoryValue", ""),
                    "count": row.get("CategoryCount", 0),
                    "rank": row.get("CategoryRank", 0)
                }
                
                # Simpan kategori
                if row.get("CategoryName") != "No Data":
                    country_data_dict[full_country_name]["has_data"] = True
                
                if row.get("CategoryRank", 0) <= 3 and row.get("CategoryName") != "Others":
                    country_data_dict[full_country_name]["top_categories"].append(category_info)
                
                if row.get("CategoryName") == "Others":
                    country_data_dict[full_country_name]["others_count"] = row.get("CategoryCount", 0)
                    
            except Exception as row_error:
                print(f"⚠️ Error processing row: {row_error}")
                print(f"   Row data: {row}")
                continue
        
        # Konversi ke array untuk response
        result_data = []
        total_movies_global = 0
        
        for country_name, data in country_data_dict.items():
            try:
                # Urutkan top categories
                top_categories_sorted = sorted(
                    [cat for cat in data["top_categories"] if cat.get("rank", 0) <= 3],
                    key=lambda x: x.get("rank", 0)
                )[:3]
                
                country_item = {
                    "name": data["name"],
                    "code": data["code"],
                    "value": data["total_movies"],
                    "total_movies": data["total_movies"],
                    "has_data": data["has_data"],
                    "category_type": category_type,
                    "top_categories": top_categories_sorted,
                    "others_count": data["others_count"]
                }
                
                result_data.append(country_item)
                total_movies_global += data["total_movies"]
                
            except Exception as country_error:
                print(f"⚠️ Error processing country {country_name}: {country_error}")
                continue
        
        print(f"✅ MAP PROCESSED: {len(result_data)} countries, {total_movies_global} total movies")
        
        if result_data:
            sample = result_data[0]
            print(f"📊 SAMPLE COUNTRY: {sample['name']} ({sample['code']})")
            print(f"📊 Total Movies: {sample['total_movies']}")
            print(f"📊 Has Data: {sample['has_data']}")
            print(f"📊 Top Categories: {len(sample['top_categories'])}")
        
        return jsonify({
            "success": True,
            "data": result_data,
            "category_type": category_type,
            "year_range": {
                "start_year": start_year,
                "end_year": end_year
            },
            "countries_count": len(result_data),
            "total_movies_global": total_movies_global
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}",
            "error_details": traceback.format_exc(),
            "data": []
        }), 500

# =========================================================
# DEBUG Endpoint (diperbarui)
# =========================================================
@marketing_bp.get("/debug-endpoints")
def debug_endpoints():
    return jsonify({
        "success": True,
        "base_url": "/api/marketing",
        "endpoints": [
            "/welcome",
            "/available-years",
            "/kpi?start_year=2000&end_year=2024",
            "/dashboard?start_year=2000&end_year=2024",
            "/charts/movies-growth-year?start_year=2000&end_year=2024",
            "/charts/genre-distribution?start_year=2000&end_year=2024",
            "/charts/country-distribution-map?start_year=2000&end_year=2024",
            "/charts/country-category-map?start_year=2000&end_year=2024&category_type=genre",
            "/charts/top-platforms?start_year=2000&end_year=2024",
            "/charts/top-most-rated?start_year=2000&end_year=2024",
            "/charts/top-highest-rated?start_year=2000&end_year=2024",
            "/charts/top-production-companies?start_year=2000&end_year=2024"
        ],
        "map_endpoints": {
            "simple": "/charts/country-distribution-map - Simple country data",
            "category": "/charts/country-category-map - With top 3 categories per country"
        },
        "category_examples": {
            "genre": "/charts/country-category-map?category_type=genre",
            "network": "/charts/country-category-map?category_type=network",
            "status": "/charts/country-category-map?category_type=status"
        }
    }), 200