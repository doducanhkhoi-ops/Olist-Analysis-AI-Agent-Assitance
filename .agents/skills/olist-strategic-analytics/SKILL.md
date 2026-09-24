---
name: olist-strategic-analytics
description: >-
  Framework phân tích chiến lược e-commerce Olist chuyên sâu (FTU TINH313 - Nhóm 6).
  CHỈ KÍCH HOẠT KHI: Người dùng rõ ràng yêu cầu "sử dụng các skill và rule đã cài để phân tích...", "phân tích sâu toàn diện", hoặc làm báo cáo chiến lược cấp cao. KHÔNG tự động kích hoạt cho các câu hỏi tra cứu hoặc vẽ biểu đồ đơn lẻ thông thường.
---

# Olist Strategic Analytics Skill (FTU TINH313 - Nhóm 6 Framework)

> ⚠️ **ĐIỀU KIỆN KÍCH HOẠT (ACTIVATION CRITERIA):**
> Skill này **CHỈ ĐƯỢC PHÉP KÍCH HOẠT** khi người dùng có câu lệnh rõ ràng: *"sử dụng các skill và rule đã cài để phân tích..."*, *"phân tích sâu...", "làm báo cáo chuyên đề..."*.
> Nếu người dùng chỉ hỏi câu hỏi số liệu thông thường hoặc yêu cầu vẽ biểu đồ trực diện đơn lẻ, **KHÔNG KÍCH HOẠT** skill này để tránh làm mất thời gian; hãy thực hiện trực tiếp và nhanh chóng theo nhu cầu người dùng.

Skill này đóng gói toàn bộ phương pháp luận phân tích nghiệp vụ chuyên sâu, mô hình chẩn đoán nghịch lý và các quy tắc dự báo kinh doanh từ công trình nghiên cứu 97 trang của **Nhóm 6 (Môn Quản trị Cơ sở Dữ liệu TINH313 - FTU)** về sàn thương mại điện tử **Olist (Brazil)**.

Mục tiêu cốt lõi: **Biến dữ liệu giao dịch thô thành quyết định chiến lược (Actionable Insights)**, giải quyết triệt để bài toán tăng trưởng bền vững (Retention & LTV) thay vì chỉ đốt tiền tìm khách mới (Acquisition).

---

## 1. Triết lý phân tích: Quy tắc 4 Bước (Insight Formulation)

Khi phân tích bất kỳ khía cạnh nào của cơ sở dữ liệu `olist_raw`, luôn tuân thủ cấu trúc 4 bước:

1. **Quan sát (Observation):** 
   - Không dừng ở con số tổng. Chỉ ra các điểm lệch chuẩn, nghịch lý hoặc chỉ số biên (Ví dụ: Bang đông khách nhất lại có AOV thấp nhất; Đơn hàng nhiều người bán phức tạp hơn nhưng thời gian giao hàng lại nhanh hơn).
2. **Bóc tách nguyên nhân (Deep Dive & Root-Cause Diagnosis):** 
   - Đối chiếu chéo đa chiều: **Địa lý (State/Region) $\times$ Mùa vụ (Seasonality) $\times$ Mạng lưới Seller (Single vs Multi) $\times$ Trải nghiệm Vận hành (SLA Logistics & Reviews)**.
3. **Đo lường tác động kinh doanh (Business Impact):** 
   - Đánh giá trực diện 3 trụ cột của Olist: Chi phí sở hữu khách hàng (**CAC**), Giá trị trọn đời (**LTV**), Tỷ lệ duy trì (**Retention Rate**), Biên lợi nhuận ròng và Uy tín sàn thương mại.
4. **Hành động theo lộ trình (Phased Recommendations):** 
   - Đưa ra giải pháp đo lường được: Chính sách phí sàn, trung tâm ươm tạo seller, thuật toán gợi ý bundle/cross-sell, chính sách gom đơn đồng bộ, kịch bản marketing 4 giai đoạn.

---

## 2. Sáu Trụ cột Nghiệp vụ & Khung Chẩn đoán Thực chiến

### 🔷 Trụ cột 1: Phân tích Người bán (Sellers) & Mạng lưới Cung ứng Đa vùng

