import os
import subprocess
import sys
import time

GIT_EXE = r'C:\Users\admin\.gemini\antigravity\bin\git\cmd\git.exe'
REPO_DIR = r'C:\Users\admin\.gemini\antigravity\scratch\sao-roque-gis-hub'
ENV_FILE = r'C:\Users\admin\.gemini\antigravity\scratch\central-inteligencia-sao-roque\.env'

def get_token():
    with open(ENV_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('GITHUB_TOKEN='):
                return line.split('=', 1)[1].strip()
    raise RuntimeError("GITHUB_TOKEN not found in .env")

def run_git(args, cwd=REPO_DIR):
    print(f">> git {' '.join(args[:3])} ...")
    res = subprocess.run([GIT_EXE] + args, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.returncode != 0:
        print(f"Error ({res.returncode}): {res.stderr}")
        raise RuntimeError(f"Git failed: {res.stderr}")
    if res.stdout:
        print(res.stdout.strip()[:300])
    return res.stdout

def push_with_retry(branch='main', max_retries=3):
    for attempt in range(1, max_retries + 1):
        print(f"Pushing to origin {branch} (Tentativa {attempt}/{max_retries})...")
        res = subprocess.run([GIT_EXE, 'push', 'origin', branch], cwd=REPO_DIR, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if res.returncode == 0:
            print(f"[OK] Push da etapa concluído com sucesso!")
            return True
        else:
            print(f"Aviso no push: {res.stderr}")
            if attempt < max_retries:
                print("Aguardando 5s para retentar...")
                time.sleep(5)
            else:
                raise RuntimeError(f"Falha definitiva no push: {res.stderr}")

def main():
    token = get_token()
    print("Token recuperado com sucesso.")

    # Remove repositório anterior se houver para começar do zero em commits limpos
    git_dir = os.path.join(REPO_DIR, '.git')
    if os.path.exists(git_dir):
        print("Resetando repositório Git local...")
        subprocess.run(['powershell', '-Command', f"Remove-Item -Path '{git_dir}' -Recurse -Force -ErrorAction SilentlyContinue"])

    # 1. Inicializa repositório
    run_git(['init'])
    run_git(['branch', '-M', 'main'])
    run_git(['config', 'user.name', 'Rodrigo Sanches'])
    run_git(['config', 'user.email', 'administradorgeral@gmail.com'])
    run_git(['config', 'http.postBuffer', '524288000'])
    run_git(['config', 'http.lowSpeedLimit', '0'])
    run_git(['config', 'http.lowSpeedTime', '999999'])
    run_git(['config', 'core.compression', '9'])

    remote_url = f"https://{token}@github.com/administradorgeral/sao-roque-gis-hub.git"
    run_git(['remote', 'add', 'origin', remote_url])

    # =========================================================================
    # LOTE 1: Core da Aplicação WebGIS, Leaflet, Módulos ES6, CSS e Documentação
    # =========================================================================
    print("\n=== LOTE 1: Aplicação WebGIS Core, Interface e Módulos IA ===")
    run_git(['add', 'index.html', 'README.md', '.nojekyll', '.gitignore'])
    run_git(['add', 'css/'])
    run_git(['add', 'js/'])
    run_git(['add', 'scripts/'])
    run_git(['commit', '-m', 'feat: core da aplicacao webgis sao roque hub com leafet, ia argon e 4 pilares'])
    push_with_retry('main')

    # =========================================================================
    # LOTE 2: Minutas da Revisão 2026 e Dados Oficiais
    # =========================================================================
    print("\n=== LOTE 2: Minutas do Plano Diretor 2026 e Dados Oficiais ===")
    run_git(['add', 'minuta_pd2026/'])
    run_git(['add', 'dados_oficiais/'])
    if os.path.exists(os.path.join(REPO_DIR, 'scratch_kml')):
        run_git(['add', 'scratch_kml/'])
    run_git(['commit', '-m', 'feat: minutas do plano diretor 2026, estudos tecnicos e legislacao municipal'])
    push_with_retry('main')

    # =========================================================================
    # LOTE 3: Camadas Vetoriais Estruturais (Cartas I a XIII, Zoneamento e Vias)
    # =========================================================================
    print("\n=== LOTE 3: Camadas Cartograficas I a XIII, Zoneamentos e Sistema Viario ===")
    # Adiciona todos os geojson exceto declividade e fragilidade
    data_dir = os.path.join(REPO_DIR, 'data')
    for f in os.listdir(data_dir):
        if f.endswith('.geojson') or f.endswith('.json'):
            if 'declividade' not in f and 'fragilidade' not in f:
                run_git(['add', f'data/{f}'])
    run_git(['commit', '-m', 'feat: cartas tematicas I a XIII, zoneamento 2006, corredores e infraestrutura'])
    push_with_retry('main')

    # =========================================================================
    # LOTE 4: Declividade Submétrica e Fragilidade Potencial
    # =========================================================================
    print("\n=== LOTE 4: Declividade Submetrica Otimizada e Fragilidade Potencial ===")
    for f in os.listdir(data_dir):
        if 'declividade' in f or 'fragilidade' in f:
            if not f.endswith('.gpkg') and not f.endswith('.tmp'):
                run_git(['add', f'data/{f}'])
    run_git(['commit', '-m', 'feat: declividade submetrica otimizada e fragilidade ambiental'])
    push_with_retry('main')

    # Sanitiza URL remota local
    run_git(['remote', 'set-url', 'origin', 'https://github.com/administradorgeral/sao-roque-gis-hub.git'])
    print("\n[SUCESSO] Todos os 4 lotes foram commitados e enviados com sucesso ao GitHub!")

if __name__ == '__main__':
    main()
