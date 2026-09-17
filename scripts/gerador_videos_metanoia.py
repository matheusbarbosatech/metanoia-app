"""
==============================================================================
🔥 GERADOR AUTOMÁTICO DE VÍDEOS VIRAIS // METANOIA (TIKTOK / REELS / SHORTS)
==============================================================================
Pipeline cinematográfico de alta retenção:
1. Cortes Visuais Dinâmicos a cada 2.5 a 3.0 segundos (Faíscas, Guerreiro, Bigorna, Tempestade, Chamas).
2. Trilha Sonora Épica de Fundo (Orquestra dramática com tambores de guerra e fade-out).
3. Vozes Neurais Gratuitas (Duarte Épico, Francisca Firme, Brian Multilingual, etc.) ou Áudio Próprio.
4. Legendas de Alto Impacto (Amarelo Ouro + Contorno Preto) + Header Oficial.
5. Renderização 9:16 Full HD (1080x1920) otimizada para o algoritmo do TikTok/Reels.
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
TRILHAS_DIR = ASSETS_DIR / "trilhas"
INPUT_AUDIO_DIR = BASE_DIR / "input_audio"

# Importa o serviço de Banco de Vídeos
sys.path.insert(0, str(BASE_DIR))
from services.video_bank_service import VideoBankService

try:
    import edge_tts
except ImportError:
    print("ERRO: Pacote 'edge-tts' não encontrado. Instale com: pip install edge-tts")
    sys.exit(1)

VOZES_DISPONIVEIS = {
    "1": {
        "nome": "Duarte Épico (Masculina Solene)",
        "id": "pt-PT-DuarteNeural",
        "desc": "Tom clássico e imponente de narrativa bíblica/épica (100% Grátis)"
    },
    "2": {
        "nome": "Francisca Firme (Feminina Clara)",
        "id": "pt-BR-FranciscaNeural",
        "desc": "Voz firme, séria e muito articulada (100% Grátis)"
    },
    "3": {
        "nome": "Brian Multilingual (Masculina Moderna)",
        "id": "en-US-BrianMultilingualNeural",
        "desc": "Modelo neural 2025 com cadência moderna em português (100% Grátis)"
    },
    "4": {
        "nome": "Thalita Multilingual (Feminina Fluida)",
        "id": "pt-BR-ThalitaMultilingualNeural",
        "desc": "Voz feminina natural e expressiva (100% Grátis)"
    },
    "5": {
        "nome": "Antonio Clássico (Masculina PT-BR)",
        "id": "pt-BR-AntonioNeural",
        "desc": "Voz masculina sóbria tradicional (100% Grátis)"
    }
}

ROTEIROS_DISPONIVEIS = {
    "1": {
        "titulo": "A Casa Vazia (Mateus 12)",
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
    """Converte segundos para formato H:MM:SS.cs para legendas ASS"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centis = int(round((seconds - int(seconds)) * 100))
    if centis >= 100:
        centis = 99
    return f"{hrs}:{mins:02d}:{secs:02d}.{centis:02d}"

