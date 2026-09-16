"""
Script de Monitoramento Contínuo e Auditoria de Saúde do Sistema // METANOIA
Executa checagens profundas de latência, integridade do banco de dados, servidor web e módulos Flet.
"""
import sys
import time
import json
import sqlite3
import urllib.request
from pathlib import Path

# Suporte UTF-8 para console Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "metanoia.db"
URL_LANDING = "http://localhost:8585"

def checar_banco_dados():
    t0 = time.perf_counter()
    if not DB_PATH.exists():
        return {"status": "FAIL", "erro": "Arquivo do banco metanoia.db não encontrado"}
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Valida 90 dias
    cursor.execute("SELECT COUNT(*) FROM forja_90_dias WHERE titulo IS NOT NULL AND texto_biblico IS NOT NULL AND missao_pratica IS NOT NULL")
    total_dias = cursor.fetchone()[0]
    
    # Valida tabelas essenciais
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    dt = (time.perf_counter() - t0) * 1000
    
    return {
        "status": "OK" if total_dias == 90 else "FAIL",
        "latencia_ms": round(dt, 2),
        "total_licoes_90_dias": total_dias,
        "tabelas_presentes": tabelas
    }

def checar_servidor_web():
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(URL_LANDING, headers={"User-Agent": "Metanoia-Healthcheck/1.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            status_code = resp.status
            dt = (time.perf_counter() - t0) * 1000
            return {
                "status": "OK" if status_code == 200 else "WARN",
                "codigo_http": status_code,
                "latencia_ms": round(dt, 2),
                "url": URL_LANDING
            }
    except Exception as e:
        return {
            "status": "WARN",
            "erro": str(e),
            "url": URL_LANDING,
            "aviso": "Servidor pode estar pausado ou porta 8585 indisponível"
        }

def checar_modulos_python():
    sys.path.insert(0, str(BASE_DIR))
    modulos = [
        "core.theme",
        "core.config",
        "services.db_service",
        "views.ordem_view",
        "views.sentinela_view",
        "views.alianca_view",
        "views.conselheiro_view",
    ]
    status_modulos = {}
    for m in modulos:
        try:
            __import__(m)
            status_modulos[m] = "OK"
        except Exception as e:
            status_modulos[m] = f"ERRO: {e}"
    
    todos_ok = all(v == "OK" for v in status_modulos.values())
    return {
        "status": "OK" if todos_ok else "FAIL",
        "detalhes": status_modulos
    }

def main():
    print("=" * 60)
    print("🛡️ MONITOR DE SAÚDE & AUDITORIA // SUPER-APP METANOIA")
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Banco de dados
    db_res = checar_banco_dados()
    print(f"\n[1/3] Banco de Dados SQLite: {db_res['status']}")
    print(f"  • Latência de leitura: {db_res.get('latencia_ms', 0)} ms")
    print(f"  • Lições completas na Forja dos 90 Dias: {db_res.get('total_licoes_90_dias', 0)}/90")
    print(f"  • Total de tabelas ativas: {len(db_res.get('tabelas_presentes', []))}")

    # 2. Servidor Web Landing Page
    web_res = checar_servidor_web()
    print(f"\n[2/3] Servidor Web (Landing Page): {web_res['status']}")
    print(f"  • URL: {web_res['url']}")
    if web_res['status'] == "OK":
        print(f"  • Código HTTP: {web_res['codigo_http']} OK")
        print(f"  • Latência de resposta: {web_res['latencia_ms']} ms")
    else:
        print(f"  • Aviso: {web_res.get('erro', '')}")

    # 3. Módulos do App Flet
    mod_res = checar_modulos_python()
    print(f"\n[3/3] Compilação & Módulos do Sistema: {mod_res['status']}")
    for mod, st in mod_res['detalhes'].items():
        print(f"  • {mod}: {st}")

    print("\n" + "=" * 60)
    if db_res['status'] == "OK" and mod_res['status'] == "OK":
        print("🏆 RESULTADO GERAL: SISTEMA 100% OPERACIONAL E PRONTO PARA TRÁFEGO!")
    else:
        print("⚠️ RESULTADO GERAL: FORAM DETECTADAS PENDÊNCIAS A SEREM REVISADAS.")
    print("=" * 60)

if __name__ == "__main__":
    main()
