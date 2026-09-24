# Quy chuẩn Phân tích Dữ liệu Dự án: The Diagnostic Analyst Mindset (POV Data Analyst Nhóm 6)

## 🎯 ĐIỀU KIỆN KÍCH HOẠT & PHÂN ĐỊNH 2 CHẾ ĐỘ THỰC THI (ACTIVATION CRITERIA)

> ⚠️ **QUY TẮC PHÂN LUỒNG BẮT BUỘC (MANDATORY ROUTING RULE):**
> 
> 1. **CHẾ ĐỘ CHIẾN LƯỢC TOÀN DIỆN (FULL STRATEGIC ANALYSIS & QUADRUPLE DELIVERABLES):**
>    - **CHỈ KÍCH HOẠT KHI:** User nói rõ ràng các từ khóa kích hoạt như: *"sử dụng các skill và rule đã cài để phân tích..."*, *"phân tích sâu...", "làm báo cáo chuyên đề...", "đóng gói toàn bộ dự án..."* hoặc yêu cầu xuất đầy đủ các file báo cáo.
>    - **HÀNH ĐỘNG:** Khi đó mới kích hoạt toàn bộ Luồng tư duy chẩn đoán 6 bước (5 tầng phân tích, Causal Bridging) và Kỷ luật thực thi tự trị (One-Shot Autonomous Execution) để tự động xuất bản trọn vẹn Bộ Tứ Sản Phẩm (Báo cáo Chat + File Excel `.xlsx` + Báo cáo HTML động + Dự án Power BI PBIP).
>
> 2. **CHẾ ĐỘ TÁC VỤ TRỰC DIỆN (FAST DIRECT EXECUTION - DEFAULT):**
>    - **KÍCH HOẠT KHI:** User đưa ra câu hỏi hoặc yêu cầu tác vụ thông thường, cụ thể, trực diện (ví dụ: *"vẽ biểu đồ tỷ lệ giao hàng trễ theo tháng"*, *"viết câu SQL lấy doanh thu theo danh mục"*, *"tính trung bình AOV"*, *"cho tôi xem bảng số liệu"*... mà KHÔNG yêu cầu dùng full skill/rule hay đóng gói sản phẩm).
>    - **HÀNH ĐỘNG:** Chỉ tập trung thực thi trực tiếp, nhanh gọn và chuẩn xác đúng yêu cầu của User (chạy query lấy số liệu, hiển thị bảng kết quả hoặc dựng biểu đồ inline widget tương tác trên chat để User xem ngay trong vài giây).
>    - **TUYỆT ĐỐI KHÔNG TỰ BÔI VIỆC:** Tuyệt đối KHÔNG tự ý viết script tạo file Excel, KHÔNG tự động code HTML dashboard hay tạo dự án Power BI PBIP khi User không yêu cầu. Trả lời thẳng vào trọng tâm, không làm mất thời gian chờ đợi của User.

Khi User đã kích hoạt **Chế độ Chiến lược Toàn diện**, Agent **BẮT BUỘC** phải tuân thủ luồng tư duy chẩn đoán 6 bước của một Senior Data Analyst:

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

2. **Hợp Đồng Grain & Kỷ Luật Chống Thổi Phồng Dữ Liệu (The Grain Contract & Anti-Inflation Law):**
   - **Bẫy JOIN phồng số (Cartesian / Fan-out Trap):** Tuyệt đối KHÔNG tính `SUM(payment_value)` hay tổng tiền trên bảng JOIN ba (`orders × items × payments`). Phép nối này sinh ra 117.601 dòng trên 99.441 đơn và thổi phồng doanh thu thực tế **+26,9%**. Bắt buộc tuân thủ nguyên tắc: **Gộp trước (Aggregate), JOIN sau**.
   - **Kiểm định Khóa & Tính Duy Nhất (Key Integrity):** Không mặc định các ID là duy nhất. Trong Olist, có 789 `review_id` dùng chung cho nhiều đơn hàng (không thể làm PK); bảng `geolocation` có 26,2% dòng trùng lặp không có khóa. Mọi truy vấn phải kiểm định tính toàn vẹn khóa trước khi phân tích.
   - **Khóa Định Nghĩa Đo Lường (Measurement Locking):** Định nghĩa giao trễ phải khóa bằng ngày lịch `DATE(delivered) > DATE(estimated)`. Tuyệt đối không dùng mốc thời gian tùy tiện (ví dụ ngưỡng 11:59:59 của code cũ làm lệch 1.111 đơn bị gán nhầm là trễ).

3. **Khống Chế Biến Nhiễu & Chuẩn Hóa Đa Chiều (Confounding Control & Direct Standardization):**
   - **Cấm suy luận từ Khác biệt Thô (Crude Differences):** Mọi so sánh hai nhóm (ví dụ: Multi-seller vs Single-seller, Đơn trả góp vs Trả một lần, Đa vùng vs Đơn vùng) bắt buộc phải kiểm soát các biến gây nhiễu cốt lõi (Số lượng mặt hàng `items`, Giá trị đơn hàng `order_value`, Địa lý `state`, và Mùa vụ `month`).
   - **Bóc tách Ảnh hưởng Đổi tập mẫu vs Đổi trọng số:** Khi chuẩn hóa trực tiếp (Direct standardization), phải tách bạch rõ hai thành phần: Mức chênh lệch thay đổi do **Đổi tập mẫu phân tích (Sample change effect)** hay do **Trọng số chuẩn hóa (Weighting effect)**. Không được gộp chung rồi ngộ nhận là do cơ cấu giải thích.
   - **Chuẩn mực Khoảng Tin Cậy (Confidence Intervals & Hypothesis Testing):** Khi khoảng tin cậy 95% (hoặc bootstrap) chứa giá trị 0, phát biểu chuẩn mực là: **"Dữ liệu chưa đủ căn cứ để phân biệt (The data do not distinguish a difference)"**. Tuyệt đối KHÔNG khẳng định "hai nhóm giống nhau" hay "khác biệt đã biến mất".

