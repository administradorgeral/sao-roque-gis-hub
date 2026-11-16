import math

with open("scripts/spatial_legal_engine.py", "r", encoding="utf-8") as f:
    text = f.read()

old_func = """def sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    elif hasattr(obj, "item"):
        return obj.item()
    return obj"""

new_func = """def sanitize_for_json(obj):
    import math
    if isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    elif hasattr(obj, "item"):
        val = obj.item()
        if isinstance(val, float) and math.isnan(val):
            return None
        return val
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj"""

norm_text = text.replace("\r\n", "\n")
norm_old = old_func.replace("\r\n", "\n")
norm_new = new_func.replace("\r\n", "\n")

if norm_old in norm_text:
    norm_text = norm_text.replace(norm_old, norm_new)
    with open("scripts/spatial_legal_engine.py", "w", encoding="utf-8") as f:
        f.write(norm_text)
    print("SUCCESS: NaN sanitizer patched!")
else:
    print("ERROR: old_func not found")
