import os

search_dirs = [
    r"C:\Users\admin\Downloads\Mapas São Roque-20261112T033114Z-1-001\Mapas São Roque",
    r"C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub"
]

found = []
for d in search_dirs:
    if os.path.exists(d):
        for root, dirs, files in os.walk(d):
            for f in files:
                if 'decliv' in f.lower() or '40537' in f.lower():
                    p = os.path.join(root, f)
                    found.append((p, os.path.getsize(p)))

print(f"Total de arquivos encontrados: {len(found)}")
for p, s in found:
    print(f"{s/1024:.1f} KB -> {p}")
