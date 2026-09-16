"""
Conselheiro de Guerra do METANOIA.
Inteligência Artificial especializada em desintoxicação de dopamina, quebra da pornografia
e edificação bíblica para homens de 18 a 35 anos.
Base de conhecimento: Gary Wilson, Tim Chester, Miguel Soriani e C.S. Lewis.
"""
import os
import urllib.request
import urllib.error
import json
from typing import List, Dict, Any

PROMPT_SISTEMA_METANOIA = """Você é o Conselheiro de Guerra do METANOIA. 
Seu papel é falar com homens jovens e adultos (18 a 35 anos) que estão lutando contra vícios sexuais, pornografia, masturbação compulsiva, falta de disciplina e crise espiritual.

Suas diretrizes fundamentais:
1. Tom de Voz: Firme, sóbrio, fraterno e acolhedor (como um irmão mais velho na fé ou um comandante no campo de batalha). Sem julgamentos hipócritas, sem rodeios e sem infantilidade.
2. Fundamentação Dupla (Ciência + Bíblia):
   - Cite a neurociência quando pertinente: receptores de dopamina, Efeito Chaser (compulsão pós-recaída), gatilhos HALT (Fome, Raiva, Solidão, Cansaço).
   - Aponte para a Cruz e para a Graça: Cristo não condena o homem que busca a luz; o perdão é real e restaura a honra do homem.
3. Resposta a Crises (SOS): Se o homem disser que está com vontade ou quase caindo:
   - Dê ordens físicas imediatas: "Larga o celular agora. Lave o rosto com água fria. Faça 20 flexões."
   - Explique que a vontade é uma onda de 3 minutos que passa se ele não alimentar o pensamento.
4. Tamanho: Seja direto, profundo e conciso (máximo de 2 a 3 parágrafos curtos). Finalize com um desafio prático de ação imediata."""

class AIAdvisorService:
    @classmethod
    def responder(cls, mensagem_usuario: str) -> str:
        # Fallback local imediato com sabedoria cirúrgica
        msg_lower = mensagem_usuario.lower()

        if any(w in msg_lower for w in ["recai", "recaí", "perdi", "falhei", "fracassei", "lixo"]):
            return (
                "Pare tudo e me ouça com atenção agora. O que você está sentindo é a mentira da acusação.\n\n"
                "Biologicamente, você ativou o 'Efeito Chaser' (Gary Wilson): seu cérebro vai tentar te convencer nas próximas 24h de que 'já que você caiu, pode cair de novo'. Isso é uma mentira da dopamina desregulada. Teologicamente: 1 João 1:9 diz que se confessarmos, Ele nos purifica de TODA injustiça.\n\n"
                "Você NÃO perdeu a batalha da sua vida. Levante dessa cadeira agora, lave o rosto com água bem gelada, dobre os joelhos por 60 segundos entregando essa vergonha na cruz, e recomece com a cabeça erguida. O justo cai sete vezes e se levanta."
            )

        if any(w in msg_lower for w in ["socorro", "ajuda", "vontade", "tentacao", "tentação", "fissura", "caindo"]):
            return (
                "LARGUE ESSE CELULAR NA MESA AGORA. Dê 3 passos para trás.\n\n"
                "A vontade do vício é uma onda química que atinge o pico em 3 minutos e quebra. Você não tem que lutar contra a onda, você só tem que não alimentá-la. Vá até a pia, jogue água gelada nos olhos e no pescoço (isso força seu coração a desacelerar) e faça 20 flexões no chão agora.\n\n"
                "Você é um homem comprado por sangue precioso. Não troque sua honra por 30 segundos de prazer roubado."
            )

        if any(w in msg_lower for w in ["casamento", "esposa", "namorada", "ereção", "brochei", "disfunção"]):
            return (
                "A pornografia adoece a capacidade do homem de se conectar com uma mulher real de carne e osso. O cérebro foi condicionado a dezenas de estímulos artificiais por minuto, e por isso o corpo 'trava' na realidade.\n\n"
                "A boa notícia da neuroplasticidade é que seu cérebro se REGENERA. Com 30 a 60 dias de sobriedade radical (sem telas, sem estímulos impuros), seus receptores de dopamina retornam ao nível normal e sua sensibilidade volta. Guarde seus olhos hoje para honrar sua esposa amanhã."
            )

        # Resposta padrão orientadora
        return (
            "A batalha pela mente é vencida nas primeiras horas da manhã e nas últimas da noite.\n\n"
            "Provérbios 4:23 nos manda: 'Sobre tudo o que se deve guardar, guarda o teu coração, porque dele procedem as fontes da vida'. O homem que aprende a governar os próprios impulsos não pode ser escravizado por nada neste mundo.\n\n"
            "Qual é o maior atrito que você está enfrentando hoje para manter o seu foco?"
        )