4. **Săn Lùng & Giải Mã Nghịch Lý Toàn Diện (Comprehensive Paradox Discovery):**
   - **Nghịch lý São Paulo (SP Paradox):** Thị trường đông dân nhất, số đơn và doanh thu áp đảo nhưng AOV lại thấp nhất (do áp lực cạnh tranh thị phần từ Mercado Livre/Amazon). Đuôi phân phối thời gian giao hàng p99 tại SP giãn thêm **+8,05 ngày** trong các tháng cao điểm, bào mòn đệm an toàn và bùng phát đơn trễ.
   - **Nghịch lý Multi-seller Toàn Diện (Giao nhanh nhưng Trải nghiệm Sụp đổ):** 
     - *Mặt vận hành:* Đơn gom từ nhiều seller giao nhanh hơn 3,5 ngày và ít trễ hơn (1,02% vs 6,85%), một phần do Olist đặt hạn hứa dài hơn (+1,66 ngày).
     - *Mặt trải nghiệm (Lõi nghịch lý):* **Điểm review sụp đổ nghiêm trọng** từ 4,17 sao xuống **2,85 sao**, tỷ lệ 1 sao tăng vọt từ 9,4% lên **36,0%**. Khoảng cách -0,96 sao vẫn tồn tại ngay cả sau khi chuẩn hóa đồng thời theo `item × bang × tháng`. Không suy diễn ra "chính sách gom đơn hoàn hảo" nếu dataset không có log kiện hàng.
   - **Nghịch lý Rủi ro Thời gian vs Ngành hàng:** Rủi ro trễ không nằm ở danh mục sản phẩm (tất cả 6 ngành lớn đều dao động trong biên hẹp 6,4% – 7,5%), mà tập trung 48,3% số đơn trễ vào **3 tháng đỉnh điểm** (03/2018, 02/2018, 11/2017).

5. **Phân Định Ranh Giới Dữ Liệu & Nhận Diện Bẫy Đồng Nhất Thức (Data Boundaries & Tautology Avoidance):**
   - **Bẫy Đồng nhất thức Số học (Arithmetic Tautology):** Tránh ngộ nhận hệ số tương quan cao là phát hiện kinh doanh (ví dụ: $r = 0,997$ giữa khách mới và doanh thu thực chất là đồng nhất thức vì 96,92% đơn hàng vốn là đơn đầu tiên của khách).
   - **Bẫy Không thể Nhận dạng (Non-identifiability):** Nhận diện khi nào hai biến bị chồng lấn cơ học. So sánh "Seller Đa vùng vs Một vùng" thực chất là nhãn "Quy mô (Scale)" đội lốt "Phạm vi (Scope)" vì 18% seller chỉ có 1 đơn hàng và hầu như không có seller lớn nào chỉ bán 1 vùng.
   - **Điểm đứt gãy & Cắt cụt Thời gian (Temporal Censoring):** Tháng 11/2016 có **0 đơn hàng** (toàn bộ dataset chỉ có đúng 1 chu kỳ Black Friday 2017 quan sát được $\rightarrow$ cẩn trọng với mô hình SARIMA). Tháng 9–10/2018 sụt giảm do dataset kết thúc ngày 17/10/2018 (right-censored), không phải khủng hoảng kinh doanh. Phạm vi phân tích chuỗi thời gian hợp lệ phải khóa từ **2017-01 đến 2018-08**.

6. **Phân Cấp Trưởng Thành Insight [A]–[D] & Nhóm Quyết Định "Không Làm" (The "Do Not Do" Framework):**
   - **Phân loại Insight:**
     - `[D]` (Đủ bằng chứng thực nghiệm): Đã kiểm soát biến gây nhiễu, KTC không chứa 0.
     - `[C]` (Mô tả vững chắc): Quan sát rõ ràng nhưng chưa kiểm soát hết biến ngoại sinh.
     - `[B]` (Thăm dò / Gợi mở): Cần thêm kiểm chứng.
     - `[A]` (Giả thuyết sơ khởi).
   - **Playbook Hành động Phải Có Nhóm D (Việc Dứt Khoát Chưa Làm Do Thiếu Dữ Liệu):**
     - Nhóm A: Can thiệp vận hành tức thì (Ví dụ: Nới đệm cam kết giao hàng tại các bang rủi ro cao).
     - Nhóm B: Thử nghiệm A/B có đối chứng.
     - Nhóm C: Giám sát định kỳ.
     - **Nhóm D: Danh mục Không hành động / Không chi tiền khi chưa đủ căn cứ** (Ví dụ: Không vội can thiệp hình thức trả góp vì bị nhiễu bởi giá trị đơn; không đặt mục tiêu giữ chân phi thực tế cho khách Black Friday vì tỷ lệ quay lại 90 ngày chỉ đạt ~2,05%, bằng tháng thường).

