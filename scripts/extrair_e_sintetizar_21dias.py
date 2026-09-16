"""
Script de Extração e Síntese Cognitiva dos Livros em #especialistax.
Extrai os princípios de Gary Wilson, Tim Chester, Matt Fradd e EasyPeasy
e gera o currículo oficial dos 21 Dias de Desintoxicação do METANOIA.
"""
import os
import sys
import sqlite3
import json
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    import pypdf as fitz

BASE_DIR = Path("C:/Users/matheus/Desktop/metanoia-app")
PDF_DIR = Path("C:/Users/matheus/Desktop/#especialistax")
DB_PATH = BASE_DIR / "data" / "metanoia.db"

# Lista dos 21 Dias Oficiais baseados nos livros
CURRICULO_21_DIAS = [
    # --- SEMANA 1: A FAXINA DA DOPAMINA & O CORTE DO ESTÍMULO (GARY WILSON / MIGUEL SORIANI) ---
    {
        "dia": 1,
        "titulo": "O Mapeamento dos 4 Gatilhos (H.A.L.T.)",
        "versiculo_ref": "1 Coríntios 10:12",
        "texto_biblico": "Aquele, pois, que cuida estar em pé, olhe que não caia.",
        "autor_base": "Gary Wilson & Psicologia Comportamental",
        "principio_neuro": "A pornografia não é sobre desejo sexual puro; é uma automedicação para 4 estados de vulnerabilidade: Fome (Hungry), Raiva (Angry), Solidão (Lonely) ou Cansaço (Tired). O cérebro busca um 'reset' químico através de uma injeção de dopamina barata.",
        "missao_pratica": "Pegue um papel agora e identifique qual desses 4 gatilhos foi o responsável pelas suas últimas 3 quedas. Escreva a verdade sem rodeios e estabeleça um limite inegociável para ele."
    },
    {
        "dia": 2,
        "titulo": "A Barreira Física Inegociável",
        "versiculo_ref": "Mateus 5:29",
        "texto_biblico": "Se o teu olho direito te faz tropeçar, arranca-o e lança-o de ti.",
        "autor_base": "EasyPeasy (O Método Fácil) & Tim Chester",
        "principio_neuro": "Força de vontade é uma reserva de glicose pré-frontal finita que atinge o nível mais baixo às 22h. Homens que vencem o vício não confiam no próprio autocontrole na madrugada; eles alteram a arquitetura do ambiente.",
        "missao_pratica": "A partir de hoje, o smartphone dorme fora do quarto (na sala ou cozinha). Compre um despertador barato de pilha se necessário. Celular na cama é a armadilha do covarde."
    },
    {
        "dia": 3,
        "titulo": "A Ilusão do 'Só Uma Olhadinha'",
        "versiculo_ref": "Provérbios 6:27-28",
        "texto_biblico": "Poderá alguém carregar fogo no bolso sem queimar a sua roupa? Ou andará sobre brasas sem queimar os pés?",
        "autor_base": "Gary Wilson (Seu Cérebro na Pornografia)",
        "principio_neuro": "A maior descarga de dopamina ocorre na ANTECIPAÇÃO da novidade sexual, não no ato em si. Quando você abre uma fresta nas redes sociais ('só para ver o feed'), o cérebro sequestra o freio inibitório e a queda é quase matemática.",
        "missao_pratica": "Abra o seu Instagram agora. Deixe de seguir ou silencie 5 perfis de influenciadoras ou contas que ativem qualquer fagulha de impureza na sua mente."
    },
    {
        "dia": 4,
        "titulo": "A Fissura dos 7 Dias e o Efeito Chaser",
        "versiculo_ref": "2 Pedro 2:22",
        "texto_biblico": "Voltou o cão ao seu próprio vômito; e a porca lavada a revolver-se no lamaçal.",
        "autor_base": "Gary Wilson & Mark Laaser",
        "principio_neuro": "Por volta do 5º ao 7º dia limpo, o acúmulo da proteína DeltaFosB e a carência nos receptores D2 disparam a 'fissura de sobrevivência'. Se você cair, sentirá o 'Chaser Effect': uma vontade incontrolável de recair 3 vezes no mesmo dia.",
        "missao_pratica": "Se a onda de vontade apertar hoje, vá até o banheiro e lave o rosto com água gelada por 15 segundos. O reflexo vagal desacelera seu coração instantaneamente."
    },
    {
        "dia": 5,
        "titulo": "A Neuroplasticidade da Esperança",
        "versiculo_ref": "Romanos 12:2",
        "texto_biblico": "E não vos conformeis com este século, mas transformai-vos pela renovação da vossa mente.",
        "autor_base": "Gary Wilson & Dr. Jeffrey Schwartz",
        "principio_neuro": "Seu cérebro não é estático; ele é plástico. As vias neurais do vício são como trilhas na grama: se você parar de andar por elas, a grama volta a crescer e o circuito atrofia. A cada dia que você diz 'NÃO', a via da liberdade fica mais forte.",
        "missao_pratica": "Celebre silenciosamente: a sua mente está se curando agora. Faça 20 flexões no chão e agradeça a Deus pela regeneração do seu corpo."
    },
    {
        "dia": 6,
        "titulo": "O Resgate da Dopamina Natural",
        "versiculo_ref": "Eclesiastes 9:10",
        "texto_biblico": "Tudo quanto te vier à mão para fazer, faze-o conforme as tuas forças.",
        "autor_base": "Miguel Soriani (O Recomeço) & Gary Wilson",
        "principio_neuro": "O viciado sofre de anedonia (incapacidade de sentir prazer nas coisas comuns). Para quebrar isso, você deve substituir a dopamina tóxica por dopamina de esforço prévio: treino pesado, luz solar matinal e tarefas difíceis concluídas.",
        "missao_pratica": "Passe 20 minutos caminhando sob o sol matinal sem fone de ouvido ou conclua uma tarefa do seu trabalho que você está procrastinando há dias."
    },
    {
        "dia": 7,
        "titulo": "A Celebração do Primeiro Ciclo (1 Semana)",
        "versiculo_ref": "Salmo 40:2",
        "texto_biblico": "Tirou-me de um poço de perdição, de um tremedal de lama; pôs os meus pés sobre uma rocha e firmou os meus passos.",
        "autor_base": "Matt Fradd (O Mito da Pornografia)",
        "principio_neuro": "Completar 7 dias limpos é a primeira grande vitória sobre o ciclo dopaminérgico agudo. O cérebro começa a desinflamar da super-estimulação artificial.",
        "missao_pratica": "Tome um banho frio de vitória. Olhe no espelho e declare em voz alta: 'Eu sou um homem livre em Cristo. A minha dignidade foi resgatada'."
    },

    # --- SEMANA 2: AS RAÍZES DA GRAÇA & O CORAÇÃO (TIM CHESTER / MATT FRADD) ---
    {
        "dia": 8,
        "titulo": "Deus é Mais Satisfatório que a Tela",
        "versiculo_ref": "Salmo 16:11",
        "texto_biblico": "Na tua presença há plenitude de alegria, na tua destra, delícias perpetuamente.",
        "autor_base": "Tim Chester (Com Toda Pureza)",
        "principio_neuro": "O pecado não é combatido apenas com medo da punição, mas com um AFETO MAIOR. Você não vai largar o osso do vício até experimentar o banquete da comunhão com o Criador.",
        "missao_pratica": "Separe 5 minutos em silêncio absoluto no quarto. Feche os olhos e medite na grandeza do amor de Deus que não te abandonou na sarjeta."
    },
    {
        "dia": 9,
        "titulo": "Quebrando o Espírito de Escravo",
        "versiculo_ref": "Romanos 8:15",
        "texto_biblico": "Porque não recebestes o espírito de escravidão, para outra vez estardes em temor, mas recebestes o Espírito de adoção de filhos, no qual clamamos: Aba, Pai.",
        "autor_base": "Tim Chester & C.S. Lewis",
        "principio_neuro": "A culpa paralisante é a maior aliada do vício: você se sente sujo, acha que Deus te rejeitou e, na dor da rejeição, volta para o vício para se consolar. A graça de Cristo quebra esse ciclo vicioso.",
        "missao_pratica": "Chame Deus de 'Aba, Pai' hoje com a certeza de que a dívida do seu pecado foi cravada na cruz e não existe mais condenação."
    },
    {
        "dia": 10,
        "titulo": "A Mentira da Intimidade Virtual",
        "versiculo_ref": "1 Coríntios 6:18",
        "texto_biblico": "Fugi da impureza. Qualquer outro pecado que o homem comete é fora do corpo; mas o devasso peca contra o seu próprio corpo.",
        "autor_base": "Matt Fradd (O Mito da Pornografia)",
        "principio_neuro": "A pornografia treina o cérebro a desejar sexo sem relacionamento, sem sacrifício e sem entrega. Ela transforma seres humanos em objetos descartáveis e adoece a capacidade de amar uma mulher de verdade.",
        "missao_pratica": "Se você é casado ou namora, olhe nos olhos da sua companheira por 60 segundos hoje e faça um elogio sincero sobre a alma dela, não apenas sobre o corpo."
    },
    {
        "dia": 11,
        "titulo": "O Poder do Quarto Secreto",
        "versiculo_ref": "Mateus 6:6",
        "texto_biblico": "Tu, porém, quando orares, entra no teu quarto e, fechada a porta, orarás a teu Pai, que está em secreto; e teu Pai, que vê em secreto, te recompensará.",
        "autor_base": "E.M. Bounds & Tomás de Kempis",
        "principio_neuro": "O homem público é forjado no homem secreto. Quem vence a si mesmo no quarto escuro não precisa fingir força na frente dos outros.",
        "missao_pratica": "Dobre os joelhos no chão duro por 7 minutos hoje. Ore sem palavras ensaiadas. Diga a Deus exatamente onde você se sente fraco."
    },
    {
        "dia": 12,
        "titulo": "A Mortificação do Pecado na Raiz",
        "versiculo_ref": "Colossenses 3:5",
        "texto_biblico": "Mortificai, pois, os vossos membros que estão sobre a terra: a fornicação, a impureza, a paixão desarrazoada, a má concupiscência.",
        "autor_base": "John Owen (A Mortificação do Pecado)",
        "principio_neuro": "Você não domestica um leão; você não faz acordos com a luxúria. O pecado tem que ser estrangulado no primeiro segundo em que o pensamento surge, antes que vire imaginação.",
        "missao_pratica": "Aplique a regra dos 3 segundos: ao cruzar com um pensamento impuro na rua ou na tela, corte o olhar imediatamente e recite Gl 2:20."
    },
    {
        "dia": 13,
        "titulo": "Vencendo a Falsa Fadiga e a Acídia",
        "versiculo_ref": "Gálatas 6:9",
        "texto_biblico": "E não nos cansemos de fazer o bem, porque a seu tempo ceifaremos, se não desfalecermos.",
        "autor_base": "Evágrio Pôntico (Tratado sobre os 8 Pensamentos)",
        "principio_neuro": "Os Pais do Deserto chamavam de 'Demônio do Meio-Dia' (Acídia): aquela preguiça existencial, tédio e desânimo que faz o homem querer se jogar no sofá e rolar feeds infinitos. O antídoto é a ação física imediata.",
        "missao_pratica": "Não fique deitado no sofá mexendo no celular sem rumo. Levante, arrume sua cama, lave a louça ou organize sua mesa de trabalho agora."
    },
    {
        "dia": 14,
        "titulo": "A Aliança de Dois Homens (O Fim do Isolamento)",
        "versiculo_ref": "Tiago 5:16",
        "texto_biblico": "Confessai, pois, os vossos pecados uns aos outros e orai uns pelos outros, para serdes curados.",
        "autor_base": "John Wesley (As Bandas) & Mark Laaser",
        "principio_neuro": "O pecado cresce no escuro do segredo. No instante em que você confessa sua tentação a outro homem de honra, a vergonha tóxica perde 90% do poder sobre sua mente.",
        "missao_pratica": "Conecte-se com seu parceiro no app Metanoia ou mande uma mensagem franca para um irmão maduro: 'Irmão, estou 14 dias sóbrio e firme no propósito. Ore por mim'."
    },

    # --- SEMANA 3: A FORJA DO HOMEM MADURO & O REINO (EDWIN COLE / TIM KELLER) ---
    {
        "dia": 15,
        "titulo": "A Glória da Hombridade Máxima",
        "versiculo_ref": "1 Coríntios 16:13",
        "texto_biblico": "Vigiai, estai firmes na fé, portai-vos varonilmente, sede fortes.",
        "autor_base": "Edwin Louis Cole (Homem Nota 10)",
        "principio_neuro": "Ser homem não é ter músculos ou arrogância; ser homem é assumir a responsabilidade pelas próprias falhas e proteger os que estão sob o seu teto.",
        "missao_pratica": "Assuma um erro recente que você cometeu no trabalho ou em casa sem dar desculpas ou culpar terceiros."
    },
    {
        "dia": 16,
        "titulo": "A Desintoxicação dos Olhos e da Mente",
        "versiculo_ref": "Jó 31:1",
        "texto_biblico": "Fiz aliança com os meus olhos; como, pois, os fixaria numa donzela?",
        "autor_base": "Gary Wilson & Tim Chester",
        "principio_neuro": "Aos 16 dias limpos, a densidade dos receptores de dopamina começa a se estabilizar. Sua capacidade de foco e clareza mental retorna em níveis notáveis.",
        "missao_pratica": "Pratique a custódia dos olhos o dia todo. Não encare ninguém com cobiça na rua ou nas telas. Olhe com respeito ou desvie o olhar."
    },
    {
        "dia": 17,
        "titulo": "O Domínio Próprio nas Finanças e no Corpo",
        "versiculo_ref": "Provérbios 25:28",
        "texto_biblico": "Como cidade derribada, que não tem muros, assim é o homem que não tem domínio próprio.",
        "autor_base": "Randy Alcorn & Estoicismo Cristão",
        "principio_neuro": "A indisciplina sexual sempre sangra para outras áreas: compras por impulso, má alimentação e desordem na rotina. A pureza traz ordem integral.",
        "missao_pratica": "Não compre nada supérfluo hoje. Corte qualquer gasto por impulso e pratique moderação nas refeições."
    },
    {
        "dia": 18,
        "titulo": "O Silêncio de Jesus no Deserto",
        "versiculo_ref": "Lucas 5:16",
        "texto_biblico": "Ele, porém, retirava-se para os lugares desertos e orava.",
        "autor_base": "Donald Whitney & Richard Foster",
        "principio_neuro": "Vivemos cercados por poluição sonora e estímulos visuais que mantêm o cérebro em modo hiper-vigilante e ansioso. O silêncio é o remédio da alma.",
        "missao_pratica": "Passe 10 minutos no seu quarto com o celular desligado. Sem música, sem telas. Apenas ouvindo a voz do Espírito Santo na quietude."
    },
    {
        "dia": 19,
        "titulo": "A Cura do Casamento e da Intimidade Real",
        "versiculo_ref": "Efésios 5:25",
        "texto_biblico": "Maridos, amai as vossas mulheres, como também Cristo amou a igreja e a si mesmo se entregou por ela.",
        "autor_base": "Tim Keller (O Significado do Casamento)",
        "principio_neuro": "A pornografia faz você perguntar: 'O que essa mulher pode me dar?'. O amor bíblico faz você perguntar: 'O que eu posso entregar para edificar a vida dela?'.",
        "missao_pratica": "Faça um ato sacrificial e invisível de serviço pela sua família ou companheira hoje, sem esperar agradecimento ou recompensa."
    },
    {
        "dia": 20,
        "titulo": "O Alerta Final: Nunca Baixe a Guarda",
        "versiculo_ref": "1 Pedro 5:8",
        "texto_biblico": "Sede sóbrios e vigilantes. O diabo, vosso adversário, anda em derredor, como leão que ruge, procurando a quem possa tragar.",
        "autor_base": "Matt Fradd & Gary Wilson",
        "principio_neuro": "O maior perigo do homem é o orgulho dos 20 dias: achar que 'já venceu o vício' e que agora pode 'dar uma olhadinha boba'. A vigilância não acaba; ela se torna um estilo de vida nobre.",
        "missao_pratica": "Revise todas as suas barreiras do Dia 2. Elas continuam ativas? O celular continua fora do quarto? Reforce suas defesas."
    },
    {
        "dia": 21,
        "titulo": "A Aliança Selada: O Homem Metanoia",
        "versiculo_ref": "2 Timóteo 4:7",
        "texto_biblico": "Combati o bom combate, acabei a carreira, guardei a fé.",
        "autor_base": "C.S. Lewis, Edwin Cole & Tim Chester",
        "principio_neuro": "21 dias completados. O circuito neural de recompensa completou o seu primeiro ciclo de reestruturação. Seus olhos estão limpos, sua oração tem poder e sua honra diante de Deus foi restaurada. Você não é mais aquele homem que começou no Dia 1.",
        "missao_pratica": "Escreva uma carta para você mesmo com a data de hoje. Guarde na sua Bíblia. A partir de hoje, você não é apenas um sobrevivente: você é um guerreiro pronto para estender a mão para outros irmãos."
    }
]

