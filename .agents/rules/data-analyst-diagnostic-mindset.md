# Quy chuẩn Phân tích Dữ liệu Dự án: The Diagnostic Analyst Mindset (POV Data Analyst Nhóm 6)

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
4. **Trực quan hóa Bảng Dữ liệu (Table Data Visualization):** BẮT BUỘC kèm theo một biểu đồ trực quan hóa dữ liệu của bảng đó (Inline HTML widget qua `<agent-embed>` / SVG / Chart / Đồ thị trực quan) ngay dưới bảng dữ liệu để người đọc dễ nhìn, nắm bắt ngay phân phối, xu hướng, tương quan và điểm dị biệt mà không phải căng mắt đọc bảng số thô.
5. **Phân tích Chuyên sâu:** Từ dữ liệu và biểu đồ vừa trực quan hóa, đưa ra lý giải, bóc tách đa chiều và kết luận chiến lược.
*(Lặp lại chu trình này cho mỗi insight tiếp theo).*