#### 1.1. So sánh Đơn hàng Tổng (All Orders) vs Đơn thành công (Delivered Orders)
* **Mục đích:** Tách bạch giữa "sức hút thương mại trên giấy" và "năng lực thực thi chuỗi cung ứng".
* **Chỉ số cảnh báo:** Khoảng cách giữa tổng đơn và đơn giao thành công lớn $\rightarrow$ Người bán có tỷ lệ hủy/hoàn đơn cao hoặc hàng tồn ảo $\rightarrow$ Nguy cơ trải nghiệm khách hàng tiêu cực.

#### 1.2. Ma trận Phân loại Người bán (Volume vs Value Matrix)
Dựa trên chỉ số **AOV = Doanh thu thành công / Số đơn thành công** và **Sản lượng đơn**:
* **Đơn nhiều, AOV thấp:** Hàng tiêu dùng nhanh giá rẻ $\rightarrow$ Rủi ro lỗi đóng gói, nhầm hàng, quá tải kho vận.
* **Đơn ít, AOV cao:** Ngành hàng cao cấp (Đồng hồ, Điện tử, Nội thất) $\rightarrow$ Cần luồng vận chuyển bảo hiểm đặc biệt, hỗ trợ CSKH VIP.
* **Đơn nhiều, AOV cao:** **Sellers Trụ cột (Key Accounts)** $\rightarrow$ Giữ chân bằng gói chiết khấu phí hoa hồng và quyền ưu tiên hiển thị.
* **Đơn ít, AOV thấp:** Sellers yếu kém $\rightarrow$ Cần đào tạo vận hành hoặc đào thải.

#### 1.3. Lõi vận hành: Seller Đa vùng (Multi-region) vs Đơn vùng (Single-region)
* **Phát hiện Bề mặt:**
  * Seller Đa vùng mang lại **12.84M BRL** doanh thu (áp đảo 176.6K BRL của Đơn vùng) và xử lý **95,302 đơn hàng** (so với 861 đơn).
  * Chỉ số Vận tốc (Order Velocity): Multi-region đạt **1.95 đơn / ngày giao hàng** (vượt trội 61% so với 1.21 của Single-region).
* **Cảnh báo Phương pháp luận (Bẫy Quy mô đội lốt Phạm vi):**
  * **535 seller (18%) chỉ có đúng 1 đơn hàng** $\rightarrow$ về mặt cơ học họ bắt buộc là "một vùng".
  * Khi seller đạt quy mô $\ge 5$ đơn, chỉ còn **41 seller một vùng** so với 2.648 seller đa vùng. Do thiếu vùng quy mô chồng lấn, câu hỏi "phạm vi hay quy mô" **không thể nhận dạng được (non-identifiable)** trên dataset Olist.
  * Phép kiểm Bootstrap 3.000 lần theo cụm seller cho tỷ lệ giao trễ có khoảng tin cậy chứa 0 `[-0,075%; +3,154%]`: **Chưa đủ căn cứ khẳng định có sự khác biệt vận hành giữa hai nhóm**.
* **Hành động Khuyến nghị:** Tập trung hỗ trợ logistics và giảm tỷ lệ trễ ở nhóm seller mới gia nhập (cold start) thay vì phân biệt đối xử theo nhãn một vùng/đa vùng.

#### 1.4. Bộ lọc Ngành hàng Yếu (Weak Category Filter)
Đánh giá theo 3 tiêu chí:
1. Doanh thu thấp hơn mức trung vị sàn.
2. Số lượng đơn đặt hàng thấp.
3. AOV thấp (< 50 BRL).
* **Phan loai:**
  * *Weak Category Specialist:* Người bán phụ thuộc vào ngành hàng yếu $\rightarrow$ Cần tư vấn chuyển đổi danh mục.
  * *Weak Category Generalist:* Người bán đa ngành có chứa danh mục yếu $\rightarrow$ Khuyến nghị cắt giảm SKU rác.
* **Nguyên nhân cốt lõi của đánh giá 1-2 sao:** **94.59%** trường hợp tiêu cực xuất phát từ lý do **"Indisponível" (Unavailable / Hết hàng / Hủy đơn đột ngột)**.

---

### 🔷 Trụ cột 2: Phân khúc Khách hàng RFM & "Nghịch lý São Paulo" (SP Paradox)

