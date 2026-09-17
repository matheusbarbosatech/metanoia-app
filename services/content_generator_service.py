import os
import sys
import json
import requests
from pathlib import Path

# Suporte UTF-8 no terminal Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent

def carregar_env():
    """Carrega variáveis do arquivo .env"""
    env = {}
    p = BASE_DIR / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env

PILARES_METANOIA = {
    "ordem_matinal": {
        "id": "ordem_matinal",
        "nome": "Ordem Matinal das 06h",
        "icone": "🌅",
        "foco": "Acordar sem tocar no celular, joelho no chão, banho gelado, foco e quebra da preguiça."
    },
    "dopamina_telas": {
        "id": "dopamina_telas",
        "nome": "Vício em Dopamina & Celular",
        "icone": "🧠",
        "foco": "Cérebro frito, feeds infinitos, Gary Wilson, cansaço crônico e falta de atenção."
    },
    "alianca_zap": {
        "id": "alianca_zap",
        "nome": "Aliança de Honra no WhatsApp",
        "icone": "🛡️",
        "foco": "Fim da solidão, pacto sagrado 1 a 1 às 21h30, Provérbios 27:17, ninguém luta sozinho."
    },
    "sacerdocio_lar": {
        "id": "sacerdocio_lar",
        "nome": "Sacerdócio do Lar & Casamento",
        "icone": "💍",
        "foco": "Honra à esposa, liderança espiritual da família, oração pelos filhos e exemplo moral."
    },
    "sala_emergencia": {
        "id": "sala_emergencia",
        "nome": "A Sala de Emergência (Anti-Porn)",
        "icone": "⚔️",
        "foco": "A batalha das 23h, choque vagal, teologia da graça, o justo cai e se levanta."
    },
    "governo_financeiro": {
        "id": "governo_financeiro",
        "nome": "Governo Financeiro & Fim das Bets",
        "icone": "🪙",
        "foco": "Morte às apostas e atalhos fáceis, trabalho duro, domínio próprio e provisão familiar."
    },
    "tempera_guerreiro": {
        "id": "tempera_guerreiro",
        "nome": "A Têmpera do Guerreiro & Jejum",
        "icone": "🔥",
        "foco": "Jejum bíblico, disciplina militar, domínio sobre a carne e 1 João 2:14."
    }
}