async def sintetizar_audio_e_ass(texto: str, audio_path: Path, ass_path: Path, voz_chave: str = "1"):
    """
    Sintetiza locução natural e gera legendas ASS dinâmicas no estilo aprovado pelo usuário.
    """
    voz_info = VOZES_DISPONIVEIS.get(voz_chave, VOZES_DISPONIVEIS["1"])
    voz_id = voz_info["id"]

    print(f"🎙️ Sintetizando áudio com a voz: '{voz_info['nome']}'...")

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
    print(f"  ✅ Áudio gerado: {audio_path.name} (~{duracao_total:.1f}s)")

    # Divide em blocos de 3 a 5 palavras para leitura rápida na tela
    blocos_ass = []
    for s in sentencas:
        palavras = s["text"].split()
        if len(palavras) <= 4:
            blocos_ass.append((s["start"], s["end"], s["text"].upper()))
        else:
            chunk_size = 4
            partes = [" ".join(palavras[i:i+chunk_size]) for i in range(0, len(palavras), chunk_size)]
            dur_fracao = (s["end"] - s["start"]) / len(partes)
            for idx, parte in enumerate(partes):
                t_ini = s["start"] + (idx * dur_fracao)
                t_fim = t_ini + dur_fracao
                blocos_ass.append((t_ini, t_fim, parte.upper()))

    # Arquivo ASS: Header oficial no topo + Legendas Amarelo Ouro de Alto Contraste
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
Dialogue: 0,0:00:00.00,{format_timestamp_ass(duracao_total + 1.5)},Header,,0,0,0,,⚔ METANOIA // FORJA DE 90 DIAS
"""
    dialogues = []
    for t_ini, t_fim, txt in blocos_ass:
        txt_escapado = txt.replace("{", "").replace("}", "")
        dialogues.append(f"Dialogue: 0,{format_timestamp_ass(t_ini)},{format_timestamp_ass(t_fim)},Subtitle,,0,0,0,,{txt_escapado}")

    ass_path.write_text(ass_template + "\n".join(dialogues), encoding="utf-8")
    print(f"  ✅ Legendas ASS sincronizadas: {len(blocos_ass)} blocos.")
    return duracao_total

def obter_duracao_midia(caminho: Path) -> float:
    """Retorna a duração exata do arquivo via ffprobe"""
    try:
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(caminho)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return float(res.stdout.strip())
    except Exception:
        return 15.0

def criar_montagem_dinamica(duracao_alvo: float, temp_bg_path: Path) -> bool:
    """
    Cria uma montagem dinâmica com cortes a cada 2.5 a 3.0 segundos
    alternando entre fogo, guerreiro, bigorna, tempestade, espada e faíscas.
    """
    clips_disponiveis = list(BG_VIDEOS_DIR.glob("*.mp4"))
    if not clips_disponiveis:
        print("❌ Nenhum clipe encontrado na pasta de vídeos de fundo.")
        return False

    # Embaralha para que cada vídeo tenha uma ordem energética diferente
    random.shuffle(clips_disponiveis)

    # Duração de cada cena (2.5s a 2.8s para dinâmica agressiva do TikTok)
    dur_corte = 2.6
    qtd_cortes = int(duracao_alvo // dur_corte) + 2
    print(f"⚡ Montando fundo dinâmico: {qtd_cortes} cortes rápidos a cada {dur_corte}s...")

    temp_cuts_dir = OUTPUT_DIR / "temp_cuts"
    temp_cuts_dir.mkdir(parents=True, exist_ok=True)

    cut_files = []
    for i in range(qtd_cortes):
        clip = clips_disponiveis[i % len(clips_disponiveis)]
        dur_clip = obter_duracao_midia(clip)
        
        # Ponto de início variado dentro do clipe
        max_start = max(0.0, dur_clip - dur_corte - 1.0)
        t_start = (i * 2.3) % (max_start if max_start > 0 else 1.0)

        cut_file = temp_cuts_dir / f"cut_{i:02d}.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-ss", f"{t_start:.2f}",
            "-t", f"{dur_corte:.2f}",
            "-i", str(clip),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30,eq=brightness=-0.08:contrast=1.2:saturation=0.95",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "22",
            "-an",
            str(cut_file)
        ]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0 and cut_file.exists():
            cut_files.append(cut_file)

    if not cut_files:
        print("❌ Falha ao processar os cortes individuais.")
        return False

    # Concatena os cortes via Demuxer
    concat_txt = temp_cuts_dir / "cuts_list.txt"
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in cut_files:
            p_str = str(c.resolve()).replace("\\", "/")
            f.write(f"file '{p_str}'\n")

    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_txt),
        "-c", "copy",
        str(temp_bg_path)
    ]
    res_c = subprocess.run(cmd_concat, capture_output=True)

    # Limpeza dos arquivos temporários de corte
    try:
        shutil.rmtree(temp_cuts_dir, ignore_errors=True)
    except Exception:
        pass

    if res_c.returncode != 0:
        print("❌ Erro ao concatenar cortes dinâmicos:")
        return False

    print(f"  ✅ Montagem de fundo concluída com {len(cut_files)} cenas dinâmicas.")
    return True

def renderizar_video_completo(audio_vocal: Path, ass_path: Path, output_path: Path, duracao: float):
    """
    Renderiza o vídeo final unindo:
    1. Fundo com cortes rápidos a cada 2.6s
    2. Trilha sonora épica orquestrada com fade-out
    3. Locução e legendas de alto impacto
    """
    temp_bg = OUTPUT_DIR / f"temp_bg_{int(time.time())}.mp4"
    
    # 1. Gera a montagem com cortes dinâmicos
    ok_bg = criar_montagem_dinamica(duracao, temp_bg)
    if not ok_bg:
        return False

    # 2. Verifica a trilha sonora
    trilha_path = TRILHAS_DIR / "trilha_epica.mp3"
    tem_trilha = trilha_path.exists() and trilha_path.stat().st_size > 10_000
    
    ass_escaped = str(ass_path.resolve()).replace("\\", "/").replace(":", "\\:")

    print("🎬 Renderizando vídeo final com Trilha Sonora Épica + Legendas...")

    if tem_trilha:
        print("  🎵 Mixando Trilha Sonora Épica (Trailer Orquestrado) a 18% de volume...")
        # Mixa vocal + trilha sonora em loop com fade-out nos últimos 2 segundos
        filter_complex = (
            f"[0:v]subtitles='{ass_escaped}'[outv];"
            f"[1:a]volume=1.2[vocal];"
            f"[2:a]volume=0.18,aloop=loop=-1:size=2e+09,afade=t=out:st={max(0.1, duracao - 2.0):.2f}:d=2.0[trilha];"
            f"[vocal][trilha]amix=inputs=2:duration=first:dropout_transition=2[outa]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-i", str(temp_bg),
            "-i", str(audio_vocal),
            "-i", str(trilha_path),
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "[outa]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{duracao + 0.3:.2f}",
            str(output_path)
        ]
    else:
        filter_complex = f"[0:v]subtitles='{ass_escaped}'[outv]"
        cmd = [
            "ffmpeg", "-y",
            "-i", str(temp_bg),
            "-i", str(audio_vocal),
            "-filter_complex", filter_complex,
            "-map", "[outv]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", f"{duracao + 0.3:.2f}",
            str(output_path)
        ]

    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0

    # Limpa o arquivo intermediário de background
    if temp_bg.exists():
        temp_bg.unlink(missing_ok=True)

    if res.returncode != 0:
        print("❌ Erro no FFmpeg final:")
        print(res.stderr[-800:])
        return False

    print(f"🎉 VÍDEO CONCLUÍDO COM SUCESSO EM {dt:.1f}s!")
    print(f"📁 Arquivo final: {output_path.resolve()}")
    print(f"📦 Tamanho: {output_path.stat().st_size / (1024*1024):.2f} MB")
    return True

def sanitizar_nome(nome: str) -> str:
    s = re.sub(r'[^a-zA-Z0-9_-]', '_', nome)
    return re.sub(r'_+', '_', s).strip('_')

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    BG_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    TRILHAS_DIR.mkdir(parents=True, exist_ok=True)
    INPUT_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    parser = argparse.ArgumentParser(description="Gerador Cinemático Viral de Vídeos Metanoia")
    parser.add_argument("--roteiro", type=str, help="Número do roteiro (1 a 5)")
    parser.add_argument("--voz", type=str, default="1", help="Voz (1: Duarte Épico, 2: Francisca, 3: Brian, 4: Thalita, 5: Antonio)")
    parser.add_argument("--audio_proprio", type=str, help="Caminho de um arquivo de áudio gravado por você (.mp3, .m4a)")
    parser.add_argument("--texto", type=str, help="Texto personalizado para o vídeo")
    parser.add_argument("--nome", type=str, help="Nome do arquivo de saída")
    args = parser.parse_args()

    print("=" * 70)
    print("⚔️  METANOIA // GERADOR AUTOMÁTICO DE VÍDEOS VIRAIS (ALTA RETENÇÃO)")
    print("=" * 70)

    # 1. Garante que os bancos de vídeo estejam abastecidos
    bank_service = VideoBankService()
    if len(bank_service.listar_videos_locais()) < 4:
        print("📥 Abastecendo acervo com clipes cinematográficos dos bancos de vídeo...")
        for tema in ["sparks fire", "blacksmith anvil", "dark warrior", "ocean storm"]:
            bank_service.obter_video_para_tema(tema)

    texto_final = ""
    prefixo = "metanoia_viral"

    if args.audio_proprio:
        audio_in = Path(args.audio_proprio)
        if not audio_in.exists():
            print(f"❌ Arquivo de áudio não encontrado: {audio_in}")
            return
        prefixo = f"metanoia_voz_propria_{sanitizar_nome(audio_in.stem)}"
        duracao = obter_duracao_midia(audio_in)
        temp_audio = audio_in
        # Legenda genérica para áudio próprio
        temp_ass = OUTPUT_DIR / f"{prefixo}_legendas.ass"
        temp_ass.write_text(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Header,Arial,34,&H000C58EA,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,8,30,30,140,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{format_timestamp_ass(duracao + 1.5)},Header,,0,0,0,,⚔ METANOIA // FORJA DE 90 DIAS
""", encoding="utf-8")
        video_final = OUTPUT_DIR / f"{prefixo}.mp4"
        sucesso = renderizar_video_completo(temp_audio, temp_ass, video_final, duracao)
        return

    if args.texto:
        texto_final = args.texto
        prefixo = sanitizar_nome(args.nome or "custom")
    elif args.roteiro and args.roteiro in ROTEIROS_DISPONIVEIS:
        item = ROTEIROS_DISPONIVEIS[args.roteiro]
        texto_final = item["texto"]
        prefixo = f"metanoia_roteiro_{args.roteiro}_{sanitizar_nome(item['titulo'])[:25]}"
    else:
        print("\n📜 ESCOLHA O ROTEIRO:")
        for k, v in ROTEIROS_DISPONIVEIS.items():
            print(f"  [{k}] {v['titulo']}")
            print(f"      Gancho: \"{v['hook']}\"\n")
        print("  [C] Escrever meu próprio texto")

        escolha = input("\n👉 Digite o número do roteiro (1 a 5) ou C: ").strip().upper()
        if escolha in ROTEIROS_DISPONIVEIS:
            item = ROTEIROS_DISPONIVEIS[escolha]
            texto_final = item["texto"]
            prefixo = f"metanoia_roteiro_{escolha}_{sanitizar_nome(item['titulo'])[:25]}"
        elif escolha == "C":
            texto_final = input("\nCole o texto da locução aqui:\n").strip()
            if not texto_final:
                print("Texto vazio. Abortando.")
                return
            prefixo = "metanoia_custom"
        else:
            item = ROTEIROS_DISPONIVEIS["4"]
            texto_final = item["texto"]
            prefixo = "metanoia_roteiro_4"

    voz_escolhida = args.voz
    if not args.roteiro and not args.texto:
        print("\n🎙️ ESCOLHA A VOZ DA NARRATIVA (100% GRÁTIS):")
        for k, v in VOZES_DISPONIVEIS.items():
            print(f"  [{k}] {v['nome']} - {v['desc']}")
        print("  [P] Usar um áudio gravado no meu celular (.mp3 na pasta input_audio)")
        v_input = input(f"\n👉 Escolha a voz (padrão 1 - Duarte Épico): ").strip()
        if v_input in VOZES_DISPONIVEIS:
            voz_escolhida = v_input
        elif v_input.upper() == "P":
            audios_user = list(INPUT_AUDIO_DIR.glob("*.*"))
            if audios_user:
                print(f"Usando seu arquivo de áudio: {audios_user[0].name}")
                # Executa com áudio próprio
                duracao = obter_duracao_midia(audios_user[0])
                temp_ass = OUTPUT_DIR / f"{prefixo}_legendas.ass"
                temp_ass.write_text(f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Header,Arial,34,&H000C58EA,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,8,30,30,140,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,{format_timestamp_ass(duracao + 1.5)},Header,,0,0,0,,⚔ METANOIA // FORJA DE 90 DIAS
""", encoding="utf-8")
                video_final = OUTPUT_DIR / f"{prefixo}.mp4"
                renderizar_video_completo(audios_user[0], temp_ass, video_final, duracao)
                return
            else:
                print(f"Coloque seu arquivo de áudio (.mp3 ou .m4a) na pasta '{INPUT_AUDIO_DIR}'. Usando voz 1.")
                voz_escolhida = "1"

    temp_audio = OUTPUT_DIR / f"{prefixo}_audio.mp3"
    temp_ass = OUTPUT_DIR / f"{prefixo}_legendas.ass"
    video_final = OUTPUT_DIR / f"{prefixo}.mp4"

    # 1. Sintetiza áudio e gera legendas ASS
    duracao = asyncio.run(sintetizar_audio_e_ass(texto_final, temp_audio, temp_ass, voz_chave=voz_escolhida))

    # 2. Renderiza vídeo com cortes dinâmicos + trilha sonora épica
    sucesso = renderizar_video_completo(temp_audio, temp_ass, video_final, duracao)

    if sucesso:
        print("\n" + "=" * 70)
        print("🚀 VÍDEO CINEMÁTICO PRONTO COM CORTES RÁPIDOS E TRILHA ÉPICA!")
        print(f"▶️  Arquivo gerado:")
        print(f"    file:///{str(video_final.resolve()).replace(chr(92), '/')}")
        print("=" * 70)

if __name__ == "__main__":
    main()
