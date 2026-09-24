---
name: ai-data-analysis-orchestration
description: >-
  Quy trình phối hợp ĐA KỸ NĂNG: Khai thác SQL (mysql_query), phân tích chiến lược (olist, data-analyst), xuất Dashboard Excel (xlsxwriter) và tạo Mockup Power BI.
  CHỈ KÍCH HOẠT KHI: Người dùng rõ ràng yêu cầu "sử dụng các skill và rule đã cài để phân tích...", "đóng gói toàn bộ dự án...", hoặc yêu cầu đầy đủ bộ tứ sản phẩm (Excel, HTML, Power BI PBIP). KHÔNG kích hoạt cho các câu hỏi tra cứu hoặc vẽ biểu đồ đơn lẻ thông thường.
---

# Kỹ năng: AI Data Analysis Orchestration

> ⚠️ **ĐIỀU KIỆN KÍCH HOẠT (ACTIVATION CRITERIA):**
> Kỹ năng điều phối cấp cao này **CHỈ ĐƯỢC PHÉP KÍCH HOẠT** khi người dùng nêu rõ: *"sử dụng các skill và rule đã cài để phân tích..."*, *"phân tích sâu...", "làm báo cáo chuyên đề...", "đóng gói toàn bộ dự án..."*.
> Nếu người dùng chỉ yêu cầu một tác vụ thông thường (ví dụ: *"vẽ biểu đồ tỷ lệ giao trễ theo tháng"*, *"viết câu SQL tính AOV"*...), **TUYỆT ĐỐI KHÔNG KÍCH HOẠT** kỹ năng này. Hãy thực hiện trực tiếp và nhanh chóng yêu cầu cụ thể của người dùng.

## Quy trình 6 Bước (Standard Workflow):

1. **Khởi tạo Môi trường (Pre-requisites):**
   - Lập tức kiểm tra và chạy `pip install pandas xlsxwriter matplotlib` chạy ngầm (Background Task) để không làm gián đoạn luồng suy nghĩ, vì quá trình này tốn nhiều thời gian.

2. **Khám phá Schema & Căn chỉnh Chiến lược (Strategy Alignment):**
   - Đọc các SKILL.md liên quan: `olist-strategic-analytics`, `data-analyst`, `sql-analysis` để lấy khung tư duy (framework).
   - Truy vấn cấu trúc bảng: `SELECT table_name FROM information_schema.tables WHERE table_schema = '<tên_database>';`

3. **Trích xuất Dữ liệu (Data Extraction):**
   - Viết các câu lệnh SQL tối ưu qua `mysql_query` để kiểm chứng các giả thuyết chiến lược. Đảm bảo dùng tiền tố database (vd: `olist_raw.table_name`).

4. **Trực quan hóa qua Excel (Excel Dashboard):**
   - Áp dụng kỹ năng `excel-visualization`: Viết script Python dùng `pandas` và `xlsxwriter` để tạo file Excel chứa dữ liệu thô và biểu đồ tương tác (Combo Chart, Pivot...).

5. **Trực quan hóa qua Power BI Tự Động (Automated PBIP Golden Blueprint):**
   - Không sinh file `.pbit` nhị phân (tránh lỗi `NullReferenceException`). Dùng chuẩn Microsoft Fabric `.pbip` (PBIR + TMDL).
   - Xuất các bảng dữ liệu tổng hợp sạch (Data Mart CSV) vào thư mục `data_bi/`.
   - Sinh mô hình TMDL (thụt lề bằng tab `\t`, gán `lineageTag` GUID, M partition trỏ tới file CSV tuyệt đối) và các Visual Containers (`cardVisual`, `donutChart`, `barChart`, `lineClusteredColumnComboChart`, `tableEx`, `slicer`) dùng schema `2.9.0`.
   - Bắt buộc chạy `powerbi-report-author validate` trên thư mục `.Report` đạt tuyệt đối `errorCount: 0` và `warningCount: 0`.
   - Mở bằng `powerbi-desktop open`, kết nối bridge và chụp ảnh nghiệm thu qua `powerbi-desktop screenshot <page-id>`.
   - Cơ chế nạp dữ liệu 1-click: Khi mở file trên Desktop, người dùng chỉ cần bấm nút [Làm mới ngay] (hoặc `Alt + H + R`), toàn bộ dữ liệu tự động đổ đầy mà không cần import CSV thủ công.

6. **Bàn Giao Bộ Tứ Toàn Diện (Quadruple Deliverables):**
   - Đảm bảo 100% bàn giao đủ 4 sản phẩm: Chat chẩn đoán, Dashboard HTML tương tác phân trang (zero-scroll), Sổ Excel chuyên nghiệp đa sheet, và Dự án Power BI PBIP nghiệm thu.
