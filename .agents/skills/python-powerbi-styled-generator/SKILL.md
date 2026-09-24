---
name: python-powerbi-styled-generator
description: End-to-end automation workflow to generate fully styled, executive-grade Power BI Template files (.pbit) using Python, adopting the Midnight Navy aesthetic (#09124F, Pill headers, Rounded Rectangles).
---

# Python Power BI Styled Generator (.pbit Mandatory)

> [!IMPORTANT]
> **CRITICAL RULE:** Whenever the user requests to generate, create, or export Power BI dashboards/reports, you **MUST ALWAYS export as a `.pbit` file (Power BI Template)**. Do NOT export as `.pbip` folders, because the user's Power BI environment specifically requires single-file `.pbit` templates.

---

## 1. Visual & Aesthetic Architecture (Learned from User's Dashboards)

Every `.pbit` layout MUST strictly follow this executive dark theme aesthetic:

### A. Canvas & Page Background
- Canvas size: `1280 x 720` (16:9).
- Section background MUST be set to **Deep Navy Midnight Blue (`#09124F`)** with **0% transparency (`0D`)**:
```json
"background": [
  {
    "properties": {
      "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#09124F'"}}}}},
      "transparency": {"expr": {"Literal": {"Value": "0D"}}}
    }
  }
],
"outspace": [
  {
    "properties": {
      "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#09124F'"}}}}}
    }
  }
]
```

### B. Header & Navigation Pills
- **Header Container:** Shape `rectangleRounded` `(h: ~74px)` with fill `#0d1b54`, border `#1e295f`, and drop shadow.
- **Title Text:** Font `Calibri`, `22pt`, Bold, Color `#ffffff`. Subtitle: `10-12pt`, Color `#41a4ff`.
- **Navigation Pills:** Top right pills using shape `pill` `(h: ~50px)`. Active pill filled with `#118DFF`, inactive pill filled with `#0d1b54` and outline `#41a4ff`.

### C. KPI Cards Section
- Height `~88px`, balanced horizontally across 1280px canvas (e.g. 4 cards of `~298px` width each).
- **Container Shape:** Shape `rectangleRounded` placed behind each card (`z < card.z`) with fill `#0d1b54`, border `#1e295f`, and drop shadow.
- **Card Visual:**
  - `background.transparency: 100D` (100% transparent).
  - `categoryLabels.show: false` (hide default category label).
  - `title.show: true`, font `Calibri`, `11pt`, color `#ffffff`, aligned `center`.
  - Values: Primary metrics in `#41a4ff`, Gold `#fbbf24` for #1 seller, Emerald `#34d399` for averages, White `#ffffff` for volume.

### D. Main Visuals (Charts & Tables)
- **Container Shapes:** Place a `rectangleRounded` shape behind every chart/table with fill `#0d1b54`, border `#1e295f`, drop shadow.
- **Data Charts:**
  - `background.transparency: 100D`.
  - Category and Value axis labels in `Calibri`, white `#ffffff` or light slate `#94a3b8`.
  - Value axis titles hidden, subtle gridlines `#1e295f`.
  - Vibrant data colors: Electric Blue `#118DFF`, Sky Blue `#38bdf8`, Gold `#fbbf24`.

---

## 2. Mandatory .pbit File Structure & Packaging

A `.pbit` file is a ZIP archive containing 6 specific parts:

```
<ReportName>.pbit (ZIP archive)
│
├── [Content_Types].xml       (UTF-8 XML declaring MIME types)
├── Version                   (UTF-16LE string: "1.28")  <-- CRITICAL!
├── Settings                  (UTF-16LE JSON)
├── Metadata                  (UTF-16LE JSON)
├── DataModelSchema           (UTF-16LE JSON - Full TMSL model definition)
└── Report/Layout             (UTF-16LE JSON - Canvas, sections, visuals)
```

### Critical Packaging Requirements:
1. **`Version` file:** MUST be explicitly set to `"1\x00.\x002\x008\x00".encode('utf-8')` (UTF-16LE representation of `1.28`). If this is wrong, Power BI Desktop will reject the file!
2. **Encoding:** `DataModelSchema`, `Report/Layout`, `Settings`, and `Metadata` MUST be encoded in `utf-16le`.
3. **DataModelSchema:** Uses standard TMSL schema. Data is embedded via Power Query M `#table` functions in table partitions so the template loads with instant data.

---

## 3. Standard Python Generator Boilerplate

```python
import json
import zipfile
import os

def export_styled_pbit(output_path, model_schema, report_layout):
    layout_bytes = json.dumps(report_layout, ensure_ascii=False).encode('utf-16le')
    schema_bytes = json.dumps(model_schema, ensure_ascii=False).encode('utf-16le')

    content_types = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="xml" ContentType="application/xml" />
  <Override PartName="/Report/Layout" ContentType="application/json" />
  <Override PartName="/DataModelSchema" ContentType="application/json" />
  <Override PartName="/Settings" ContentType="application/json" />
  <Override PartName="/Metadata" ContentType="application/json" />
  <Override PartName="/Version" ContentType="application/json" />
</Types>"""

    settings = json.dumps({"Version": 4, "ReportSettings": {}, "QueriesSettings": {"Version": "2.157.1354.0"}}).encode('utf-16le')
    metadata = json.dumps({"Version": 5, "AutoCreatedRelationships": []}).encode('utf-16le')
    version = "1\x00.\x002\x008\x00".encode('utf-8')  # 1.28 in UTF-16LE

    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types.encode('utf-8'))
        z.writestr('Version', version)
        z.writestr('Settings', settings)
        z.writestr('Metadata', metadata)
        z.writestr('DataModelSchema', schema_bytes)
        z.writestr('Report/Layout', layout_bytes)

    print(f"Exported .pbit successfully to: {output_path}")
```