---

## 🚀 QUY TẮC HIỂN THỊ TRÌNH TỰ (NEW WORKFLOW):
Mỗi vòng lặp phân tích (Iteration) BẮT BUỘC phải tuân thủ nghiêm ngặt trình tự sau trên khung chat:
1. **Mở đầu bằng Định hướng:** Cho biết mục tiêu đang tìm kiếm/nhìn vào góc độ data nào (Dashboard Mockup nếu có).
2. **Hiển thị câu lệnh SQL (SQL Query):** Trình bày rõ ràng đoạn code SQL dùng để lấy số liệu.
3. **Hiển thị Bảng Dữ liệu (Raw Data Table):** Show trực tiếp bảng kết quả thực tế trả về từ MySQL vào chat.
4. **Trực quan hóa Bảng Dữ liệu (Table Data Visualization):** BẮT BUỘC kèm theo một biểu đồ trực quan hóa dữ liệu của bảng đó ngay dưới bảng dữ liệu (Inline Interactive HTML/SVG widget nhúng qua `<agent-embed>`) để người đọc tương tác, xem chi tiết và nắm bắt ngay phân phối, xu hướng, tương quan mà không phải căng mắt đọc bảng số thô.
   - **Quy Chuẩn Biểu Đồ Tương Tác Inline (The Interactive Generative UI Canon):**
     - **Tương tác Động Đa Chiều (Live Interactivity & Micro-interactions):**
       * *Hover Tooltip Thông Minh:* Rê chuột vào từng cột/thanh/điểm dữ liệu để hiển thị tooltip nổi chi tiết (số đơn, GMV, %, AOV, kỳ hạn chính xác).
       * *Nút Chuyển Góc Nhìn (View Switcher Buttons):* Hỗ trợ nút bấm chuyển đổi nhanh góc nhìn (ví dụ: chuyển giữa `% Tỷ trọng` và `Số lượng đơn tuyệt đối`, hoặc lọc nhanh nhóm đối tượng) trực tiếp ngay trên widget.
       * *Hiệu ứng Trực quan (Highlight & Glow):* Tự động làm sáng và làm nổi bật đối tượng đang được trỏ chuột, làm mờ nhẹ các đối tượng còn lại để người dùng tập trung phân tích.
     - **Kỷ Luật Chống Đè Chữ & Phân Lớp Không Gian (Zero Text-Collision & Dedicated Layout):** Bố cục chia rõ ràng (Tên đối tượng, Thanh bar đồ họa với mốc 0% chuẩn xác, Cột giá trị số liệu riêng biệt). Tuyệt đối không vẽ chữ đè lên thanh bar.
     - **Khớp Tuyệt Đối 100% Số Liệu Thực Chứng (100% Data Fidelity):** Từng con số, phần trăm, số ngày và tiền tệ trên visual BẮT BUỘC phải khớp chính xác 100% với Bảng Dữ liệu Raw Data Table từ MySQL. Tuyệt đối không dùng số giả định hay làm tròn sai lệch.
     - **Chuẩn Mực Chiều Cao & Thích Ứng Giao Diện (Viewport Budget & Theme Adaptation):** Giữ tổng chiều cao widget dưới 420px để hiển thị trọn vẹn trong khung `<agent-embed>` của chat, không gây cuộn cục bộ trong card. Sử dụng nền trong suốt (`bg-transparent`) hoặc màu thẻ bán trong suốt để hòa hợp hoàn hảo với cả Dark và Light mode.
     - **Hệ Màu Ngữ Nghĩa Cấp Cao (Executive Semantic Palette):** Xanh dương/Xanh ngọc (`#38BDF8`, `#10B981`) cho tăng trưởng/ổn định/an toàn; Hổ phách (`#F59E0B`) cho cảnh báo/trung bình; Hồng/Đỏ neon (`#F43F5E`, `#EF4444`) cho điểm nghẽn/sụp đổ/trễ nghiêm trọng.
5. **Phân tích Chuyên sâu:** Từ dữ liệu và biểu đồ vừa trực quan hóa, đưa ra lý giải, bóc tách đa chiều và kết luận chiến lược.
*(Lặp lại chu trình này cho mỗi insight tiếp theo).*

