"""
==============================================================================
🔥 GERADOR AUTOMÁTICO DE VÍDEOS VIRAIS // METANOIA (TIKTOK / REELS / SHORTS)
==============================================================================
Pipeline cinematográfico autônomo:
1. Seleção de Voz Neural Natural (sem artefatos de pitch) ou ElevenLabs.
2. Integração com Banco de Vídeos via API (Pexels + Pixabay do .env).
3. Legendas automáticas de alta retenção (Amarelo Ouro + Contorno Preto).
4. Header oficial "⚔ METANOIA // FORJA DE 90 DIAS" no topo.
5. Renderização em formato vertical 9:16 (1080x1920) em segundos.
==============================================================================
"""
import re
import os
import sys
import time
import shutil
import random
import asyncio
import argparse
import subprocess
from pathlib import Path

# Suporte UTF-8 no terminal Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"
BG_VIDEOS_DIR = ASSETS_DIR / "videos_fundo"

# Importa o serviço unificado de Banco de Vídeos (Pexels + Pixabay)
sys.path.insert(0, str(BASE_DIR))
from services.video_bank_service import VideoBankService

try:
    import edge_tts
except ImportError:
    print("ERRO: Pacote 'edge-tts' não encontrado. Instale com: pip install edge-tts")
    sys.exit(1)

# Catálogo de vozes neurais de alta fidelidade
VOZES_DISPONIVEIS = {
    "1": {
        "nome": "Antonio Natural (Masculina PT-BR)",
        "id": "pt-BR-AntonioNeural",
        "desc": "Voz grave, sóbria e 100% natural, tom de guerreiro e mentor (100% Grátis)",
        "tipo": "edge"
    },
    "2": {
        "nome": "Francisca Natural (Feminina PT-BR)",
        "id": "pt-BR-FranciscaNeural",
        "desc": "Voz feminina firme, clara e inspiradora (100% Grátis)",
        "tipo": "edge"
    },
    "3": {
        "nome": "Duarte Épico (Masculina PT-PT)",
        "id": "pt-PT-DuarteNeural",
        "desc": "Tom clássico, épico e solene de narrativa bíblica e histórica (100% Grátis)",
        "tipo": "edge"
    },
    "4": {
        "nome": "Thalita Multilingual (Feminina PT-BR)",
        "id": "pt-BR-ThalitaMultilingualNeural",
        "desc": "Novo modelo neural multilíngue de alta fluidez (100% Grátis)",
        "tipo": "edge"
    },
    "5": {
        "nome": "ElevenLabs (Ultra-Realista Studio)",
        "id": "elevenlabs",
        "desc": "Voz com respiração e emoção humana (requer ELEVENLABS_API_KEY no .env)",
        "tipo": "elevenlabs"
    }
}

