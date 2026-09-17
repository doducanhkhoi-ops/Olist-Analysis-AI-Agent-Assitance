import os
import mysql.connector
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

base_dir = r"c:\Users\ASUS\Documents\Năm III\CSDL"
data_bi_dir = os.path.join(base_dir, "data_bi")
os.makedirs(data_bi_dir, exist_ok=True)

conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="@Kk1332006",
    database="olist_raw"
)

print("[*] 1. Extracting Quadrants Data...")
q_quadrant = """
SELECT 
    delivery_quadrant_id,
    delivery_quadrant,
    COUNT(*) as total_orders,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as order_share_pct,
    ROUND(SUM(total_order_value), 2) as total_gmv,
    ROUND(AVG(total_order_value), 2) as aov,
    ROUND(AVG(review_score), 2) as avg_review_score,
    ROUND(SUM(CASE WHEN review_score = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as one_star_pct,
    ROUND(SUM(CASE WHEN review_score = 5 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as five_star_pct,
    ROUND(AVG(TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_carrier_date) / 24.0), 2) as avg_seller_handling_days,
    ROUND(AVG(TIMESTAMPDIFF(HOUR, order_delivered_carrier_date, order_delivered_customer_date) / 24.0), 2) as avg_carrier_transit_days,
    ROUND(AVG(TIMESTAMPDIFF(HOUR, order_purchase_timestamp, order_delivered_customer_date) / 24.0), 2) as avg_total_delivery_days,
    ROUND(AVG(TIMESTAMPDIFF(HOUR, order_delivered_customer_date, order_estimated_delivery_date) / 24.0), 2) as avg_sla_buffer_days
FROM (
    SELECT 
        o.order_id,
        o.order_purchase_timestamp,
        o.order_delivered_carrier_date,
        o.order_delivered_customer_date,
        o.order_estimated_delivery_date,
        oi.max_shipping_limit,
        oi.total_order_value,
        r.review_score,
        CASE 
            WHEN DATE(o.order_delivered_customer_date) <= DATE(o.order_estimated_delivery_date) 
                 AND o.order_delivered_carrier_date <= oi.max_shipping_limit 
                 THEN 'Q1'
            WHEN DATE(o.order_delivered_customer_date) <= DATE(o.order_estimated_delivery_date) 
                 AND o.order_delivered_carrier_date > oi.max_shipping_limit 
                 THEN 'Q2'
            WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) 
                 AND o.order_delivered_carrier_date <= oi.max_shipping_limit 
                 THEN 'Q3'
            WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) 
                 AND o.order_delivered_carrier_date > oi.max_shipping_limit 
                 THEN 'Q4'
        END as delivery_quadrant_id,
        CASE 
            WHEN DATE(o.order_delivered_customer_date) <= DATE(o.order_estimated_delivery_date) 
                 AND o.order_delivered_carrier_date <= oi.max_shipping_limit 
                 THEN 'Q1: Chuẩn SLA (Seller Đúng, Carrier Kịp)'
            WHEN DATE(o.order_delivered_customer_date) <= DATE(o.order_estimated_delivery_date) 
                 AND o.order_delivered_carrier_date > oi.max_shipping_limit 
                 THEN 'Q2: Carrier Gánh (Seller Trễ, Carrier Kịp)'
            WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) 
                 AND o.order_delivered_carrier_date <= oi.max_shipping_limit 
                 THEN 'Q3: Carrier Gãy (Seller Đúng, Carrier Trễ)'
            WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) 
                 AND o.order_delivered_carrier_date > oi.max_shipping_limit 
                 THEN 'Q4: Thảm Họa Kép (Seller Trễ, Carrier Trễ)'
        END as delivery_quadrant
    FROM orders o
    JOIN (
        SELECT order_id, MAX(shipping_limit_date) as max_shipping_limit, SUM(price) as total_order_value
        FROM order_items
        GROUP BY order_id
    ) oi ON o.order_id = oi.order_id
    LEFT JOIN reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
      AND o.order_delivered_carrier_date IS NOT NULL
) t
WHERE delivery_quadrant_id IS NOT NULL
GROUP BY delivery_quadrant_id, delivery_quadrant
ORDER BY total_orders DESC;
"""
df_quadrants = pd.read_sql(q_quadrant, conn)
df_quadrants.to_csv(os.path.join(data_bi_dir, "fact_fulfillment_quadrants.csv"), index=False, encoding="utf-8-sig")