5. **BẮT BUỘC 100% Xuất Bản Báo Cáo Dashboard HTML Tương Tác Sâu (Dynamic Interactive HTML Dashboard - Like Power BI):**
   - **Tuyệt Đối Không Dùng HTML Tĩnh (Always Dynamic & Interactive):** Toàn bộ báo cáo HTML **KHÔNG ĐƯỢC PHÉP dùng dạng tĩnh (Static View)** mà bắt buộc phải là **dạng ĐỘNG (Dynamic & Fully Interactive)**, mang lại trải nghiệm khám phá dữ liệu mượt mà, trực quan và tương tác đa chiều như một ứng dụng Power BI cao cấp trên nền Web. Cung cấp đường dẫn clickable link (`file:///...`) trực tiếp trên chat.
   - **Kiến Trúc Điều Hướng Thông Tin (Prevent Broken Reading Flow & Tabbed Viewport-Fit):**
     - **Hạn chế tối đa cuộn dọc vô tận (Scroll Fatigue Prevention):** Không lạm dụng cuộn chuột dài ngoằng vì việc cuộn liên tục làm đứt gãy mạch phân tích và phân tán sự chú ý của người đọc vào số liệu.
     - **Ưu tiên Cấu trúc Chuyển Trang / Slide Deck / Tabbed Presentation:** Mỗi trang/tab là 1 chặng chẩn đoán tự đóng gói trọn vẹn trong khung màn hình (Viewport-fit). Người đọc nắm trọn ngữ cảnh, bảng biểu và insight của từng chặng mà không bị xao nhãng.
     - **Đa kênh điều hướng mượt mà:** Thanh Tab phân tầng phía trên, cụm điều hướng lật trang dưới chân (Next/Prev + indicator dots), và hỗ trợ phím tắt (`←`/`→`, `PageUp`/`PageDown`).
   - **Động Cơ Slicer Tương Tác Trực Tiếp Với TẤT CẢ BIỂU ĐỒ (Deep Chart Cross-filtering & Morph Transitions):**
     - **Tương tác Slicer tới 100% Biểu đồ trên Trang:** Nhấn mạnh rằng Slicer (đặc trưng là Slicer Lọc Quốc gia / Địa bàn, Lọc Danh mục / Mặt hàng, Kỳ hạn, Nhóm khách...) **BẮT BUỘC phải liên kết trực tiếp tới TẤT CẢ BIỂU ĐỒ**.
     - **Cơ chế Lọc Đơn lẻ vs Toàn thể:** Khi bấm chọn 1 quốc gia/mặt hàng cụ thể $\rightarrow$ 100% biểu đồ, KPI cards và bảng số liệu trên trang lập tức chuyển sang hiển thị **chỉ số riêng của 1 mình đối tượng đó**; khi bỏ chọn/chọn All $\rightarrow$ hiển thị bức tranh toàn cảnh so sánh đối chiếu.
     - **Chuyển động Morph mượt mà (Smooth Morph Transitions):** Việc cập nhật biểu đồ không được giật cục (instant snap) mà bắt buộc có hiệu ứng chuyển động morph (animated data transitions / smooth tweening) giữa các trạng thái dữ liệu, tạo cảm giác chuyên nghiệp cấp cao.
     - **Tương tác Slicer & Bảng Dữ Liệu (Row Focus & Dimming):** Tự động highlight dòng thỏa mãn điều kiện và làm mờ nhẹ các dòng còn lại. Kèm nút **"Xóa bộ lọc" (1-Click Global Reset)** để hoàn tác tức thì.
     - **Phản hồi Thao tác Phi Gián Đoạn (Zero-Friction Glassmorphic Toast):** Tuyệt đối không dùng `alert(...)` trình duyệt. Mọi hành vi sao chép SQL hoặc thông báo tương tác phải dùng thẻ Toast kính mờ tự động ẩn sau 2,5s.
     - **Tự động Căn Chuẩn Kích Thước Biểu Đồ khi Đổi Trang (Chart Canvas Auto-Resize):** Khi chuyển tab/trang, mã JavaScript bắt buộc kích hoạt `chart.resize()` để các biểu đồ trong tab vừa mở không bao giờ bị méo tỉ lệ hoặc thu nhỏ kích thước.
   - **Hệ Màu Sắc Đa Dạng & Chuẩn Mực (Dựa trên Skill ui-ux-pro-max):**
     - Áp dụng triệt để nguyên lý thiết kế từ skill **`ui-ux-pro-max`**: Không giới hạn trong một tông màu đơn điệu mà sử dụng **hệ bảng màu sản phẩm đa dạng, giàu tương phản và ngữ nghĩa** (Semantic Data Palettes: Modern Tech, Cyber Teal, Vibrant Emerald, Coral Crimson, Electric Indigo, Warm Amber).
     - Đảm bảo tỷ lệ tương phản chuẩn WCAG 4.5:1, typography phân cấp rõ rệt (Plus Jakarta Sans / Inter + JetBrains Mono `tabular-nums`), hỗ trợ glassmorphism nhẹ nhàng và không dùng các thành phần trang trí sáo rỗng (Anti-AI-Slop).
   - **Đồng Bộ 100% Nội Dung & Căn Bệnh Cốt Lõi (Mandatory Conclusion & Core Diagnosis):** Web HTML phải đồng bộ 100% nội dung phân tích chuyên sâu với báo cáo trên chat, tuân thủ cùng mạch logic kết nối (Causal Bridging) và bắt buộc có đầy đủ phần chẩn đoán căn bệnh cốt lõi ở trang cuối cùng.
   - **Ngôn Ngữ Tinh Gọn, Chống Cringe & Thừa Thãi (Anti-Cringe & Anti-Buzzword):** Tuyệt đối không dùng các từ ngữ phô trương tính năng thừa thãi kiểu AI ("Slicer thông minh", "Hệ thống AI"). Nhãn gãy gọn: "Slicer: [Tên trường]". Toàn bộ nhãn, tiêu đề thẻ phải tự nhiên, chuẩn mực nghiệp vụ báo cáo cấp cao.

