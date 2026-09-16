# -*- coding: utf-8 -*-
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from services.db_service import DatabaseService

def executar_testes():
    print("=== TESTES PROFUNDOS // METANOIA ===")
    db = DatabaseService()

    # 1. Validação dos 90 Dias
    print("\n[1/4] Testando Forja dos 90 Dias...")
    dias_chave = [1, 7, 14, 21, 22, 35, 50, 51, 60, 70, 71, 80, 89, 90]
    for dia in dias_chave:
        licao = db.get_licao_do_dia(dia)
        assert licao is not None, f"Falha no dia {dia}"
        assert len(licao["titulo"]) > 5, f"Título curto no dia {dia}"
        assert len(licao["principio_neurocientifico"]) > 20, f"Princípio curto no dia {dia}"
        print(f"  [OK] Dia {dia:02d}: [{licao['graduacao']}] {licao['titulo']}")

    # 2. Validação do Parceiro de Aliança
    print("\n[2/4] Testando Parceiro de Aliança e Higienização de WhatsApp...")
    db.salvar_parceiro_alianca("Pastor Samuel", "(11) 97777-6666")
    p = db.get_parceiro_alianca()
    assert p["nome"] == "Pastor Samuel"
    assert p["telefone_whatsapp"] == "5511977776666"
    print(f"  [OK] Parceiro salvo: {p['nome']} -> {p['telefone_whatsapp']}")

    # 3. Validação da Teologia da Graça
    print("\n[3/4] Testando Restauração com Graça (Sem autoflagelação)...")
    msg = db.zerar_contador_com_graca("Combate difícil na madrugada")
    assert "chão não é o seu lugar" in msg
    prog = db.get_progresso()
    assert prog["dias_limpos"] == 0
    print(f"  [OK] Mensagem de Graça: {msg[:65]}...")
    print(f"  [OK] Contador zerado com dignidade, Recorde mantido em {prog['recorde_dias']} dias.")

    # 4. Validação das 5 Graduações Bíblicas
    print("\n[4/4] Testando as 5 Graduações de Maturidade Bíblica...")
    cenarios = [
        (0, 1, "O RESGATADO"),
        (20, 1, "O RESGATADO"),
        (21, 2, "O DISCÍPULO"),
        (45, 2, "O DISCÍPULO"),
        (51, 3, "O GUERREIRO"),
        (65, 3, "O GUERREIRO"),
        (71, 4, "O SACERDOTE"),
        (88, 4, "O SACERDOTE"),
        (90, 5, "O PATRIARCA"),
        (120, 5, "O PATRIARCA"),
    ]
    for d, nivel_esp, tit_esp in cenarios:
        g = db.calcular_graduacao_biblica(d)
        assert g["nivel"] == nivel_esp, f"Dia {d}: esperava nível {nivel_esp}, veio {g['nivel']}"
        assert g["titulo"] == tit_esp, f"Dia {d}: esperava {tit_esp}, veio {g['titulo']}"
        print(f"  [OK] {d:03d} dias limpos -> Nível {g['nivel']}: {g['titulo']} ({g['passo_label']})")

    print("\n==============================================")
    print("✅ TODOS OS 4 NÚCLEOS DE TESTE PASSARAM COM SUCESSO!")
    print("==============================================")

if __name__ == "__main__":
    executar_testes()
