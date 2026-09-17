import os
import mysql.connector
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Kk1332006",
    database="olist_raw",
    port=3306
)

print("[*] Extracting Data Marts...")
q1 = """
SELECT 
    CASE 
        WHEN oi.price < 50 THEN '1. Gia re (< 50 BRL)'
        WHEN oi.price < 100 THEN '2. Pho thong (50-100 BRL)'
        WHEN oi.price < 250 THEN '3. Trung cap (100-250 BRL)'
        ELSE '4. Cao cap (>= 250 BRL)'
    END AS price_tier,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS merchandise_gmv,
    ROUND(SUM(oi.freight_value), 2) AS freight_gmv,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_gmv,
    ROUND(AVG(oi.freight_value / NULLIF(oi.price, 0)) * 100, 2) AS freight_tax_pct,
    ROUND(AVG(oi.price), 2) AS avg_price,
    ROUND(AVG(oi.freight_value), 2) AS avg_freight,
    ROUND(AVG(r.review_score), 2) AS avg_review_score,
    ROUND(SUM(CASE WHEN r.review_score = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT o.order_id), 2) AS pct_1_star
FROM orders o
STRAIGHT_JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY price_tier
ORDER BY price_tier;
"""
df_price_tier = pd.read_sql(q1, conn)

q2 = """
SELECT 
    CASE 
        WHEN c.customer_state = s.seller_state THEN '1. Noi Bang (Intra-state)'
        WHEN c.customer_state IN ('SP','RJ','MG','PR','SC','RS') AND s.seller_state IN ('SP','RJ','MG','PR','SC','RS') THEN '2. Lien Bang Tam Diem (SE-S)'
        ELSE '3. Lien Vung Xa (N/NE/CO)'
    END AS trade_corridor,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_gmv,
    ROUND(SUM(oi.price), 2) AS merchandise_gmv,
    ROUND(SUM(oi.freight_value), 2) AS freight_gmv,
    ROUND(AVG(oi.freight_value / NULLIF(oi.price, 0)) * 100, 2) AS avg_freight_burden_pct,
    ROUND(AVG(oi.price), 2) AS avg_item_price,
    ROUND(AVG(oi.freight_value), 2) AS avg_freight,
    ROUND(AVG(r.review_score), 2) AS avg_review_score,
    ROUND(SUM(CASE WHEN r.review_score = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT o.order_id), 2) AS pct_1_star,
    ROUND(AVG(DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp)), 2) AS avg_transit_days
FROM orders o
STRAIGHT_JOIN order_items oi ON o.order_id = oi.order_id
STRAIGHT_JOIN customers c ON o.customer_id = c.customer_id
STRAIGHT_JOIN sellers s ON oi.seller_id = s.seller_id
LEFT JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY trade_corridor
ORDER BY trade_corridor;
"""
df_corridor = pd.read_sql(q2, conn)

q3 = """
SELECT 
    CASE 
        WHEN freight_ratio < 0.10 THEN '1. Thap (<10%)'
        WHEN freight_ratio < 0.20 THEN '2. Tieu chuan (10-20%)'
        WHEN freight_ratio < 0.35 THEN '3. Cao (20-35%)'
        WHEN freight_ratio < 0.60 THEN '4. Nang ganh (35-60%)'
        ELSE '5. Bao mon cuc do (>60%)'
    END AS freight_burden_tier,
    COUNT(*) AS total_orders,
    ROUND(SUM(total_order_val), 2) AS total_gmv,
    ROUND(SUM(item_val), 2) AS total_item_gmv,
    ROUND(SUM(freight_val), 2) AS total_freight_gmv,
    ROUND(AVG(item_val), 2) AS avg_item_price,
    ROUND(AVG(freight_val), 2) AS avg_freight,
    ROUND(AVG(freight_ratio)*100, 2) AS avg_freight_pct,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(SUM(CASE WHEN review_score = 1 THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS pct_1_star,
    ROUND(AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)), 2) AS avg_delivery_days
FROM (
    SELECT 
        o.order_id,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date,
        SUM(oi.price) AS item_val,
        SUM(oi.freight_value) AS freight_val,
        SUM(oi.price + oi.freight_value) AS total_order_val,
        SUM(oi.freight_value) / NULLIF(SUM(oi.price), 0) AS freight_ratio,
        AVG(r.review_score) AS review_score
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN reviews r ON o.order_id = r.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_delivered_customer_date IS NOT NULL
    GROUP BY o.order_id, o.order_purchase_timestamp, o.order_delivered_customer_date
) sub
WHERE freight_ratio IS NOT NULL
GROUP BY freight_burden_tier
ORDER BY freight_burden_tier;
"""
df_burden = pd.read_sql(q3, conn)