6. **Kỷ Luật Tinh Gọn Kỹ Thuật (Ponytail / Minimalist YAGNI) & Chuẩn Hóa Văn Phong (Watermark Remover):**
   - **Kỷ Luật Tinh Gọn Ponytail (The Minimalist / Lazy Senior Dev Ladder):**
     - **Tối giản mã nguồn & Diff ngắn nhất (YAGNI):** Giải pháp đơn giản nhất chạy được là giải pháp đúng nhất. Tuyệt đối không tạo abstraction dư thừa, không viết class/factory chỉ phục vụ một mục đích, không viết script cồng kềnh khi thư viện chuẩn hoặc one-liner giải quyết được.
     - **Tái sử dụng trước khi tạo mới (Code Reuse):** Tận dụng tối đa các helper, script mẫu và template chuẩn có sẵn trong repo thay vì viết lại từ đầu.
     - **Tối ưu hóa thời gian thực thi (Performance & Conciseness):** Trực diện vào mục tiêu, giải quyết tận gốc nguyên nhân kỹ thuật (root cause) thay vì chắp vá triệu chứng. Giữ mã ngắn gọn, hiệu năng cao, không boilerplate.
   - **Chuẩn Hóa Văn Phong Bằng Watermark Remover (`clean-user-facing-text`):**
     - **Triệt tiêu dấu vết AI (Zero AI Watermark / Anti-Cliché):** Loại bỏ hoàn toàn các câu từ mở đầu/kết thúc sáo rỗng kiểu AI ("Dưới đây là...", "Hy vọng phân tích này giúp ích...", "Là một Senior Analyst...", "Điều quan trọng cần lưu ý là..."), các cụm từ đệm vô nghĩa, và các tiêu đề trang trí rập khuôn.
     - **Nhịp điệu Hành chính Cấp cao (Executive Cadence & High Burstiness):** Hành văn tự nhiên, trực diện, đanh thép, độ dài câu biến hóa linh hoạt (câu ngắn xen kẽ câu dài), tập trung 100% vào logic kinh doanh, bằng chứng thực tế và hành động khắc phục cụ thể.
     - **Bảo toàn Tuyệt đối Dữ liệu & Sự thật:** Không bịa đặt chi tiết, giữ nguyên độ chính xác từng byte của số liệu thực chứng từ SQL, công thức, mã code và đường dẫn liên kết.
     - **Làm sạch ký tự Unicode cơ học (Layer A):** Tẩy sạch các ký tự điều khiển vô hình, zero-width spaces, confusable homoglyphs trên tất cả các file tài liệu và code bàn giao.

