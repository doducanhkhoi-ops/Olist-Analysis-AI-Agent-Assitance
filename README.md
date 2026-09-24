# Antigravity & Agentic Data Analytics System

Bộ khung tư duy phân tích dữ liệu chẩn đoán (Diagnostic Analytics Engine), hệ thống quy chuẩn vận hành (Rules), kỹ năng chuyên sâu (Skills) và MCP kết nối cho trợ lý AI Antigravity.

---

## 1. Cấu Trúc Hệ Thống

```text
├── .agents/
│   ├── plugins/
│   │   └── powerbi-mcp/          # Cấu hình plugin kết nối Power BI Modeling MCP
│   ├── rules/
│   │   ├── AnalyticFlow.md       # Quy chuẩn tư duy chẩn đoán 6 bước và kỷ luật phân tích
│   │   └── data-analyst-diagnostic-mindset.md # Quy chuẩn hiển thị trình tự phân tích trên chat
│   └── skills/                   # 20 bộ kỹ năng chuyên ngành cho AI Data Analyst
│       ├── ai-data-analysis-orchestration/
│       ├── olist-strategic-analytics/
│       ├── data-analyst/
│       ├── sql-analysis/
│       ├── sql-optimization-patterns/
│       ├── database-design/
│       ├── data-qa/
│       ├── data-storytelling/
│       ├── excel-visualization/
│       ├── powerbi-report-authoring/
│       ├── powerbi-report-design/
│       ├── semantic-model-authoring/
│       ├── python-powerbi-styled-generator/
│       ├── fast-pptx-generator/
│       ├── hallmark/
│       ├── dbhub/
│       ├── churn-prevention/
│       ├── dashboard-spec/
│       ├── executive-memo/
│       └── financial-modeling/
├── AnalyticFlow.md               # Bản đặc tả quy chuẩn tư duy chẩn đoán gốc
└── GEMINI.md                     # Quy tắc hệ thống Antigravity cho phân tích dữ liệu
```

---

## 2. Quy Chuẩn Tư Duy Chẩn Đoán 6 Bước (Diagnostic Mindset)

Mọi phân tích dữ liệu đều tuân theo quy trình 6 bước:

```text
[1. Triệu chứng bề mặt]
         │
         ▼
[2. Giả thuyết đa chiều (Cung - Cầu - Vận hành)]
         │
         ▼
[3. Cắt lớp dữ liệu (Thực tế vs ảo, địa lý, ma trận)]
         │
         ▼
[4. Giải mã nghịch lý kinh doanh]
         │
         ▼
[5. Xác định căn bệnh cốt lõi]
         │
         ▼
[6. Kịch bản khắc phục và hành động]
```

### Kỷ luật phân tích cốt lõi:
1. **Hợp đồng Grain:** Không tính toán tổng tiền trên các bảng nối ba (`orders` x `items` x `payments`). Gộp trước (Aggregate), nối sau (Join).
2. **Kiểm định khóa:** Xác thực tính duy nhất của khóa ngoại trước khi phân tích. Không giả định khóa luôn hợp lệ.
3. **Kiểm soát biến nhiễu:** Khi so sánh hai nhóm, bắt buộc kiểm soát biến số lượng hàng, giá trị đơn, địa lý và mùa vụ bằng phương pháp chuẩn hóa trực tiếp.
4. **Trực quan hóa tức thì:** Trình bày kết quả theo chu trình: Mục tiêu định hướng -> Mã SQL -> Bảng dữ liệu thực tế -> Biểu đồ inline widget tương tác -> Phân tích kết luận.

---

## 3. Danh Mục Kỹ Năng (Skills)

| Kỹ năng | Vai trò |
| :--- | :--- |
| **`ai-data-analysis-orchestration`** | Điều phối toàn diện chu trình phân tích: SQL, Excel, HTML và Power BI PBIP. |
| **`olist-strategic-analytics`** | Khung phân tích thương mại điện tử chuyên sâu (Mô hình đa vùng, SLA vận chuyển, RFM, bài toán duy trì). |
| **`data-analyst`** | Quy trình phân tích dữ liệu đầu-cuối: Định nghĩa chỉ số, QA dữ liệu, Cohort và Experiment. |
| **`sql-analysis`** | Kỹ thuật viết truy vấn SQL phân tích doanh thu, hành vi, tỷ lệ duy trì và phễu chuyển đổi. |
| **`sql-optimization-patterns`** | Chẩn đoán và tối ưu hiệu năng truy vấn SQL với Execution Plan. |
| **`database-design`** | Thiết kế lược đồ dữ liệu, chiến lược đánh chỉ mục (Index) và chuẩn hóa dữ liệu. |
| **`data-qa`** | Kiểm toán chất lượng dữ liệu: Trùng lặp, giá trị rỗng, ngoại lai và xung đột dữ liệu. |
| **`data-storytelling`** | Chuyển đổi dữ liệu và phân tích thành câu chuyện trực quan phục vụ ra quyết định. |
| **`excel-visualization`** | Tự động hóa bảng tính Excel, tạo dashboard tài chính và biểu đồ với Python (`xlsxwriter`, `openpyxl`). |
| **`powerbi-report-authoring`** | Xây dựng và tinh chỉnh báo cáo Power BI định dạng PBIR / PBIP theo schema chuẩn. |
| **`powerbi-report-design`** | Thiết kế bố cục, bảng màu và trải nghiệm người dùng cho báo cáo Power BI. |
| **`semantic-model-authoring`** | Thiết kế mô hình dữ liệu ngữ nghĩa, công thức DAX và định dạng TMDL. |
| **`python-powerbi-styled-generator`** | Tự động tạo Power BI template và áp dụng theme chuẩn. |
| **`fast-pptx-generator`** | Tạo slide thuyết trình tự động định dạng 16:9 với `python-pptx`. |
| **`hallmark`** | Tiêu chuẩn thiết kế giao diện web, dashboard HTML sạch, chống khuôn mẫu AI. |
| **`dbhub`** | Khai thác cơ sở dữ liệu qua DBHub MCP. |
| **`churn-prevention`** | Chiến lược giữ chân khách hàng và giảm tỷ lệ rời bỏ. |
| **`dashboard-spec`** | Đặc tả kỹ thuật và tiêu chuẩn nghiệp vụ cho dashboard điều hành. |
| **`executive-memo`** | Định dạng báo cáo tóm tắt dành cho cấp quản lý. |
| **`financial-modeling`** | Xây dựng mô hình tài chính, unit economics và dự báo kinh doanh. |

---

## 4. Cấu Hình MCP & Plugins

* **Power BI Modeling MCP:** Cung cấp kết nối trực tiếp với mô hình Power BI qua tệp cấu hình `.agents/plugins/powerbi-mcp/mcp_config.json`.
* **Cơ sở dữ liệu hỗ trợ:** MySQL, SQLite và các hệ quản trị CSDL quan hệ thông qua các bộ tool MCP tương thích.