q4 = """
SELECT 
    COALESCE(ct.product_category_name_english, p.product_category_name, 'Unknown') AS category_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS merchandise_gmv,
    ROUND(SUM(oi.freight_value), 2) AS freight_gmv,
    ROUND(AVG(oi.freight_value / NULLIF(oi.price, 0)) * 100, 2) AS freight_tax_pct,
    ROUND(AVG(oi.price), 2) AS avg_price,
    ROUND(AVG(oi.freight_value), 2) AS avg_freight,
    ROUND(AVG(r.review_score), 2) AS avg_review_score,
    ROUND(SUM(CASE WHEN r.review_score = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT o.order_id), 2) AS pct_1_star
FROM orders o
STRAIGHT_JOIN order_items oi ON o.order_id = oi.order_id
STRAIGHT_JOIN products p ON oi.product_id = p.product_id
LEFT JOIN category_translation ct ON p.product_category_name = ct.product_category_name
LEFT JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY category_name
HAVING COUNT(DISTINCT o.order_id) >= 500
ORDER BY freight_tax_pct DESC
LIMIT 20;
"""
df_category = pd.read_sql(q4, conn)
conn.close()

os.makedirs('data_bi', exist_ok=True)
df_price_tier.to_csv('data_bi/fact_freight_price_tier.csv', index=False, encoding='utf-8')
df_corridor.to_csv('data_bi/fact_freight_trade_corridor.csv', index=False, encoding='utf-8')
df_burden.to_csv('data_bi/fact_freight_burden_tiers.csv', index=False, encoding='utf-8')
df_category.to_csv('data_bi/fact_category_freight_deadweight.csv', index=False, encoding='utf-8')
print("[+] CSV Data Marts saved.")

wb = openpyxl.Workbook()
navy_header_fill = PatternFill(start_color='0A192F', end_color='0A192F', fill_type='solid')
sub_header_fill = PatternFill(start_color='1E293B', end_color='1E293B', fill_type='solid')
white_font_bold = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
title_font = Font(name='Calibri', size=16, bold=True, color='0A192F')
subtitle_font = Font(name='Calibri', size=10, italic=True, color='475569')
regular_font = Font(name='Calibri', size=10)
bold_font = Font(name='Calibri', size=10, bold=True)

thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

def style_sheet(ws, title, subtitle, df, num_formats):
    ws.views.sheetView[0].showGridLines = True
    ws['A1'] = title
    ws['A1'].font = title_font
    ws['A2'] = subtitle
    ws['A2'].font = subtitle_font
    
    headers = list(df.columns)
    start_row = 4
    for col_idx, col_name in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=col_idx, value=col_name.replace('_', ' ').title())
        cell.fill = navy_header_fill
        cell.font = white_font_bold
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border
    
    for r_idx, row_data in enumerate(df.values, start_row + 1):
        for c_idx, val in enumerate(row_data, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = regular_font
            cell.border = thin_border
            col_name = headers[c_idx - 1]
            if col_name in num_formats:
                cell.number_format = num_formats[col_name]
                cell.alignment = Alignment(horizontal='right', vertical='center')
            elif isinstance(val, (int, float)):
                cell.alignment = Alignment(horizontal='right', vertical='center')
            else:
                cell.alignment = Alignment(horizontal='left', vertical='center')
    
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 13)