ROTEIROS_DISPONIVEIS = {
    "1": {
        "titulo": "A Casa Vazia (Mateus 12)",
        "tema_video": "dark warrior",
        "hook": "Se o METANOIA virasse apenas um aplicativo anti-pornografia, nós teríamos falhado.",
        "texto": (
            "Se o METANOIA virasse apenas um aplicativo anti-pornografia, nós teríamos falhado miseravelmente. "
            "A pornografia é apenas a sala de emergência, onde o homem chega sangrando e pedindo socorro. "
            "Mas o que cura esse homem de verdade é o discipulado completo. "
            "Jesus ensinou em Mateus 12 que quando o espírito sai e acha a casa vazia, "
            "ele volta com outros sete espíritos piores. "
            "Não adianta você tirar a pornografia e deixar a sua alma vazia. "
            "Você precisa de uma forja diária de noventa dias: "
            "Ordem Matinal, joelhos no chão e aliança com homens de honra. "
            "Preencha a sua casa. O link oficial está na bio."
        )
    },
    "2": {
        "titulo": "A Regra dos 3 Minutos de Gary Wilson",
        "tema_video": "fire flames",
        "hook": "Parar de ver pornografia só na força de vontade é uma mentira biológica.",
        "texto": (
            "Parar de ver pornografia só na força de vontade é uma mentira biológica. "
            "Gary Wilson provou que a fissura por dopamina atinge o pico em três minutos e depois quebra. "
            "Quando a noite chega, seu córtex pré-frontal está exausto. "
            "Se você ficar negociando com o celular na mão, você vai cair de novo. "
            "Homens livres não confiam na própria carne; eles confiam em sistemas de emergência. "
            "O METANOIA tem o Protocolo Sentinela: "
            "quando o perigo aperta, ele assume o comando, "
            "desacelera seus batimentos com choque vagal e destrói a onda do vício. "
            "Pare de lutar desarmado. Toque no link da bio."
        )
    },
    "3": {
        "titulo": "O Segredo das 23 Horas",
        "tema_video": "rain night dark",
        "hook": "A sua pior batalha não acontece na rua. Ela acontece às onze da noite.",
        "texto": (
            "A sua pior batalha não acontece na rua. Ela acontece às onze da noite, "
            "quando a porta do seu quarto se fecha. "
            "Você passou o dia inteiro fingindo que estava tudo bem. "
            "Mas no escuro, o cansaço bate e você troca sua honra e comunhão com Deus "
            "por trinta segundos de dopamina roubada na tela. "
            "O pior não é a recaída: é a vergonha na manhã seguinte de não conseguir orar. "
            "O que você precisa não é de culpa; é de um Sistema de Ordem Interior. "
            "A Forja dos noventa dias pega você pela mão da lama até o altar do casamento. "
            "Comece sua prova de sete dias no link da bio."
        )
    },
    "4": {
        "titulo": "A Aliança de Honra (Ferro com Ferro)",
        "tema_video": "blacksmith anvil",
        "hook": "Nenhum homem vence o vício trancado sozinho no quarto.",
        "texto": (
            "Nenhum homem vence o vício trancado sozinho no quarto. "
            "O pecado secreto adora as sombras. "
            "Salomão escreveu em Provérbios 27: Como o ferro com o ferro se afia, "
            "assim o homem ao seu irmão. "
            "No METANOIA você não entra em grupos de cinquenta pessoas para passar vergonha. "
            "Você faz um pacto sagrado um para um com um irmão de guerra. "
            "Às vinte e uma e trinta da noite, três perguntas rápidas no WhatsApp. "
            "Se você estiver de pé, vocês celebram. Se você vacilar, ele recebe o alerta na hora. "
            "A transparência quebra o vício. Conheça a Forja no link da bio."
        )
    },
    "5": {
        "titulo": "A Carta de Paulo para o Homem Moderno",
        "tema_video": "dark warrior",
        "hook": "Se o Apóstolo Paulo escrevesse uma carta para você hoje, o que ele diria?",
        "texto": (
            "Se o Apóstolo Paulo escrevesse uma carta para você hoje, o que ele diria? "
            "Ele diria: Até quando você vai viver escravo de um retângulo de vidro iluminado? "
            "Cristo te comprou por preço de sangue, e você entrega sua energia vital para pixels vazios? "
            "Chega de autoajuda fofa e promessas vazias de internet. "
            "O METANOIA foi criado para homens decididos: "
            "Ordem Matinal sem tocar em redes sociais, tempo de joelhos no chão e honra diária. "
            "Você não foi feito para a vergonha; foi feito para a espada. "
            "O link da Prova de Fogo está na bio."
        )
    }
}

