"""
Banco de Dados Local SQLite do METANOIA (100% Offline-First).
Armazena o progresso do homem, o contador de sobriedade/dias limpos,
o protocolo da Ordem Matinal e os registros do Botão SOS.
"""
import sqlite3
import datetime
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from core.config import DB_PATH

class DatabaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
            cls._instance.init_db()
        return cls._instance

    def get_connection(self):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Cria as tabelas oficiais do Metanoia."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Tabela do Homem (Progresso & Dias Limpos)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS progresso_homem (
                id INTEGER PRIMARY KEY,
                dias_limpos INTEGER DEFAULT 0,
                recorde_dias INTEGER DEFAULT 0,
                xp_forja INTEGER DEFAULT 0,
                ultimo_checkin_data TEXT,
                brasa_ativa INTEGER DEFAULT 1,
                patente_atual TEXT DEFAULT 'O PEREGRINO'
            )
            """)

            # 2. Lições da Trilha 21 Dias de Desintoxicação (Neurociência + Palavra)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS trilha_21_dias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dia INTEGER UNIQUE NOT NULL,
                titulo TEXT NOT NULL,
                versiculo_referencia TEXT NOT NULL,
                texto_biblico TEXT NOT NULL,
                principio_neurocientifico TEXT NOT NULL,
                missao_pratica TEXT NOT NULL,
                xp_recompensa INTEGER DEFAULT 30
            )
            """)

            # 3. Registros de Batalha (Botão SOS Acionado)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros_sos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL,
                gatilho TEXT NOT NULL,
                vitoria INTEGER DEFAULT 1
            )
            """)

            # 4. A Aliança (Pacto de Honra 1-to-1)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS alianca_checkin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                olhos_guardados INTEGER DEFAULT 1,
                ordem_matinal INTEGER DEFAULT 1,
                honrou_casa INTEGER DEFAULT 1,
                observacao TEXT
            )
            """)

            # 5. Configuração do Parceiro de Aliança (WhatsApp)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS parceiro_alianca (
                id INTEGER PRIMARY KEY,
                nome TEXT DEFAULT 'Irmão de Guerra',
                telefone_whatsapp TEXT DEFAULT '5511999999999',
                ativo INTEGER DEFAULT 1,
                ultimo_envio TEXT
            )
            """)

            # 6. Forja dos 90 Dias (Tabela Oficial)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS forja_90_dias (
                dia INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                fase TEXT NOT NULL,
                graduacao TEXT NOT NULL,
                versiculo_referencia TEXT NOT NULL,
                texto_biblico TEXT NOT NULL,
                principio_neurocientifico TEXT NOT NULL,
                missao_pratica TEXT NOT NULL,
                duracao_audio TEXT DEFAULT '2 min',
                xp_recompensa INTEGER DEFAULT 30
            )
            """)

            # 7. Chat Histórico do Conselheiro
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS conselheiro_historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                conteudo TEXT NOT NULL,
                data_hora TEXT NOT NULL
            )
            """)

            conn.commit()
            self._seed_initial_data(cursor, conn)

    def _seed_initial_data(self, cursor, conn):
        # 1. Garante perfil inicial
        cursor.execute("SELECT COUNT(*) FROM progresso_homem")
        if cursor.fetchone()[0] == 0:
            hoje = datetime.date.today().isoformat()
            cursor.execute("""
            INSERT INTO progresso_homem (id, dias_limpos, recorde_dias, xp_forja, ultimo_checkin_data, brasa_ativa, patente_atual)
            VALUES (1, 1, 1, 30, ?, 1, 'O PEREGRINO')
            """, (hoje,))

        # 2. Popula os 21 Dias de Desintoxicação (Base Gary Wilson + Tim Chester + Miguel Soriani)
        cursor.execute("SELECT COUNT(*) FROM trilha_21_dias")
        if cursor.fetchone()[0] == 0:
            licoes = [
                (1, "O Mapeamento dos 4 Gatilhos (H.A.L.T.)", "1 Coríntios 10:12",
                 "Aquele, pois, que cuida estar em pé, olhe que não caia.",
                 "A pornografia raramente é sobre desejo sexual puro; é uma válvula de escape para 4 estados: Fome (Hungry), Raiva (Angry), Solidão (Lonely) ou Cansaço (Tired). Seu cérebro quer anestesiar a dor com dopamina barata.",
                 "Identifique qual dos 4 gatilhos mais te assediou nas últimas 48h. Escreva em um papel e defina uma barreira física para ele."),
                
                (2, "A Barreira Física Inegociável", "Mateus 5:29",
                 "Se o teu olho direito te faz tropeçar, arranca-o e lança-o de ti.",
                 "Força de vontade é um recurso biológico finito que se esgota às 22h. Não confie no seu autocontrole de madrugada. O segredo dos homens livres é a fricção do ambiente.",
                 "Hoje à noite, o smartphone dorme fora do quarto (na sala ou cozinha) carregando. Nada de tela ao alcance da mão na cama."),
                
                (3, "A Ilusão do 'Só Uma Olhadinha'", "Provérbios 6:27",
                 "Poderá alguém carregar fogo no bolso sem queimar a sua roupa?",
                 "O cérebro adicto usa a técnica da racionalização: 'Vou só ver o feed do Instagram', 'só uma olhada de 5 segundos'. O pico de dopamina ocorre na ANTECIPAÇÃO, não no ato. Ao abrir a fresta, a comporta inteira é arrombada.",
                 "Cancele hoje mesmo o seguimento de 3 perfis nas redes sociais que ativam pensamentos impuros."),

                (4, "A Fissura dos 7 Dias (O Chaser Effect)", "2 Pedro 2:22",
                 "Voltou o cão ao seu próprio vômito; e a porca lavada a revolver-se no lamaçal.",
                 "Ao atingir 5 a 7 dias limpos, o cérebro entra em abstinência aguda. Os receptores de dopamina gritam por estímulo. Se você ceder, sentirá o 'Efeito Chaser': uma compulsão violenta de recair 3 vezes no mesmo dia.",
                 "Se a onda de vontade vier hoje, aplique a técnica da água congelada no rosto por 15 segundos para ativar o reflexo de mergulho vagal."),

                (5, "O Resgate da Dopamina Natural", "Eclesiastes 9:10",
                 "Tudo quanto te vier à mão para fazer, faze-o conforme as tuas forças.",
                 "O cérebro precisa de dopamina saudável para não morrer de apatia. A dopamina real vem da conquista com esforço prévio: treino físico pesado, banho frio e trabalho honesto concluído.",
                 "Faça 30 flexões ou caminhe 20 minutos sob a luz do sol sem fones de ouvido hoje."),

                (6, "A Confissão no Secreto e a Graça", "1 João 1:9",
                 "Se confessarmos os nossos pecados, ele é fiel e justo para nos perdoar os pecados e nos purificar de toda injustiça.",
                 "O diabo ama a escuridão. O pecado só tem poder enquanto for um segredo vergonhoso. A graça de Cristo não serve para acobertar o erro, mas para arrancar a podridão para fora e sarar a ferida.",
                 "Fique 5 minutos de joelhos no chão do seu quarto. Sem justificativas. Apenas confesse onde você falhou e receba a purificação da cruz."),

                (7, "A Aliança de Dois Homens", "Eclesiastes 4:9-10",
                 "Melhor é serem dois do que um... Se um cair, o outro levanta o seu companheiro; mas ai do que estiver só; pois, caindo, não haverá outro que o levante.",
                 "Nenhum homem vence a guerra da impureza isolado. O isolamento é o abatedouro do homem. Homens de verdade prestam contas com verdade e sem máscaras.",
                 "Envie uma mensagem franca para um irmão de confiança dizendo: 'Estou focado em vencer a pureza na minha vida. Posso contar com sua oração?'.")
            ]
            cursor.executemany("""
            INSERT INTO trilha_21_dias (dia, titulo, versiculo_referencia, texto_biblico, principio_neurocientifico, missao_pratica, xp_recompensa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, licoes)

        conn.commit()

    # --- MÉTODOS DO PROCESSO DO HOMEM ---

    def get_progresso(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM progresso_homem WHERE id = 1")
            row = cursor.fetchone()
            if row:
                return dict(row)
            return {"dias_limpos": 0, "xp_forja": 0, "patente_atual": "O PEREGRINO"}

    def registrar_sos(self, gatilho: str, vitoria: bool = True):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            cursor.execute("""
            INSERT INTO registros_sos (data_hora, gatilho, vitoria)
            VALUES (?, ?, ?)
            """, (agora, gatilho, 1 if vitoria else 0))

            # Se venceu o momento crítico, ganha XP de Honra
            if vitoria:
                cursor.execute("UPDATE progresso_homem SET xp_forja = xp_forja + 50 WHERE id = 1")
            conn.commit()

    def get_licao_do_dia(self, dia: int) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # 1. Tenta buscar na Forja dos 90 Dias
            cursor.execute("SELECT * FROM forja_90_dias WHERE dia = ?", (dia,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            # 2. Fallback para trilha_21_dias
            cursor.execute("SELECT * FROM trilha_21_dias WHERE dia = ?", (dia,))
            row2 = cursor.fetchone()
            return dict(row2) if row2 else None

    def concluir_licao(self, dia: int) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            xp = 30
            cursor.execute("SELECT xp_recompensa FROM forja_90_dias WHERE dia = ?", (dia,))
            row = cursor.fetchone()
            if row:
                xp = row["xp_recompensa"]
            else:
                cursor.execute("SELECT xp_recompensa FROM trilha_21_dias WHERE dia = ?", (dia,))
                row2 = cursor.fetchone()
                if row2:
                    xp = row2["xp_recompensa"]

            cursor.execute("""
            UPDATE progresso_homem
            SET xp_forja = xp_forja + ?, dias_limpos = dias_limpos + 1
            WHERE id = 1
            """, (xp,))
            conn.commit()
            return xp

    # --- PARCEIRO DE ALIANÇA (WHATSAPP 1-TO-1) ---

    def get_parceiro_alianca(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM parceiro_alianca WHERE id = 1")
            row = cursor.fetchone()
            if row:
                return dict(row)
            return {"nome": "Irmão de Guerra", "telefone_whatsapp": "5511999999999"}

    def salvar_parceiro_alianca(self, nome: str, telefone: str) -> bool:
        # Higieniza telefone para manter apenas dígitos
        tel_limpo = "".join(filter(str.isdigit, telefone))
        if not tel_limpo.startswith("55") and len(tel_limpo) in [10, 11]:
            tel_limpo = f"55{tel_limpo}"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO parceiro_alianca (id, nome, telefone_whatsapp, ativo)
            VALUES (1, ?, ?, 1)
            """, (nome.strip(), tel_limpo))
            conn.commit()
            return True

    # --- TEOLOGIA DA GRAÇA & RESTAURAÇÃO (SEM CULPA TÓXICA) ---

    def zerar_contador_com_graca(self, motivo: str = "") -> str:
        """
        Zera o contador sem humilhação ou autoflagelação.
        Preserva o recorde histórico e concede uma palavra de redenção e coragem.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT dias_limpos, recorde_dias FROM progresso_homem WHERE id = 1")
            row = cursor.fetchone()
            dias_atuais = row["dias_limpos"] if row else 0
            recorde = row["recorde_dias"] if row else 0

            novo_recorde = max(recorde, dias_atuais)
            agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

            # Registra a queda com mansidão
            cursor.execute("""
            INSERT INTO registros_sos (data_hora, gatilho, vitoria)
            VALUES (?, ?, 0)
            """, (agora, f"Tropeço / Graça Renovada: {motivo}"))

            # Zera os dias limpos mas mantém XP e atualiza recorde
            cursor.execute("""
            UPDATE progresso_homem
            SET dias_limpos = 0, recorde_dias = ?
            WHERE id = 1
            """, (novo_recorde,))
            conn.commit()

            return (
                "Irmão, o chão não é o seu lugar. 'O justo cai sete vezes e se levanta' (Pv 24:16). "
                "O sangue de Jesus te purifica de todo pecado agora. Levante a cabeça, "
                "não aceite a culpa paralisante do diabo, compartilhe a verdade na Aliança e volte para a forja hoje!"
            )

    @staticmethod
    def calcular_graduacao_biblica(dias: int) -> Dict[str, Any]:
        """Calcula o Nível de Maturidade Bíblica do Homem (Os 5 Estágios de Transformação)."""
        if dias < 21:
            passo = min(4, max(1, (dias // 5) + 1))
            passos_nomes = {
                1: "Passo da Ruptura (Corte das Telas)",
                2: "Passo da Confissão (Sem Máscaras)",
                3: "Passo do Choque Vagal (Autocontrole)",
                4: "Passo do Perdão da Culpa"
            }
            return {
                "nivel": 1,
                "titulo": "O RESGATADO",
                "passo_label": f"Passo {passo}/4: {passos_nomes.get(passo, 'Sobriedade')}",
                "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
                "versiculo": "Colossenses 1:13",
                "texto_versiculo": "Ele nos resgatou do império das trevas e nos transportou para o reino do Filho do seu amor.",
                "cor_badge": "#EF4444",
                "cor_bg": "rgba(239, 68, 68, 0.15)",
                "icone": "🛡️",
                "mantra": "Você saiu da lama do Egito. As correntes foram quebradas; agora aprenda a andar livre."
            }
        elif dias < 51:
            passo = min(4, max(1, ((dias - 21) // 7) + 1))
            passos_nomes = {
                1: "Passo da Ordem Matinal (06h)",
                2: "Passo do Altar do Silêncio",
                3: "Passo da Aliança 1-to-1",
                4: "Passo da Palavra Incisiva"
            }
            return {
                "nivel": 2,
                "titulo": "O DISCÍPULO",
                "passo_label": f"Passo {passo}/4: {passos_nomes.get(passo, 'Constância')}",
                "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
                "versiculo": "Lucas 9:23",
                "texto_versiculo": "Se alguém quer vir após mim, negue-se a si mesmo, tome cada dia a sua cruz e siga-me.",
                "cor_badge": "#3B82F6",
                "cor_bg": "rgba(59, 130, 246, 0.15)",
                "icone": "📖",
                "mantra": "O discípulo não vive de motivação passageira; ele vive do ritmo diário da cruz."
            }
        elif dias < 71:
            passo = min(4, max(1, ((dias - 51) // 5) + 1))
            passos_nomes = {
                1: "Passo da Blindagem no Dia Mau",
                2: "Passo do Choque Térmico",
                3: "Passo do Jejum e Oração",
                4: "Passo da Firmeza Moral"
            }
            return {
                "nivel": 3,
                "titulo": "O GUERREIRO",
                "passo_label": f"Passo {passo}/4: {passos_nomes.get(passo, 'Resiliência')}",
                "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
                "versiculo": "2 Timóteo 2:3",
                "texto_versiculo": "Sofre comigo as aflições como bom soldado de Jesus Cristo.",
                "cor_badge": "#8B5CF6",
                "cor_bg": "rgba(139, 92, 246, 0.15)",
                "icone": "⚔️",
                "mantra": "A Palavra habita em você. Quando a vida aperta, você não foge: você luta e vence."
            }
        elif dias < 90:
            passo = min(4, max(1, ((dias - 71) // 5) + 1))
            passos_nomes = {
                1: "Passo da Honra Feminina (Pureza)",
                2: "Passo da Mordomia Financeira",
                3: "Passo da Autoridade no Lar",
                4: "Passo do Sacerdócio Consagrado"
            }
            return {
                "nivel": 4,
                "titulo": "O SACERDOTE",
                "passo_label": f"Passo {passo}/4: {passos_nomes.get(passo, 'Governo')}",
                "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
                "versiculo": "1 Pedro 2:9",
                "texto_versiculo": "Vós sois a geração eleita, o sacerdócio real, a nação santa.",
                "cor_badge": "#EA580C",
                "cor_bg": "rgba(234, 88, 12, 0.15)",
                "icone": "👑",
                "mantra": "Você governa seus olhos, suas finanças e seu lar. Pronto para honrar no casamento e no trabalho."
            }
        else:
            grau = min(4, (dias - 90) // 30)
            return {
                "nivel": 5,
                "titulo": "O PATRIARCA",
                "passo_label": f"Grau {grau + 1}: Mentor de Gerações",
                "fase": "A ESPADA FORJADA (DIA 90 EM DIANTE)",
                "versiculo": "1 João 2:13",
                "texto_versiculo": "Pais, eu vos escrevo porque conheceis aquele que é desde o princípio.",
                "cor_badge": "#10B981",
                "cor_bg": "rgba(16, 185, 129, 0.15)",
                "icone": "🏛️",
                "mantra": "A sua vitória agora é o escudo de outros homens. Gere discípulos e guarde o legado do Reino."
            }

    def get_graduacao_biblica(self) -> Dict[str, Any]:
        p = self.get_progresso()
        return self.calcular_graduacao_biblica(p.get("dias_limpos", 0))

    # Mantém compatibilidade com bjj caso chamado
    def get_graduacao_bjj(self) -> Dict[str, Any]:
        return self.get_graduacao_biblica()