7. **BẮT BUỘC BỘ TỨ BÀN GIAO (MANDATORY QUADRUPLE DELIVERABLES: CHAT + EXCEL + HTML + POWER BI):**
   - Mọi đề bài phân tích dữ liệu từ người dùng, Agent **BẮT BUỘC phải đồng thời bàn giao trọn vẹn 4 sản phẩm**, không được thiếu bất kỳ thành phần nào:
     1. **Báo cáo Chẩn đoán trên Khung Chat (Diagnostic Chat Readout):** Đi theo đúng trình tự Định hướng $\rightarrow$ Câu lệnh SQL $\rightarrow$ Bảng kết quả Raw Data $\rightarrow$ Phân tích chuyên sâu đa chiều & nghịch lý.
     2. **Báo cáo Dashboard HTML Tương Tác Chống Cuộn Dọc (Paginated Interactive HTML):** Xuất bản file `.html` chuẩn Dark Slate/Midnight Navy, cấu trúc lật trang (slide/tab), cross-filtering sâu và phím tắt điều hướng. Cung cấp link `file:///...`.
     3. **Sổ Báo Cáo Excel Chuyên Nghiệp (Executive Excel Workbook):** Xuất bản file `.xlsx` (qua `xlsxwriter` / `openpyxl`) chứa các sheet dữ liệu sạch, Pivot Tables, công thức chuẩn xác và định dạng số chuyên nghiệp (VND/BRL/%, K/M formatting). Cung cấp link `file:///...`.
     4. **Báo Cáo Dashboard Power BI Desktop Tự Động (Automated Power BI PBIP):**
         - **Kiến trúc Data Mart CSV Siêu Nhẹ (Automated CSV Data Mart):** Tuyệt đối không bắt người dùng tự import thủ công. Agent tự chạy SQL xuất các bảng aggregated data mart ra thư mục `data_bi/` (vài chục KB, cực nhẹ và mở tức thì).
          - **Quy chuẩn Khung Vàng Bất Biến (Golden PBIP Blueprint):** Mọi dự án `.pbip` tạo mới bắt buộc kế thừa cấu trúc chuẩn đã nghiệm thu:
            + **CẤM sinh file `.pbit` thủ công bằng zip/python:** Tệp `.pbit` nén nhị phân thiếu luồng .NET Analysis Services sẽ gây văng app (`NullReferenceException`). Bắt buộc dùng định dạng chuẩn Microsoft Fabric: `.pbip` (PBIR + TMDL).
            + **Tệp định danh `.platform` & Theme:** Bắt buộc có tệp định danh `.platform` ở cả 2 thư mục `.Report` và `.SemanticModel`, kèm thư mục `StaticResources/` (chứa theme `Fluent2` & `ExecutiveMidnightSlate`).
            + **Phiên bản Schema Visual Container:** Sử dụng schema `2.9.0` (`.../visualContainer/2.9.0/schema.json`) cho toàn bộ visual containers để tránh lỗi cảnh báo schema unreachable khi offline.
            + **Mã Nguồn TMDL Chuẩn:** Bảng TMDL bắt buộc thụt lề bằng Tab (`\t`), định dạng UTF-8 (`Encoding=65001`), gán GUID `lineageTag` duy nhất cho từng cột và từng bảng, kèm thuộc tính `summarizeBy` chuẩn xác. Trong partition M, trỏ tới file CSV tuyệt đối bằng `Csv.Document(File.Contents("..."), ...)`.
            + **Dựng Sẵn 100% Visual Containers:** Mọi Visual Containers (`cardVisual`, `donutChart`, `barChart`, `lineClusteredColumnComboChart`, `tableEx`, `slicer`) phải dùng mã định danh 20 ký tự hex và dựng sẵn 100% trên canvas theo phong cách Modern Dark Slate / Midnight Navy.
          - **Cơ Chế Nạp Dữ Liệu 1-Click (1-Click Seamless Data Hydration):** Khi người dùng mở file `.pbip` trên Desktop, hệ thống hiện banner làm mới dữ liệu. Người dùng **chỉ cần bấm duy nhất nút [Làm mới ngay]** (hoặc `Alt + H + R`), toàn bộ dữ liệu tự động đổ đầy vào tất cả biểu đồ mà không cần thao tác Power Query hay import CSV thủ công.
          - **Kỷ Luật Chống Sót Mẫu Cũ & Thích Ứng Ngữ Cảnh Dữ Liệu 100% (Zero-Residual-Leak & Full Context Adaptation Law):**
            + **Cấm Tuyệt Đối Lặp Lại Tiêu Đề & Nhãn Cũ:** Mọi dự án kế thừa scaffold tuyệt đối không được để sót bất kỳ văn bản, tiêu đề, nhãn đo lường hay bộ lọc nào từ đề tài cũ. Bắt buộc thích ứng 100% nội dung với insight và tập dữ liệu hiện tại.
            + **Tiêu Chuẩn Cập Nhật Textbox PBIR (PBIR Textbox Binding):** Trong Fabric PBIR 2.9.0, chuỗi văn bản của Textbox visual nằm tại `visual.objects.general[0].properties.paragraphs[0].textRuns[0].value`. Khi render hoặc patch, mã sinh bắt buộc ghi trực tiếp vào đường dẫn này (không ghi vào khóa `visual.objects.textbox` vốn không được PBIR hỗ trợ).
            + **Thanh Lọc Toàn Diện Filters, DataPoints & Selectors (Clean Slate Purge):** Mọi visual khi chuyển giao dữ liệu mới bắt buộc phải purge toàn bộ các `filterConfig`, `dataPoint.selector`, và `lineStyles.selector` trỏ tới các bảng/cột của template cũ, thay thế bằng đúng danh mục cột của data mart mới.
            + **Kiểm Tra Dư Lượng Bắt Buộc (Mandatory Semantic Leak Scan):** Sau khi xuất bản và trước khi nghiệm thu, Agent BẮT BUỘC phải quét tự động toàn bộ file `.json` trong thư mục `.Report` để đối chiếu với danh sách từ khóa của các đề tài trước đó (như `thanh toán`, `trả góp`, `installment`, `freight`, `handover`, v.v.). Nếu phát hiện dù chỉ 1 từ khóa còn sót lại, quá trình xuất bản bị coi là thất bại và phải vá lỗi ngay lập tức.
          - **Kỷ luật Tiền kiểm Bắt buộc (Mandatory Pre-flight CLI Validation):** Sau khi sinh mã PBIP/PBIR, Agent BẮT BUỘC phải tự động chạy `powerbi-report-author validate` trên thư mục `.Report`. Phải đạt tuyệt đối `errorCount: 0` và `warningCount: 0` (`result: "succeeded"`). Nếu chưa đạt, CẤM thông báo hoàn thành hay mở ứng dụng Desktop cho người dùng.
          - **Tự động Mở & Chụp Ảnh Nghiệm Thu (Bridge Auto-Launch & Screenshot):** Sử dụng `powerbi-desktop open` để mở báo cáo kiểm tra trạng thái bridge `connected`, và chụp ảnh màn hình nghiệm thu (`powerbi-desktop screenshot <page-id>`) nhúng trực tiếp vào chat làm bằng chứng nghiệm thu trực quan cho người dùng.
          - **Quy Chuẩn Thiết Kế Power BI Fabric PBIP Chuyên Sâu (The Bulletproof PBIP Design Canon):**
            + **Lộ Toàn Bộ Nút Lọc Slicer (Horizontal Tile Ribbon Standard):** Slicer BẮT BUỘC phải dùng định dạng thanh nút bấm nằm ngang (`orientation: 1D`, `mode: 'Basic'`), hiển thị lộ toàn bộ các phân khúc/nút lọc ra ngoài canvas thay vì thu gọn trong dropdown. Kích thước chuẩn: chiều rộng trải dài toàn hàng (`w=1880, h=55` ở `y=60`).
            + **Triệt Tiêu Hoàn Toàn Chữ Đơn Vị Địa Phương Hóa ("nghìn", "triệu") - Zero Locale Units:**
              * Mọi thẻ KPI (`cardVisual`), tâm biểu đồ Donut (`donutChart`), và nhãn trục BẮT BUỘC đặt cứng thuộc tính `"displayUnits": 1D` (None) trong JSON schema.
              * Định dạng số nguyên bằng `#,##0`, tiền tệ bằng `$#,##0.00`, tỷ lệ bằng `0.00%`.
              * Đối với biểu đồ Donut: nhãn dữ liệu BẮT BUỘC dùng `"labelStyle": "Category, percent of total"`, không dùng raw count có nguy cơ bị Power BI tự động thêm "nghìn" hoặc "triệu" trên máy tính người dùng.
            + **Kỷ Luật Tương Tác Chéo & Mô Hình Quan Hệ Đa Bảng (Bidirectional Cross-Filtering & Multi-Table Relationships):**
              * Các visual trên cùng một trang tối thiểu truy vấn từ một bảng Fact trung tâm; **nếu có 2 hay nhiều bảng dữ liệu CSV liên quan thì KHUYẾN KHÍCH thiết lập quan hệ (Relationships / Star Schema) trong TMDL** để trình bày đa chiều trên cùng một canvas.
              * Tuyệt đối tránh các bảng "hòn đảo độc lập" (không có liên kết logic/quan hệ). Khi tương tác (chọn dòng trên Bảng, lát cắt Donut, cột Bar chart, điểm Combo chart, hoặc Slicer) $\rightarrow$ **100% visuals liên quan trên trang PHẢI đồng bộ lọc/highlight** theo ngữ cảnh đó.
            + **Kiểm Soát Tương Phản & Hệ Màu Sắc Toàn Diện Theo `ui-ux-pro-max` (Global Contrast & Dynamic State Visibility):**
              * Bắt buộc kiểm tra mọi thành phần (văn bản, nhãn trục, data label, viền card, thanh bar, lát cắt) luôn hiển thị rõ ràng, tương phản sắc nét chuẩn WCAG (tối thiểu 4.5:1), không bị chìm nền hoặc mờ chữ.
              * Áp dụng hệ màu chuyên nghiệp từ skill **`ui-ux-pro-max`** (Semantic Palettes: Modern Tech, Midnight Slate, Cyber Teal, Vibrant Emerald, Coral Crimson, Warm Amber).
              * Màu sắc tổng thể phải đảm bảo tính thẩm mỹ cao và **rõ nét ở cả 2 trạng thái: khi không tương tác và khi đang tương tác/highlight/dimmed một thành phần cụ thể** (trạng thái bị làm mờ vẫn phải đọc được ngữ cảnh, trạng thái highlight phải nổi bật dứt khoát).
            + **Độ Khớp Tuyệt Đối 100% Số Liệu Thực Chứng (100% Strict Data Consistency):**
              * Toàn bộ số liệu trên Power BI (thẻ KPI, bảng, biểu đồ) **BẮT BUỘC phải chuẩn xác và khớp tuyệt đối 100% với số liệu báo cáo trong đoạn chat và kết quả thực tế từ SQL**. Tuyệt đối không để xảy ra sai lệch số liệu, không dùng số giả định hay làm tròn sai bản chất.
            + **Khung Lưới Vàng 13 Visual Containers Bất Biến & Bắt Buộc Kiểm Tra Tọa Độ Tự Động (Mandatory 13-Container Golden Grid & Spatial Audit Assertion):**
              * **Căn nguyên lỗi góc phải dưới bị trống:** Xuất phát từ việc các script sinh mã PBIP (`build_..._pbip.py`) kế thừa danh sách visual từ scaffold cũ nhưng bị sót visual container `a1000000000000000009` (Table 2 ở `x=970, y=630, w=930, h=430`). Trong khi đó, lệnh `powerbi-report-author validate` CHỈ kiểm tra cú pháp JSON schema hợp lệ, hoàn toàn không kiểm tra độ phủ không gian hình học (spatial layout).
              * **Bố cục Chuẩn 13 Containers (Canvas 1920x1080):**
                1. `Header Textbox`: `x=20, y=10, w=1880, h=50`
                2. `Slicer Ribbon (Tile/Horizontal)`: `x=20, y=68, w=1880, h=48`
                3. `5 Thẻ KPI Cards`: `y=124, h=95, w=368` tại `x = 20, 396, 772, 1148, 1524` (Khóa cứng `"labelDisplayUnits": "'1'"` chống lỗi "nghìn/triệu").
                4. `Hàng Giữa (Mid-row, y=228, h=392, w=930)`: Visual Trái `a6` (`x=20`) & Visual Phải `a7` (`x=970`).
                5. `Hàng Đáy (Bottom-row, y=630, h=430, w=930)`: **BẮT BUỘC ĐỦ CẢ 2 VISUALS ĐỐI XỨNG**:
                   - Đáy Trái `a8` (`x=20, y=630, w=930, h=430`): Bảng dữ liệu / Matrix 1.
                   - Đáy Phải `a9` (`x=970, y=630, w=930, h=430`): Bảng dữ liệu / Matrix 2 / Chi tiết nhân quả. Tuyệt đối KHÔNG ĐƯỢC BỎ TRỐNG.
              * **Kỷ Luật Kiểm Tra Tọa Độ Tự Động Trong Script Python (Canvas Spatial Assertion):**
                Mọi script sinh mã PBIP bắt buộc phải chứa đoạn code tự động kiểm tra bounding box trước khi xuất bản:
                ```python
                # Canvas Grid & Bounding Box Spatial Audit
                assert any(v['position']['x'] >= 900 and v['position']['y'] >= 600 for v in page_visuals), \
                    "LỖI FATAL: Góc phải bên dưới (x=970, y=630) đang bị bỏ trống! Phải bổ sung visual container thứ 13!"
                assert len(page_visuals) >= 13, f"LỖI FATAL: Báo cáo chỉ có {len(page_visuals)}/13 visual containers!"
                ```
            + **Tiêu Chuẩn 100% Tiếng Anh & IN HOA TIÊU ĐỀ (100% English & ALL CAPS Standard):**
              * Toàn bộ tiêu đề biểu đồ (`FIGURE X.X - ...`), tên thẻ KPI, tên trục BẮT BUỘC viết bằng tiếng Anh chuyên nghiệp và **VIẾT IN HOA TOÀN BỘ (ALL CAPS)**.
            + **Kỷ Luật Tính Toán & Hàm Tổng Hợp (Mathematical Integrity):**
              * Tuyệt đối không SUM các cột tỷ lệ (%), late rate, hoặc median spend / median days. Dùng `DistinctCount` cho đơn hàng, `Sum` cho GMV, `Average` cho điểm số và tỷ lệ trễ.