print("[*] 2. Extracting Regional Logistics Friction...")
q_regional = """
SELECT 
    c.customer_state as state,
    COUNT(*) as total_orders,
    SUM(CASE WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) AND o.order_delivered_carrier_date <= oi.max_shipping_limit THEN 1 ELSE 0 END) as carrier_breakdown_orders,
    ROUND(SUM(CASE WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) AND o.order_delivered_carrier_date <= oi.max_shipping_limit THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as carrier_breakdown_pct,
    ROUND(AVG(TIMESTAMPDIFF(HOUR, o.order_delivered_carrier_date, o.order_delivered_customer_date) / 24.0), 1) as avg_transit_days,
    ROUND(AVG(CASE WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) AND o.order_delivered_carrier_date <= oi.max_shipping_limit THEN TIMESTAMPDIFF(HOUR, o.order_delivered_carrier_date, o.order_delivered_customer_date) / 24.0 ELSE NULL END), 1) as avg_transit_days_delayed,
    ROUND(AVG(r.review_score), 2) as avg_review_score
FROM orders o
JOIN (
    SELECT order_id, MAX(shipping_limit_date) as max_shipping_limit
    FROM order_items
    GROUP BY order_id
) oi ON o.order_id = oi.order_id
JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_delivered_carrier_date IS NOT NULL
GROUP BY c.customer_state
HAVING total_orders >= 500
ORDER BY carrier_breakdown_pct DESC;
"""
df_regional = pd.read_sql(q_regional, conn)
df_regional.to_csv(os.path.join(data_bi_dir, "fact_regional_logistics_friction.csv"), index=False, encoding="utf-8-sig")

print("[*] 3. Extracting Category Seller Overdue...")
q_category = """
SELECT 
    COALESCE(REPLACE(t.product_category_name_english, '\r', ''), REPLACE(p.product_category_name, '\r', ''), 'unknown') as category_name,
    COUNT(DISTINCT o.order_id) as total_orders,
    ROUND(SUM(CASE WHEN o.order_delivered_carrier_date > oi.shipping_limit_date THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as seller_overdue_pct,
    ROUND(AVG(TIMESTAMPDIFF(HOUR, o.order_purchase_timestamp, o.order_delivered_carrier_date) / 24.0), 1) as avg_seller_handling_days,
    ROUND(AVG(r.review_score), 2) as avg_review_score
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN category_translation t ON p.product_category_name = t.product_category_name
LEFT JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_carrier_date IS NOT NULL
GROUP BY category_name
HAVING total_orders >= 1000
ORDER BY seller_overdue_pct DESC;
"""
df_category = pd.read_sql(q_category, conn)
df_category.to_csv(os.path.join(data_bi_dir, "fact_category_seller_overdue.csv"), index=False, encoding="utf-8-sig")

print("[*] 4. Building KPI Summary...")
kpis = [
    {"metric_name": "Tổng đơn hàng hoàn thành (Delivered)", "metric_value": 96999, "unit": "đơn", "formatted": "96,999 đơn", "note": "Tập dữ liệu hoàn tất giao nhận"},
    {"metric_name": "Tỷ trọng Carrier cứu đơn kịp thời (Q2)", "metric_value": 79.26, "unit": "%", "formatted": "79.26%", "note": "6,944 / 8,761 đơn seller ngâm trễ"},
    {"metric_name": "Đơn bị Carrier làm gãy dù Seller đúng (Q3)", "metric_value": 4745, "unit": "đơn", "formatted": "4,745 đơn", "note": "Chiếm 4.89% đơn toàn sàn"},
    {"metric_name": "Điểm Review khi đúng hạn (Q1/Q2)", "metric_value": 4.29, "unit": "sao", "formatted": "4.29 sao", "note": "Hài lòng tuyệt đối"},
    {"metric_name": "Điểm Review khi vỡ cam kết (Q3/Q4)", "metric_value": 2.27, "unit": "sao", "formatted": "2.27 sao", "note": "Sụp đổ -2.02 sao, 52.5% 1-sao"},
    {"metric_name": "Tổng GMV bị hủy hoại danh tiếng (Q3+Q4)", "metric_value": 989777.56, "unit": "BRL", "formatted": "R$ 989.8K", "note": "6,562 đơn rơi vào vực thẳm review"}
]
df_kpi = pd.DataFrame(kpis)
df_kpi.to_csv(os.path.join(data_bi_dir, "fact_fulfillment_kpi_summary.csv"), index=False, encoding="utf-8-sig")

print("[+] CSV Data Mart successfully built in data_bi/ !")

# Build Excel file
print("[*] 5. Creating Executive Excel Workbook...")
excel_path = os.path.join(base_dir, "Olist_Fulfillment_Handover_Analysis.xlsx")

wb = openpyxl.Workbook()
ws_kpi = wb.active
ws_kpi.title = "Executive_KPIs"
ws_quad = wb.create_sheet(title="Fulfillment_Quadrants")
ws_reg = wb.create_sheet(title="Regional_Logistics_Friction")
ws_cat = wb.create_sheet(title="Category_Seller_SLA")
ws_rel = wb.create_sheet(title="Relational_Data_Model")

