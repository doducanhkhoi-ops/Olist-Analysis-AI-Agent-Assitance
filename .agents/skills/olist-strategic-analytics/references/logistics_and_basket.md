# Logistics SLA & Order Basket Dynamics

Được đúc kết từ Dashboard 2.pbix và Chương III.3 của Báo cáo Nhóm 6.

## 1. Hành vi Mua hàng theo Số lượng Seller (Single vs Multi-seller)
- **Cơ cấu đơn hàng:**
  - `Single-seller` (1 người bán): Chiếm ~98.7% đơn hàng.
  - `Multi-seller` (Từ 2 người bán trở lên): Chiếm ~1.3% đơn hàng.
- **Giá trị kinh tế:**
  - AOV của đơn Multi-seller (257.36 BRL) **cao hơn 62%** so với Single-seller (158.52 BRL).
  - Số mặt hàng trung bình (Avg Items): 2.43 items vs 1.12 items.
- **Nghịch lý Logistics:**
  - Đơn Multi-seller phức tạp hơn trong đóng gói và điều phối, nhưng tỷ lệ giao trễ (`late_delivery_pct`) chỉ **1.41%**, thấp hơn nhiều so với Single-seller (**8.20%**).
  - *Nguyên nhân:* 85% đơn multi-seller tập trung tại các bang Đông Nam (SP, RJ, MG) có mật độ seller dày đặc, hạ tầng bưu chính phát triển và chính sách gom đơn giao đồng bộ trong cùng 1 ngày của Olist hoạt động rất hiệu quả.

## 2. Đa dạng hóa Danh mục Hàng hóa (Category Diversity)
- Đơn 1 Category: AOV ~ 158 BRL.
- Đơn 2 Categories: AOV ~ 253 BRL.
- Đơn 3 Categories: AOV ~ 313 BRL.
- **Hàm ý:** Cross-selling và gợi ý mua kèm sản phẩm khác ngành hàng là đòn bẩy trực tiếp làm tăng AOV và doanh thu trên mỗi lượt truy cập (Revenue per Visit).

## 3. Quản trị Rủi ro Logistics theo Vùng Miền
- Đo lường: `order_delivered_customer_date > order_estimated_delivery_date`.
- Tỷ lệ giao trễ tập trung cao ở các bang miền Bắc và Đông Bắc (Norte / Nordeste) như AL, MA, PA, BA do địa hình phức tạp và thiếu trung tâm hoàn tất đơn hàng (Fulfillment Center).