class ContentGeneratorService:
    """
    Serviço de Geração de Roteiros e Ideias com IA:
    - Primário: DevWorld AI (Claude 3.5 Sonnet / Claude Opus Ilimitado -f)
    - Secundário: Google Gemini 1.5
    """
    def __init__(self):
        self.env = carregar_env()
        self.devworld_key = self.env.get("DEVWORLD_API_KEY", "")
        self.devworld_base = self.env.get("DEVWORLD_BASE_URL", "https://chat.devwservices.shop/v1")
        self.devworld_model = self.env.get("DEVWORLD_MODEL", "devworld/claude-sonnet-5-r")
        self.gemini_key = self.env.get("GEMINI_API_KEY", "")

    def listar_pilares(self):
        return list(PILARES_METANOIA.values())

    def gerar_roteiro_ia(self, pilar_id: str = "ordem_matinal", tom: str = "Confrontador e Sóbrio", modo_modelo: str = "alta_velocidade"):
        """
        Gera um roteiro viral decupado cena a cena para o METANOIA em formato JSON estruturado.
        """
        pilar_info = PILARES_METANOIA.get(pilar_id, PILARES_METANOIA["ordem_matinal"])

        # Seleciona o modelo DevWorld de acordo com o modo
        modelo_escolhido = self.devworld_model
        if modo_modelo == "ilimitado":
            modelo_escolhido = "devworld/claude-opus-5-f"
        elif modo_modelo == "alta_velocidade":
            modelo_escolhido = "devworld/claude-sonnet-5-r"

        system_prompt = f"""Você é o Head Copywriter e Diretor Criativo do projeto 'METANOIA // A Forja dos 90 Dias'.
Sua missão é criar um roteiro de vídeo curto viral (para TikTok, Instagram Reels e YouTube Shorts) de 30 a 40 segundos de altíssima retenção.

DIRETRIZES DA MARCA:
- Público: Homens cristãos de 22 a 45 anos que querem disciplina, pureza, liderança do lar e força espiritual.
- Tom de voz: {tom}. Sem clichês religiosos fofos, sem autoajuda rasa. Tom de homem para homem, bíblico, maduro e militar.
- Blindagem de anúncios: NUNCA use palavras banidas (não fale 'pornografia', fale 'escravo do celular', 'impureza no secreto', 'dopamina roubada', 'batalha das 23h').
- Call to Action: Sempre direcionar para 'A Prova de Fogo de 7 Dias' ou 'A Forja dos 90 Dias' no link da bio.

FORMATO DE RESPOSTA OBRIGATÓRIO (APENAS JSON VÁLIDO, SEM MARKDOWN FORA DO JSON):
{{
  "titulo": "Título Curto de Alto Impacto",
  "pilar": "{pilar_info['nome']}",
  "hook_3s": "Gancho verbal dos primeiros 3 segundos",
  "texto_locucao": "Texto corrido completo que será lido pela voz neural (de 30 a 40 segundos, aprox 70 a 90 palavras)",
  "cenas": [
    {{
      "tempo": "00s - 04s",
      "fala": "trecho da fala",
      "visual": "descrição em português do que aparece na tela",
      "broll_query_en": "termo cirúrgico em inglês para buscar no Pexels (ex: man looking at phone dark room bed)"
    }},
    {{
      "tempo": "04s - 09s",
      "fala": "trecho da fala",
      "visual": "descrição em português",
      "broll_query_en": "termo em inglês"
    }},
    {{
      "tempo": "09s - 15s",
      "fala": "trecho da fala",
      "visual": "descrição em português",
      "broll_query_en": "termo em inglês"
    }},
    {{
      "tempo": "15s - 22s",
      "fala": "trecho da fala",
      "visual": "descrição em português (a virada positiva)",
      "broll_query_en": "termo em inglês"
    }},
    {{
      "tempo": "22s - 28s",
      "fala": "trecho da fala",
      "visual": "descrição em português",
      "broll_query_en": "termo em inglês"
    }},
    {{
      "tempo": "28s - 35s",
      "fala": "trecho da fala e CTA",
      "visual": "descrição em português",
      "broll_query_en": "termo em inglês"
    }}
  ],
  "legenda_post": "Legenda completa para colar no Instagram/TikTok com chamada para comentar FORJA",
  "hashtags": "#metanoia #homensdehonra #disciplina #ordemmatinal #cristao"
}}
"""

        user_prompt = f"Crie um roteiro viral inédito e magnético focado no pilar: '{pilar_info['nome']}'.\nTema central: {pilar_info['foco']}\nLembre-se de retornar APENAS o JSON puro."

        # 1. Tentativa via DevWorld
        if self.devworld_key:
            try:
                headers = {
                    "Authorization": f"Bearer {self.devworld_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": modelo_escolhido,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1500
                }
                res = requests.post(f"{self.devworld_base}/chat/completions", headers=headers, json=payload, timeout=25)
                if res.status_code == 200:
                    raw_content = res.json()["choices"][0]["message"]["content"].strip()
                    # Limpa blocos de markdown ```json ... ``` se houver
                    clean_json = re.sub(r"^```json\s*", "", raw_content, flags=re.IGNORECASE)
                    clean_json = re.sub(r"^```\s*", "", clean_json)
                    clean_json = re.sub(r"\s*```$", "", clean_json).strip()
                    data = json.loads(clean_json)
                    data["fonte_ia"] = f"DevWorld ({modelo_escolhido})"
                    return data
            except Exception as e:
                print(f"⚠️ Erro ao gerar via DevWorld ({modelo_escolhido}): {e}. Tentando modelo alternativo...")

        # 2. Fallback de alta velocidade na DevWorld se o -f falhar
        if modelo_escolhido != "devworld/claude-sonnet-5-r" and self.devworld_key:
            try:
                payload["model"] = "devworld/claude-sonnet-5-r"
                res = requests.post(f"{self.devworld_base}/chat/completions", headers=headers, json=payload, timeout=20)
                if res.status_code == 200:
                    raw_content = res.json()["choices"][0]["message"]["content"].strip()
                    clean_json = re.sub(r"^```json\s*", "", raw_content, flags=re.IGNORECASE)
                    clean_json = re.sub(r"^```\s*", "", clean_json)
                    clean_json = re.sub(r"\s*```$", "", clean_json).strip()
                    data = json.loads(clean_json)
                    data["fonte_ia"] = "DevWorld (claude-sonnet-5-r Fallback)"
                    return data
            except Exception as e:
                print(f"⚠️ Erro no fallback DevWorld: {e}")

        # 3. Fallback estruturado de alta qualidade caso as APIs de rede oscilem
        return self._roteiro_backup(pilar_id)

    def _roteiro_backup(self, pilar_id: str):
        """Retorna roteiro pré-configurado de alta conversão para contingência"""
        pilar_info = PILARES_METANOIA.get(pilar_id, PILARES_METANOIA["ordem_matinal"])
        return {
            "titulo": f"A Guerra Secreta: {pilar_info['nome']}",
            "pilar": pilar_info["nome"],
            "hook_3s": "A primeira escolha do seu dia decide quem é o dono da sua vida.",
            "texto_locucao": (
                "A primeira escolha do seu dia decide quem é o dono da sua vida. "
                "Se ao acordar você já abre o celular na cama, a sua mente foi sequestrada antes de falar com Deus. "
                "Você absorve o ruído de estranhos e passa o dia sem foco e sem paz. "
                "Homens livres têm um Altar Matinal: pés no chão, joelho dobrado e palavra antes do mundo. "
                "A Forja METANOIA te guia dia após dia por 90 dias. "
                "O link da sua prova de 7 dias está na bio."
            ),
            "cenas": [
                {"tempo": "00s - 05s", "fala": "A primeira escolha do seu dia decide quem é o dono da sua vida.", "visual": "Mão procurando o celular no escuro no criado-mudo", "broll_query_en": "alarm waking up phone dark bedroom"},
                {"tempo": "05s - 11s", "fala": "Se ao acordar você já abre o celular na cama, a sua mente foi sequestrada.", "visual": "Luz azul do celular refletida nos olhos cansados", "broll_query_en": "scrolling social media bed morning light"},
                {"tempo": "11s - 17s", "fala": "Você absorve o ruído de estranhos e passa o dia sem foco e sem paz.", "visual": "Homem exausto com a mão na testa na mesa de trabalho", "broll_query_en": "tired businessman rubbing eyes office desk"},
                {"tempo": "17s - 24s", "fala": "Homens livres têm um Altar Matinal: pés no chão, joelho dobrado e palavra.", "visual": "Homem ajoelhado orando na alvorada com luz do sol", "broll_query_en": "man praying knee sunrise morning"},
                {"tempo": "24s - 30s", "fala": "A Forja METANOIA te guia dia após dia por noventa dias.", "visual": "Bíblia aberta na mesa rústica / homem lavando o rosto com água gelada", "broll_query_en": "bible open sunlight table"},
                {"tempo": "30s - 36s", "fala": "O link da sua prova de sete dias está na bio.", "visual": "Homem em pé com postura firme encarando o horizonte / Selo Metanoia", "broll_query_en": "confident man outdoors sunrise determined"}
            ],
            "legenda_post": f"⚔️ Não comece o seu dia derrotado pela tela. A sua mente pertence a Deus.\n\nComente 'FORJA' e receba o acesso da Prova de 7 Dias no seu direct.",
            "hashtags": "#metanoia #ordemmatinal #disciplina #homensdehonra #fe",
            "fonte_ia": "Catálogo Mestre METANOIA"
        }
