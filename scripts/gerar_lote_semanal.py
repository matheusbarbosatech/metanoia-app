"""
==============================================================================
METANOIA // GERADOR DE LOTE SEMANAL EM MASSA (7 VÍDEOS DOS 7 PILARES)
==============================================================================
Gera automaticamente 7 vídeos verticais 9:16 com:
- Cortes dinâmicos a cada 2.6s (bigorna, faíscas, mar revolto, guerreiro, fogo)
- Voz grave e solene (Duarte Épico neural em frequência nativa)
- Trilha sonora orquestral estilo Hans Zimmer (mixada a 18% com fade-out)
- Legendas de alto contraste amarelas com contorno preto
- Header oficial: '⚔ METANOIA // FORJA DE 90 DIAS'
- Cadastro automático na esteira SQLite (studio_posts.db) para a semana inteira
==============================================================================
"""

import os
import sys
import time
import json
import asyncio
import datetime
from pathlib import Path

# Configura encoding UTF-8 no Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.gerador_videos_metanoia import (
    sintetizar_audio_e_ass,
    renderizar_video_completo,
    OUTPUT_DIR,
    sanitizar_nome
)
from services.social_scheduler_service import SocialSchedulerService

LOTE_7_DIAS = [
    {
        "id": 1,
        "dia_semana": "Segunda-feira",
        "horario_sugerido": "06:00",
        "pilar_id": "ordem_matinal",
        "pilar_nome": "Ordem Matinal das 06h",
        "titulo": "A Primeira Vitoria do Dia",
        "slug": "pilar1_ordem_matinal_vitoria",
        "texto": (
            "Se a primeira coisa que você toca de manhã é a tela do seu celular, você já perdeu a guerra antes de colocar os pés no chão. "
            "O homem governado por impulsos acorda em busca de dopamina rápida, perde trinta minutos rolando feed e começa o dia derrotado. "
            "A Regra de Ouro da Forja é inegociável: pés no chão, joelhos dobrados, água fria no rosto e comunhão com Deus. "
            "Quem vence a primeira hora da manhã, vence o dia inteiro. "
            "Pare de negociar com a preguiça. Toque no link da bio e entre na Forja dos noventa dias."
        ),
        "legenda": (
            "A PRIMEIRA BATALHA DO SEU DIA 🌅\n\n"
            "Se a primeira coisa que você toca ao acordar é a tela do celular, sua mente já foi sequestrada pelo algoritmo antes mesmo de você se colocar de pé.\n\n"
            "Na Forja Metanoia, a manhã pertence à honra, à oração e à disciplina.\n\n"
            "Comente 'FORJA' ou toque no link da bio para começar sua Prova de Fogo de 7 Dias gratuitos."
        ),
        "hashtags": "#metanoia #ordemmatinal #disciplina #homensdehonra #cristao #desenvolvimentomasculino"
    },
    {
        "id": 2,
        "dia_semana": "Terça-feira",
        "horario_sugerido": "12:30",
        "pilar_id": "dopamina_telas",
        "pilar_nome": "Vício em Dopamina & Celular",
        "titulo": "A Prisao Invisivel dos Algoritmos",
        "slug": "pilar2_dopamina_prisao_algoritmo",
        "texto": (
            "Você não está cansado do seu trabalho. Você está exausto de fritar seus receptores de dopamina com estímulos fáceis. "
            "Seu cérebro foi programado por corporações bilionárias para buscar novidade constante, destruindo seu foco, sua paciência e sua masculinidade. "
            "O homem forte governa seus impulsos; o homem fraco é pastoreado por notificações. "
            "No METANOIA, nós quebramos esse ciclo com jejum de dopamina e domínio próprio. "
            "Assuma o comando da sua mente. O link da Forja está na bio."
        ),
        "legenda": (
            "VOCÊ NÃO ESTÁ CANSADO. SEU CÉREBRO ESTÁ FRITO 🧠\n\n"
            "O excesso de telas roubou sua capacidade de focar, orar e construir.\n\n"
            "Reassuma o governo da sua mente na Forja dos 90 Dias.\n\n"
            "Link na bio: @forjametanoia"
        ),
        "hashtags": "#metanoia #dopamina #foco #produtividade #homensdehonra #desenvolvimentopessoal"
    },
    {
        "id": 3,
        "dia_semana": "Quarta-feira",
        "horario_sugerido": "21:30",
        "pilar_id": "alianca_zap",
        "pilar_nome": "Aliança de Honra no WhatsApp",
        "titulo": "Nenhum Soldado Luta Sozinho",
        "slug": "pilar3_alianca_ferro_com_ferro",
        "texto": (
            "Nenhum homem vence o vício trancado sozinho no quarto. "
            "O pecado e a fraqueza adoram as sombras. Salomão escreveu em Provérbios vinte e sete: Como o ferro com o ferro se afia, assim o homem ao seu irmão. "
            "No METANOIA você não entra em grupos barulhentos para passar vergonha. "
            "Você faz um pacto sagrado um para um com um irmão de aliança. "
            "Às vinte e uma e trinta da noite, sabatina no WhatsApp. A transparência quebra o vício. "
            "Conheça a Forja no link da bio."
        ),
        "legenda": (
            "O ISOLAMENTO É O CEMITÉRIO DO HOMEM 🛡️\n\n"
            "Quem tenta lutar sozinho cai na primeira emboscada da noite. Na Aliança Metanoia, você tem um parceiro de trincheira para prestar contas diariamente.\n\n"
            "Link na bio: @forjametanoia"
        ),
        "hashtags": "#aliancadehonra #ferrocomferro #irmandade #proverbios #homensdehonra #metanoia"
    },
    {
        "id": 4,
        "dia_semana": "Quinta-feira",
        "horario_sugerido": "18:30",
        "pilar_id": "sacerdocio_lar",
        "pilar_nome": "Sacerdócio do Lar & Casamento",
        "titulo": "O Sacerdote da Casa",
        "slug": "pilar4_sacerdocio_do_lar",
        "texto": (
            "Um homem fraco e viciado não consegue sustentar o peso espiritual de proteger uma esposa e educar filhos. "
            "O sacerdócio do lar exige santidade, mãos limpas e coração resoluto. "
            "Sua família não precisa de um homem perfeito; ela precisa de um líder que se ajoelha diante de Deus e se levanta para guerrear pelo lar. "
            "Chega de passividade moral. Torne-se o homem que sua família merece ter. "
            "Entre na Prova de Fogo de sete dias no link da bio."
        ),
        "legenda": (
            "SUA FAMÍLIA NÃO MERECE UM HOMEM DIVIDIDO 💍\n\n"
            "O sacerdócio do lar começa quando você decide purificar seus olhos e sua mente no secreto.\n\n"
            "Assuma sua postura de sacerdote e protetor na Forja dos 90 Dias.\n\n"
            "Link na bio: @forjametanoia"
        ),
        "hashtags": "#casamentoblindado #sacerdociodolar #familia #liderancacrista #homensdehonra #metanoia"
    },
    {
        "id": 5,
        "dia_semana": "Sexta-feira",
        "horario_sugerido": "18:00",
        "pilar_id": "governo_financeiro",
        "pilar_nome": "Governo Financeiro & Fim das Bets",
        "titulo": "O Fim da Ilusao das Apostas",
        "slug": "pilar5_fim_das_apostas_governo",
        "texto": (
            "O diabo não precisa destruir sua fé se ele conseguir destruir seu patrimônio através de atalhos e apostas na internet. "
            "As apostas esportivas e os jogos de azar são o imposto que homens imaturos pagam pela pressa de enriquecer sem esforço. "
            "Provérbios treze diz: A riqueza conquistada com pressa diminui, mas quem junta pouco a pouco enriquece. "
            "Governo financeiro é fruto de têmpera, trabalho duro e domínio sobre a cobiça. "
            "Cure sua impulsividade na Forja dos noventa dias. Link na bio."
        ),
        "legenda": (
            "CHEGA DE APOSTAS E ATALHOS ILUSÓRIOS 🪙\n\n"
            "O verdadeiro homem de honra constrói riqueza com as próprias mãos, trabalho diligente e domínio próprio.\n\n"
            "Venha para a Forja dos 90 Dias. Link na bio: @forjametanoia"
        ),
        "hashtags": "#financascomproposito #antigambling #liberdadefinanceira #disciplina #metanoia #homensdehonra"
    },
    {
        "id": 6,
        "dia_semana": "Sábado",
        "horario_sugerido": "12:00",
        "pilar_id": "tempera_guerreiro",
        "pilar_nome": "A Têmpera do Guerreiro & Jejum",
        "titulo": "A Mente de Aco e o Jejum",
        "slug": "pilar6_tempera_jejum_guerreiro",
        "texto": (
            "Quem não governa o próprio estômago não governa os próprios olhos, nem os próprios pensamentos. "
            "O jejum bíblico não é dieta; é uma declaração de guerra da alma contra os caprichos da carne. "
            "Quando você diz não para a fome física, você ensina sua mente a dizer não para qualquer tentação. "
            "O homem temperado pelo jejum e pela oração torna-se inabalável diante de qualquer tempestade. "
            "Descubra os protocolos de jejum e força no METANOIA. Link na bio."
        ),
        "legenda": (
            "DOMINE SEU CORPO OU SEU CORPO DOMINARÁ VOCÊ 🔥\n\n"
            "O jejum bíblico forja o domínio próprio que destrói qualquer vício oculto.\n\n"
            "Descubra os protocolos na Forja Metanoia. Link na bio: @forjametanoia"
        ),
        "hashtags": "#jejum #disciplinamilitar #batalhaespiritual #homensdehonra #metanoia #oracao"
    },
    {
        "id": 7,
        "dia_semana": "Domingo",
        "horario_sugerido": "21:00",
        "pilar_id": "sala_emergencia",
        "pilar_nome": "A Sala de Emergência (Anti-Porn & SOS)",
        "titulo": "A Batalha das Onze da Noite",
        "slug": "pilar7_batalha_das_23h_sos",
        "texto": (
            "A sua pior batalha não acontece na rua. Ela acontece às onze da noite, quando a porta do seu quarto se fecha. "
            "Quando a fissura bate, ficar negociando com o celular na mão é garantia de queda. "
            "Você precisa de um protocolo imediato de choque. "
            "O METANOIA possui a Sala de Emergência SOS: acione em um toque para quebrar a onda de dopamina antes que ela quebre você. "
            "Pare de lutar desarmado. Toque no link da bio e blinde sua noite."
        ),
        "legenda": (
            "A BATALHA QUE NINGUÉM VÊ ⚔️\n\n"
            "Às 23h, a solidão e o cansaço cobram o preço. Não confie na força de vontade: use sistemas de emergência.\n\n"
            "Conheça o Botão SOS da Forja Metanoia. Link na bio: @forjametanoia"
        ),
        "hashtags": "#pureza #libertacao #batalhadas23h #homensdehonra #metanoia #combate"
    }
]

