# Seller Performance & Geographical Reach Framework

Được đúc kết từ Dashboard 1.pbix và Chương III.1 của Báo cáo Nhóm 6.

## 1. So sánh All Orders vs Delivered Orders
- `total_orders`: Bao gồm tất cả đơn (kể cả canceled, unavailable, created).
- `successful_orders`: Chỉ đơn `delivered`.
- **Insight:** Seller có độ chênh lệch lớn giữa 2 chỉ số này cảnh báo khâu tồn kho ảo hoặc tỷ lệ hủy đơn cao do xử lý đơn chậm.

## 2. Ma trận Doanh thu vs Khối lượng (Volume vs Value)
- Trục X: `seller_order_count` (Số đơn thành công)
- Trục Y: `AOV` (Doanh thu / Số đơn)
- **4 Phân nhóm chiến lược:**
  1. *Volume Leaders (Đơn cao, AOV thấp):* Nhóm bán hàng gia dụng, phụ kiện giá rẻ. Cần hỗ trợ tự động hóa in vận đơn.
  2. *Value Leaders (Đơn thấp, AOV cao):* Nhóm bán đồng hồ, điện máy, nội thất cao cấp. Cần bảo hiểm hàng hóa và chăm sóc khách hàng VIP.
  3. *Core Stars (Đơn cao, AOV cao):* Top sellers đóng góp GMV lớn nhất cho Olist.
  4. *Low Performers (Đơn thấp, AOV thấp):* Cần đào tạo hoặc loại bỏ khỏi sàn.

## 3. Phân loại Seller theo Phạm vi Địa lý
- **Single-region Sellers:** Chỉ bán hàng cho khách hàng trong cùng 1 bang (nội bang). Tỷ lệ trễ hạn thấp.
- **Multi-region Sellers:** Bán hàng xuyên bang cho khách hàng ở nhiều bang khác nhau. Đóng góp doanh thu lớn nhưng tỷ lệ giao trễ (`avg_late_delivery_pct`) cao hơn do khoảng cách địa lý.

## 4. Phân loại Danh mục Hàng hóa (Category Performance)
- Tiêu chí đánh giá 3 chiều:
  - Số lượng đơn hàng (Orders) < 50
  - Tổng doanh thu (Revenue) < 5000 BRL
  - Giá trị đơn trung bình (AOV) < 50 BRL
- Gán nhãn: `Yếu (3/3)`, `Yếu (2/3)`, `Bình thường/Mạnh`.
