"""
Script oficial de Geração da Forja dos 90 Dias do METANOIA.
Popula o banco metanoia.db com os 90 Dias Completos de Transformação Masculina:
- Fase 01 (Dias 01 a 21) // O RESGATADO: O Fogo (Quebra da Dopamina & Ruptura com o Vício)
- Fase 02 (Dias 22 a 50) // O DISCÍPULO: A Bigorna & O Martelo (A Ordem Matinal & Altar do Silêncio)
- Fase 03 (Dias 51 a 70) // O GUERREIRO: A Têmpera (Choque Térmico, Jejum e Blindagem da Carne)
- Fase 04 (Dias 71 a 89) // O SACERDOTE: O Fio de Corte (Honra à Mulher, Casamento e Governo do Lar)
- Dia 90+ // O PATRIARCA: A Espada Forjada (Mentoria e Legado de Honra)
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("C:/Users/matheus/Desktop/metanoia-app/data/metanoia.db")

# Estruturação rica e profunda dos 90 dias
LICOES_90_DIAS = [
    # =========================================================================
    # FASE 01: O FOGO (DIAS 01 A 21) // O RESGATADO (Colossenses 1:13)
    # =========================================================================
    {
        "dia": 1,
        "titulo": "O Mapeamento dos 4 Gatilhos (H.A.L.T.)",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "1 Coríntios 10:12",
        "texto_biblico": "Aquele, pois, que cuida estar em pé, olhe que não caia.",
        "principio_neuro": "A pornografia não é desejo sexual puro; é anestesia para 4 vulnerabilidades: Fome (Hungry), Raiva (Angry), Solidão (Lonely) ou Cansaço (Tired). O cérebro adicto busca dopamina barata para fugir da dor emocional.",
        "missao_pratica": "Identifique qual desses 4 estados mais provocou suas últimas quedas. Escreva a verdade em um papel e defina uma barreira física imediata.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 2,
        "titulo": "A Barreira Física Inegociável",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Mateus 5:29",
        "texto_biblico": "Se o teu olho direito te faz tropeçar, arranca-o e lança-o de ti.",
        "principio_neuro": "A força de vontade é um recurso biológico finito que se esgota após as 22h. Homens livres não confiam no autocontrole na madrugada; eles alteram a arquitetura física do ambiente.",
        "missao_pratica": "A partir de hoje, o smartphone dorme fora do quarto carregando (na sala ou cozinha). Celular na cama é a armadilha do homem fraco.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 3,
        "titulo": "A Ilusão do 'Só Uma Olhadinha'",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Provérbios 6:27-28",
        "texto_biblico": "Poderá alguém carregar fogo no bolso sem queimar a sua roupa? Ou andará sobre brasas sem queimar os pés?",
        "principio_neuro": "O pico de dopamina ocorre na ANTECIPAÇÃO da novidade sexual, não no ato. Quando você abre uma fresta nas redes sociais, o córtex pré-frontal é sequestrado e a queda se torna inevitável.",
        "missao_pratica": "Abra seu Instagram/TikTok agora. Deixe de seguir ou silencie 5 perfis que ativem pensamentos lascivos. Feche as portas do inferno.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 4,
        "titulo": "A Fissura dos 7 Dias e o Efeito Chaser",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "2 Pedro 2:22",
        "texto_biblico": "Voltou o cão ao seu próprio vômito; e a porca lavada a revolver-se no lamaçal.",
        "principio_neuro": "Entre o 4º e o 7º dia limpo, a falta de estímulo dopaminérgico gera a fissura aguda. Se você ceder, sentirá o 'Chaser Effect': uma compulsão descontrolada de recair múltiplas vezes no mesmo dia.",
        "missao_pratica": "Se a vontade apertar hoje, vá até a pia e mergulhe o rosto em água gelada por 15 segundos. O reflexo vagal derruba os batimentos cardíacos.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 5,
        "titulo": "A Neuroplasticidade da Esperança",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Romanos 12:2",
        "texto_biblico": "E não vos conformeis com este século, mas transformai-vos pela renovação da vossa mente.",
        "principio_neuro": "Seu cérebro não é de pedra; ele é maleável. Vias neurais antigas são como trilhas no mato: se você para de andar por elas, o mato cresce e o vício atrofia. A cada 'NÃO', uma nova sinapse de liberdade é criada.",
        "missao_pratica": "Faça 20 flexões no chão e declare em voz alta: 'Meu cérebro está sendo curado pelo poder de Deus'.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 6,
        "titulo": "O Resgate da Dopamina Natural",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Eclesiastes 9:10",
        "texto_biblico": "Tudo quanto te vier à mão para fazer, faze-o conforme as tuas forças.",
        "principio_neuro": "A pornografia causa anedonia (incapacidade de se alegrar com coisas simples). Para restaurar a sensibilidade dos receptores D2, você precisa de dopamina saudável: esforço prévio seguido de conquista.",
        "missao_pratica": "Caminhe 15 minutos sob a luz do sol da manhã sem celular, ou termine agora uma tarefa difícil do trabalho que estava parada.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 7,
        "titulo": "O Primeiro Marco: 7 Dias de Fogo",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Salmo 40:2",
        "texto_biblico": "Tirou-me de um poço de perdição, de um tremedal de lama; pôs os meus pés sobre uma rocha.",
        "principio_neuro": "Completar 7 dias limpos desinflama a tempestade dopaminérgica primária. A névoa mental começa a dissipar e a testosterona atinge um pico transitório de reorganização.",
        "missao_pratica": "Tome um banho frio solene. Olhe no espelho com firmeza e agradeça a Cristo por ter quebrado a primeira corrente.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 8,
        "titulo": "Um Afeto Maior que a Carne",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Salmo 16:11",
        "texto_biblico": "Na tua presença há plenitude de alegria, na tua destra, delícias perpetuamente.",
        "principio_neuro": "Thomas Chalmers ensina o poder expulsivo de um novo afeto: um homem nunca larga um osso sujo até que veja e deseje um banquete real diante de si. Você vence o pecado amando mais a Deus.",
        "missao_pratica": "Passe 5 minutos em silêncio no quarto de joelhos, agradecendo a Deus por não ter te abandonado no dia mais vergonhoso da sua vida.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 9,
        "titulo": "Quebrando o Espírito de Escravo",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Romanos 8:15",
        "texto_biblico": "Porque não recebestes o espírito de escravidão, para outra vez estardes em temor, mas recebestes o espírito de adoção.",
        "principio_neuro": "O vício cria a 'identidade de derrotado'. O cérebro diz: 'Eu sempre caio mesmo, sou assim'. Isso é mentira da carne. Você é filho adotivo de Deus, não prisioneiro de impulsos genitais.",
        "missao_pratica": "Escreva em um bloco de notas: 'Eu não sou escravo de telas. Eu sou filho do Rei do Universo.' Leia em voz alta antes de almoçar.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 10,
        "titulo": "A Destruição do Monstro no Escuro",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Tiago 5:16",
        "texto_biblico": "Confessai as vossas culpas uns aos outros e orai uns pelos outros, para que sareis.",
        "principio_neuro": "O circuito da vergonha é tóxico: pecado gera vergonha, vergonha gera isolamento, isolamento gera dor e dor busca pornografia para anestesiar. A única forma de romper esse ciclo é a luz da verdade.",
        "missao_pratica": "Abra a aba da Aliança no app e confirme se o seu parceiro de guerra está alinhado. A luz expulsa as baratas da alma.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 11,
        "titulo": "A Anatomia da Falsa Promessa",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Hebreus 11:25",
        "texto_biblico": "Escolhendo antes ser maltratado com o povo de Deus do que por um pouco de tempo ter o gozo do pecado.",
        "principio_neuro": "A pornografia promete intimidade e entrega solidão; promete poder e entrega fraqueza erétil; promete alívio e entrega desespero. Aprenda a reconhecer a propaganda enganosa do diabo.",
        "missao_pratica": "Quando o pensamento impuro piscar na tela mental, responda imediatamente: 'Você é uma mentira que rouba minha alma. Não compro o seu veneno.'",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 12,
        "titulo": "O Deserto da Dopamina (O Flatline)",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Oséias 2:14",
        "texto_biblico": "Portanto, eis que eu a atrairei, e a levarei para o deserto, e lhe falarei ao coração.",
        "principio_neuro": "Por volta da 2ª semana, muitos homens experimentam o 'Flatline': libido baixa, cansaço e falta de ânimo. Não se assuste! Seu cérebro está recalibrando a linha de base química. O deserto é a cura.",
        "missao_pratica": "Mesmo se sentir apatia, cumpra suas obrigações sem reclamar. Homem de Deus não é guiado por sentimentos voláteis; é guiado por dever.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 13,
        "titulo": "A Espada do 'Está Escrito'",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Mateus 4:4",
        "texto_biblico": "Não só de pão viverá o homem, mas de toda a palavra que sai da boca de Deus.",
        "principio_neuro": "Jesus não dialogou com Satanás no deserto; Ele sacou a espada das Escrituras. Tentar argumentar com a carne quando a dopamina sobe é derrota certa. Declare a Palavra viva e corte a conversa.",
        "missao_pratica": "Decore hoje 1 Tessalonicenses 4:3-4: 'Pois esta é a vontade de Deus: a vossa santificação, que vos abstenhais da prostituição.' Repita 5 vezes.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 14,
        "titulo": "O Voto das Duas Semanas",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "1 Samuel 7:12",
        "texto_biblico": "Até aqui nos ajudou o Senhor.",
        "principio_neuro": "14 dias limpos. A tempestade neural arrefece. O córtex pré-frontal volta a retomar o comando do freio motor. Você já é mais forte hoje do que quando começou.",
        "missao_pratica": "Envie um áudio de 30 segundos para seu parceiro de aliança agradecendo pelo apoio nos primeiros 14 dias de batalha.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 15,
        "titulo": "A Mentira da 'Necessidade Biológica'",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "1 Coríntios 6:13",
        "texto_biblico": "Os alimentos são para o estômago e o estômago para os alimentos; mas Deus aniquilará tanto um como os outros. O corpo, porém, não é para a prostituição, mas para o Senhor.",
        "principio_neuro": "A cultura mente dizendo que ejaculação frequente é obrigatória para a saúde da próstata. O corpo tem mecanismos naturais de reciclagem noturna (polução noturna). Você não vai morrer por ficar limpo; vai renascer.",
        "missao_pratica": "Reforce a decisão: você não é um animal no cio conduzido por hormônios; é um homem governado pelo Espírito.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 16,
        "titulo": "O Altar do Quarto Fechado",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Mateus 6:6",
        "texto_biblico": "Tu, porém, quando orares, entra no teu quarto e, fechada a porta, orarás a teu Pai que está em secreto.",
        "principio_neuro": "O mesmo quarto onde você se humilhava em segredo com a luz azul da tela deve se tornar o santuário onde você chora de quebrantamento e honra a Deus. Consagre o seu espaço físico.",
        "missao_pratica": "Ajoelhe-se ao lado da sua cama e unja o seu quarto com oração, declarando que ali habita a pureza e a presença de Cristo.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 17,
        "titulo": "A Faxina nos Algoritmos",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Salmo 101:3",
        "texto_biblico": "Não porei coisa injusta diante dos meus olhos; aborreço o proceder dos que se desviam; isso não se apegará a mim.",
        "principio_neuro": "Os algoritmos do Instagram e YouTube são desenhados para capturar sua atenção com micro-estímulos eróticos no feed 'Explorar'. Limpe seu histórico e resete o algoritmo ou desinstale o app se necessário.",
        "missao_pratica": "Vá nas configurações das suas redes sociais e limpe todo o histórico de busca e interesse. Não alimente a fera.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 18,
        "titulo": "A Graça que Ensina a Dizer Não",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Tito 2:11-12",
        "texto_biblico": "Porque a graça de Deus se há manifestado... ensinando-nos que, renunciando à impiedade e às concupiscências mundanas, vivamos neste presente século sóbria, justa e piamente.",
        "principio_neuro": "Graça bíblica não é passe livre para pecar; é poder sobrenatural para dizer NÃO ao que antes te escravizava. A graça fortalece o córtex e subjuga a carne.",
        "missao_pratica": "Quando surgir qualquer gatilho hoje, diga em voz alta: 'A graça de Deus me ensina a dizer não a isso.' E mude de cômodo.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 19,
        "titulo": "O Sono do Homem Integro",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Salmo 4:8",
        "texto_biblico": "Em paz me deito e logo adormeço, pois só tu, Senhor, me fazes viver em segurança.",
        "principio_neuro": "A culpa do vício rouba o sono profundo (estágio 3 e REM). Quando a consciência é limpa pelo sangue de Cristo, o sistema nervoso parassimpático opera com potência total, restaurando as energias.",
        "missao_pratica": "Deite na cama sem telas 30 minutos antes de dormir. Respire fundo e agradeça pela paz de fechar os olhos de mãos limpas.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 20,
        "titulo": "A Véspera da Transição",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Isaías 43:18-19",
        "texto_biblico": "Não vos lembreis das coisas passadas... Eis que faço uma coisa nova; agora está saindo à luz.",
        "principio_neuro": "Você está a 24 horas de completar 3 semanas completas de pureza. O ferro bruto suportou a fornalha dos 1.200°C. O lodo do Egito foi queimado. Agora você sairá do fogo e irá para a bigorna.",
        "missao_pratica": "Escreva as 3 maiores mudanças que você já percebeu em si mesmo desde o Dia 1 (clareza, energia, paz). Guarde esse bilhete.",
        "duracao_audio": "2 min",
        "xp": 30
    },
    {
        "dia": 21,
        "titulo": "A COROA DO RESGATADO (21 DIAS)",
        "fase": "FASE 01 // O FOGO (DIAS 01 A 21)",
        "graduacao": "O RESGATADO",
        "versiculo_ref": "Colossenses 1:13",
        "texto_biblico": "Ele nos resgatou do império das trevas e nos transportou para o reino do Filho do seu amor.",
        "principio_neuro": "21 dias limpos. A ciência atesta o renascimento de receptores dopaminérgicos e o fim do hábito mecânico. A escória foi queimada. Você não é mais o fugitivo da lama; é um homem resgatado para a guerra.",
        "missao_pratica": "Comemore com um café forte e uma oração de pé. Você concluiu a Fase 01. Amanhã começa a Bigorna do Discípulo!",
        "duracao_audio": "3 min",
        "xp": 100
    },

    # =========================================================================
    # FASE 02: A BIGORNA & O MARTELO (DIAS 22 A 50) // O DISCÍPULO (Lucas 9:23)
    # =========================================================================
    {
        "dia": 22,
        "titulo": "A Ordem Matinal das 06h (A Cruz Diária)",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Lucas 9:23",
        "texto_biblico": "Se alguém quer vir após mim, negue-se a si mesmo, tome cada dia a sua cruz e siga-me.",
        "principio_neuro": "O discípulo acorda e governa o primeiro pensamento. Nada de Instagram nos primeiros 10 minutos. O cérebro precisa das primícias da ordem para não vagar sem leme durante o dia.",
        "missao_pratica": "Acorde amanhã 15 minutos mais cedo. Ajoelhe-se antes de tocar no celular e entregue seu dia ao Senhor.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 23,
        "titulo": "O Altar do Silêncio e a Respiração",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Habacuque 2:20",
        "texto_biblico": "O Senhor, porém, está no seu santo templo; cale-se diante dele toda a terra.",
        "principio_neuro": "O homem moderno tem pavor do silêncio porque o silêncio confronta a mente. Pratique a oração contemplativa silenciosa: 3 minutos em quietude desaceleram as ondas cerebrais Beta para Alfa.",
        "missao_pratica": "Fique 3 minutos sentado em silêncio absoluto, respirando em 4 tempos (4s inspira, 4s segura, 4s expira). Apenas adore a Deus.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 24,
        "titulo": "O Martelo da Palavra nos Provérbios",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Provérbios 4:23",
        "texto_biblico": "Sobre tudo o que se deve guardar, guarda o teu coração, porque dele procedem as fontes da vida.",
        "principio_neuro": "A sabedoria bíblica dos Provérbios recalibra o discernimento moral. Ler 1 capítulo de Provérbios por dia alimenta o córtex com diretrizes práticas de causa e efeito.",
        "missao_pratica": "Leia o capítulo de Provérbios correspondente ao dia de hoje (ex: Dia 24 = Provérbios 24). Destaque um versículo de impacto.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 25,
        "titulo": "A Cura da Procrastinação Masculina",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Provérbios 24:33-34",
        "texto_biblico": "Um pouco para dormir, um pouco para toscanejar... assim sobrevirá a tua pobreza como um ladrão.",
        "principio_neuro": "A procrastinação é a prima-irmã da pornografia: ambas fogem do desconforto do trabalho em direção ao alívio instantâneo. O discípulo abraça o atrito com coragem.",
        "missao_pratica": "Escolha a tarefa mais desagradável e pesada do seu dia hoje. Comece por ela nos primeiros 30 minutos da sua jornada de trabalho.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 26,
        "titulo": "O Trabalho como Culto a Deus",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Colossenses 3:23",
        "texto_biblico": "Tudo o que fizerem, façam de todo o coração, como para o Senhor, e não para os homens.",
        "principio_neuro": "O homem viciado trabalha com mente fragmentada e culpa. Quando você trabalha com excelência, o cérebro produz dopamina sustentável ligada à honra de cumprir uma vocação nobre.",
        "missao_pratica": "Execute suas funções hoje com o dobro de capricho e pontualidade, sem reclamar e sem fofoca de corredor.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 27,
        "titulo": "O Domínio da Língua e da Queixa",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Efésios 4:29",
        "texto_biblico": "Não saia da vossa boca nenhuma palavra torpe, mas só a que for boa para promover a edificação.",
        "principio_neuro": "A murmuração constante vicia o cérebro no estresse e no papel de vítima. Homem maduro não reclama do calor, do chefe ou do trânsito; ele governa sua boca.",
        "missao_pratica": "Fique as próximas 24 horas sem pronunciar uma única palavra de queixa ou palavrão. Se falhar, faça 10 flexões na hora.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 28,
        "titulo": "As 4 Semanas de Liberdade (28 Dias)",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Gálatas 5:1",
        "texto_biblico": "Para a liberdade foi que Cristo nos libertou. Permanecei, pois, firmes e não vos submetais de novo a jugo de escravidão.",
        "principio_neuro": "Um ciclo lunar biológico completo limpo. A dependência psicológica aguda dá lugar a uma nova rotina. O discípulo já aprendeu a andar com os próprios pés.",
        "missao_pratica": "Escreva uma mensagem de gratidão para alguém que orou por você quando você estava no fundo do poço.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 29,
        "titulo": "A Aliança de Davi e Jônatas",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "1 Samuel 18:3",
        "texto_biblico": "E Jônatas e Davi fizeram aliança; porque Jônatas o amava como à sua própria alma.",
        "principio_neuro": "Homens precisam de amizades leais e sem afetação. Dois guerreiros que cuidam das costas um do outro na batalha são invencíveis contra as setas do diabo.",
        "missao_pratica": "Ligue ou mande mensagem para seu parceiro de aliança no app e pergunte: 'Irmão, como está a sua mente hoje? Como posso orar por você?'.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 30,
        "titulo": "O Fim do Olhar Lascivo no Trânsito e na Rua",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Mateus 5:28",
        "texto_biblico": "Eu, porém, vos digo que qualquer que olhar para uma mulher com intenção impura, no seu coração já cometeu adultério com ela.",
        "principio_neuro": "A 'segunda olhada' é a armadilha da carne: a primeira olhada é involuntária; a virada de pescoço para conferir o corpo de uma mulher na rua é uma decisão voluntária de cobiça. O discípulo guarda o pescoço reto.",
        "missao_pratica": "Pratique a 'guarda dos olhos': hoje, ao andar na rua ou na academia, mantenha os olhos no horizonte sem escanear o corpo alheio.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 31,
        "titulo": "O Alinhamento das Finanças com Deus",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Lucas 16:10",
        "texto_biblico": "Quem é fiel no pouco também é fiel no muito; e quem é injusto no pouco também é injusto no muito.",
        "principio_neuro": "Homens desorganizados financeiramente vivem em constante ansiedade oculta, e a ansiedade busca alívio no vício. O discípulo sabe para onde vai cada real que ganha.",
        "missao_pratica": "Abra seu extrato bancário hoje. Elimine uma assinatura digital inútil ou corte um gasto supérfluo que está drenando seu orçamento.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 32,
        "titulo": "O Cuidado com a Casa e o Quarto",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "1 Coríntios 14:40",
        "texto_biblico": "Mas faça-se tudo decentemente e com ordem.",
        "principio_neuro": "A desordem externa reflete e amplifica a confusão interna. Quarto bagunçado, cama desfeita e roupas amontoadas sinalizam fraqueza e apatia mental.",
        "missao_pratica": "Arrume sua cama com precisão militar antes de sair de casa e organize sua mesa de trabalho.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 33,
        "titulo": "A Memória da Cruz nos Momentos de Orgulho",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Gálatas 6:14",
        "texto_biblico": "Longe esteja de mim gloriar-me, senão na cruz de nosso Senhor Jesus Cristo.",
        "principio_neuro": "Quando o homem atinge mais de 30 dias limpo, surge uma nova armadilha: o orgulho espiritual ('Já venci, sou superior'). O orgulho precede a ruína. Você permanece em pé apenas pela misericórdia de Deus.",
        "missao_pratica": "Ajoelhe-se por 2 minutos e diga: 'Senhor, se não fosse a tua graça, eu ainda estaria na lama. Toda a honra é tua.'",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 34,
        "titulo": "A Nutrição do Templo do Espírito",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "1 Coríntios 6:19",
        "texto_biblico": "Acaso não sabeis que o vosso corpo é santuário do Espírito Santo?",
        "principio_neuro": "Picos de açúcar e alimentos ultraprocessados causam inflamação sistêmica e quedas abruptas de glicose, disparando irritabilidade e impulsividade. Comida limpa sustenta mente limpa.",
        "missao_pratica": "Passe o dia de hoje sem refrigerantes e sem doces industriais. Beba 3 litros de água mineral pura.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 35,
        "titulo": "O Marco dos 35 Dias: A Metade da Bigorna",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Filipenses 1:6",
        "texto_biblico": "Aquele que começou boa obra em vós há de completá-la até ao Dia de Cristo Jesus.",
        "principio_neuro": "5 semanas inteiras sem alimentar o vício. A memória de curto prazo melhora sensivelmente e a autoconfiança de olhar as pessoas nos olhos retorna com força.",
        "missao_pratica": "Olhe as pessoas nos olhos ao cumprimentá-las hoje. Não abaixe a cabeça para ninguém.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 36,
        "titulo": "A Vigilância das Amizades Fúteis",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "1 Coríntios 15:33",
        "texto_biblico": "Não vos enganeis: as más conversações corrompem os bons costumes.",
        "principio_neuro": "Grupos de WhatsApp com piadas indecentes e compartilhamento de fotos vazadas reativam o circuito da podridão. Homem de Deus sai do grupo ou exige respeito inegociável.",
        "missao_pratica": "Silencie para sempre ou saia de grupos de mensagens onde mulheres são tratadas como carne ou onde circulam links impróprios.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 37,
        "titulo": "A Oração Pela Futura Esposa ou Pelo Casamento",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Provérbios 31:10",
        "texto_biblico": "Mulher virtuosa, quem a achará? O seu valor muito excede o de rubis.",
        "principio_neuro": "O vício te treinava para ser um consumidor egoísta de corpos. O discipulado te treina para ser um protetor generoso de corações. Ore pelo destino da mulher da sua vida.",
        "missao_pratica": "Faça uma oração sincera pela sua esposa (ou pela mulher que Deus colocará no seu caminho para ser mãe dos seus filhos).",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 38,
        "titulo": "O Fim da Covardia Moral",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "2 Timóteo 1:7",
        "texto_biblico": "Porque Deus não nos deu o espírito de covardia, mas de poder, de amor e de moderação.",
        "principio_neuro": "A dopamina barata deixa o homem frouxo e complacente. Quando os receptores saram, o homem recupera a coragem de assumir responsabilidades difíceis e proteger os indefesos.",
        "missao_pratica": "Tenha hoje aquela conversa difícil que você estava adiando por covardia (no trabalho ou na família). Fale com firmeza e mansidão.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 39,
        "titulo": "A Resistência ao Cansaço Noturno",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Salmo 119:105",
        "texto_biblico": "Lâmpada para os meus pés é tua palavra e luz, para o meu caminho.",
        "principio_neuro": "O cansaço da sexta-feira à noite é um dos momentos de maior risco. O cérebro diz: 'Você trabalhou a semana toda, você merece uma recompensa'. Não caia nessa armadilha.",
        "missao_pratica": "Sua recompensa é um sono reparador de honra, não o retorno à escravidão. Desligue os eletrônicos cedo hoje.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 40,
        "titulo": "Os 40 Dias no Deserto (Como Jesus Venceu)",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Mateus 4:1",
        "texto_biblico": "A seguir, foi Jesus levado pelo Espírito ao deserto, para ser tentado pelo diabo.",
        "principio_neuro": "40 dias é o número bíblico da provação e do preparo. Moisés no Sinai, Elias no Horebe e Jesus no deserto. Você completou 40 dias de provação da sua fé.",
        "missao_pratica": "Tire 15 minutos em oração de agradecimento. Você sobreviveu à quarentena da mente. A lâmina está tomando forma.",
        "duracao_audio": "3 min",
        "xp": 50
    },
    {
        "dia": 41,
        "titulo": "A Honra aos Pais e a Raiz dos Traumas",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Efésios 6:2",
        "texto_biblico": "Honra a teu pai e a tua mãe, que é o primeiro mandamento com promessa.",
        "principio_neuro": "Muitas dores que levaram você à pornografia vieram de ausência paterna ou feridas familiares. Perdoar seus pais quebra as cadeias emocionais que alimentavam o vício.",
        "missao_pratica": "Ligue ou mande uma mensagem de afeto para seus pais. Se eles já partiram, perdoe-os em oração diante de Deus.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 42,
        "titulo": "A Leitura Consistente de Livros Sólidos",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "2 Timóteo 4:13",
        "texto_biblico": "Quando vieres, traze a capa... e os livros, especialmente os pergaminhos.",
        "principio_neuro": "Vídeos curtos de 15 segundos no TikTok destroem a capacidade de foco sustentado. Ler livros clássicos reconstrói a mielinização das vias de atenção profunda do cérebro.",
        "missao_pratica": "Leia 10 páginas de um livro edificante de papel hoje, com o celular em outro cômodo.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 43,
        "titulo": "A Quebra do Ciclo da Autocrítica Tóxica",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Romanos 8:1",
        "texto_biblico": "Agora, pois, já nenhuma condenação há para os que estão em Cristo Jesus.",
        "principio_neuro": "Ficar se chamando mentalmente de 'lixo' não santifica ninguém; apenas ativa cortisol e depressão. A convicção do Espírito Santo aponta o erro com esperança de conserto; a voz de acusação do diabo paralisa.",
        "missao_pratica": "Se vier pensamentos de autoflagelação, declare: 'Cristo já pagou o preço por mim. Eu caminho em novidade de vida.'",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 44,
        "titulo": "A Generosidade Secreta",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Mateus 6:3-4",
        "texto_biblico": "Quando tu deres esmola, não saiba a tua mão esquerda o que faz a tua direita.",
        "principio_neuro": "O vício te tornou autofocado e mesquinho. A generosidade em segredo ativa circuitos de ocitocina e altruísmo genuíno, desalojando o egoísmo do coração.",
        "missao_pratica": "Pague o almoço de alguém que precisa ou ajude uma pessoa necessitada hoje sem contar para absolutamente ninguém.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 45,
        "titulo": "O Treino Físico Intencional",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "1 Coríntios 9:26",
        "texto_biblico": "Pois eu assim corro, não como a coisa incerta; assim combato, não como batendo no ar.",
        "principio_neuro": "O corpo precisa suar e sentir a dor da superação muscular para dissipar o excesso de energia represada. Treino pesado com pesos eleva a sensibilidade à insulina e a firmeza postural.",
        "missao_pratica": "Faça uma sessão de treino intenso (musculação, corrida ou calistenia) com empenho total hoje.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 46,
        "titulo": "A Gestão das Tensões do Casamento ou Namoro",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Provérbios 15:1",
        "texto_biblico": "A resposta branda desvia o furor, mas a palavra dura suscita a ira.",
        "principio_neuro": "Quando o homem não tem mais a pornografia como válvula de escape, ele pode descarregar a irritabilidade na parceira. O discípulo aprende a respirar e responder com sabedoria e acolhimento.",
        "missao_pratica": "Se houver atrito com sua parceira hoje, não grite e não emburre. Ouça com paciência e responda com amor.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 47,
        "titulo": "O Amor ao Silêncio da Manhã",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Salmo 5:3",
        "texto_biblico": "Pela manhã, Senhor, ouves a minha voz; pela manhã te apresento a minha oração e fico esperando.",
        "principio_neuro": "As primeiras horas do dia são as mais sagradas e produtivas. Quem vence a manhã vence o dia. O discípulo já fez das 06h seu momento inegociável de comunhão.",
        "missao_pratica": "Aprecie o nascer do sol e celebre: a sua rotina agora pertence a Deus, não ao feed infinito.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 48,
        "titulo": "A Limpeza Completa de Dispositivos",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Josué 7:13",
        "texto_biblico": "Santificai-vos para amanhã, porque assim diz o Senhor... Anátema há no meio de ti.",
        "principio_neuro": "Se ainda resta alguma pasta escondida no computador, algum backup antigo no pendrive ou alguma foto do passado, jogue fora agora. Não deixe um fio desencapado para trás.",
        "missao_pratica": "Faça uma varredura no seu computador e exclua definitivamente qualquer arquivo ou pasta suspeita.",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 49,
        "titulo": "A Bigorna Está Quase Pronta",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Jeremias 23:29",
        "texto_biblico": "Não é a minha palavra como fogo, diz o Senhor, e como martelo que esmiúça a penha?",
        "principio_neuro": "Foram 28 dias tomando marteladas da Palavra na bigorna. O orgulho quebrou, o ritmo diário foi implantado e você aprendeu a disciplina dos joelhos no chão.",
        "missao_pratica": "Agradeça a Deus por cada martelada que te moldou até aqui. Amanhã você conclui a Fase do Discípulo!",
        "duracao_audio": "2 min",
        "xp": 35
    },
    {
        "dia": 50,
        "titulo": "A COROA DO DISCÍPULO (50 DIAS)",
        "fase": "FASE 02 // A BIGORNA (DIAS 22 A 50)",
        "graduacao": "O DISCÍPULO",
        "versiculo_ref": "Lucas 9:23",
        "texto_biblico": "Se alguém quer vir após mim, negue-se a si mesmo, tome cada dia a sua cruz e siga-me.",
        "principio_neuro": "50 dias limpos. Meio caminho andado rumo ao renascimento total. O ferro bruto não tem mais escória e foi forjado em formato de espada. Agora vem a fase do choque térmico: A Têmpera do Guerreiro.",
        "missao_pratica": "Compartilhe essa vitória de 50 dias com seu parceiro de aliança. Você é oficialmente um Discípulo de Honra!",
        "duracao_audio": "3 min",
        "xp": 100
    },

    # =========================================================================
    # FASE 03: A TÊMPERA (DIAS 51 A 70) // O GUERREIRO (1 João 2:14 / 2 Tm 2:3)
    # =========================================================================
    {
        "dia": 51,
        "titulo": "O Choque Térmico (A Têmpera do Aço)",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "2 Timóteo 2:3",
        "texto_biblico": "Sofre comigo as aflições como bom soldado de Jesus Cristo.",
        "principio_neuro": "A têmpera é o choque térmico que endurece as moléculas do aço. O banho frio voluntário ensina o córtex pré-frontal a subjugar o instinto primário de fuga diante do desconforto.",
        "missao_pratica": "Tome um banho 100% gelado de 2 minutos logo pela manhã. Não hesite antes de entrar. O guerreiro comanda o corpo.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 52,
        "titulo": "O Jejum das Emoções e da Comida",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Mateus 6:16",
        "texto_biblico": "Quando jejuardes, não mostreis um semblante triste como os hipócritas.",
        "principio_neuro": "O jejum bíblico ensina à carne que o estômago não é o senhor da sua vida. Quando você governa o apetite pela comida, ganha autoridade natural sobre o apetite sexual.",
        "missao_pratica": "Faça um jejum de café da manhã hoje (beba apenas água até o meio-dia) e dedique o tempo que gastaria comendo para orar.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 53,
        "titulo": "A Armadura Completa no Dia Mau",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Efésios 6:13",
        "texto_biblico": "Portanto, tomai toda a armadura de Deus, para que possais resistir no dia mau e, havendo feito tudo, ficar firmes.",
        "principio_neuro": "O 'dia mau' sempre chega: uma demissão, uma briga em família ou uma frustração financeira. O homem fraco corre para a pornografia; o guerreiro veste a armadura da fé e fica de pé.",
        "missao_pratica": "Memorize os itens de Efésios 6: a verdade, a justiça, a fé, a salvação e a Palavra de Deus. Declare essa armadura sobre sua vida.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 54,
        "titulo": "A Autoridade Contra os Dardos Inflamados",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Efésios 6:16",
        "texto_biblico": "Embraçando sempre o escudo da fé, com o qual podereis apagar todos os dardos inflamados do maligno.",
        "principio_neuro": "Dardos inflamados são pensamentos intrusivos que parecem ter surgido do nada (uma imagem do passado, uma lembrança suja). Não assuma a culpa por um dardo que voou; apague-o no escudo da fé.",
        "missao_pratica": "Ao surgir uma memória impura, repreenda na hora em nome de Jesus e troque o foco mental para uma passagem bíblica.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 55,
        "titulo": "A Força dos Jovens que Venceram o Maligno",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "1 João 2:14",
        "texto_biblico": "Jovens, eu vos escrevi, porque sois fortes, e a palavra de Deus permanece em vós, e já vencestes o maligno.",
        "principio_neuro": "Sua força não vem dos seus músculos; vem da Palavra habitando na sua mente. Um homem cheio da Palavra não tem espaço para as ilusões podres da carne.",
        "missao_pratica": "Recite 1 João 2:14 em voz alta 3 vezes no seu quarto. Você é um guerreiro forjado.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 56,
        "titulo": "Oito Semanas de Batalha (56 Dias)",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Salmo 144:1",
        "texto_biblico": "Bendito seja o Senhor, minha rocha, que adestra as minhas mãos para a batalha e os meus dedos para a guerra.",
        "principio_neuro": "8 semanas limpas. Os circuitos pré-frontais atingem alta maturidade. Você não se reconhece mais naquele homem assustado e dependente do Dia 1.",
        "missao_pratica": "Dê um aperto de mão firme e um abraço leal em um amigo ou familiar hoje. Deixe sua firmeza transparecer.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 57,
        "titulo": "O Silêncio Diante da Provocação",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Provérbios 16:32",
        "texto_biblico": "Melhor é o que tarda em irar-se do que o homem poderoso, e o que controla o seu ânimo do que aquele que toma uma cidade.",
        "principio_neuro": "Verdadeiro poder masculino não é agressividade histérica; é autocontrole inabalável. Quem se descontrola entrega a chave do cérebro para o inimigo.",
        "missao_pratica": "Se alguém te fechar no trânsito ou te tratar com grosseria hoje, respire fundo e abençoe a pessoa em silêncio.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 58,
        "titulo": "A Oração de Guerra de Madrugada",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Salmo 63:1",
        "texto_biblico": "Ó Deus, tu és o meu Deus, de madrugada te buscarei.",
        "principio_neuro": "A oração da madrugada exige sacrifício do sono. Esse sacrifício voluntário gera profunda convicção espiritual e autoridade sobre a carne.",
        "missao_pratica": "Coloque o alarme para 05h30 amanhã. Faça uma oração de pé pelo avivamento da sua família e pela santidade da Igreja.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 59,
        "titulo": "O Fim da Falsa Espiritualidade",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Tiago 1:22",
        "texto_biblico": "Sede praticantes da palavra e não somente ouvintes, enganando-vos a vós mesmos.",
        "principio_neuro": "Falar de teologia sem viver pureza prática é a maior hipocrisia humana. O guerreiro não posta versículos para impressionar os outros; ele vive a palavra no secreto.",
        "missao_pratica": "Ajude silenciosamente em uma tarefa doméstica pesada na sua casa (lavar a louça, arrumar a garagem) sem pedir aplausos.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 60,
        "titulo": "DOIS MESES DE HONRA (60 DIAS)",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "1 Coríntios 16:13",
        "texto_biblico": "Vigiai, estai firmes na fé; portai-vos varonilmente e fortalecei-vos.",
        "principio_neuro": "60 dias limpos! A neurociência comprova a recuperação quase total dos receptores D2 de dopamina. O apetite sexual real pelo sexo oposto em um casamento saudável volta a ser natural e puro.",
        "missao_pratica": "Comemore os 60 dias! Faça um relato no diário do app sobre como sua vida mudou nesses 2 meses.",
        "duracao_audio": "3 min",
        "xp": 60
    },
    {
        "dia": 61,
        "titulo": "A Guarda dos Sentidos no Ambiente Digital",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Provérbios 25:28",
        "texto_biblico": "Como cidade derribada, que não tem muros, assim é o homem que não pode conter o seu espírito.",
        "principio_neuro": "Um homem sem limites digitais é uma cidade sem muralhas na antiguidade: qualquer invasor entra e ateia fogo. Seus muros são suas regras inegociáveis de uso do celular.",
        "missao_pratica": "Defina uma hora limite: após as 21h30, nenhuma tela é aberta. Apenas livros, oração e descanso.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 62,
        "titulo": "A Vitória Sobre o Estresse no Trabalho",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "João 16:33",
        "texto_biblico": "No mundo tereis aflições, mas tende bom ânimo; eu venci o mundo.",
        "principio_neuro": "O estresse crônico eleva o cortisol, e o cortisol tenta desligar o córtex pré-frontal pedindo um alívio químico. O guerreiro descarrega o estresse na oração e no treino, nunca na tela.",
        "missao_pratica": "Se o dia de trabalho for pesado, faça uma caminhada rápida de 10 minutos orando em espírito antes de voltar para casa.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 63,
        "titulo": "A Aliança Inquebrável com o Irmão",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Provérbios 27:17",
        "texto_biblico": "Como o ferro com o ferro se afia, assim o homem ao seu irmão.",
        "principio_neuro": "O ferro afia o ferro com atrito e faíscas. A prestação de contas real às vezes dói, mas afia a lâmina moral do homem.",
        "missao_pratica": "Envie o relatório da Aliança hoje com 100% de verdade e honestidade para o WhatsApp do seu parceiro.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 64,
        "titulo": "A Firmeza nas Reuniões e Conversas",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Mateus 5:37",
        "texto_biblico": "Seja, porém, o vosso falar: Sim, sim; Não, não; porque o que passa disto é de procedência maligna.",
        "principio_neuro": "Homens ambíguos geram desconfiança. Homens de Deus são transparentes e pontuais. Cumpra rigorosamente sua palavra dada.",
        "missao_pratica": "Se você prometeu entregar algo para alguém hoje, entregue antes do prazo e com excelência.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 65,
        "titulo": "O Choque Térmico na Fraqueza da Carne",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "1 Pedro 4:1",
        "texto_biblico": "Ora, pois, já que Cristo padeceu na carne, armai-vos também vós com este mesmo pensamento; porque aquele que padeceu na carne já cessou do pecado.",
        "principio_neuro": "Sofrer o desconforto na carne (treino, banho frio, renúncia voluntária) amadurece o sistema de recompensa. Quem aprendeu a sofrer por disciplina não cai por prazer barato.",
        "missao_pratica": "Tome mais um banho frio consciente de vitória hoje e agradeça pelo fortalecimento do seu espírito.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 66,
        "titulo": "O Exame das Concupiscências Ocultas",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Salmo 139:23-24",
        "texto_biblico": "Sonda-me, ó Deus, e conhece o meu coração; prova-me e conhece os meus pensamentos.",
        "principio_neuro": "Deus conhece as intenções mais profundas do subconsciente. Deixe a luz do Espírito iluminar se ainda resta alguma inveja, vaidade ou impureza escondida.",
        "missao_pratica": "Passe 5 minutos em oração sincera pedindo para Deus sondar e limpar as motivações secretas do seu coração.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 67,
        "titulo": "A Vitória Sobre a Autopiedade",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Jeremias 12:5",
        "texto_biblico": "Se te fatigas correndo com homens que vão a pé, como poderás competir com cavalos?",
        "principio_neuro": "A autopiedade é o veneno que paralisa homens. Não reclame que a sua luta é mais difícil que a dos outros. Deus te escolheu para vencer gigantes.",
        "missao_pratica": "Elimine qualquer pensamento de 'coitadinho de mim'. Você é um soldado alistado no exército de Cristo.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 68,
        "titulo": "A Paz Que Excede Todo o Entendimento",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "Filipenses 4:7",
        "texto_biblico": "E a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos sentimentos em Cristo Jesus.",
        "principio_neuro": "A ansiedade patológica do vício foi substituída pela paz soberana de quem não tem nada a esconder debaixo do tapete. Respire essa liberdade.",
        "missao_pratica": "Respire fundo 10 vezes com a mão no peito e sinta a paz de uma mente limpa.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 69,
        "titulo": "A Véspera do Sacerdócio",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "2 Timóteo 4:7",
        "texto_biblico": "Combati o bom combate, acabei a carreira, guardei a fé.",
        "principio_neuro": "O aço passou pelo fogo e suportou o choque térmico da água fria. A estrutura molecular está alinhada e não quebra mais. Agora você entrará na fase do Sacerdócio e da Liderança do Lar.",
        "missao_pratica": "Prepare sua mente: ser livre do vício é apenas o começo; agora você foi chamado para governar sua casa com honra.",
        "duracao_audio": "2 min",
        "xp": 40
    },
    {
        "dia": 70,
        "titulo": "A COROA DO GUERREIRO (70 DIAS)",
        "fase": "FASE 03 // A TÊMPERA (DIAS 51 A 70)",
        "graduacao": "O GUERREIRO",
        "versiculo_ref": "2 Timóteo 2:3",
        "texto_biblico": "Sofre comigo as aflições como bom soldado de Jesus Cristo.",
        "principio_neuro": "70 dias de vitória ininterrupta! A lâmina foi temperada e ganhou dureza inabalável. O homem que vence a si mesmo está pronto para ser o sacerdote e protetor do seu lar.",
        "missao_pratica": "Celebre essa conquista épica com seu irmão de guerra. Bem-vindo à Fase Final: O Sacerdote e o Fio de Corte!",
        "duracao_audio": "3 min",
        "xp": 100
    },

    # =========================================================================
    # FASE 04: O FIO DE CORTE (DIAS 71 A 89) // O SACERDOTE (Efésios 5:25 / 1 Pe 2:9)
    # =========================================================================
    {
        "dia": 71,
        "titulo": "A Aliança com os Olhos (O Pacto de Jó)",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Jó 31:1",
        "texto_biblico": "Fiz concerto com os meus olhos; como, pois, os fixaria numa virgem?",
        "principio_neuro": "Jó entendeu que a pureza não começa no ato físico, mas no contrato moral selado com a retina. O sacerdote trata mulheres com respeito sagrado e proteção paternal.",
        "missao_pratica": "Renove seu pacto de Jó: 'Meus olhos pertencem a Deus e à aliança da minha casa.'",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 72,
        "titulo": "O Olhar Puro Para Com as Mulheres",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "1 Timóteo 5:2",
        "texto_biblico": "Às mulheres idosas como a mães; às moças como a irmãs, com toda a pureza.",
        "principio_neuro": "A cura definitiva da pornografia ocorre quando o cérebro deixa de enxergar mulheres como objetos de consumo sexual e passa a enxergá-las como filhas amadas de Deus, irmãs e mães.",
        "missao_pratica": "Ao falar com qualquer mulher hoje, olhe nos olhos dela com respeito, deferência e pureza santa.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 73,
        "titulo": "O Amor Sacrificial Pela Esposa",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Efésios 5:25",
        "texto_biblico": "Vós, maridos, amai as vossas mulheres, como também Cristo amou a igreja e a si mesmo se entregou por ela.",
        "principio_neuro": "Cristo não exigiu privilégios; Ele sangrou na cruz para santificar sua noiva. O sacerdócio masculino no casamento é liderança através do serviço humilde e sacrifício voluntário.",
        "missao_pratica": "Faça algo concreto para abençoar sua esposa ou namorada hoje (uma massagem nos pés, lavar a louça ou um elogio sincero sem pedir nada em troca).",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 74,
        "titulo": "A Blindagem Espiritual do Lar",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Josué 24:15",
        "texto_biblico": "Eu e a minha casa serviremos ao Senhor.",
        "principio_neuro": "A autoridade espiritual de um homem não vem de gritos ou imposição autoritária; vem da sua integridade no escuro. Filhos e esposas respeitam homens que têm autoridade moral.",
        "missao_pratica": "Ore em voz alta na sua sala ou quarto, ungindo seu lar e declarando que a sua casa é território consagrado ao Altíssimo.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 75,
        "titulo": "O Culto Doméstico e a Mesa Posta",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Deuteronômio 6:7",
        "texto_biblico": "E as ensinarás a teus filhos e delas falarás assentado em tua casa, e andando pelo caminho.",
        "principio_neuro": "Comer junto à mesa sem telas e com conversas profundas é o maior fator de proteção emocional e moral para crianças e adolescentes. O sacerdote reúne a família ao redor da mesa.",
        "missao_pratica": "Faça uma refeição à mesa hoje sem celulares. Agradeça a Deus pelo alimento e abençoe quem estiver com você.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 76,
        "titulo": "A Gestão Financeira Honrada (Fim das Dívidas)",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Provérbios 22:7",
        "texto_biblico": "O rico domina sobre o pobre, e o que toma emprestado é servo do que empresta.",
        "principio_neuro": "O endividamento impulsivo é a mesma compulsão da dopamina barata: querer o benefício antes do trabalho. O sacerdote governa o dinheiro com sabedoria, poupa e constrói reserva de segurança.",
        "missao_pratica": "Faça um plano realista para zerar suas dívidas nos próximos meses. Não gaste nada por impulso hoje.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 77,
        "titulo": "A Honra no Casamento e a Intimidade Sagrada",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Hebreus 13:4",
        "texto_biblico": "Venerado seja entre todos o matrimônio e o leito sem mácula; porém aos fornicadores e aos adúlteros Deus os julgará.",
        "principio_neuro": "O sexo no casamento cristão é uma aliança de amor mútuo, ternura e santidade, livre da pornografia que tratava corpos como mercadoria descartável. A intimidade sagrada cura as feridas da alma.",
        "missao_pratica": "Converse francamente com sua parceira com carinho e honre a aliança exclusiva entre vocês.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 78,
        "titulo": "A Diligência Profissional e a Provisão Digna",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "1 Timóteo 5:8",
        "texto_biblico": "Mas, se alguém não tem cuidado dos seus e principalmente dos da sua família, negou a fé e é pior do que o infiel.",
        "principio_neuro": "O homem de honra provê não apenas com dinheiro, mas com presença emocional, segurança psicológica e direção espiritual. Seja o porto seguro da sua família.",
        "missao_pratica": "Chegue no horário, cumpra suas promessas e demonstre aos seus liderados que você é um homem em quem se pode confiar.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 79,
        "titulo": "O Perdão aos Ofensores",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Colossenses 3:13",
        "texto_biblico": "Suportando-vos uns aos outros e perdoando-vos uns aos outros... assim como Cristo vos perdoou.",
        "principio_neuro": "Rancor e mágoa represados são toxinas que inflamam o sistema límbico. O sacerdote libera perdão para manter os canais de oração desobstruídos com o céu.",
        "missao_pratica": "Pense na pessoa que mais te feriu nos últimos anos. Solte essa dívida diante da cruz e perdoe-a sinceramente.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 80,
        "titulo": "O MARCO DOS 80 DIAS",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "1 Pedro 2:9",
        "texto_biblico": "Vós sois a geração eleita, o sacerdócio real, a nação santa, o povo adquirido.",
        "principio_neuro": "80 dias limpos. A transformação é visível na sua pele, no seu olhar firme, na sua fala ponderada e na sua paz interior. Você foi forjado pelo fogo de Deus.",
        "missao_pratica": "Olhe no espelho e agradeça: você é um sacerdote real levantado para esta geração.",
        "duracao_audio": "2 min",
        "xp": 50
    },
    {
        "dia": 81,
        "titulo": "O Exemplo Silencioso Para os Homens Mais Jovens",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Tito 2:7",
        "texto_biblico": "Em tudo te dá por exemplo de boas obras; na doutrina manifesta integridade, gravidade, incorrupção.",
        "principio_neuro": "Jovens não aprendem com palestras moralistas; aprendem imitando homens reais que vivem com honra, coragem e pureza. Seu exemplo silencioso fala mais alto que mil discursos.",
        "missao_pratica": "Sirva de modelo hoje com postura ereta, linguagem limpa e respeito absoluto com todos ao seu redor.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 82,
        "titulo": "A Quebra do Ciclo Geracional",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Salmo 78:4",
        "texto_biblico": "Não os encobriremos aos seus filhos, cantando à geração futura os louvores do Senhor.",
        "principio_neuro": "A escravidão que aprisionou seu avô e seu pai termina em você. Seus filhos e netos não verão um homem viciado e covarde em casa; verão um pai de honra e um marido fiel.",
        "missao_pratica": "Declare com fé: 'A maldição do vício e da pornografia morreu na minha geração. A partir de mim há honra e bênção.'",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 83,
        "titulo": "A Oração Pela Restauração de Amigos Caídos",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Gálatas 6:1",
        "texto_biblico": "Irmãos, se algum homem chegar a ser surpreendido nalguma ofensa, vós, que sois espirituais, encaminhai o tal com espírito de mansidão.",
        "principio_neuro": "Você conhece a dor e a vergonha da lama porque esteve lá. Não julgue quem ainda está preso. Interceda por amigos que estão sofrendo em silêncio no vício.",
        "missao_pratica": "Ore nominalmente por 2 amigos que você sabe que estão lutando contra vícios e precisando de salvação.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 84,
        "titulo": "As 12 Semanas de Forja (84 Dias)",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "2 Coríntios 5:17",
        "texto_biblico": "Assim que, se alguém está em Cristo, nova criatura é; as coisas velhas já passaram; eis que tudo se fez novo.",
        "principio_neuro": "12 semanas completas. A neurociência clássica considera 84 a 90 dias o período ouro do reboot completo do sistema de recompensa cerebral. As vias neurais velhas foram substituídas por autopistas de retidão.",
        "missao_pratica": "Comemore com um momento de louvor a Deus no seu quarto. A nova criatura é uma realidade viva.",
        "duracao_audio": "2 min",
        "xp": 50
    },
    {
        "dia": 85,
        "titulo": "A Prontidão Para a Batalha Contínua",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "1 Pedro 5:8",
        "texto_biblico": "Sede sóbrios; vigiai; porque o diabo, vosso adversário, anda em derredor, bramando como leão, buscando a quem possa tragar.",
        "principio_neuro": "A vitória de 85 dias não significa que você pode baixar a guarda. A sobriedade não é um troféu estático na prateleira; é uma postura diária de humildade e vigilância.",
        "missao_pratica": "Reafirme: o inimigo não terá espaço no meu smartphone, na minha cama ou nos meus pensamentos.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 86,
        "titulo": "O Altar do Casamento Como Ministério",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Malaquias 2:15",
        "texto_biblico": "Portanto, cuidai de vós mesmos, e ninguém seja infiel para com a mulher da sua mocidade.",
        "principio_neuro": "Seu casamento é seu primeiro ministério e seu maior púlpito. O sacerdote edifica sua mulher com ternura, cuidado financeiro e segurança.",
        "missao_pratica": "Escreva um bilhete à mão para sua esposa ou namorada dizendo o quanto você a valoriza e admira.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 87,
        "titulo": "O Fio de Corte Perfeito da Lâmina",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Hebreus 4:12",
        "texto_biblico": "Porque a palavra de Deus é viva e eficaz, e mais penetrante do que espada alguma de dois gumes.",
        "principio_neuro": "O fio de corte do ferreiro não serve para enfeitar estantes; serve para cortar o mal pela raiz, proteger a família e trabalhar com retidão.",
        "missao_pratica": "Esteja pronto para cortar qualquer mentira ou desonestidade que se aproxime do seu ambiente de trabalho ou casa.",
        "duracao_audio": "2 min",
        "xp": 45
    },
    {
        "dia": 88,
        "titulo": "A Véspera do Renascimento dos 90 Dias",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Salmo 126:3",
        "texto_biblico": "Grandes coisas fez o Senhor por nós, pelas quais estamos alegres.",
        "principio_neuro": "Faltam apenas 48 horas. Olhe para trás e veja de onde Deus te tirou: da lama do vício solitário às 23h da noite até a honra inabalável de um sacerdote de Deus.",
        "missao_pratica": "Tire um tempo com seu parceiro de aliança e relembrem onde vocês estavam quando começaram essa jornada.",
        "duracao_audio": "2 min",
        "xp": 50
    },
    {
        "dia": 89,
        "titulo": "O Último Exame da Forja",
        "fase": "FASE 04 // A LÂMINA (DIAS 71 A 89)",
        "graduacao": "O SACERDOTE",
        "versiculo_ref": "Apocalipse 3:11",
        "texto_biblico": "Eis que venho sem demora; guarda o que tens, para que ninguém tome a tua coroa.",
        "principio_neuro": "Você suportou o fogo, tomou as marteladas da bigorna, suportou o choque da têmpera e teve o fio afiado pela Palavra. Amanhã você será coroado O PATRIARCA.",
        "missao_pratica": "Ore de joelhos com gratidão profunda. Amanhã é o Grande Dia 90!",
        "duracao_audio": "2 min",
        "xp": 50
    },

    # =========================================================================
    # DIA 90+: A ESPADA FORJADA // O PATRIARCA (1 João 2:13 / 2 Timóteo 2:2)
    # =========================================================================
    {
        "dia": 90,
        "titulo": "O DIA 90: A COROAÇÃO DO PATRIARCA",
        "fase": "A ESPADA FORJADA (DIA 90 EM DIANTE)",
        "graduacao": "O PATRIARCA",
        "versiculo_ref": "2 Timóteo 2:2",
        "texto_biblico": "E o que de mim ouviste... transmite-o a homens fiéis, que sejam idôneos para também ensinarem os outros.",
        "principio_neuro": "90 DIAS COMPLETOS. O reboot do cérebro foi consumado. O homem viciado morreu; o patriarca nasceu. Sua missão a partir de hoje não é apenas se manter limpo: é ser o escudo e o mentor de outros irmãos que ainda estão na lama.",
        "missao_pratica": "Declare publicamente ou ao seu parceiro: 'Eu sou um Patriarca de Deus. Minha vida é um legado de honra.' Assuma a mentoria de um novo irmão!",
        "duracao_audio": "3 min",
        "xp": 200
    }
]

def popular_banco():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 1. Cria ou recria a tabela oficial forja_90_dias
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

    # 2. Tabela de configuração do Parceiro de Aliança
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS parceiro_alianca (
        id INTEGER PRIMARY KEY,
        nome TEXT DEFAULT 'Pedro Ramos',
        telefone_whatsapp TEXT DEFAULT '5511999999999',
        ativo INTEGER DEFAULT 1,
        ultimo_envio TEXT
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM parceiro_alianca WHERE id = 1")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO parceiro_alianca (id, nome, telefone_whatsapp, ativo)
        VALUES (1, 'Pedro Ramos (Irmão de Aliança)', '5511999999999', 1)
        """)

    # 3. Popula ou atualiza os 90 Dias
    for l in LICOES_90_DIAS:
        cursor.execute("""
        INSERT OR REPLACE INTO forja_90_dias (
            dia, titulo, fase, graduacao, versiculo_referencia,
            texto_biblico, principio_neurocientifico, missao_pratica,
            duracao_audio, xp_recompensa
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            l["dia"], l["titulo"], l["fase"], l["graduacao"], l["versiculo_ref"],
            l["texto_biblico"], l["principio_neuro"], l["missao_pratica"],
            l["duracao_audio"], l["xp"]
        ))

    # Também mantém trilha_21_dias sincronizada caso código legado consulte
    for l in LICOES_90_DIAS[:21]:
        cursor.execute("""
        INSERT OR REPLACE INTO trilha_21_dias (
            dia, titulo, versiculo_referencia, texto_biblico,
            principio_neurocientifico, missao_pratica, xp_recompensa
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            l["dia"], l["titulo"], l["versiculo_ref"], l["texto_biblico"],
            l["principio_neuro"], l["missao_pratica"], l["xp"]
        ))

    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM forja_90_dias")
    total = cursor.fetchone()[0]
    conn.close()
    print(f"Sucesso! {total} dias populados na tabela forja_90_dias.")

if __name__ == "__main__":
    popular_banco()