#### 2.1. Bức tranh 4 Phân khúc Rủi ro Rời bỏ (RFM Churn Segments)
* **Lost Customers (82.94%):** Recency cao, Frequency thấp, Monetary thấp. Khách hàng "thử 1 lần rồi đi", không thấy lý do gắn bó thành thói quen.
* **Can't Lose Them (14.71%):** Từng chi tiêu lớn nhưng giãn cách thời gian mua gần nhất rất lâu. Họ đang "dừng lại quan sát xem Olist có đủ hiểu mình hay không".
* **Hibernating (2.05%):** "Ngủ đông", tần suất mua thấp, cần lý do cụ thể để quay lại.
* **At Risk (0.30%):** Nhóm nguy cơ cao cần can thiệp khẩn cấp.

#### 2.2. Hội chứng "3 Không" & Căn bệnh "Thùng Rỗng Đáy" (Leaky Bucket)
* **Thực trạng:** Hơn **95%** khách hàng chỉ mua duy nhất **1 lần**; tỷ lệ mua lặp lại (`repeat_purchase_rate`) qua các tháng xấp xỉ **0.00%**.
* **Hệ quả:** Olist chịu chi phí thu hút khách hàng (CAC) liên tục tăng, phụ thuộc hoàn toàn vào khách mới, biên lợi nhuận bị bào mòn.

#### 2.3. Giải mã Nghịch lý São Paulo (The SP Paradox)
* **Nghịch lý:** SP là bang có dân số, số đơn và tổng doanh thu lớn nhất cả nước, nhưng **AOV lại thấp nhất** trong số các bang! Khách hàng SP chỉ mua nhỏ lẻ (mua nhanh, giá trị thấp, giỏ hàng bình quân chỉ 1.04 danh mục).
* **Bóc tách thị phần cạnh tranh:**
  * Tại thị trường São Paulo, Olist chỉ chiếm **14.6% thị phần** (thua xa **Mercado Livre 53.0%** và **Amazon Brazil 28.5%**).
  * Khách hàng SP xem Olist như một kênh mua hàng phụ/ngách cho các món đồ lặt vặt; các đơn hàng giá trị cao họ đổ dồn sang Mercado Livre.
* **Sự đối lập với các bang vùng xa:** Các bang miền Bắc (AC, AP, RR) có số lượng khách ít nhưng **AOV cao vượt trội**, vì chi phí và thời gian giao hàng lớn buộc khách hàng phải gom đơn mua hàng giá trị cao để bõ công vận chuyển.

---

### 🔷 Trụ cột 3: Hành vi Giỏ hàng & Nghịch lý Logistics Đơn Multi-seller

#### 3.1. Nghịch lý Multi-seller Toàn Diện (Giao nhanh nhưng Trải nghiệm Sụp đổ)
* **Quan sát Bề mặt:**
  * **98%** đơn hàng là Single-seller; chỉ **~1,5% – 2%** đơn là Multi-seller ($\ge 2$ người bán).
  * Đơn Multi-seller có AOV thô cao hơn hẳn (~257 BRL vs ~158 BRL), giao nhanh hơn (-3,5 ngày) và tỷ lệ trễ thấp hơn rõ rệt (1,02% vs 6,85%).
* **Giải phẫu Bản chất Đa chiều (True Root-Causes):**
  1. **AOV không hề "gấp đôi":** Khi giữ cố định số mặt hàng (`items = 3`), AOV của multi-seller (296,25 BRL) và single-seller (291,77 BRL) gần như bằng nhau. Chênh lệch AOV thô chủ yếu do giỏ hàng có nhiều mặt hàng hơn.
  2. **Tỷ lệ trễ thấp một phần do hạn cam kết dài hơn:** Đơn multi-seller được đặt thời hạn giao dài hơn (+1,66 ngày) và hưởng lợi thế tuyến giao tập trung ở miền Đông Nam (SP, RJ, MG).
  3. **MẶT TỐI SỤP ĐỔ CỦA NGHỊCH LÝ (Review Collapse):** Điểm đánh giá của đơn multi-seller tụt sâu xuống **2,85 sao** (so với 4,17 sao của single-seller); tỷ lệ **1 sao chiếm tới 36,0%** (so với 9,4%). Khoảng cách âm **-0,96 sao** vẫn tồn tại vững chắc ngay cả sau khi chuẩn hóa đồng thời theo `item × bang × tháng` (53/61 ô cùng chiều âm).