navy_header = "0F172A"
blue_accent = "1E293B"
font_title = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
font_header = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Segoe UI", size=10, bold=True, color="0F172A")
font_regular = Font(name="Segoe UI", size=10, color="0F172A")

fill_header = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
fill_title = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
fill_rescue = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
fill_danger = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color="CBD5E1"),
    right=Side(style='thin', color="CBD5E1"),
    top=Side(style='thin', color="CBD5E1"),
    bottom=Side(style='thin', color="CBD5E1")
)

# Sheet 1: KPIs
ws_kpi.merge_cells("A1:E1")
ws_kpi["A1"] = "OLIST LOGISTICS AUDIT: EXECUTIVE FULFILLMENT KPI COCKPIT"
ws_kpi["A1"].font = font_title
ws_kpi["A1"].fill = fill_title
ws_kpi["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws_kpi.row_dimensions[1].height = 40

kpi_headers = ["Chỉ Số Trọng Yếu (KPI)", "Giá Trị Thực", "Đơn Vị", "Định Dạng Báo Cáo", "Ghi Chú Vận Hành & Tác Động Chiến Lược"]
for col_num, h in enumerate(kpi_headers, 1):
    c = ws_kpi.cell(row=3, column=col_num)
    c.value = h
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal="center", vertical="center")
ws_kpi.row_dimensions[3].height = 25

for r_idx, row in df_kpi.iterrows():
    r = r_idx + 4
    ws_kpi.cell(row=r, column=1, value=row["metric_name"]).font = font_bold
    ws_kpi.cell(row=r, column=2, value=row["metric_value"]).font = font_regular
    ws_kpi.cell(row=r, column=3, value=row["unit"]).font = font_regular
    ws_kpi.cell(row=r, column=4, value=row["formatted"]).font = font_bold
    ws_kpi.cell(row=r, column=5, value=row["note"]).font = font_regular
    for c in range(1, 6):
        cell = ws_kpi.cell(row=r, column=c)
        cell.border = thin_border
        if c in [2, 3, 4]:
            cell.alignment = Alignment(horizontal="center", vertical="center")

