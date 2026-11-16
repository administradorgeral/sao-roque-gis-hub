with open('C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/index.html', encoding='utf-8') as f:
    html = f.read()

import re
titles = re.findall(r'<h[34][^>]*>(.*?)</h[34]>', html)
for t in titles:
    clean_t = re.sub(r'<[^>]+>', '', t).strip()
    print("  Title:", clean_t)
