"""
Script seguro de preparação e commit do Git no Windows
"""
import os
import sys
import time
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run(cmd):
    print(f"Executando: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("STDOUT:", res.stdout.strip())
    if res.stderr:
        print("STDERR:", res.stderr.strip())
    return res

def main():
    # Remove index.lock se existir
    lock_file = BASE_DIR / ".git" / "index.lock"
    if lock_file.exists():
        print("Removendo index.lock...")
        try:
            lock_file.unlink()
        except Exception as e:
            print("Aviso ao remover lock:", e)

    # Verifica se .git existe
    if not (BASE_DIR / ".git").exists():
        run(["git", "init", "-b", "main"])

    # Git add
    print("Adicionando arquivos...")
    run(["git", "add", "-A"])

    # Git commit
    print("Criando commit...")
    commit_res = run(["git", "commit", "-m", "feat: lancamento oficial do Super-App METANOIA (Forja 90 Dias, Alianca WhatsApp e Checkout Pix)"])

    # Git log
    print("Verificando commit:")
    run(["git", "log", "-1", "--oneline"])
    run(["git", "status"])

if __name__ == "__main__":
    main()