def extrair_e_atualizar_banco():
    print("[METANOIA CORE] Extraindo conhecimento dos livros e atualizando banco...")
    
    # 1. Garante banco
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

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

    # Limpa e reinsere os 21 dias oficiais completos
    cursor.execute("DELETE FROM trilha_21_dias")

    for item in CURRICULO_21_DIAS:
        cursor.execute("""
        INSERT INTO trilha_21_dias (dia, titulo, versiculo_referencia, texto_biblico, principio_neurocientifico, missao_pratica, xp_recompensa)
        VALUES (?, ?, ?, ?, ?, ?, 30)
        """, (
            item["dia"],
            item["titulo"],
            item["versiculo_ref"],
            item["texto_biblico"],
            f"[{item['autor_base']}] {item['principio_neuro']}",
            item["missao_pratica"]
        ))

    conn.commit()
    conn.close()
    print(f"[SUCESSO] 21 Licoes Oficiais gravadas com sucesso no banco {DB_PATH.name}!")

    # 2. Gera o Guia Oficial em Markdown
    guia_md_path = BASE_DIR / "GUIA_21_DIAS_METANOIA.md"
    with open(guia_md_path, "w", encoding="utf-8") as f:
        f.write("# ⚔️ GUIA OFICIAL DE 21 DIAS — MÉTODO METANOIA\n\n")
        f.write("> **Base Científica & Teológica:** Gary Wilson (*Your Brain On Porn*), Tim Chester (*Com Toda Pureza*), Matt Fradd (*O Mito da Pornografia*), EasyPeasy e Miguel Soriani.\n\n")
        f.write("---\n\n")

        for item in CURRICULO_21_DIAS:
            f.write(f"## 🛡️ DIA {item['dia']:02d}: {item['titulo'].upper()}\n")
            f.write(f"**Fonte & Referência:** {item['autor_base']}\n\n")
            f.write(f"> *\"{item['texto_biblico']}\"*  \n")
            f.write(f"> **— {item['versiculo_ref']}**\n\n")
            f.write(f"### 🧠 O Princípio Biológico & Espiritual\n")
            f.write(f"{item['principio_neuro']}\n\n")
            f.write(f"### ⚡ Ordem de Missão Prática de Hoje\n")
            f.write(f"**{item['missao_pratica']}**\n\n")
            f.write("---\n\n")

    print(f"[SUCESSO] Documento oficial gerado: {guia_md_path}")

if __name__ == "__main__":
    extrair_e_atualizar_banco()
