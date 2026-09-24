# Customer RFM & Retention Analysis Framework

Được đúc kết từ Dashboard 2.pbix và Chương III.2 của Báo cáo Nhóm 6.

## 1. Phương pháp chấm điểm RFM trên Olist
Do Olist là sàn thương mại điện tử, tần suất mua hàng lặp lại (Repeat Purchase) tương đối thấp so với hàng tạp hóa/FMCG.
- **Recency (R - Số ngày kể từ lần mua gần nhất):**
  - $\le 60$ ngày: 5 điểm
  - $61 - 150$ ngày: 4 điểm
  - $151 - 300$ ngày: 3 điểm
  - $301 - 450$ ngày: 2 điểm
  - $> 450$ ngày: 1 điểm
- **Frequency (F - Số lần mua thành công):**
  - $\ge 20$ lần: 5 điểm
  - $10 - 19$ lần: 4 điểm
  - $5 - 9$ lần: 3 điểm
  - $2 - 4$ lần: 2 điểm
  - $< 2$ lần: 1 điểm
- **Monetary (M - Tổng chi tiêu bao gồm cả cước vận chuyển):**
  - $\ge 1000$ BRL: 5 điểm
  - $500 - 999$ BRL: 4 điểm
  - $200 - 499$ BRL: 3 điểm
  - $100 - 199$ BRL: 2 điểm
  - $< 100$ BRL: 1 điểm

## 2. 11 Phân khúc Khách hàng Chiến lược
1. **Champions (555, 554, 544, 545, 454, 455, 445):** Khách hàng VIP nhất, chi tiêu lớn, mua thường xuyên.
2. **Loyal Customers (543, 444, 435, 355, 354, 345, 344, 335):** Khách hàng trung thành, phản hồi tốt.
3. **Potential Loyalists:** Mới mua gần đây, chi tiêu khá, có tiềm năng thành khách quen.
4. **Recent Customers:** Khách mới mua lần đầu gần đây.
5. **Promising:** Khách mua đơn giá trị cao nhưng tần suất chưa nhiều.
6. **Customers Needing Attention:** Khách từng có tương tác tốt nhưng lâu chưa quay lại.
7. **About to Sleep:** Nguy cơ chuyển sang ngủ đông.
8. **At Risk:** Khách hàng giá trị cao trước đây nhưng đã lâu không mua.
9. **Can't Lose Them:** Từng chi tiêu rất lớn nhưng đã dừng hẳn mua sắm.
10. **Hibernating:** Mua thưa thớt, giá trị thấp, đã lâu không quay lại.
11. **Lost Customers:** Khách hàng đã hoàn toàn rời bỏ.

## 3. Nghịch lý bang São Paulo (SP Paradox)
- **Hiện tượng:** SP chiếm hơn 40% tổng số khách hàng của Olist, nhưng hơn 80% khách tại SP nằm ở nhóm `Lost`, `About to Sleep`, hoặc `Hibernating`.
- **AOV tại SP:** Thấp hơn mức trung bình của toàn quốc.
- **Hàm ý chiến lược:** Thay vì tiếp tục đổ chi phí quảng cáo (CAC) tìm khách mới tại SP, Olist cần chuyển hướng ngân sách sang các chiến dịch Retention & Loyalty (Voucher mua lại lần 2, chương trình hội viên).
