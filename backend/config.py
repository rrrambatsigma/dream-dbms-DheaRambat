# config.py
import urllib

# Buat string koneksi untuk SQL Server menggunakan Windows Authentication
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-IKTCBU6;"         # <- nama server kamu
    "DATABASE=FINAL_PROJECT;"      # <- nama database kamu
    "Trusted_Connection=yes;"      # <- Windows Authentication
)

# Encode connection string agar bisa dipakai di SQLAlchemy
params = urllib.parse.quote_plus(connection_string)

# Connection URI untuk SQLAlchemy
SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"

# ============================================
# SECRET KEY FLASK (UNTUK SESSION, JWT, ETC)
# ============================================

SECRET_KEY = "PROJECT_FINAL_SUPER_SECRET"