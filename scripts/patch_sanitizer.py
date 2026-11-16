with open("scripts/spatial_legal_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

sanitize_def = """def sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    elif hasattr(obj, "item"):
        return obj.item()
    return obj
"""

old_block = """        # 3. Hash Criptográfico de Auditoria SHA-256
        serialized_data = json.dumps(report, sort_keys=True, ensure_ascii=False)"""

new_block = """        # Sanitização de tipos numpy/int32/float64
        report = sanitize_for_json(report)

        # 3. Hash Criptográfico de Auditoria SHA-256
        serialized_data = json.dumps(report, sort_keys=True, ensure_ascii=False)"""

norm_text = text.replace("\r\n", "\n")
if "def sanitize_for_json" not in norm_text:
    # insert before class SpatialLegalEngine
    idx = norm_text.find("class SpatialLegalEngine:")
    norm_text = norm_text[:idx] + sanitize_def + "\n\n" + norm_text[idx:]

norm_text = norm_text.replace(old_block, new_block)

with open("scripts/spatial_legal_engine.py", "w", encoding="utf-8") as f:
    f.write(norm_text)

print("SUCCESS: spatial_legal_engine.py patched with sanitize_for_json!")