def format_timestamp_ass(seconds: float) -> str:
    """Converte segundos para o formato de tempo do ASS: H:MM:SS.cs"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    if centis >= 100:
        centis = 99
    return f"{hrs}:{mins:02d}:{secs:02d}.{centis:02d}"

async def sintetizar_audio_e_ass(texto: str, audio_path: Path, ass_path: Path, voz_chave: str = "1"):
    """
    Sintetiza locução natural (sem distorção metálica) e gera legendas ASS estilizadas.
    """
    voz_info = VOZES_DISPONIVEIS.get(voz_chave, VOZES_DISPONIVEIS["1"])
    voz_id = voz_info["id"]

    print(f"🎙️ Sintetizando áudio natural com: '{voz_info['nome']}'...")

    # IMPORTANTE: Sem 'pitch=-3Hz'! A distorção metálica acontecia por causa do pitch shift.
    # O pitch="+0Hz" e rate="+0%" mantém a voz neural 100% pura, límpida e humana.
    communicate = edge_tts.Communicate(texto, voz_id, pitch="+0Hz", rate="+0%")

    audio_data = bytearray()
    sentencas = []

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
        elif chunk["type"] == "SentenceBoundary":
            s_start = chunk["offset"] / 10_000_000
            s_dur = chunk["duration"] / 10_000_000
            sentencas.append({
                "start": s_start,
                "end": s_start + s_dur,
                "text": chunk["text"].strip()
            })

    audio_path.write_bytes(audio_data)
    duracao_total = sentencas[-1]["end"] if sentencas else 10.0
    print(f"  ✅ Áudio neural natural gerado: {audio_path.name} ({len(audio_data)} bytes, ~{duracao_total:.1f}s)")

    # Quebra as frases em blocos visuais curtos (3 a 5 palavras) para dinâmica de retenção
    blocos_ass = []
    for s in sentencas:
        palavras = s["text"].split()
        if len(palavras) <= 5:
            blocos_ass.append((s["start"], s["end"], s["text"].upper()))
        else:
            chunk_size = 4
            partes = [" ".join(palavras[i:i+chunk_size]) for i in range(0, len(palavras), chunk_size)]
            dur_fracao = (s["end"] - s["start"]) / len(partes)
            for idx, parte in enumerate(partes):
                t_ini = s["start"] + (idx * dur_fracao)
                t_fim = t_ini + dur_fracao
                blocos_ass.append((t_ini, t_fim, parte.upper()))

    # Arquivo ASS com Header brutalista e Legendas Amarelas de Alto Impacto
    ass_template = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Header,Arial,34,&H000C58EA,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,8,30,30,140,1
Style: Subtitle,Arial Black,54,&H0000FFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,3,2,60,60,420,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{format_timestamp_ass(duracao_total + 1.0)},Header,,0,0,0,,⚔ METANOIA // FORJA DE 90 DIAS
"""
    dialogues = []
    for t_ini, t_fim, txt in blocos_ass:
        txt_escapado = txt.replace("{", "").replace("}", "")
        dialogues.append(f"Dialogue: 0,{format_timestamp_ass(t_ini)},{format_timestamp_ass(t_fim)},Subtitle,,0,0,0,,{txt_escapado}")

    ass_path.write_text(ass_template + "\n".join(dialogues), encoding="utf-8")
    print(f"  ✅ Legendas sincronizadas geradas ({len(blocos_ass)} blocos).")
    return duracao_total

def renderizar_video_ffmpeg(audio_path: Path, ass_path: Path, output_path: Path, video_fundo: Path, duracao: float):
    """
    Renderiza o vídeo vertical 1080x1920 combinando o clipe de fundo em HD, áudio e legendas.
    """
    print(f"🎬 Renderizando vídeo 1080x1920 com clipe: {video_fundo.name}...")
    ass_escaped = str(ass_path.resolve()).replace("\\", "/").replace(":", "\\:")

    filter_complex = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"eq=brightness=-0.12:contrast=1.25:saturation=0.9,"
        f"subtitles='{ass_escaped}'[outv]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(video_fundo),
        "-i", str(audio_path),
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_path)
    ]

    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0

    if res.returncode != 0:
        print("❌ Erro no FFmpeg:")
        print(res.stderr[-800:])
        return False

    print(f"🎉 VÍDEO CONCLUÍDO COM SUCESSO EM {dt:.1f}s!")
    print(f"📁 Arquivo: {output_path.resolve()}")
    print(f"📦 Tamanho: {output_path.stat().st_size / (1024*1024):.2f} MB")
    return True

