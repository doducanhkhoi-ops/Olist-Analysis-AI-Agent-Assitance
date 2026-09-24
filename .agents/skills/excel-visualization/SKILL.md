---
name: excel-visualization
description: >-
  Expert guide and automation runbook for Excel data visualization, interactive dashboards,
  PivotTables, PivotCharts, Slicers, and chart debugging using Python (win32com & openpyxl).
  Use whenever creating Excel dashboards, embedding charts, fixing blank/broken charts,
  handling font encoding, or building interactive Excel reports.
---

# Excel Visualization & Interactive Dashboard Skill

Skill này đóng gói toàn bộ quy trình chuyên sâu, các bẫy kỹ thuật (gotchas) và chuẩn mực thiết kế biểu đồ tương tác, PivotTable, Slicer trên Excel bằng code tự động hóa (Python `win32com.client` & `openpyxl`).

---

## 1. Nguyên Tắc Lựa Chọn Biểu Đồ (Chart Selection Matrix)

| Nhu Cầu Phân Tích | Loại Dữ Liệu | Loại Biểu Đồ Chuẩn | Mã Excel COM (`XlChartType`) | Ghi Chú Tối Kỵ |
| :--- | :--- | :--- | :--- | :--- |
| **Xu hướng theo thời gian (Trend)** | Tháng, Quý, Tuần, Ngày $\times$ Doanh số | **Line Chart with Markers** | `xlLineMarkers` = `65` hoặc `xlLine` = `4` | **Tuyệt đối không dùng Clustered Column** nếu có >3 đối tượng qua 12 mốc thời gian (gây rối mắt, 72 cột chồng chéo). |
| **So sánh quy mô danh mục (Ranking)** | Top sản phẩm, Top sellers, Khách hàng | **Bar / Column Chart** | `xlColumnClustered` = `51`, `xlBarClustered` = `57` | Dùng Bar ngang nếu tên danh mục dài. |
| **Tỷ trọng / Cơ cấu (Composition)** | Phân khúc khách hàng, kênh thanh toán | **Donut / Stacked Column** | `xlDoughnut` = `-4120`, `xlColumnStacked100` = `53` | Tránh Pie Chart quá 5 lát cắt. |
| **Tương quan (Correlation)** | Giá trị đơn (AOV) vs Tần suất đặt hàng | **Scatter Plot** | `xlXYScatter` = `-4169` | Thêm đường xu hướng (Trendline) nếu cần. |

---

## 2. Các Lỗi Thường Gặp & Cách Khắc Phục Triệt Để (Critical Gotchas)

### 🔴 Lỗi 1: Biểu đồ bị trắng trơn (Blank/Empty Chart)
* **Nguyên nhân:** Khung chart được khởi tạo qua `Shapes.AddChart2()` nhưng chưa được gắn nguồn dữ liệu từ PivotTable.
* **Giải pháp:** Bắt buộc gọi `SetSourceData` trỏ vào `TableRange1` của PivotTable:
  ```python
  chart_shape = ws_dash.Shapes.AddChart2(201, 65, 500, 40, 550, 320)
  chart = chart_shape.Chart
  chart.SetSourceData(pt.TableRange1)  # BẮT BUỘC: kết nối dữ liệu PivotTable
  ```

### 🔴 Lỗi 2: Lỗi thêm Slicer qua COM (`Exception occurred / Invalid args`)
* **Nguyên nhân:** Phương thức `Slicers.Add()` của Excel yêu cầu tham số `Level` bị bỏ trống không được truyền `None` trực tiếp trong `pywin32`.
* **Giải pháp:** Sử dụng `pythoncom.Empty`:
  ```python
  import pythoncom
  sc = wb.SlicerCaches.Add2(pt, "Quốc Gia")
  # Tham số: (DestinationSheet, Level, Name, Caption, Top, Left, Width, Height)
  slicer = sc.Slicers.Add(ws_dash, pythoncom.Empty, "CountrySlicer", "Lọc Quốc Gia", 40, 350, 140, 200)
  ```

### 🔴 Lỗi 3: File bị khóa do người dùng đang mở (`Cannot access file.xlsx`)
* **Nguyên nhân:** Người dùng đang mở file xem biểu đồ thì code cố tình ghi đè lên đường dẫn đó.
* **Giải pháp:** Bắt ngoại lệ và tự động xuất phiên bản tiếp theo (`_v2.xlsx`, `_v3.xlsx`):
  ```python
  try:
      wb.SaveAs(xlsx_path, 51)
  except pywintypes.com_error:
      v2_path = xlsx_path.replace(".xlsx", "_v2.xlsx")
      wb.SaveAs(v2_path, 51)
  ```

