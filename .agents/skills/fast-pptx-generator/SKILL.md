---
name: fast-pptx-generator
description: Fast executive PowerPoint (.pptx) generator using native in-memory python-pptx engine. Produces polished 16:9 executive-ready decks in under 2 seconds without slow CLI batch overhead or screenshot loops.
---

# Fast PPTX Generator Skill

Kỹ năng tạo bài thuyết trình PowerPoint (`.pptx`) siêu tốc (One-Shot In-Memory Execution) dành cho dự án phân tích dữ liệu và báo cáo kinh doanh.

## 🎯 Khi Nào Kích Hoạt?
- Người dùng yêu cầu: *"tạo slide PowerPoint"*, *"xuất file pptx"*, *"làm slide thuyết trình"*, *"tạo deck nhanh"*, hoặc gọi tên skill `fast-pptx-generator`.
- Cần xuất file PowerPoint chất lượng cao ngay lập tức mà không phải chờ đợi qua các vòng lặp CLI hay chụp ảnh kiểm thử kéo dài hàng phút.

## ⚡ Triết Lý Kỹ Thuật (Architecture & Performance)
1. **Thuần Python Trong Bộ Nhớ (`python-pptx`):**
   - Loại bỏ hoàn toàn tầng trung gian CLI (`officecli`), không ghi file batch JSON, không phụ thuộc PowerShell resident process.
   - Toàn bộ 7-10 slide được khởi tạo, tính toán tọa độ, nhúng dữ liệu và định kiểu trong RAM chỉ mất **1-2 giây**.
2. **Quy Chuẩn Thiết Kế Điều Hành (Midnight Executive Theme):**
   - **Tỉ lệ Canvas:** 16:9 chuẩn mực (`13.333 in` x `7.5 in`).
   - **Bảng màu:**
     * Nền chính: `#0B111E` (Dark Slate)
     * Thẻ/Container: `#162032` (Deep Navy) & Cảnh báo `#241219` (Dark Crimson)
     * Tiêu đề: White `#FFFFFF` (Font Georgia) & Phụ đề Sky Blue `#38BDF8` (Font Calibri)
     * Điểm nhấn số liệu: Amber `#F59E0B`, Emerald `#10B981`, Rose `#EF4444`, Sky Blue `#38BDF8`
3. **Bảng Số Liệu Chuẩn Trực Quan (Zero Formatting Bugs):**
   - Tự động áp dụng kích thước chữ `10pt`, đệm ô `0.05 in` (chống rớt dòng/overflow).
   - Zebra striping tự động (hàng chẵn `#111927`, hàng lẻ `#0F172A`).
   - Căn lề thông minh: Hạng/Đánh giá căn giữa, Số liệu căn phải, Văn bản căn trái.
   - Nhận diện hàng cảnh báo để đổi màu chữ đỏ nổi bật.
4. **Speaker Notes Tự Động:**
   - Mỗi slide nội dung tự động nhúng Speaker Notes chi tiết hỗ trợ người thuyết trình.

## 🚀 Cách Sử Dụng Trong Script
Sử dụng module lõi có sẵn tại: `c:/Users/ASUS/Documents/Năm III/CSDL/.agents/skills/fast-pptx-generator/scripts/fast_deck.py`

```python
import sys
sys.path.append(r"c:\Users\ASUS\Documents\Năm III\CSDL\.agents\skills\fast-pptx-generator\scripts")
from fast_deck import FastDeck, Theme
from pptx.util import Inches, Pt

deck = FastDeck()

# 1. Slide Tiêu đề
s1 = deck.add_blank_slide()
deck.add_header(s1, "TIÊU ĐỀ BÁO CÁO CHIẾN LƯỢC", "Phụ đề tóm tắt bối cảnh và insight chính")

# 2. Slide Bảng dữ liệu
s2 = deck.add_blank_slide()
deck.add_header(s2, "BẢNG VÀNG TOP DOANH THU", "Chi tiết các sản phẩm sinh lời lớn nhất")
headers = ["Hạng", "Mã SKU", "Ngành Hàng", "Số Đơn", "Lượng Bán", "Doanh Thu", "Giá TB", "Đánh Giá"]
rows = [
    ["#1", "bb50f2e2...", "Sức khỏe sắc đẹp", "186", "194", "63.560.00", "327.63", "4.24 ★"],
    # ...
]
deck.add_table(s2, Inches(0.6), Inches(1.5), Inches(12.13), Inches(5.2), headers, rows)
deck.add_notes(s2, "Kịch bản thuyết trình cho người trình bày...")

# 3. Lưu file
deck.save(r"D:\TaiLieuDaiHoc\Năm III\CSDL\Ten_File.pptx")
```
