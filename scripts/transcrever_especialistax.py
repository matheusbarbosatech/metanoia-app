"""
Script de Transcrição Automatizada da Pasta #especialistax via Deepgram Nova-2.
Extrai áudio leve via FFmpeg, envia para a Deepgram com formatação e pontuação,
e salva transcrições completas organizadas por pasta e aula.
Com suporte a retoma (checkpoint) e failover.
"""
import os
import sys
import subprocess
import urllib.request
import urllib.error
import json
import time
from pathlib import Path

import functools

# Suporte a caracteres especiais no terminal do Windows (cp1252) e flush imediato
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

print = functools.partial(print, flush=True)

# Configurações de Caminhos
INPUT_DIR = Path("C:/Users/matheus/Desktop/#especialistax")
BASE_DIR = Path("C:/Users/matheus/Desktop/metanoia-app")
OUTPUT_DIR = BASE_DIR / "data" / "transcricoes_especialistax"
TEMP_AUDIO_DIR = BASE_DIR / "data" / "temp_audio"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEMP_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Chave Deepgram (com suporte a variável de ambiente ou chave padrão ativa)
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY", "a557aa825d3e48f112361a29e9eaabefa00e50a8")
DEEPGRAM_URL = "https://api.deepgram.com/v1/listen?model=nova-2&language=pt&smart_format=true&punctuate=true&paragraphs=true"

# Ordem de Prioridade (As pastas mais práticas primeiro)
PRIORIDADE_PASTAS = [
    "21_Dias_sem_Pornografia-Miguel_Soriani-2022",
    "O_Recomeco_2_0-Miguel_Soriani-2023",
    "Despornifique-se",
    "O Reboot Guia Definitivo Para Voc",
    "O_Recomeco_Guia_para_Superar_o_Vicio_em_Pornografia-Miguel_Soriani-2022",
    "Padre_Paulo_Ricardo-31-O_mal_da_pornografia_e_da_masturba"
]

def obter_prioridade(path: Path) -> int:
    path_str = str(path)
    for idx, pref in enumerate(PRIORIDADE_PASTAS):
        if pref in path_str:
            return idx
    return 99

def escanear_arquivos():
    exts = {".mp4", ".mkv", ".avi", ".mov", ".m4v", ".webm", ".mp3", ".m4a", ".wav"}
    arquivos = [p for p in INPUT_DIR.rglob("*") if p.suffix.lower() in exts]
    arquivos.sort(key=obter_prioridade)
    return arquivos

def extrair_audio(video_path: Path, temp_audio_path: Path) -> bool:
    """Extrai áudio mono leve 16kHz em MP3 via FFmpeg."""
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-ar", "16000", "-ac", "1", "-b:a", "64k",
        "-f", "mp3", str(temp_audio_path)
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
        return res.returncode == 0 and temp_audio_path.exists() and temp_audio_path.stat().st_size > 0
    except Exception as e:
        print(f"   [ERRO FFmpeg] {e}")
        return False

def transcrever_deepgram(audio_path: Path, api_key: str):
    """Envia áudio para a API Deepgram Nova-2."""
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "audio/mp3"
    }

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    req = urllib.request.Request(DEEPGRAM_URL, data=audio_data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        if e.code == 402:
            print("\n[ALERTA CRITICO] Saldo de creditos Deepgram esgotado (HTTP 402).")
            print("Crie uma nova conta gratuita ou insira outra chave para continuar.")
            sys.exit(402)
        print(f"   [ERRO HTTP Deepgram] {e.code}: {err_msg}")
        return None
    except Exception as e:
        print(f"   [ERRO Conexao Deepgram] {e}")
        return None

def processar_lote():
    arquivos = escanear_arquivos()
    total = len(arquivos)
    print("=" * 65)
    print(f"  METANOIA // TRANSCRIÇÃO DEEPGRAM NOVA-2 (#ESPECIALISTAX)")
    print(f"  Total de arquivos na fila: {total}")
    print(f"  Pasta de destino: {OUTPUT_DIR}")
    print("=" * 65)

    sucessos = 0
    pulados = 0
    falhas = 0

    for idx, arq in enumerate(arquivos, start=1):
        rel_path = arq.relative_to(INPUT_DIR)
        out_txt = OUTPUT_DIR / rel_path.with_suffix(".txt")
        out_json = OUTPUT_DIR / rel_path.with_suffix(".json")

        # 1. Checa se já foi transcrito anteriormente
        if out_txt.exists() and out_txt.stat().st_size > 50:
            print(f"[{idx}/{total}] [JA TRANSCCRITO] {rel_path}")
            pulados += 1
            continue

        out_txt.parent.mkdir(parents=True, exist_ok=True)
        print(f"[{idx}/{total}] Processando: {rel_path.name} ({arq.stat().st_size / (1024*1024):.1f} MB)...")

        temp_audio = TEMP_AUDIO_DIR / f"temp_{int(time.time()*1000)}.mp3"

        # 2. Extrai áudio leve
        ok_audio = extrair_audio(arq, temp_audio)
        if not ok_audio:
            print(f"   [FALHA] Não foi possível extrair áudio de {arq.name}")
            falhas += 1
            continue

        # 3. Transcreve via Deepgram Nova-2
        t0 = time.time()
        res_dg = transcrever_deepgram(temp_audio, DEEPGRAM_API_KEY)
        duracao_req = time.time() - t0

        # Remove áudio temporário imediatamente para economizar disco
        if temp_audio.exists():
            try:
                temp_audio.unlink()
            except Exception:
                pass

        if not res_dg:
            print(f"   [FALHA] Falha na transcrição via Deepgram.")
            falhas += 1
            continue

        # 4. Extrai texto e salva
        try:
            channels = res_dg.get("results", {}).get("channels", [{}])
            alts = channels[0].get("alternatives", [{}])
            transcript = alts[0].get("transcript", "").strip()

            # Tenta pegar parágrafos se disponível
            paragraphs = alts[0].get("paragraphs", {}).get("transcript")
            if paragraphs:
                texto_salvar = paragraphs.strip()
            else:
                texto_salvar = transcript

            if not texto_salvar:
                texto_salvar = "[Áudio sem fala identificada ou silêncio]"

            # Grava TXT e JSON
            with open(out_txt, "w", encoding="utf-8") as f:
                f.write(f"# Transcrição Oficial: {arq.name}\n")
                f.write(f"# Caminho Original: {rel_path}\n")
                f.write(f"# Gerado via Deepgram Nova-2 em: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(texto_salvar)

            with open(out_json, "w", encoding="utf-8") as f:
                json.dump(res_dg, f, ensure_ascii=False, indent=2)

            palavras = len(texto_salvar.split())
            print(f"   [SUCESSO] Transcrito em {duracao_req:.1f}s | {palavras} palavras salvas em {out_txt.name}")
            sucessos += 1

        except Exception as err:
            print(f"   [ERRO Salvar] {err}")
            falhas += 1

    print("\n" + "=" * 65)
    print(f"  TRANSCRIÇÃO CONCLUÍDA / PAUSADA")
    print(f"  Sucessos: {sucessos} | Já prontos: {pulados} | Falhas: {falhas}")
    print("=" * 65)

if __name__ == "__main__":
    processar_lote()
