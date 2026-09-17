# Olist E-Commerce Diagnostic & Strategic Analytics Engine

Hệ thống chẩn đoán dữ liệu thương mại điện tử chuyên sâu (Enterprise Diagnostic Analytics) khai thác trực tiếp từ cơ sở dữ liệu quy mô lớn của sàn thương mại điện tử Olist (Brazil). Dự án tập trung vào việc bóc tách các điểm nghẽn chuỗi cung ứng, giải mã các nghịch lý vận hành và tự động hóa quy trình phân tích thành bộ tứ sản phẩm bàn giao: **Báo cáo Chẩn đoán (Chat), Sổ Báo cáo Tài chính/Vận hành (Excel), Dashboard Tương tác Đa tầng (HTML) và Mô hình Phân tích Tự động Chuẩn Microsoft Fabric (Power BI PBIP)**.

---

## 🧭 Kiến Trúc Hệ Thống (System Architecture)

```text
[CSDL Thực Chứng: MySQL olist_raw (99,441 Đơn)]
                      │
                      ▼
[Python Diagnostic Engine: generate_handover_data.py]
  (Đo lường độ lệch SLA, gộp trước - JOIN sau, chống fan-out)
                      │
        ┌─────────────┼─────────────────────────┐
        ▼             ▼                         ▼
[Data Mart CSV]  [Sổ Báo Cáo Excel]     [Paginated HTML Cockpit]
  (Thư mục       (Olist_Fulfillment_     (Olist_Fulfillment_
   data_bi/)      Handover_Analysis.      Handover_Cockpit.html)
        │         xlsx - 5 Sheet)        (Chart.js, Slicers, UI/UX)
        ▼
[Mô Hình Power BI PBIP]
  (PBIR + TMDL, Schema 2.9.0, Theme Midnight Navy)
        │
        ▼
[CLI Pre-flight Validation: powerbi-report-author]
  (Bắt buộc kiểm định: 0 Error, 0 Warning)
```

---

## 🎯 Chuyên Đề Tiêu Biểu: Điểm Nghẽn Bàn Giao & Nghịch Lý Carrier Cứu Đơn
*(The Fulfillment Handover Bottleneck & The Carrier Rescue Paradox)*

### 1. Ma Trận 4 Phân Khúc Bàn Giao Thực Chứng (96,999 Đơn Hàng Delivered)

| Phân Khúc Bàn Giao | Quy Mô Đơn | Tỷ Trọng | Doanh Thu (BRL) | AOV (BRL) | Điểm Review | % 1-Sao | TG Seller Chuẩn Bị | TG Carrier Transit | Đệm SLA Còn Lại |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Q1: Chuẩn SLA** *(Seller đúng, Carrier kịp)* | 83,493 | 86.08% | R$ 11,205,605 | R$ 134.21 | **4.31 ★** | 6.32% | 2.54 ngày | 7.99 ngày | **+13.08 ngày** |
| **Q2: Carrier Gánh** *(Seller trễ, Carrier cứu)* | 6,944 | 7.16% | R$ 1,083,205 | R$ 155.99 | **4.07 ★** | 9.91% | **8.60 ngày** | **7.62 ngày** | **+9.36 ngày** |
| **Q3: Carrier Gãy** *(Seller đúng, Carrier trễ)* | 4,745 | 4.89% | R$ 664,632 | R$ 140.07 | **2.27 ★** | **52.39%** | 3.03 ngày | **31.56 ngày** | **-11.58 ngày** |
| **Q4: Thảm Họa Kép** *(Seller trễ, Carrier trễ)* | 1,817 | 1.87% | R$ 325,145 | R$ 178.95 | **2.27 ★** | **52.72%** | **13.86 ngày** | **18.33 ngày** | **-10.53 ngày** |

### 2. Hai Nghịch Lý Cốt Lõi Được Phát Hiện
1. **Bẫy Dung Túng Người Bán (The Tolerated Laggard Trap):** Có tới **79.26% số đơn hàng người bán ngâm trễ hạn (6,944 đơn Q2) được đơn vị vận chuyển chạy nước rút giao trong 7.62 ngày** để bù giờ cho người bán. Khách hàng vẫn chấm 4.07 sao vì nhận trước ngày cam kết, tạo tâm lý chủ quan cho người bán và biến thành khủng hoảng giao trễ vào mùa cao điểm Black Friday.
2. **Cơ Chế Phạt Nhị Phân & Đáy Review Đồng Nhất:** Dù lỗi trễ 100% do bưu cục trong khi người bán gửi cực nhanh trong 3 ngày (Q3) hay cả người bán lẫn bưu cục cùng trễ (Q4), **điểm review của khách hàng đều chạm đáy ở mức chính xác 2.27 sao và tỷ lệ 1-sao chạm 52.4%**. Khách hàng trừng phạt nhị phân theo ngày hứa trên ứng dụng, khiến người bán chuẩn mực bị phạt oan điểm hiển thị.

---

## 🚀 Hướng Dẫn Thực Thi Quy Trình Phân Tích (Step-by-Step Execution)

### Bước 1: Kiểm tra kết nối CSDL và dữ liệu nguồn
```bash
python check_db_connection.py
```
*Kiểm định trạng thái 99,441 đơn hàng, tính toàn vẹn khóa ngoại trên bảng `orders`, `order_items`, `payments`, `reviews`.*

### Bước 2: Trích xuất Data Mart & Tạo sổ báo cáo Excel
```bash
python generate_handover_data.py
```
*Tự động trích xuất các bảng dữ liệu tổng hợp vào `data_bi/` và xuất file Excel `Olist_Fulfillment_Handover_Analysis.xlsx` (5 sheet: KPIs, Quadrants, Regional, Category, Relational Model).*

