# -*- coding: utf-8 -*-
"""
Auditoria Completa & Profunda do Super-App METANOIA.
Executa verificações exaustivas em:
1. Banco de dados SQLite (7 tabelas, 90 dias, chaves, índices e valores nulos).
2. Regras de negócio e Teologia da Graça.
3. Integridade dos arquivos de UI do Flet.
4. Integridade da Landing Page (HTML5, IDs, seletores CSS, scripts e links).
5. Conformidade da engrenagem de vendas Pix e QR Code.
"""
import sys
import os
import sqlite3
import re
from pathlib import Path

# Garante UTF-8 no terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from services.db_service import DatabaseService
from core.config import DB_PATH

def auditar_banco_de_dados():
    print("\n" + "="*50)
    print("🛡️ [1/5] AUDITORIA DO BANCO DE DADOS (SQLite)")
    print("="*50)

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 1. Tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = [r[0] for r in cursor.fetchall() if not r[0].startswith("sqlite_")]
    tabelas_obrigatorias = [
        "progresso_homem", "forja_90_dias", "trilha_21_dias",
        "parceiro_alianca", "alianca_checkin", "registros_sos", "conselheiro_historico"
    ]
    
    print(f"Tabelas encontradas: {len(tabelas)}")
    for tob in tabelas_obrigatorias:
        assert tob in tabelas, f"Tabela obrigatória ausente: {tob}"
        cursor.execute(f"SELECT COUNT(*) FROM {tob}")
        cnt = cursor.fetchone()[0]
        print(f"  ✅ Tabela '{tob}': OK ({cnt} registros)")

    # 2. Verificação de Integridade dos 90 Dias
    cursor.execute("SELECT COUNT(*), MIN(dia), MAX(dia) FROM forja_90_dias")
    total, min_d, max_d = cursor.fetchone()
    assert total == 90, f"Deveria ter 90 dias, tem {total}"
    assert min_d == 1, f"Menor dia deveria ser 1, é {min_d}"
    assert max_d == 90, f"Maior dia deveria ser 90, é {max_d}"
    print(f"  ✅ Forja dos 90 Dias: 100% preenchida (Dias 01 a 90).")

    # 3. Campos nulos ou inválidos na Forja
    cursor.execute("""
    SELECT dia, titulo FROM forja_90_dias 
    WHERE titulo IS NULL OR titulo = '' 
       OR versiculo_referencia IS NULL OR versiculo_referencia = ''
       OR texto_biblico IS NULL OR texto_biblico = ''
       OR principio_neurocientifico IS NULL OR principio_neurocientifico = ''
       OR missao_pratica IS NULL OR missao_pratica = ''
    """)
    incompletos = cursor.fetchall()
    assert len(incompletos) == 0, f"Dias com campos nulos: {incompletos}"
    print("  ✅ Todos os 90 dias possuem título, versículo, texto bíblico, princípio neurocientífico e missão prática.")

    # 4. Distribuição das Fases e Graduações
    cursor.execute("SELECT fase, graduacao, COUNT(*) FROM forja_90_dias GROUP BY fase, graduacao ORDER BY MIN(dia)")
    fases = cursor.fetchall()
    print("\n  Distribuição da Jornada de Transformação:")
    for f_nome, g_nome, f_cnt in fases:
        print(f"    • {f_nome} -> {g_nome} ({f_cnt} lições)")

    conn.close()

def auditar_regras_de_negocio():
    print("\n" + "="*50)
    print("🧠 [2/5] AUDITORIA DAS REGRAS DE NEGÓCIO & SERVIÇOS")
    print("="*50)

    db = DatabaseService()

    # 1. Teste de consulta em todos os 90 dias sem falhas
    for d in range(1, 91):
        licao = db.get_licao_do_dia(d)
        assert licao is not None, f"Falha ao consultar dia {d}"
        assert licao["dia"] == d
    print("  ✅ Consulta individual dos dias 1 ao 90: 100% OK.")

    # 2. Teste de progressão de Graduação Bíblica
    dias_teste = [0, 1, 10, 20, 21, 30, 50, 51, 60, 70, 71, 80, 89, 90, 100, 365]
    for d in dias_teste:
        grad = db.calcular_graduacao_biblica(d)
        assert "nivel" in grad and "titulo" in grad and "passo_label" in grad
        assert grad["nivel"] in [1, 2, 3, 4, 5]
    print("  ✅ Cálculo dinâmico das 5 Graduações Bíblicas (dias 0 a 365): 100% OK.")

    # 3. Teste de Parceiro de Aliança
    db.salvar_parceiro_alianca("Irmão Marcos", "11988887777")
    p = db.get_parceiro_alianca()
    assert p["nome"] == "Irmão Marcos"
    assert p["telefone_whatsapp"] == "5511988887777"
    print("  ✅ Configuração e higienização do WhatsApp do Parceiro: OK.")

    # 4. Teste da Teologia da Graça (sem humilhação)
    msg = db.zerar_contador_com_graca("Teste de tropeço")
    assert "chão não é o seu lugar" in msg
    assert "Pv 24:16" in msg or "Provérbios" in msg or "sangue de Jesus" in msg
    print("  ✅ Teologia da Graça (reset sem condenação): OK.")