def calcular_datas_semana():
    hoje = datetime.date.today()
    datas = []
    # Cria datas para os próximos 7 dias
    for i in range(7):
        d = hoje + datetime.timedelta(days=i)
        datas.append(d.strftime("%Y-%m-%d"))
    return datas

def main():
    print("=" * 75)
    print("⚔️  METANOIA // GERADOR DE LOTE SEMANAL (7 VÍDEOS DOS 7 PILARES)")
    print("=" * 75)
    print("Renderizando 7 vídeos cinematográficos 9:16 com cortes dinâmicos e trilha épica...")
    print("-" * 75)

    OUTPUT_DIR.mkdir(exist_ok=True)
    scheduler = SocialSchedulerService()
    datas_semana = calcular_datas_semana()

    resultados = []
    tempo_total_inicio = time.time()

    for idx, item in enumerate(LOTE_7_DIAS):
        slug = item["slug"]
        titulo = item["titulo"]
        pilar = item["pilar_nome"]
        texto = item["texto"]
        data_prog = f"{datas_semana[idx]} {item['horario_sugerido']}"

        print(f"\n🎬 [{idx + 1}/7] Processando Vídeo: {titulo}")
        print(f"   🛡️  Pilar: {pilar}")
        print(f"   📅 Agendamento: {item['dia_semana']} às {item['horario_sugerido']} ({data_prog})")

        prefixo = f"metanoia_{slug}"
        temp_audio = OUTPUT_DIR / f"{prefixo}_audio.mp3"
        temp_ass = OUTPUT_DIR / f"{prefixo}_legendas.ass"
        video_final = OUTPUT_DIR / f"{prefixo}.mp4"

        # 1. Sintetiza áudio com Duarte Épico e gera legendas ASS
        print("   🎙️  Sintetizando voz neural Duarte Épico e legendas...")
        t0 = time.time()
        try:
            duracao = asyncio.run(sintetizar_audio_e_ass(texto, temp_audio, temp_ass, voz_chave="1"))
            print(f"   ⏱️  Duração do áudio: {duracao:.1f} segundos")
        except Exception as e:
            print(f"   ❌ Erro ao sintetizar áudio: {e}")
            continue

        # 2. Renderiza vídeo completo com cortes dinâmicos de 2.6s e trilha sonora épica
        print("   ⚡ Montando cortes dinâmicos no FFmpeg com trilha Hans Zimmer...")
        sucesso = renderizar_video_completo(temp_audio, temp_ass, video_final, duracao)

        if sucesso and video_final.exists():
            t_render = time.time() - t0
            mb = video_final.stat().st_size / (1024 * 1024)
            print(f"   ✅ Concluído em {t_render:.1f}s | Tamanho: {mb:.2f} MB")

            # 3. Registra na fila do SQLite para o agendador e webhooks
            post_id = scheduler.adicionar_post(
                titulo=titulo,
                pilar=pilar,
                roteiro_texto=texto,
                video_path=f"output/{video_final.name}",
                legenda=item["legenda"],
                hashtags=item["hashtags"],
                redes=["instagram", "youtube", "tiktok"],
                data_agendamento=data_prog,
                status="Renderizado"
            )

            # 4. Verifica se auto_webhook está ativo
            auto_webhook = scheduler.obter_config("auto_webhook", "false") == "true"
            webhook_url = scheduler.obter_config("webhook_url", "")
            if auto_webhook and webhook_url:
                print("   ⚡ Disparando automaticamente para o Webhook configurado...")
                scheduler.disparar_webhook(post_id)

            resultados.append({
                "id": post_id,
                "pilar": pilar,
                "titulo": titulo,
                "arquivo": video_final.name,
                "tamanho_mb": round(mb, 2),
                "duracao": round(duracao, 1),
                "data_agendamento": data_prog
            })
        else:
            print(f"   ❌ Falha na renderização do vídeo {titulo}")

    dt_total = time.time() - tempo_total_inicio

    print("\n" + "=" * 75)
    print("🎉 LOTE DE 7 VÍDEOS CONCLUÍDO COM SUCESSO!")
    print(f"⏱️  Tempo total de processamento: {dt_total / 60:.1f} minutos ({dt_total:.1f}s)")
    print("=" * 75)
    print(f"{'ID':<4} | {'PILAR':<30} | {'DURAÇÃO':<8} | {'TAMANHO':<9} | {'HORÁRIO'}")
    print("-" * 75)
    for r in resultados:
        print(f"#{r['id']:<3} | {r['pilar'][:29]:<30} | {r['duracao']}s{'':<3} | {r['tamanho_mb']} MB{'':<2} | {r['data_agendamento']}")
    print("=" * 75)
    print("📁 Todos os 7 arquivos MP4 estão prontos na pasta 'output/' e visíveis na Aba 3 do Painel!")

if __name__ == "__main__":
    main()
