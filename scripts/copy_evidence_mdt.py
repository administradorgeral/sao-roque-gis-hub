import shutil
import os

src_dir = r"C:\Users\admin\.gemini\antigravity\brain\890f7393-d873-454e-a355-9e483a1bb71c\browser_sandbox\screenshots"
dst_dir = r"C:\Users\admin\.gemini\antigravity\brain\8a767400-ab0f-40a5-b1b7-b7e6cab406ec\evidence_mdt"

os.makedirs(dst_dir, exist_ok=True)

files = ["step_8.png", "step_10.png", "step_14.png"]
for f in files:
    src = os.path.join(src_dir, f)
    dst = os.path.join(dst_dir, f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copiado: {dst} ({os.path.getsize(dst)/1024:.1f} KB)")