formats = {
    'total_orders': '#,##0',
    'merchandise_gmv': 'R$ #,##0.00',
    'freight_gmv': 'R$ #,##0.00',
    'total_gmv': 'R$ #,##0.00',
    'total_item_gmv': 'R$ #,##0.00',
    'total_freight_gmv': 'R$ #,##0.00',
    'freight_tax_pct': '0.00%',
    'avg_freight_burden_pct': '0.00%',
    'avg_freight_pct': '0.00%',
    'pct_1_star': '0.00%',
    'avg_price': 'R$ #,##0.00',
    'avg_item_price': 'R$ #,##0.00',
    'avg_freight': 'R$ #,##0.00',
    'avg_review_score': '0.00',
    'avg_transit_days': '0.0',
    'avg_delivery_days': '0.0'
}

ws1 = wb.active
ws1.title = 'Executive Summary'
ws1.views.sheetView[0].showGridLines = True
ws1['A1'] = 'OLIST FREIGHT DEADWEIGHT & REVENUE EROSION AUDIT'
ws1['A1'].font = title_font
ws1['A2'] = 'Chan doan tac dong cua thue phi van chuyen len gia tri gio hang va bien loi nhuan'
ws1['A2'].font = subtitle_font

kpis = [
    ('Tong Don Hang Phan Tich', 96428, '#,##0'),
    ('Tong GMV Nen Tang (BRL)', 15489664.91, 'R$ #,##0.00'),
    ('GMV Hang Hoa Thuc Te (BRL)', 13279836.59, 'R$ #,##0.00'),
    ('Tong Cuoc Phi Logistics (BRL)', 2209828.32, 'R$ #,##0.00'),
    ('Ty Le Cuoc Phi / Hang Hoa Binh Quan (%)', 24.16, '0.00%'),
    ('Ty Le Cuoc Nhom Gia Re (<50 BRL) (%)', 56.93, '0.00%'),
    ('Diem Danh Gia Review Toan San', 4.14, '0.00')
]

for idx, (label, val, fmt) in enumerate(kpis, 4):
    ws1.cell(row=idx, column=1, value=label).font = white_font_bold
    ws1.cell(row=idx, column=1).fill = sub_header_fill
    c = ws1.cell(row=idx, column=2, value=val)
    c.font = bold_font
    c.number_format = fmt
    c.alignment = Alignment(horizontal='right')
    c.border = thin_border
    ws1.row_dimensions[idx].height = 24

ws1.column_dimensions['A'].width = 38
ws1.column_dimensions['B'].width = 25

ws2 = wb.create_sheet('Price Tier Burden')
style_sheet(ws2, 'Phan Tich Thue Phi Ship Theo Phan Khuc Gia', 'Muc do bao mon cua phi ship doi voi gio hang gia re', df_price_tier, formats)

ws3 = wb.create_sheet('Trade Corridors')
style_sheet(ws3, 'Hanh Lang Thuong Mai & Ma Sat Logistics', 'So sanh chi phi va thoi gian van chuyen noi bang vs lien bang xa', df_corridor, formats)

ws4 = wb.create_sheet('Freight Burden Tiers')
style_sheet(ws4, 'Phan Tang Ganh Nang Cuoc Phi Toan Mang Luoi', 'Phan bo don hang va danh gia review theo ty le phi ship', df_burden, formats)

ws5 = wb.create_sheet('Top Categories Deadweight')
style_sheet(ws5, 'Top 20 Nganh Hang Chiu Thue Phi Ship Cao Nhat', 'Cac nganh hang co ty le cuoc tren gia hang vuot nguong', df_category, formats)

excel_file = 'Olist_Freight_Deadweight_Analysis.xlsx'
wb.save(excel_file)
print('[+] Excel Workbook saved as: ' + excel_file)