def sanitizar_nome(nome: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9_-]', '_', nome)
    return re.sub(r'_+', '_', s).strip('_')

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    BG_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(description="Gerador Cinemático de Vídeos Metanoia com IA")
    parser.add_argument("--roteiro", type=str, help="Número do roteiro (1 a 5)")
    parser.add_argument("--voz", type=str, default="1", help="Número da voz (1: Antonio, 2: Francisca, 3: Duarte, 4: Thalita)")
    parser.add_argument("--tema", type=str, help="Tema para busca de vídeo de fundo (ex: blacksmith, fire, warrior)")
    parser.add_argument("--texto", type=str, help="Texto personalizado para o vídeo")
    parser.add_argument("--nome", type=str, help="Nome do arquivo de saída")
    args = parser.parse_args()

    print("=" * 68)
    print("⚔️  METANOIA // GERADOR AUTOMÁTICO DE VÍDEOS DE ALTO IMPACTO (IA)")
    print("=" * 68)

    bank_service = VideoBankService()

    texto_final = ""
    prefixo = "video_metanoia"
    tema_busca = "dark warrior"

    if args.texto:
        texto_final = args.texto
        prefixo = sanitizar_nome(args.nome or "custom")
        tema_busca = args.tema or "dark warrior"
    elif args.roteiro and args.roteiro in ROTEIROS_DISPONIVEIS:
        item = ROTEIROS_DISPONIVEIS[args.roteiro]
        texto_final = item["texto"]
        prefixo = f"metanoia_roteiro_{args.roteiro}_{sanitizar_nome(item['titulo'])[:25]}"
        tema_busca = args.tema or item.get("tema_video", "dark warrior")
    else:
        print("\n📜 ESCOLHA UM DOS ROTEIROS DE ALTA RETENÇÃO:")
        for k, v in ROTEIROS_DISPONIVEIS.items():
            print(f"  [{k}] {v['titulo']}")
            print(f"      Gancho: \"{v['hook']}\"\n")
        print("  [C] Escrever meu próprio texto")

        escolha = input("\n👉 Digite o número do roteiro (1 a 5) ou C: ").strip().upper()
        if escolha in ROTEIROS_DISPONIVEIS:
            item = ROTEIROS_DISPONIVEIS[escolha]
            texto_final = item["texto"]
            prefixo = f"metanoia_roteiro_{escolha}_{sanitizar_nome(item['titulo'])[:25]}"
            tema_busca = item.get("tema_video", "dark warrior")
        elif escolha == "C":
            texto_final = input("\nCole o texto da locução aqui:\n").strip()
            if not texto_final:
                print("Texto vazio. Abortando.")
                return
            prefixo = "metanoia_custom"
            tema_busca = "dark warrior"
        else:
            item = ROTEIROS_DISPONIVEIS["1"]
            texto_final = item["texto"]
            prefixo = "metanoia_roteiro_1"
            tema_busca = item.get("tema_video", "dark warrior")

    # Escolha de Voz
    voz_escolhida = args.voz
    if not args.roteiro and not args.texto:
        print("\n🎙️ ESCOLHA A VOZ DA NARRATIVA:")
        for k, v in VOZES_DISPONIVEIS.items():
            print(f"  [{k}] {v['nome']} - {v['desc']}")
        v_input = input(f"\n👉 Escolha a voz (padrão 1 - Antonio Natural): ").strip()
        if v_input in VOZES_DISPONIVEIS:
            voz_escolhida = v_input

    # 1. Obtém vídeo de fundo correspondente do banco (Pexels / Pixabay)
    print("\n" + "-" * 50)
    video_fundo = bank_service.obter_video_para_tema(tema_busca)
    if not video_fundo or not video_fundo.exists():
        locais = bank_service.listar_videos_locais()
        if locais:
            video_fundo = locais[0]
            print(f"Usando vídeo local: {video_fundo.name}")
        else:
            print("❌ Nenhum vídeo encontrado nos bancos nem localmente.")
            return

    temp_audio = OUTPUT_DIR / f"{prefixo}_audio.mp3"
    temp_ass = OUTPUT_DIR / f"{prefixo}_legendas.ass"
    video_final = OUTPUT_DIR / f"{prefixo}.mp4"

    # 2. Gera o áudio neural natural e legendas ASS
    print("-" * 50)
    duracao = asyncio.run(sintetizar_audio_e_ass(texto_final, temp_audio, temp_ass, voz_chave=voz_escolhida))

    # 3. Renderiza o vídeo vertical 1080x1920
    print("-" * 50)
    sucesso = renderizar_video_ffmpeg(temp_audio, temp_ass, video_final, video_fundo, duracao)

    if sucesso:
        print("\n" + "=" * 68)
        print("🚀 VÍDEO PRONTO PARA O TIKTOK, REELS E YOUTUBE SHORTS!")
        print(f"▶️  Arquivo gerado:")
        print(f"    file:///{str(video_final.resolve()).replace(chr(92), '/')}")
        print("=" * 68)

if __name__ == "__main__":
    main()
