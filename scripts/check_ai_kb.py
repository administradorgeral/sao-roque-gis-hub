import json

with open("C:/Users/admin/.gemini/antigravity/scratch/sao-roque-gis-hub/data/base_conhecimento_ia.json", "r", encoding="utf-8") as f:
    d = json.load(f)

print("Metadados:", d.get("metadados"))
print("Total camadas auditadas:", len(d.get("camadas_auditadas", [])))
print("Total classes:", len(d.get("classes_camadas", [])))
print("Total cruzamentos legislativos:", len(d.get("cruzamentos_legislacao", [])))
print("Cartas do Plano Diretor presentes em camadas_auditadas:")
for c in d.get("camadas_auditadas", []):
    if "carta_" in c.get("id", ""):
        print(f"  {c['id']}: {c['nome']}")