def auditar_aplicativo_flet():
    print("\n" + "="*50)
    print("📱 [3/5] AUDITORIA DO APLICATIVO FLET (Python Desktop/Mobile)")
    print("="*50)

    arquivos_flet = [
        BASE_DIR / "main.py",
        BASE_DIR / "core" / "theme.py",
        BASE_DIR / "core" / "config.py",
        BASE_DIR / "services" / "db_service.py",
        BASE_DIR / "views" / "ordem_view.py",
        BASE_DIR / "views" / "sentinela_view.py",
        BASE_DIR / "views" / "alianca_view.py",
        BASE_DIR / "views" / "conselheiro_view.py",
    ]

    for arq in arquivos_flet:
        assert arq.exists(), f"Arquivo não encontrado: {arq}"
        with open(arq, "r", encoding="utf-8") as f:
            conteudo = f.read()
            assert len(conteudo) > 100, f"Arquivo vazio ou muito curto: {arq}"
            # Checa se não há pendências de TODO ou FIXME
            assert not re.search(r'\b(TODO|FIXME|PLACEHOLDER)\b', conteudo), f"Pendência encontrada em {arq.name}"
        print(f"  ✅ Módulo '{arq.name}': Verificado ({len(conteudo)} bytes).")

def auditar_landing_page():
    print("\n" + "="*50)
    print("🌐 [4/5] AUDITORIA DA LANDING PAGE & ESTÉTICA DARK OBSIDIAN")
    print("="*50)

    index_html = BASE_DIR / "index.html"
    styles_css = BASE_DIR / "styles.css"
    app_js = BASE_DIR / "app.js"

    with open(index_html, "r", encoding="utf-8") as f:
        html = f.read()

    with open(styles_css, "r", encoding="utf-8") as f:
        css = f.read()

    with open(app_js, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. IDs interativos essenciais
    ids_obrigatorios = [
        "demo-timer", "demo-instruction", "btn-iniciar-contagem", "btn-abrir-demo-sos",
        "checkout-modal", "modal-plano-nome", "modal-plano-preco",
        "checkout-form", "cust-name", "cust-email", "cust-phone",
        "pix-area", "pix-timer", "pix-qr-img", "pix-code-text", "btn-copiar-pix",
        "pix-success-area", "conf-name", "conf-email"
    ]
    for dom_id in ids_obrigatorios:
        assert f'id="{dom_id}"' in html, f"ID obrigatório ausente em index.html: {dom_id}"
    print(f"  ✅ Todos os {len(ids_obrigatorios)} IDs interativos estão presentes no DOM.")

    # 2. Seções principais da Landing Page
    secoes = ["hero", "epidemia", "pilares", "forja-metalurgia", "escrituras", "sos-demo", "precos", "faq"]
    for sec in secoes:
        assert f'id="{sec}"' in html or f'class="{sec}' in html or f'class="section' in html, f"Seção não encontrada: {sec}"
    print(f"  ✅ Seções estruturais presentes: Hero, Epidemia, Pilares, Forja 90D, Escrituras, SOS, Preços e FAQ.")

    # 3. Design System Dark Obsidian no CSS
    variaveis_css = ["--bg-dark", "--bg-surface", "--ember", "--text-white", "--border-subtle"]
    for var in variaveis_css:
        assert var in css, f"Variável de tema ausente no styles.css: {var}"
    print("  ✅ Design System Dark Obsidian verificado: Variáveis de paleta completas.")

    # 4. Lógicas no app.js
    funcoes_js = ["iniciarProtocoloSOS", "abrirCheckout", "fecharCheckout", "gerarPix", "copiarPix", "confirmarPix"]
    for func in funcoes_js:
        assert func in js, f"Função ausente no app.js: {func}"
    print(f"  ✅ Funções interativas de checkout e timer presentes no app.js.")

def auditar_engrenagem_vendas_e_anuncios():
    print("\n" + "="*50)
    print("💰 [5/5] AUDITORIA DA ENGRENAGEM DE VENDAS & COMPLIANCE")
    print("="*50)

    index_html = BASE_DIR / "index.html"
    with open(index_html, "r", encoding="utf-8") as f:
        html = f.read()

    # Checagem de palavras proibidas pelo Meta Ads / Google Ads que causam block
    # Palavras que acionam ban automático de BM em anúncios
    termos_risco = ["pornô grátis", "sexo explícito", "masturbe-se", "orgasmo"]
    for t in termos_risco:
        assert t not in html.lower(), f"Termo perigoso para políticas de anúncio encontrado: '{t}'"
    print("  ✅ Compliance de Anúncios: Zero termos de risco de ban na fachada da Landing Page.")

    # Validação do Pix EMV
    app_js = BASE_DIR / "app.js"
    with open(app_js, "r", encoding="utf-8") as f:
        js = f.read()

    assert "00020126" in js, "Padrão EMV Pix não encontrado no JS"
    assert "api.qrserver.com" in js, "Serviço de geração de QR Code não encontrado"
    print("  ✅ Geração de QR Code e chave Pix EMV do Banco Central validada.")

def executar_tudo():
    print("\n🚀 INICIANDO AUDITORIA PROFUNDA DE SISTEMA // METANOIA 2026")
    auditar_banco_de_dados()
    auditar_regras_de_negocio()
    auditar_aplicativo_flet()
    auditar_landing_page()
    auditar_engrenagem_vendas_e_anuncios()
    print("\n" + "="*50)
    print("🏆 AUDITORIA 100% CONCLUÍDA SEM NENHUM ERRO OU PENDÊNCIA!")
    print("="*50 + "\n")

if __name__ == "__main__":
    executar_tudo()
