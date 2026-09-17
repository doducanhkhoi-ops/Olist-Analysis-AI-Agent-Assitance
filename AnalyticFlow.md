# Quy chuẩn Phân tích Dữ liệu Dự án: The Diagnostic Analyst Mindset

Mỗi khi nhận yêu cầu đọc dữ liệu, phân tích cơ sở dữ liệu (`olist_raw`, `awesome_chocolates`, v.v.), hoặc xây dựng báo cáo / dashboard cho dự án này, Agent **BẮT BUỘC** phải tuân thủ luồng tư duy chẩn đoán 6 bước của một Senior Data Analyst:

---

## 🧭 Luồng Tư Duy Chẩn Đoán 6 Bước (The 6-Step Diagnostic Flow)

```
[1. Triệu chứng Bề mặt (Red Flags)]
       │
       ▼
[2. Đặt Giả thuyết Đa chiều (Cung - Cầu - Vận hành)]
       │
       ▼
[3. Cắt lớp Dữ liệu (Drill-down: Thực tế vs Ảo, Địa lý, Ma trận)]
       │
       ▼
[4. Săn lùng & Giải mã Nghịch lý (Paradox Discovery)]
       │
       ▼
[5. Định vị Căn bệnh Cốt lõi (Core Problem Pinpointing)]
       │
       ▼
[6. Playbook Hành động Chiến lược (Actionable Business Remedy)]
```

---

### Quy tắc Thực thi Cụ thể:

1. **KHÔNG BAO GIỜ dừng ở Thống kê Mô tả (Descriptive Stats):**
   - Tuyệt đối không chỉ đưa ra các số liệu phẳng như "Tổng doanh thu là X, số đơn là Y".
   - Luôn đặt câu hỏi: *Con số này tăng/giảm do đâu? Có bao nhiêu % là ảo (hủy/hoàn)? Tỷ lệ khách quay lại là bao nhiêu?*

2. **Bóc tách Đa chiều (Multi-dimensional Drilling):**
   - **Phía Cung (Sellers):** Phân biệt đơn thành công vs đơn hủy; phân tích năng lực Seller Đa vùng (Multi-region) vs Đơn vùng; nhận diện danh mục yếu (Weak Categories) và lý do đánh giá 1 sao (kiểm tra tỷ lệ *Unavailable*).
   - **Phía Cầu (Customers):** Phân cụm RFM; đo lường tỷ lệ mua lặp lại (`repeat_purchase_rate`); kiểm tra hội chứng "Thùng rỗng đáy" (Leaky Bucket).
   - **Phía Vận hành (Logistics & Geography):** Đo SLA giao hàng (`late_delivery_pct`); đối chiếu tương quan giữa giao trễ và điểm review.

3. **Luôn tìm kiếm Nghịch lý Kinh doanh (Paradox Discovery):**
   - **Nghịch lý São Paulo (SP Paradox):** Thị trường đông nhất, doanh thu cao nhất nhưng AOV lại thấp nhất (do áp lực cạnh tranh thị phần từ Mercado Livre/Amazon).
   - **Nghịch lý Multi-seller:** Đơn mua từ nhiều người bán phức tạp hơn nhưng thời gian giao lại nhanh hơn và tỷ lệ trễ thấp hơn (do tập trung ở bang phát triển và chính sách gom đơn đồng bộ).

4. **Chỉ đúng Căn bệnh Cốt lõi (Core Problem):**
   - Định nghĩa rõ bản chất căn bệnh kinh doanh: Lệ thuộc tăng trưởng vào khách mới (Acquisition reliance), tỷ lệ duy trì (Retention) kém, trần tâm lý giá (Psychological ceiling), hay sự sụp đổ doanh thu mùa Giáng sinh do nỗi sợ giao trễ.