# Sheet 2: Quadrants
ws_quad.merge_cells("A1:M1")
ws_quad["A1"] = "MA TRẬN 4 GÓC PHẦN TƯ BÀN GIAO & VẬN TẢI (THE 4 FULFILLMENT QUADRANTS)"
ws_quad["A1"].font = font_title
ws_quad["A1"].fill = fill_title
ws_quad["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws_quad.row_dimensions[1].height = 40

quad_headers = [
    "Mã", "Phân Khúc Bàn Giao", "Số Đơn Hàng", "Tỷ Trọng (%)", "Tổng GMV (BRL)", "AOV (BRL)", 
    "Review Score", "% 1 Sao", "% 5 Sao", "Seller Chuẩn Bị (Ngày)", "Carrier Transit (Ngày)", "Tổng Giao (Ngày)", "Đệm SLA (Ngày)"
]
for col_num, h in enumerate(quad_headers, 1):
    c = ws_quad.cell(row=3, column=col_num)
    c.value = h
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws_quad.row_dimensions[3].height = 30

for r_idx, row in df_quadrants.iterrows():
    r = r_idx + 4
    vals = [
        row["delivery_quadrant_id"], row["delivery_quadrant"], row["total_orders"], row["order_share_pct"],
        row["total_gmv"], row["aov"], row["avg_review_score"], row["one_star_pct"], row["five_star_pct"],
        row["avg_seller_handling_days"], row["avg_carrier_transit_days"], row["avg_total_delivery_days"], row["avg_sla_buffer_days"]
    ]
    for c_idx, val in enumerate(vals, 1):
        cell = ws_quad.cell(row=r, column=c_idx, value=val)
        cell.font = font_bold if c_idx in [1, 2, 7] else font_regular
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center" if c_idx in [1, 7, 8, 9, 10, 11, 12, 13] else ("right" if c_idx in [3, 4, 5, 6] else "left"), vertical="center")
        if row["delivery_quadrant_id"] == "Q2":
            cell.fill = fill_rescue
        elif row["delivery_quadrant_id"] in ["Q3", "Q4"]:
            cell.fill = fill_danger

# Sheet 3: Regional
ws_reg.merge_cells("A1:G1")
ws_reg["A1"] = "ĐIỂM NGHẼN VẬN TẢI THEO BANG KHÁCH HÀNG (CARRIER BREAKDOWN BY STATE)"
ws_reg["A1"].font = font_title
ws_reg["A1"].fill = fill_title
ws_reg["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws_reg.row_dimensions[1].height = 40

reg_headers = ["Bang Nhận Hàng", "Tổng Đơn", "Đơn Bị Carrier Làm Trễ (Q3)", "Tỷ Lệ Carrier Gãy (%)", "Transit TB Toàn Bộ (Ngày)", "Transit TB Khi Bị Trễ (Ngày)", "Review TB Bang"]
for col_num, h in enumerate(reg_headers, 1):
    c = ws_reg.cell(row=3, column=col_num)
    c.value = h
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws_reg.row_dimensions[3].height = 25

for r_idx, row in df_regional.iterrows():
    r = r_idx + 4
    vals = [row["state"], row["total_orders"], row["carrier_breakdown_orders"], row["carrier_breakdown_pct"], row["avg_transit_days"], row["avg_transit_days_delayed"], row["avg_review_score"]]
    for c_idx, val in enumerate(vals, 1):
        cell = ws_reg.cell(row=r, column=c_idx, value=val)
        cell.font = font_bold if c_idx in [1, 4] else font_regular
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center" if c_idx in [1, 4, 5, 6, 7] else "right", vertical="center")

# Sheet 4: Category
ws_cat.merge_cells("A1:E1")
ws_cat["A1"] = "TỶ LỆ VI PHẠM HẠN BÀN GIAO CỦA SELLER THEO NGÀNH HÀNG (SELLER SLA LAG BY CATEGORY)"
ws_cat["A1"].font = font_title
ws_cat["A1"].fill = fill_title
ws_cat["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws_cat.row_dimensions[1].height = 40

cat_headers = ["Ngành Hàng", "Tổng Đơn Hàng", "Tỷ Lệ Seller Trễ Hạn (%)", "TG Chuẩn Bị TB (Ngày)", "Review TB Ngành"]
for col_num, h in enumerate(cat_headers, 1):
    c = ws_cat.cell(row=3, column=col_num)
    c.value = h
    c.font = font_header
    c.fill = fill_header
    c.alignment = Alignment(horizontal="center", vertical="center")
ws_cat.row_dimensions[3].height = 25

for r_idx, row in df_category.iterrows():
    r = r_idx + 4
    vals = [row["category_name"], row["total_orders"], row["seller_overdue_pct"], row["avg_seller_handling_days"], row["avg_review_score"]]
    for c_idx, val in enumerate(vals, 1):
        cell = ws_cat.cell(row=r, column=c_idx, value=val)
        cell.font = font_bold if c_idx in [1, 3] else font_regular
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center" if c_idx in [3, 4, 5] else ("right" if c_idx == 2 else "left"), vertical="center")

# Sheet 5: Relational Data Model
ws_rel.merge_cells("A1:D1")
ws_rel["A1"] = "MÔ HÌNH QUAN HỆ VÀ CHUỖI DỮ LIỆU (RELATIONAL DATA LINEAGE)"
ws_rel["A1"].font = font_title
ws_rel["A1"].fill = fill_title
ws_rel["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws_rel.row_dimensions[1].height = 40

rel_rows = [
    ("Bảng Nguồn (Source Table)", "Khóa Liên Kết (Join Key)", "Bảng Đích (Target Table)", "Mục Đích Sử Dụng Phân Tích"),
    ("orders (o)", "o.order_id = oi.order_id", "order_items (oi)", "Đo lường thời điểm giao hàng, hạn chót bưu cục, tính tổng giá trị đơn"),
    ("orders (o)", "o.order_id = r.order_id", "reviews (r)", "Khảo sát điểm review_score, tỷ lệ 1-sao và 5-sao theo phân khúc SLA"),
    ("orders (o)", "o.customer_id = c.customer_id", "customers (c)", "Phân bổ địa bàn khách hàng theo 27 bang Brazil (Interstate latency)"),
    ("order_items (oi)", "oi.product_id = p.product_id", "products (p)", "Phân loại danh mục hàng hóa và đặc thù xử lý của seller"),
    ("products (p)", "p.product_category_name = t.product_category_name", "category_translation (t)", "Chuẩn hóa tên danh mục sang tiếng Anh thương mại quốc tế")
]
for r_idx, r_data in enumerate(rel_rows, 3):
    for c_idx, val in enumerate(r_data, 1):
        cell = ws_rel.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 3:
            cell.font = font_header
            cell.fill = fill_header
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.font = font_bold if c_idx == 1 else font_regular
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="left", vertical="center")

# Auto-fit column widths
for ws in [ws_kpi, ws_quad, ws_reg, ws_cat, ws_rel]:
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

wb.save(excel_path)
print(f"[+] Excel workbook saved successfully: {excel_path}")
conn.close()