### 🔴 Lỗi 4: Lỗi Font chữ tiếng Việt hiển thị ô vuông / dấu hỏi
* **Nguyên nhân:** Font mặc định của Excel không hiển thị tốt tiếng Việt có dấu trong Title/Label hoặc mã hóa Unicode đường dẫn bị hỏng.
* **Giải pháp:**
  - Luôn đọc file nguồn với `encoding='utf-8-sig'`.
  - Luôn gán rõ Font Name chuẩn:
    ```python
    chart.ChartTitle.Format.TextFrame2.TextRange.Font.Name = "Segoe UI"
    chart.ChartTitle.Format.TextFrame2.TextRange.Font.Size = 13
    ```

### 🔴 Lỗi 5: Hiện thông báo "Cannot quit Microsoft Excel" khi người dùng tắt Excel
* **Nguyên nhân:** Khi tự động hóa qua COM (`win32com` hoặc PowerShell), một tiến trình nền `EXCEL.EXE /automation -Embedding` bị treo do giữ tham chiếu COM chưa được dọn dẹp triệt để. Khi người dùng cố gắng tắt giao diện Excel, Excel phát hiện còn COM client đang khóa ứng dụng nên chặn thoát.
* **Giải pháp:** Sau khi chạy xong script, luôn dọn dẹp các tiến trình Excel ngầm:
  ```powershell
  Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'EXCEL.EXE' -and $_.CommandLine -like '*embedding*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
  ```

---

## 3. Template Code Chuẩn Mực (Production Script)

```python
import os
import csv
import pythoncom
import win32com.client

def build_interactive_dashboard(csv_path: str, output_xlsx: str):
    excel = win32com.client.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    try:
        wb = excel.Workbooks.Add()
        
        # 1. Nạp Sheet Data
        ws_data = wb.Sheets(1)
        ws_data.Name = "Data"
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for r_idx, row in enumerate(reader, 1):
                for c_idx, val in enumerate(row, 1):
                    if r_idx > 1 and val.replace('.', '', 1).isdigit():
                        ws_data.Cells(r_idx, c_idx).Value = float(val)
                    else:
                        ws_data.Cells(r_idx, c_idx).Value = val

        # 2. Tạo Sheet Dashboard
        ws_dash = wb.Sheets.Add(None, ws_data)
        ws_dash.Name = "Dashboard"
        
        last_row = ws_data.UsedRange.Rows.Count
        src_range = ws_data.Range(f"A1:C{last_row}")
        
        # 3. Tạo Pivot Cache & Pivot Table
        pivot_cache = wb.PivotCaches().Create(1, src_range, 5) # 1=xlDatabase, 5=xlPivotTableVersion15
        pt = pivot_cache.CreatePivotTable(ws_dash.Range("A3"), "SalesPivot", True, 5)
        
        # Thiết lập Rows, Columns, Values
        pt.PivotFields("Tháng").Orientation = 1       # xlRowField
        pt.PivotFields("Quốc Gia").Orientation = 2    # xlColumnField
        fld_val = pt.PivotFields("Doanh Số")
        fld_val.Orientation = 4                       # xlDataField
        fld_val.Function = -4157                      # xlSum
        fld_val.NumberFormat = "#,##0 $"

        # 4. Tạo Slicer tương tác
        sc = wb.SlicerCaches.Add2(pt, "Quốc Gia")
        sc.Slicers.Add(ws_dash, pythoncom.Empty, "CountrySlicer", "Lọc Quốc Gia", 40, 320, 140, 200)

        # 5. Tạo PivotChart (65 = xlLineMarkers)
        chart_shape = ws_dash.Shapes.AddChart2(201, 65, 480, 40, 520, 320)
        chart = chart_shape.Chart
        chart.SetSourceData(pt.TableRange1) # RÀNG BUỘC NGUỒN DỮ LIỆU
        chart.HasTitle = True
        chart.ChartTitle.Text = "Xu Hướng Doanh Số (2021)"
        chart.ChartTitle.Format.TextFrame2.TextRange.Font.Name = "Segoe UI"

        # 6. Lưu file an toàn
        try:
            wb.SaveAs(output_xlsx, 51)
        except Exception:
            fallback = output_xlsx.replace(".xlsx", "_v2.xlsx")
            wb.SaveAs(fallback, 51)
            output_xlsx = fallback

        return output_xlsx
    finally:
        wb.Close(False)
        excel.Quit()
```