8. **Kỷ Luật Thực Thi Đơn Vòng Tự Trị (One-Shot Autonomous Execution - Tuyệt Đối Không Dừng Hỏi Giữa Chừng):**
   - **Thực Hiện Xuyên Suốt Toàn Bộ Các Tầng (Continuous Multi-Tier Execution):** Khi nhận đề bài phân tích, Agent **BẮT BUỘC phải tự động chạy xuyên suốt từ Tầng 1 đến Tầng cuối cùng (Định vị Căn bệnh & Playbook)**, đồng thời tự động xuất bản trọn vẹn Bộ Tứ Sản Phẩm (Chat + Excel + HTML + PBIP).
   - **CẤM Dừng Ngang Hàng Để Hỏi Ý Kiến:** Tuyệt đối KHÔNG dừng lại ở Tầng 1 hay Tầng 2 để hỏi người dùng kiểu "bạn có muốn phân tích tiếp không" hay "bạn có muốn xuất file không". Mọi phân tích phải được hoàn thành trọn vẹn A-Z trong 1 lượt phản hồi duy nhất.

9. **Kỷ Luật Về Đường Dẫn Vật Lý & Trực Quan Hóa Khung Chat (The Interactive Generative UI Canon):**
   - **Đường Dẫn Vật Lý Thực Tế Ổ D (Physical Drive D Precedence):**
     * Thư mục gốc dự án thực tế nằm tại: `D:\TaiLieuDaiHoc\Năm III\CSDL`.
     * Toàn bộ các đường link tài liệu, file bàn giao (`.pbip`, `.xlsx`, `.html`, `.csv`, folder) gửi cho người dùng BẮT BUỘC phải sử dụng đường dẫn tuyệt đối ổ `D:` chuẩn định dạng clickable: `[Tên file](file:///D:/TaiLieuDaiHoc/N%C4%83m%20III/CSDL/...)`. Tuyệt đối không dùng đường dẫn `c:\Users\ASUS\Documents\...` khi xuất link bàn giao để tránh lỗi Windows File Explorer.
   - **Kỷ Luật Trực Quan Hóa Khung Chat — Tương Tác Sống Động (Zero Static Images & Zero "Preview Unavailable"):**
     * **CẤM TUYỆT ĐỐI dùng cú pháp Markdown Image với đường dẫn file cục bộ `![...](file:///...)`:** Trình duyệt / Electron Webview của chat chặn hoàn toàn giao thức `file:///` đối với thẻ ảnh `<img>` cục bộ do chính sách bảo mật CSP (Content Security Policy), dẫn đến lỗi sập ảnh hiển thị dòng chữ *"Preview unavailable"*.
     * **CẤM TUYỆT ĐỐI in ra các khối mã nguồn HTML/CSS/JS thô (` ```html ... ``` `)** dưới danh nghĩa "trực quan hóa" trong nội dung chat.
     * **QUY CHUẨN XÂY DỰNG INLINE INTERACTIVE HTML/SVG WIDGET (The Living Generative UI Standard):**
       1. Viết code HTML/SVG/JavaScript tự trị hoàn toàn (không gọi thư viện CDN bên ngoài để tránh vi phạm CSP). Tích hợp sẵn CSS chuyển động, hover tooltip, và nút bấm switch góc nhìn (% vs số lượng).
       2. Lưu file widget `.html` trong thư mục Artifact Directory của phiên chat (`<appDataDir>\brain\<conversation-id>\widget_x.html`).
       3. Nhúng trực tiếp vào nội dung chat bằng thẻ native:
          `<agent-embed src="file:///<appDataDir>/brain/<conversation-id>/widget_x.html"></agent-embed>`
       4. Biểu đồ hiển thị trực quan ngay lập tức, hỗ trợ rê chuột (hover tooltip) đọc số liệu chi tiết, bấm nút lọc/đổi chế độ mượt mà, tự thích ứng 100% Dark/Light theme, không vỡ hạt và không bao giờ bị lỗi "Preview unavailable"!