### Bước 3: Dựng dự án Power BI Desktop PBIP chuẩn Microsoft Fabric
```bash
python build_handover_pbip_complete.py
```
*Tạo toàn bộ mã nguồn TMDL (mô hình dữ liệu) và PBIR v2 (visual containers: cardVisual, donutChart, barChart, lineClusteredColumnComboChart, tableEx, slicer).*

### Bước 4: Kiểm định mã nguồn Power BI qua CLI
```bash
powerbi-report-author validate "reports/Fulfillment_Handover_Diagnostic.Report"
```
*Bắt buộc trả về `result: "succeeded"` với `errorCount: 0` và `warningCount: 0`.*

### Bước 5: Tạo Dashboard HTML tương tác sâu (UX/UI Optimized)
```bash
python generate_handover_dashboard_html.py
```
*Xuất bản `Olist_Fulfillment_Handover_Cockpit.html` chuẩn giao diện Tab-Based Natural Flow, biểu đồ 360px thoáng mắt, bộ lọc tương tác 2 chiều và thông báo toast.*

### Bước 6: Khởi chạy Power BI Desktop Bridge
```bash
powerbi-desktop open "reports/Fulfillment_Handover_Diagnostic.pbip"
```
*Kích hoạt giao diện Power BI Desktop, kết nối bridge tự động và nạp dữ liệu tức thì.*

---

## 📦 Danh Mục Tệp Tin Đẩy Lên GitHub (Staging Manifest)

### Các tệp tin cốt lõi (BẮT BUỘC THEO DÕI):
* **Mã nguồn tự động hóa:**
  * `generate_handover_data.py`: Trích xuất dữ liệu, tính toán ma trận và sinh file Excel.
  * `build_handover_pbip_complete.py`: Trình dựng dự án Fabric PBIP hoàn chỉnh.
  * `generate_handover_dashboard_html.py`: Trình render HTML Dashboard tương tác.
  * `check_db_connection.py`: Script kiểm tra CSDL và đối soát số dòng.
* **Sản phẩm bàn giao phân tích:**
  * `Olist_Fulfillment_Handover_Cockpit.html`: Dashboard tương tác 5 chặng logic (HTML standalone).
  * `Olist_Fulfillment_Handover_Analysis.xlsx`: Sổ báo cáo Excel 5 sheet chuẩn tài chính.
  * `Fulfillment_Handover_Preview.svg`: Bản thiết kế đồ họa Vector độ nét cao.
  * `reports/Fulfillment_Handover_Diagnostic.pbip`: File dự án Power BI.
  * `reports/Fulfillment_Handover_Diagnostic.Report/`: Toàn bộ visual containers, theme, layout PBIR.
  * `reports/Fulfillment_Handover_Diagnostic.SemanticModel/`: Toàn bộ bảng TMDL và partition M.
* **Kho Data Mart CSV (Nguồn cấp Power BI):**
  * `data_bi/fact_fulfillment_quadrants.csv`
  * `data_bi/fact_regional_logistics_friction.csv`
  * `data_bi/fact_category_seller_overdue.csv`
  * `data_bi/fact_fulfillment_kpi_summary.csv`
* **Tài liệu phương pháp luận:**
  * `AnalyticFlow.md`: Chuẩn tư duy phân tích chẩn đoán 6 bước.
  * `GEMINI.md`: Quy chuẩn kỹ thuật về hợp đồng Grain, triệt tiêu AI watermark và bộ tứ bàn giao.
  * `README.md`: Tài liệu hướng dẫn kiến trúc và thực thi hệ thống.
  * `.gitignore`: Cấu hình loại trừ file nặng, database dump và cache.

### Các tệp tin đã loại trừ (`.gitignore`):
* `olist_dump.sql` (159 MB) & `OLIST.zip` (44 MB): Vượt giới hạn kích thước tệp của GitHub.
* `mysql-*.msi` / `mysql-*.zip`: Bộ cài đặt phần mềm bên ngoài.
* `.env`: Khóa bảo mật môi trường và mật khẩu cục bộ.
* `__pycache__/`, `*.pyc`: File cache nhị phân của Python.

---

## 🛠️ Lệnh Đẩy Mã Nguồn Lên GitHub (Git Commands)

Sử dụng công cụ Git có sẵn tại máy cục bộ:

```bash
# 1. Khởi tạo Git repository (nếu chưa khởi tạo)
git init

# 2. Thêm remote repository trên GitHub
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# 3. Kiểm tra trạng thái các tệp tin theo dõi
git status

# 4. Đưa toàn bộ các tệp tin cấu trúc và phân tích vào Staging
git add generate_handover_data.py build_handover_pbip_complete.py generate_handover_dashboard_html.py check_db_connection.py
git add Olist_Fulfillment_Handover_Cockpit.html Olist_Fulfillment_Handover_Analysis.xlsx Fulfillment_Handover_Preview.svg
git add reports/Fulfillment_Handover_Diagnostic.pbip reports/Fulfillment_Handover_Diagnostic.Report/ reports/Fulfillment_Handover_Diagnostic.SemanticModel/
git add data_bi/fact_fulfillment_quadrants.csv data_bi/fact_regional_logistics_friction.csv data_bi/fact_category_seller_overdue.csv data_bi/fact_fulfillment_kpi_summary.csv
git add README.md AnalyticFlow.md GEMINI.md .gitignore requirements.txt

# 5. Tạo commit với thông điệp chuẩn mực
git commit -m "feat: complete fulfillment handover SLA audit with automated PBIP, Excel and interactive HTML cockpit"

# 6. Đặt nhánh chính là main và đẩy mã nguồn lên GitHub
git branch -M main
git push -u origin main
```
