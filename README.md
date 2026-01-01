
---

# 🎬 DREAM Entertainment

**Integrated Database Management System for TV Shows & IMDb Analytics**

DREAM Entertainment (Find Your Story – DREAM) merupakan platform manajemen basis data terintegrasi yang menggabungkan dataset TV Shows dan IMDb untuk mendukung pengelolaan, pencarian, analisis, dan visualisasi data industri hiburan. Sistem ini dirancang untuk memenuhi kebutuhan tiga jenis pengguna: **User Native**, **User Marketing**, dan **User Executive**.

---

## 📌 Tujuan Sistem

* Mengintegrasikan data TV Shows dan IMDb dalam satu basis data terstruktur.
* Menyediakan antarmuka interaktif untuk eksplorasi dan pencarian konten.
* Menyediakan dashboard analitik real-time berbasis visualisasi.
* Menerapkan sistem keamanan berbasis **Role-Based Access Control (RBAC)**.

---

## 👥 Jenis Pengguna

| Role               | Deskripsi Fitur                                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| **User Native**    | Landing page trending shows, advanced search, show detail page, discover by category, dan tab About.                      |
| **User Marketing** | Dashboard KPI, analisis pertumbuhan film, distribusi genre, peta distribusi negara, dan analisis platform.                |
| **User Executive** | Dashboard strategis berisi KPI Cards, bar chart, pie chart, stacked bar chart, executive table, dan world map interaktif. |

---

## 🏗️ Arsitektur Sistem

Sistem dibangun menggunakan **three-tier architecture**:

| Layer    | Teknologi                            |
| -------- | ------------------------------------ |
| Frontend | Vue.js, CSS                          |
| Backend  | Flask (Python) – REST API            |
| Database | Microsoft SQL Server (SSMS, DBeaver) |

---

## 🗄️ Proses Pengolahan Database

1. Import data menggunakan **SSIS, Bulk Insert, dan BCP**.
2. Cleansing data dengan mengubah nilai tidak valid (`\N`, `/N`) menjadi `NULL`.
3. Normalisasi hingga **1NF** dengan memecah kolom multi-nilai.
4. Pembentukan skema final dengan relasi **Primary Key** dan **Foreign Key**.
5. Penerapan indexing untuk meningkatkan performa query.
6. Integrasi TV Shows dan IMDb melalui tabel bridging seperti `TitleGenres` dan `GenreTypes`.

---

## 🔐 Keamanan Sistem

Sistem menerapkan keamanan berlapis:

* Autentikasi menggunakan **Stored Procedure** (`sp_CreateAccount`, `sp_Login`).
* Hash password dengan algoritma **SHA-256**.
* Penetapan role otomatis menggunakan **Trigger**.
* Pembatasan akses database berbasis **role_native**, **role_marketing**, dan **role_executive**.
* Proteksi tabel sensitif (`dbo.Users`) menggunakan perintah `DENY`.
* Autentikasi API menggunakan **JWT Token** dan middleware validasi role.

---

## 🌐 API Endpoint

### API Executive

Menyediakan endpoint untuk KPI, tabel eksekutif, bar chart, pie chart, stacked bar chart, dan world map.

Contoh endpoint:

* `/api/executive/kpi`
* `/api/executive/chart`
* `/api/executive/map`
* `/api/executive/table`

### API Marketing

Menyediakan endpoint analitik berbasis filter tahun.

Contoh endpoint:

* `/api/marketing/kpi`
* `/api/marketing/charts/movies-growth-year`
* `/api/marketing/charts/top-platforms`

### API Native

Digunakan oleh pengguna publik tanpa login.

Contoh endpoint:

* `/api/native/top-trending`
* `/api/native/search`
* `/api/native/detail/<show_id>`

---

## 📊 Fitur Visualisasi

* **Line Chart** – Pertumbuhan jumlah film per tahun.
* **Bar Chart** – Top production countries, top platforms, top genres.
* **Pie / Donut Chart** – Distribusi status, genre, bahasa, dan negara.
* **Stacked Bar Chart** – Distribusi perusahaan berdasarkan genre, negara, dan status.
* **Choropleth Map** – Distribusi produksi film secara global.

---

## 🧪 Tools yang Digunakan

| Komponen    | Teknologi              |
| ----------- | ---------------------- |
| Database    | Microsoft SQL Server   |
| Backend     | Python Flask           |
| Frontend    | Vue.js                 |
| IDE / Tools | DBeaver, VS Code, SSIS |

---

## 🏁 Kesimpulan

DREAM Entertainment berhasil mengintegrasikan dataset TV Shows dan IMDb menjadi sistem manajemen basis data terpusat yang mendukung eksplorasi data, analisis strategis, serta visualisasi interaktif. Sistem ini memberikan nilai tambah melalui penerapan RBAC, optimasi performa query dengan indexing, serta arsitektur yang scalable untuk pengembangan lebih lanjut di industri hiburan berbasis data.

---

## 👨‍💻 Author

* **L0224010 – Rambat Ungu Aryati**
* **L0224004 – Dhea Meidiyana Windawati**
