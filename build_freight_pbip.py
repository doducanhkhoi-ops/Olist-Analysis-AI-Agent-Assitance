import os
import shutil
import json
import uuid

base_dir = r"c:\Users\ASUS\Documents\Năm III\CSDL"
reports_dir = os.path.join(base_dir, "reports")
data_bi_dir = os.path.join(base_dir, "data_bi")
proj_name = "Freight_Deadweight_Diagnostic"

target_pbip = os.path.join(reports_dir, f"{proj_name}.pbip")
target_rep = os.path.join(reports_dir, f"{proj_name}.Report")
target_sm = os.path.join(reports_dir, f"{proj_name}.SemanticModel")
ref_rep = os.path.join(reports_dir, "Payment_Pro.Report")

if os.path.exists(target_pbip): os.remove(target_pbip)
if os.path.exists(target_rep): shutil.rmtree(target_rep)
if os.path.exists(target_sm): shutil.rmtree(target_sm)

os.makedirs(target_rep, exist_ok=True)
os.makedirs(target_sm, exist_ok=True)

# 1. PBIP file
pbip_data = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
    "version": "1.0",
    "artifacts": [{"report": {"path": f"{proj_name}.Report"}}],
    "settings": {"enableAutoRecovery": True}
}
with open(target_pbip, "w", encoding="utf-8") as f:
    json.dump(pbip_data, f, indent=2)

# Copy .platform metadata
ref_platform = os.path.join(ref_rep, ".platform")
if os.path.exists(ref_platform):
    shutil.copy(ref_platform, os.path.join(target_rep, ".platform"))
    shutil.copy(ref_platform, os.path.join(target_sm, ".platform"))

# 2. SemanticModel
with open(os.path.join(target_sm, "definition.pbism"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
        "version": "4.2",
        "settings": {}
    }, f, indent=2)

sm_def = os.path.join(target_sm, "definition")
os.makedirs(sm_def, exist_ok=True)
sm_tables = os.path.join(sm_def, "tables")
os.makedirs(sm_tables, exist_ok=True)
sm_cultures = os.path.join(sm_def, "cultures")
os.makedirs(sm_cultures, exist_ok=True)

with open(os.path.join(sm_def, "database.tmdl"), "w", encoding="utf-8") as f:
    f.write("database\n\tcompatibilityLevel: 1606\n")

with open(os.path.join(sm_cultures, "vi-VN.tmdl"), "w", encoding="utf-8") as f:
    f.write("cultureInfo vi-VN\n")

with open(os.path.join(sm_def, "model.tmdl"), "w", encoding="utf-8") as f:
    f.write("""model Model
\tculture: vi-VN
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: en-US
\tvalueFilterBehavior: independent
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 1

annotation PBI_QueryOrder = ["fact_freight_price_tier","fact_freight_burden_tiers","fact_category_freight_deadweight","fact_freight_trade_corridor"]

annotation PBI_ProTooling = ["DevMode"]

ref table fact_freight_price_tier
ref table fact_freight_burden_tiers
ref table fact_category_freight_deadweight
ref table fact_freight_trade_corridor

ref cultureInfo vi-VN
""")

