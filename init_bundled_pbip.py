import os
import shutil
import json

src_rep = r"reports\Freight_Deadweight_Diagnostic.Report"
src_sm = r"reports\Freight_Deadweight_Diagnostic.SemanticModel"
dst_rep = r"reports\Bundled_Orders_Diagnostic.Report"
dst_sm = r"reports\Bundled_Orders_Diagnostic.SemanticModel"

if os.path.exists(dst_rep): shutil.rmtree(dst_rep)
if os.path.exists(dst_sm): shutil.rmtree(dst_sm)

shutil.copytree(src_rep, dst_rep)
shutil.copytree(src_sm, dst_sm)

pbip_path = r"reports\Bundled_Orders_Diagnostic.pbip"
pbip_dict = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
    "version": "1.0",
    "artifacts": [{"report": {"path": "Bundled_Orders_Diagnostic.Report"}}],
    "settings": {"enableAutoRecovery": True}
}
with open(pbip_path, "w", encoding="utf-8") as f:
    json.dump(pbip_dict, f, indent=2)

pbir_dict = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pbir/1.0.0/schema.json",
    "version": "1.0",
    "datasetReference": {
        "byPath": {
            "path": "../Bundled_Orders_Diagnostic.SemanticModel"
        }
    }
}
with open(os.path.join(dst_rep, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump(pbir_dict, f, indent=2)

print("[+] Initialized Bundled_Orders_Diagnostic PBIP structure.")