* **Cảnh báo Suy diễn:** Dataset Olist không có thông tin tracking từng kiện hàng, không được tự phỏng đoán "chính sách gom đơn hoàn hảo". Vấn đề cốt lõi là trải nghiệm nhận hàng rời rạc, bất tiện từ nhiều người bán làm khách hàng thất vọng cực độ dù hàng đến đúng hạn cam kết.

#### 3.2. Quy luật Đa dạng Danh mục (Category Diversity)
* **Heatmap Seller $\times$ Category:**
  * 1 seller & 1 category: AOV ~ **158 BRL**.
  * 2 sellers & 2 categories: AOV ~ **253 BRL**.
  * 3 sellers & 2 categories: AOV ~ **443 BRL**.
* **Thực trạng hạn chế:** Đa dạng ngành hàng trung bình trên mỗi đơn hiện chỉ đạt **~1.04 - 1.05**, kể cả vào các đợt siêu sale. Khách hàng chưa có thói quen tự gom hàng đa ngành $\rightarrow$ **Cơ hội vàng cho thuật toán Cross-selling & Bundle Recommendations**.

---

### 🔷 Trụ cột 4: SLA Logistics & Trải nghiệm Khách hàng theo Địa lý

#### 4.1. Tỷ lệ Giao hàng Trễ (`late_delivery_pct`)
* Công thức SLA: Đo khoảng cách giữa `order_delivered_customer_date` (ngày thực tế) và `order_estimated_delivery_date` (ngày cam kết).
* **Vùng rủi ro cao (Đông Bắc / Bắc):** **Alagoas (AL: 23.99%)** và **Maranhão (MA: 19.50%)** có tỷ lệ trễ kỷ lục $\rightarrow$ Hơn **60%** khách hàng tại đây rơi vào nhóm Lost/Hibernating do sụt giảm niềm tin nghiêm trọng.
* **Vùng vận hành tốt (Đông Nam):** **São Paulo (SP: 5.9%)** và **Minas Gerais (MG: 5.6%)** giao rất nhanh và ổn định.

#### 4.2. Tương quan Điểm Đánh giá (Review Score)
* Điểm hài lòng trung bình tương quan nghịch rõ rệt với tỷ lệ giao trễ. Khi tỷ lệ trễ vượt qua 10%, điểm review tụt sâu dưới 4.0.
* **Nguyên nhân đánh giá 1 sao:** Không chỉ do giao chậm, mà chủ yếu là do tình trạng "Unavailable" (seller tự ý báo hết hàng sau khi khách đã thanh toán).

---

### 🔷 Trụ cột 5: Mô hình Hồi quy Đo lường Độ nhạy Giá (Price Elasticity)

#### 5.1. Hệ số Góc Ngành Sức khỏe & Sắc đẹp (Health & Beauty)
* **Kết quả mô hình hồi quy:** Hệ số góc $\text{Slope} \approx \mathbf{+1.89}$.
* **Bản chất kinh tế:** Trong dải giá tiêu chuẩn (90 - 140 BRL), khi giá trung bình tăng 1 BRL, số lượng sản phẩm bán ra vẫn tăng thêm 1.89 đơn vị. Điều này cho thấy người tiêu dùng ngành mỹ phẩm/chăm sóc sức khỏe chuộng các thương hiệu cao cấp, chính hãng và sẵn sàng trả giá cao để đảm bảo chất lượng.
* **Ngưỡng trần tâm lý (Psychological Resistance Ceiling):** Khi giá chạm ngưỡng đỉnh **~150 BRL**, đường hồi quy bắt đầu thoái lui, sản lượng mua có xu hướng sụt giảm nhẹ.
* **Khuyến nghị định giá:** Áp dụng chiến lược giá sát trần (~140 BRL cho sản phẩm đơn lẻ) hoặc thiết lập các **Combo 2 sản phẩm (~289 BRL)** để tối đa hóa AOV mà không vượt qua điểm rơi tâm lý.

---

### 🔷 Trụ cột 6: Khung Dự báo Mùa vụ & Kịch bản Chiến dịch 4 Giai đoạn