5. **Đề xuất Giải pháp Chiến lược (Actionable Playbook):**
   - Chuyển từ tìm khách mới sang giữ chân (Gamification, Loyalty cho nhóm *Can't Lose Them*).
   - Đẩy mạnh tăng giá trị giỏ hàng (AOV) bằng thuật toán Cross-selling & Bundle đa ngành.
   - Lập kịch bản marketing theo giai đoạn (Phased Calendar) và hóa giải nỗi sợ mùa vụ bằng voucher trả góp 0% và bảo hiểm giao hàng đúng hẹn.

---

## 🚀 QUY TẮC HIỂN THỊ TRÌNH TỰ (NEW WORKFLOW):
Mỗi vòng lặp phân tích (Iteration) BẮT BUỘC phải tuân thủ nghiêm ngặt trình tự sau trên khung chat:
1. **Mở đầu bằng Định hướng:** Cho biết mục tiêu đang tìm kiếm/nhìn vào góc độ data nào (Dashboard Mockup nếu có).
2. **Hiển thị câu lệnh SQL (SQL Query):** Trình bày rõ ràng đoạn code SQL dùng để lấy số liệu.
3. **Hiển thị Bảng Dữ liệu (Raw Data Table):** Show trực tiếp bảng kết quả thực tế trả về từ MySQL vào chat.
4. **Phân tích Chuyên sâu:** Từ dữ liệu vừa show, đưa ra lý giải, bóc tách đa chiều và kết luận chiến lược.
*(Lặp lại chu trình này cho mỗi insight tiếp theo).*

5. **Xuất bản Báo cáo Dashboard HTML Đồng Bộ & Tương Tác Sâu (Bespoke Interactive Agentic HTML):**
   - Web HTML **BẮT BUỘC** phải đồng bộ 100% nội dung phân tích chuyên sâu với báo cáo trên chat, tuân thủ cùng mạch logic kết nối (Causal Threading).
   - **Đầy Đủ Phần Tổng Hợp / Định Vị Căn Bệnh Cốt Lõi (Mandatory Conclusion & Core Problem Diagnosis):** Báo cáo HTML bắt buộc phải có đầy đủ phần kết luận chẩn đoán căn bệnh cốt lõi ở cuối trang như trong báo cáo chat, không được phép cắt xén hay bỏ qua.
   - **Tập trung Phân tích Sâu, Không Đưa Giải Pháp Sớm (Analysis-First):** Dành toàn bộ dung lượng mổ xẻ dữ liệu, giải phẫu đa chiều, đào sâu căn nguyên gốc rễ thay vì vội vàng đưa ra khuyến nghị/playbook generic.
   - **Tính Kết Nối Liền Mạch Giữa Các Bảng (Causal Bridging):** Giữa các bảng số liệu và biểu đồ (cả trên chat lẫn web HTML) bắt buộc phải có câu văn cầu nối logic ở cuối phần trước hoặc đầu phần sau: Nêu rõ bảng A phát hiện ra điểm nghẽn gì, dẫn tới câu hỏi tiếp theo là gì, và bảng B được đưa ra để mổ xẻ tiếp khía cạnh nào.
   - **Trực Quan Hóa Đa Dạng & Chuẩn Dữ Liệu:** Đồ thị và bảng biểu phải phù hợp tuyệt đối với bản chất số liệu (Dual-axis, Stacked Bar, Heatmap Matrix, Radar, Donut), loại bỏ các biểu đồ gượng ép sáo rỗng.
   - **Tương Tác Sâu Cả Biểu Đồ (Deep Slicers & Chart Cross-Filtering):** Bộ lọc Slicer khi người dùng bấm chọn (ví dụ: phương thức, kỳ hạn, danh mục) không chỉ cập nhật thẻ KPI và bảng dữ liệu mà **BẮT BUỘC phải tương tác động với cả BIỂU ĐỒ** (cập nhật số liệu biểu đồ, highlight phân khúc được chọn, hoặc chuyển đổi góc nhìn đồ thị).
   - **Ngôn Ngữ Tinh Gọn, Chống Cringe & Thừa Thãi (Anti-Cringe & Anti-Buzzword):** Tuyệt đối không dùng các từ ngữ phô trương tính năng thừa thãi kiểu AI (như "Slicer tương tác", "Bộ lọc trực tiếp", "Hệ thống thông minh"). Nếu là bộ lọc thì chỉ cần ghi gãy gọn là "Slicer" hoặc "Slicer: [Tên trường]". Toàn bộ nhãn, tiêu đề thẻ phải tự nhiên, chuẩn mực nghiệp vụ báo cáo cấp cao.
   - **Tiêu chuẩn Thiết kế (Anti-AI-Slop & Agentic Bespoke Design):** Hệ màu chuyên nghiệp có chiều sâu (Modern Dark Slate / Midnight Navy phối hợp neon/cyber indicator accents), Typography phân cấp chặt chẽ (Plus Jakarta Sans / Inter + JetBrains Mono), micro-interactions mượt mà, kèm nút Copy SQL và in ấn/PDF xuất bản. Cung cấp đường dẫn clickable link (`file:///...`) trực tiếp trên chat.

7. **Quy Trình Thực Thi 2 Pha Tinh Gọn (The 2-Phase Diagnostic Protocol):**
   - **Pha 1: Thẩm Định Giả Thuyết & Kiểm Chứng Thực Nghiệm (4–5 phút):**
     - Đặt định hướng chẩn đoán và câu hỏi kinh doanh sắc bén.
     - Khai thác MySQL, hiển thị câu lệnh SQL và bảng số liệu thực chứng trên chat.
     - Mổ xẻ cơ chế nghịch lý và định vị căn bệnh cốt lõi.
   - **Pha 2: Tự Động Hóa Đóng Gói Bộ Tứ Ấn Phẩm (5–6 phút):**
     - Sau khi logic và dữ liệu đã được chốt: Tự động chạy script sinh đồng bộ 4 sản phẩm:
       1. CSV Data Marts trong `data_bi/`.
       2. Sổ báo cáo Excel điều hành 5 sheet (`.xlsx`) định dạng số học chuẩn.
       3. Dashboard HTML Cockpit chuyển tab tương tác 2 chiều với Chart.js (`.html`).
       4. Dự án Power BI Fabric PBIP (`.pbip`, `.Report`, `.SemanticModel`, TMDL, 12 visuals schema 2.9.0, validate 0 lỗi).
     - Áp dụng kỹ năng Watermark Remover trên toàn bộ văn bản và tài liệu `README.md`.
     - Đóng gói Git commit sạch sẵn sàng đồng bộ.