def create_table_tmdl(table_name, columns, csv_file):
    lines = ["table " + table_name, "\tlineageTag: " + str(uuid.uuid4()), ""]
    m_transform_list = []
    for c_name, d_type, f_str, m_type in columns:
        lines.append("\tcolumn " + c_name)
        lines.append("\t\tdataType: " + d_type)
        if f_str:
            lines.append("\t\tformatString: " + f_str)
        lines.append("\t\tlineageTag: " + str(uuid.uuid4()))
        lines.append("\t\tsummarizeBy: " + ("none" if d_type == "string" else "sum"))
        lines.append("\t\tsourceColumn: " + c_name)
        lines.append("\t\tannotation SummarizationSetBy = Automatic")
        if d_type == "double":
            lines.append('\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}')
        lines.append("")
        m_transform_list.append('{"' + c_name + '", ' + m_type + '}')
    
    num_cols = len(columns)
    csv_abs_path = os.path.join(data_bi_dir, csv_file).replace('\\', '\\\\')
    lines.append("\tpartition " + table_name + " = m")
    lines.append("\t\tmode: import")
    lines.append("\t\tsource =")
    lines.append("\t\t\t\tlet")
    lines.append('\t\t\t\t    Nguon = Csv.Document(File.Contents("' + csv_abs_path + '"),[Delimiter=",", Columns=' + str(num_cols) + ', Encoding=65001, QuoteStyle=QuoteStyle.None]),')
    lines.append('\t\t\t\t    #"Tieu de Duoc Tang cap" = Table.PromoteHeaders(Nguon, [PromoteAllScalars=true]),')
    lines.append('\t\t\t\t    #"Thay doi Loai" = Table.TransformColumnTypes(#"Tieu de Duoc Tang cap",{' + ', '.join(m_transform_list) + '})')
    lines.append("\t\t\t\tin")
    lines.append('\t\t\t\t    #"Thay doi Loai"')
    lines.append("")
    lines.append("\tannotation PBI_ResultType = Table")
    lines.append("")
    
    with open(os.path.join(sm_tables, table_name + ".tmdl"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# 1. fact_freight_price_tier
create_table_tmdl("fact_freight_price_tier", [
    ("delivery_quadrant_id", "string", None, "type text"),
    ("delivery_quadrant", "string", None, "type text"),
    ("total_orders", "int64", "#,##0", "Int64.Type"),
    ("order_share_pct", "double", None, "type number"),
    ("total_gmv", "double", "#,##0.00", "type number"),
    ("aov", "double", "#,##0.00", "type number"),
    ("avg_review_score", "double", None, "type number"),
    ("one_star_pct", "double", None, "type number"),
    ("five_star_pct", "double", None, "type number"),
    ("avg_seller_handling_days", "double", None, "type number"),
    ("avg_carrier_transit_days", "double", None, "type number"),
    ("avg_total_delivery_days", "double", None, "type number"),
    ("avg_sla_buffer_days", "double", None, "type number")
], "fact_freight_price_tier.csv")

# 2. fact_freight_burden_tiers
create_table_tmdl("fact_freight_burden_tiers", [
    ("state", "string", None, "type text"),
    ("total_orders", "int64", "#,##0", "Int64.Type"),
    ("carrier_breakdown_orders", "int64", "#,##0", "Int64.Type"),
    ("carrier_breakdown_pct", "double", None, "type number"),
    ("avg_transit_days", "double", None, "type number"),
    ("avg_transit_days_delayed", "double", None, "type number"),
    ("avg_review_score", "double", None, "type number")
], "fact_freight_burden_tiers.csv")

# 3. fact_category_freight_deadweight
create_table_tmdl("fact_category_freight_deadweight", [
    ("category_name", "string", None, "type text"),
    ("total_orders", "int64", "#,##0", "Int64.Type"),
    ("seller_overdue_pct", "double", None, "type number"),
    ("avg_seller_handling_days", "double", None, "type number"),
    ("avg_review_score", "double", None, "type number")
], "fact_category_freight_deadweight.csv")

# 4. fact_freight_trade_corridor
create_table_tmdl("fact_freight_trade_corridor", [
    ("metric_name", "string", None, "type text"),
    ("metric_value", "double", None, "type number"),
    ("unit", "string", None, "type text"),
    ("formatted", "string", None, "type text"),
    ("note", "string", None, "type text")
], "fact_freight_trade_corridor.csv")

# 3. Report Definition
with open(os.path.join(target_rep, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byPath": {"path": f"../{proj_name}.SemanticModel"}}
    }, f, indent=2)

rep_def = os.path.join(target_rep, "definition")
os.makedirs(rep_def, exist_ok=True)

with open(os.path.join(rep_def, "version.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
        "version": "2.0.0"
    }, f, indent=2)

if os.path.exists(os.path.join(ref_rep, "StaticResources")):
    shutil.copytree(os.path.join(ref_rep, "StaticResources"), os.path.join(target_rep, "StaticResources"))

with open(os.path.join(ref_rep, "definition", "report.json"), "r", encoding="utf-8") as f:
    report_json = json.load(f)
with open(os.path.join(rep_def, "report.json"), "w", encoding="utf-8") as f:
    json.dump(report_json, f, indent=2)

page_id = "page_handover_01"
rep_pages = os.path.join(rep_def, "pages")
os.makedirs(rep_pages, exist_ok=True)
with open(os.path.join(rep_pages, "pages.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": [page_id],
        "activePageName": page_id
    }, f, indent=2)

page_dir = os.path.join(rep_pages, page_id)
os.makedirs(page_dir, exist_ok=True)
visuals_dir = os.path.join(page_dir, "visuals")
os.makedirs(visuals_dir, exist_ok=True)

with open(os.path.join(page_dir, "page.json"), "w", encoding="utf-8") as f:
    json.dump({
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": page_id,
        "displayName": "Chẩn Đoán Bàn Giao Vận Tải",
        "displayOption": "FitToPage",
        "height": 1080,
        "width": 1920
    }, f, indent=2)

# Copy and adapt visual containers from ref_rep
ref_visuals_dir = os.path.join(ref_rep, "definition", "pages", "8f64cc421d0e0604367e", "visuals")

# Mapping rules to adapt visuals cleanly
# We will copy the visuals and rewrite their table/column references and enforce schema 2.9.0
visual_configs = [
    # Header shape
    ("a1000000000000000001", "a1000000000000000001", {}),
    # Header title
    ("a1000000000000000002", "a1000000000000000002", {"text": "OLIST FULFILLMENT AUDIT: GIẢI PHẪU ĐIỂM NGHẼN BÀN GIAO & NGHỊCH LÝ CARRIER CỨU ĐƠN"}),
    # Slicer
    ("a1000000000000000003", "a1000000000000000003", {
        "entity": "fact_freight_price_tier",
        "property": "delivery_quadrant",
        "queryRef": "fact_freight_price_tier.delivery_quadrant",
        "headerText": "LỌC PHÂN KHÚC BÀN GIAO SLA:"
    }),
    # Card 1: Total Orders
    ("c1000000000000000001", "c1000000000000000001", {
        "entity": "fact_freight_price_tier",
        "property": "total_orders",
        "labelText": "TỔNG ĐƠN GIAO THÀNH CÔNG",
        "color": "#38BDF8"
    }),
    # Card 2: Total GMV
    ("c1000000000000000002", "c1000000000000000002", {
        "entity": "fact_freight_price_tier",
        "property": "total_gmv",
        "labelText": "TỔNG DOANH THU HOÀN TẤT (BRL)",
        "color": "#10B981"
    }),
    # Card 3: Carrier Saved
    ("c1000000000000000003", "c1000000000000000003", {
        "entity": "fact_freight_price_tier",
        "property": "aov",
        "labelText": "GIÁ TRỊ ĐƠN TB AOV (BRL)",
        "color": "#F59E0B"
    }),
    # Card 4: Review Score
    ("c1000000000000000004", "c1000000000000000004", {
        "entity": "fact_freight_price_tier",
        "property": "avg_review_score",
        "labelText": "ĐIỂM REVIEW SCORE TB",
        "color": "#EC4899"
    }),
    # Card 5: One Star Rate
    ("c1000000000000000005", "c1000000000000000005", {
        "entity": "fact_freight_price_tier",
        "property": "one_star_pct",
        "labelText": "TỶ LỆ KHÁCH CHẤM 1 SAO (%)",
        "color": "#EF4444"
    }),
    # Donut: Orders by Quadrant
    ("a1000000000000000005", "a1000000000000000005", {
        "cat_entity": "fact_freight_price_tier",
        "cat_prop": "delivery_quadrant_id",
        "val_entity": "fact_freight_price_tier",
        "val_prop": "total_orders",
        "title": "Cơ Cấu Số Đơn Theo 4 Phân Khúc Bàn Giao"
    }),
    # Combo Chart: Total Orders vs Review Score
    ("a1000000000000000006", "a1000000000000000006", {
        "cat_entity": "fact_freight_price_tier",
        "cat_prop": "delivery_quadrant_id",
        "y_entity": "fact_freight_price_tier",
        "y_prop": "total_orders",
        "y2_entity": "fact_freight_price_tier",
        "y2_prop": "avg_review_score",
        "title": "Tương Quan Số Đơn & Điểm Đánh Giá Giữa 4 Góc Phần Tư"
    }),
    # Bar Chart: Regional Breakdown Rate
    ("a1000000000000000007", "a1000000000000000007", {
        "cat_entity": "fact_freight_burden_tiers",
        "cat_prop": "state",
        "val_entity": "fact_freight_burden_tiers",
        "val_prop": "carrier_breakdown_pct",
        "title": "Tỷ Lệ Bưu Cục Làm Trễ (Carrier Gãy) Theo Bang Khách Hàng (%)"
    }),
    # Table: Detailed Quadrants Breakdown
    ("a1000000000000000008", "a1000000000000000008", {
        "entity": "fact_freight_price_tier",
        "title": "Bảng Kê Chi Tiết Vận Hành & Khách Hàng Giữa 4 Góc Phần Tư"
    })
]

for src_name, dst_name, cfg in visual_configs:
    src_v_path = os.path.join(ref_visuals_dir, src_name, "visual.json")
    if not os.path.exists(src_v_path):
        continue
    with open(src_v_path, "r", encoding="utf-8") as f:
        v_data = json.load(f)
    
    # Enforce schema 2.9.0
    v_data["$schema"] = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.9.0/schema.json"
    
    # Textbox title
    if "text" in cfg and "textbox" in v_data.get("visual", {}).get("objects", {}):
        paragraphs = v_data["visual"]["objects"]["textbox"][0]["properties"]["paragraphs"]
        paragraphs[0]["textRuns"][0]["value"] = cfg["text"]
    
    # Card visual configuration
    if v_data.get("visual", {}).get("visualType") == "cardVisual" and "entity" in cfg:
        proj = v_data["visual"]["query"]["queryState"]["Data"]["projections"][0]
        proj["field"]["Aggregation"]["Expression"]["Column"]["Expression"]["SourceRef"]["Entity"] = cfg["entity"]
        proj["field"]["Aggregation"]["Expression"]["Column"]["Property"] = cfg["property"]
        proj["queryRef"] = f"Sum({cfg['entity']}.{cfg['property']})"
        proj["nativeQueryRef"] = cfg["property"]
        
        objs = v_data["visual"].get("objects", {})
        if "label" in objs and len(objs["label"]) > 0:
            objs["label"][0]["properties"]["text"]["expr"]["Literal"]["Value"] = f"'{cfg['labelText']}'"
        if "value" in objs and len(objs["value"]) > 0 and "color" in cfg:
            objs["value"][0]["properties"]["fontColor"]["solid"]["color"]["expr"]["Literal"]["Value"] = f"'{cfg['color']}'"
    
    # Slicer
    if v_data.get("visual", {}).get("visualType") == "slicer" and "entity" in cfg:
        proj = v_data["visual"]["query"]["queryState"]["Values"]["projections"][0]
        proj["field"]["Column"]["Expression"]["SourceRef"]["Entity"] = cfg["entity"]
        proj["field"]["Column"]["Property"] = cfg["property"]
        proj["queryRef"] = f"{cfg['entity']}.{cfg['property']}"
        proj["nativeQueryRef"] = cfg["property"]
        objs = v_data["visual"].get("objects", {})
        if "header" in objs and len(objs["header"]) > 0:
            objs["header"][0]["properties"]["text"]["expr"]["Literal"]["Value"] = f"'{cfg['headerText']}'"

    # Donut Chart
    if v_data.get("visual", {}).get("visualType") == "donutChart" and "cat_entity" in cfg:
        q_state = v_data["visual"]["query"]["queryState"]
        if "Category" in q_state:
            q_state["Category"]["projections"][0]["field"]["Column"]["Expression"]["SourceRef"]["Entity"] = cfg["cat_entity"]
            q_state["Category"]["projections"][0]["field"]["Column"]["Property"] = cfg["cat_prop"]
            q_state["Category"]["projections"][0]["queryRef"] = f"{cfg['cat_entity']}.{cfg['cat_prop']}"
        if "Y" in q_state:
            q_state["Y"]["projections"][0]["field"]["Aggregation"]["Expression"]["Column"]["Expression"]["SourceRef"]["Entity"] = cfg["val_entity"]
            q_state["Y"]["projections"][0]["field"]["Aggregation"]["Expression"]["Column"]["Property"] = cfg["val_prop"]
            q_state["Y"]["projections"][0]["queryRef"] = f"Sum({cfg['val_entity']}.{cfg['val_prop']})"
        if "title" in cfg and "title" in v_data.get("visual", {}).get("visualContainerObjects", {}):
            v_data["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"]["expr"]["Literal"]["Value"] = f"'{cfg['title']}'"

    # Combo Chart
    if v_data.get("visual", {}).get("visualType") == "lineClusteredColumnComboChart" and "cat_entity" in cfg:
        q_state = v_data["visual"]["query"]["queryState"]
        if "Category" in q_state:
            q_state["Category"]["projections"][0]["field"]["Column"]["Expression"]["SourceRef"]["Entity"] = cfg["cat_entity"]
            q_state["Category"]["projections"][0]["field"]["Column"]["Property"] = cfg["cat_prop"]
            q_state["Category"]["projections"][0]["queryRef"] = f"{cfg['cat_entity']}.{cfg['cat_prop']}"
        if "Y" in q_state:
            q_state["Y"]["projections"][0]["field"]["Aggregation"]["Expression"]["Column"]["Expression"]["SourceRef"]["Entity"] = cfg["y_entity"]
            q_state["Y"]["projections"][0]["field"]["Aggregation"]["Expression"]["Column"]["Property"] = cfg["y_prop"]
            q_state["Y"]["projections"][0]["queryRef"] = f"Sum({cfg['y_entity']}.{cfg['y_prop']})"
        if "Y2" in q_state:
            q_state["Y2"]["projections"][0]["field"]["Aggregation"]["Expression"]["Column"]["Expression"]["SourceRef"]["Entity"] = cfg["y2_entity"]
            q_state["Y2"]["projections"][0]["field"]["Aggregation"]["Expression"]["Column"]["Property"] = cfg["y2_prop"]
            q_state["Y2"]["projections"][0]["queryRef"] = f"Average({cfg['y2_entity']}.{cfg['y2_prop']})"
        if "title" in cfg and "title" in v_data.get("visual", {}).get("visualContainerObjects", {}):
            v_data["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"]["expr"]["Literal"]["Value"] = f"'{cfg['title']}'"

    # Bar Chart
    if v_data.get("visual", {}).get("visualType") == "barChart" and "cat_entity" in cfg:
        q_state = v_data["visual"]["query"]["queryState"]
        if "Category" in q_state:
            q_state["Category"]["projections"][0]["field"]["Column"]["Expression"]["SourceRef"]["Entity"] = cfg["cat_entity"]
            q_state["Category"]["projections"][0]["field"]["Column"]["Property"] = cfg["cat_prop"]
            q_state["Category"]["projections"][0]["queryRef"] = f"{cfg['cat_entity']}.{cfg['cat_prop']}"
        if "Y" in q_state:
            q_state["Y"]["projections"][0]["field"]["Aggregation"]["Expression"]["Column"]["Expression"]["SourceRef"]["Entity"] = cfg["val_entity"]
            q_state["Y"]["projections"][0]["field"]["Aggregation"]["Expression"]["Column"]["Property"] = cfg["val_prop"]
            q_state["Y"]["projections"][0]["queryRef"] = f"Sum({cfg['val_entity']}.{cfg['val_prop']})"
        if "title" in cfg and "title" in v_data.get("visual", {}).get("visualContainerObjects", {}):
            v_data["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"]["expr"]["Literal"]["Value"] = f"'{cfg['title']}'"

    # TableEx
    if v_data.get("visual", {}).get("visualType") == "tableEx" and "entity" in cfg:
        ent = cfg["entity"]
        table_cols = [
            ("delivery_quadrant", "delivery_quadrant", "Phân Khúc SLA", False),
            ("total_orders", "total_orders", "Số Đơn", True),
            ("total_gmv", "total_gmv", "Tổng GMV", True),
            ("aov", "aov", "AOV", True),
            ("avg_review_score", "avg_review_score", "Review TB", True),
            ("one_star_pct", "one_star_pct", "% 1 Sao", True),
            ("avg_seller_handling_days", "avg_seller_handling_days", "Seller Xử Lý", True),
            ("avg_carrier_transit_days", "avg_carrier_transit_days", "Carrier Transit", True),
            ("avg_sla_buffer_days", "avg_sla_buffer_days", "Đệm SLA (Ngày)", True)
        ]
        projs = []
        for c_prop, q_ref, native_ref, is_num in table_cols:
            if is_num:
                projs.append({
                    "field": {
                        "Aggregation": {
                            "Expression": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Entity": ent}},
                                    "Property": c_prop
                                }
                            },
                            "Function": 0
                        }
                    },
                    "queryRef": f"Sum({ent}.{c_prop})",
                    "nativeQueryRef": native_ref
                })
            else:
                projs.append({
                    "field": {
                        "Column": {
                            "Expression": {"SourceRef": {"Entity": ent}},
                            "Property": c_prop
                        }
                    },
                    "queryRef": f"{ent}.{c_prop}",
                    "nativeQueryRef": native_ref,
                    "active": True
                })
        v_data["visual"]["query"]["queryState"]["Values"]["projections"] = projs
        if "title" in cfg and "title" in v_data.get("visual", {}).get("visualContainerObjects", {}):
            v_data["visual"]["visualContainerObjects"]["title"][0]["properties"]["text"]["expr"]["Literal"]["Value"] = f"'{cfg['title']}'"

    # Save to target
    dst_dir = os.path.join(visuals_dir, dst_name)
    os.makedirs(dst_dir, exist_ok=True)
    with open(os.path.join(dst_dir, "visual.json"), "w", encoding="utf-8") as f:
        json.dump(v_data, f, indent=2)

print(f"[+] Successfully scaffolded complete PBIP report at {target_rep}")