#### 6.1. Chu kỳ Doanh thu & Cảnh báo Dữ liệu Cắt cụt (Temporal Censoring)
* **Thực trạng dữ liệu:**
  * **Năm 2016:** Tháng 11/2016 có **0 đơn hàng** $\rightarrow$ toàn bộ dataset thực tế chỉ quan sát được **đúng 1 chu kỳ Black Friday duy nhất (11/2017)**. Mọi mô hình dự báo mùa vụ nhiều năm (như SARIMA) cần được diễn giải với sự thận trọng cao nhất.
  * **Năm 2017:** Bùng nổ đỉnh điểm Black Friday (24/11/2017 đạt 1.176 đơn = 6,11 lần ngày thường), tăng trưởng chủ yếu do người mua mới (+46,2%).
  * **Năm 2018:** Cắt cụt vào **17/10/2018** khiến tháng 9 và tháng 10 sụt giảm đột ngột do hết dữ liệu, không phải do suy thoái kinh doanh.
  * **Khóa Dải Chuỗi Thời Gian Chuẩn:** Bắt buộc phân tích xu hướng ổn định từ **2017-01 đến 2018-08**.

#### 6.2. Dự báo Khách hàng mới & Bẫy Đồng nhất thức Số học ($r = 0,997$)
* **Cảnh báo Ngộ nhận Tương quan:** Tương quan $r = 0,993$ giữa khách mới và doanh thu (hay $r = 1,000$ giữa khách mới và số đơn) là **đồng nhất thức số học**, vì **96,92%** đơn hàng là lần mua đầu tiên của khách.
* **Thực tế Cohort Khách mới Tháng 11/2017:** Chỉ có **2,05%** khách quay lại mua sau 90 ngày (không khác biệt có ý nghĩa thống kê so với tháng 10 ở mức 2,08%). Giá trị của đợt cao điểm nằm ở doanh số tức thời, không chuyển hóa thành tệp khách hàng trung thành dài hạn.

#### 6.3. Playbook Chiến dịch Marketing 4 Giai đoạn (Phased Campaign Calendar)

| Giai đoạn | Ngành hàng Tiềm năng Chủ lực | Hành động Chiến lược Cốt lõi |
| :--- | :--- | :--- |
| **Tháng 9 (Hậu mùa đông)** | **Xây dựng, An ninh & Dụng cụ** (`ferramentas_seguranca`, `casa_construcao`) | Kích cầu xu hướng sửa sang, làm mới nhà cửa sau mùa đông. Khởi động chiến dịch sớm thu hút khách mới. |
| **Tháng 10 (Chuẩn bị lễ hội)** | **Ô tô, Phụ kiện & Công nghệ** (`automotive`, `informatica_acessorios`) | Nhu cầu tân trang phương tiện và thiết bị công nghệ. Bắt đầu tung khuyến mãi sớm phối hợp với các hãng công nghệ lớn. |
| **Tháng 11 (Black Friday)** | **Sức khỏe, Sắc đẹp & Gia dụng** (`beleza_saude` bùng nổ ~253K BRL, `utilidades_domesticas`, `cama_mesa_banho`) | Chạy Flash Sale liên tục theo khung giờ. Thiết kế Combo đa ngành cross-sell. Chuẩn bị trước hạ tầng logistics để tránh quá tải. |
| **Tháng 12 (Giáng sinh & Nghỉ lễ)** | **Đồng hồ, Quà tặng & Thể thao** (`relogios_presentes`, `esporte_lazer`, bảo dưỡng xe) | Khuyến mãi quà tặng dịp lễ. **Tung voucher trả góp 0% lãi suất** (`payment_installments`). Cam kết SLA giao hàng trước Giáng sinh để phá vỡ "Pre-Christmas drop". |

---

## 3. Bộ Chỉ số Chẩn đoán Nhanh (Diagnostic Checklist)

Trước khi phát hành báo cáo hoặc xây dựng dashboard, hãy kiểm tra 5 chỉ số sau:
1. **Tỷ trọng Doanh thu Multi-region:** Có duy trì trên **95%** hay không?
2. **Khoảng cách AOV giữa các Bang:** Có xuất hiện "SP Paradox" (AOV bang lớn thấp hơn bang xa) không?
3. **Tỷ lệ Khách hàng Lost + Hibernating:** Nếu vượt quá **80%**, cần rung chuông cảnh báo về mô hình giữ chân khách hàng.
4. **Tỷ lệ Đơn hàng Multi-seller:** Đã đạt trên **2%** chưa? Nếu chưa, hệ thống gợi ý giỏ hàng đang kém hiệu quả.
5. **Đỉnh Doanh thu Tháng 11 vs Tháng 12:** Có duy trì được đà doanh số tháng 12 hay bị rơi tự do do nỗi sợ logistics?
