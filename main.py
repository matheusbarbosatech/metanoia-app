"""
METANOIA — Ordem Interior. Honra Diária. Comunhão no Secreto.
Sistema Operacional de Sobriedade e Discipulado para Homens (18 a 35 anos).
Tecnologia: Python Flet (Material 3 / Dark Obsidian), SQLite Local (100% Offline-First).
"""
import sys
from pathlib import Path

# Garante resolução dos módulos
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import flet as ft
from core.config import APP_NAME, APP_TAGLINE
from core.theme import AppColors, AppStyles
from services.db_service import DatabaseService
from views.ordem_view import OrdemView
from views.sentinela_view import SentinelaView
from views.alianca_view import AliancaView
from views.conselheiro_view import ConselheiroView

def main(page: ft.Page):
    page.title = f"{APP_NAME} — {APP_TAGLINE}"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = AppColors.BG_DARK

    try:
        page.window.width = 440
        page.window.height = 880
        page.window.min_width = 360
        page.window.min_height = 700
        page.window.resizable = True
    except Exception:
        pass

    db = DatabaseService()
    db.init_db()

    current_tab_index = 0
    body_container = ft.Container(expand=True)

    # Função para atualizar badges do topo
    progresso = db.get_progresso()
    graduacao = db.get_graduacao_bjj()
    
    dias_limpos_txt = ft.Text(f"🔥 {progresso.get('dias_limpos', 0)}d", style=AppStyles.CAPTION, color=AppColors.EMBER, weight=ft.FontWeight.BOLD)
    xp_txt = ft.Text(f"⚔️ {progresso.get('xp_forja', 0)}xp", style=AppStyles.CAPTION, color=AppColors.TEXT_WHITE, weight=ft.FontWeight.BOLD)
    
    # Badge de Maturidade Bíblica
    nivel_txt = ft.Text(
        f"{graduacao['icone']} {graduacao['titulo']}",
        style=AppStyles.CAPTION,
        color=graduacao["cor_badge"],
        weight=ft.FontWeight.BOLD
    )
    nivel_container = ft.Container(
        padding=ft.padding.symmetric(horizontal=10, vertical=4),
        border_radius=8,
        bgcolor=graduacao["cor_bg"],
        border=ft.border.all(1, graduacao["cor_badge"]),
        content=nivel_txt,
        tooltip=f"{graduacao['fase']} | {graduacao['passo_label']}\n'{graduacao['texto_versiculo']}' ({graduacao['versiculo']})"
    )

    def refresh_header():
        p = db.get_progresso()
        g = db.get_graduacao_biblica()
        dias_limpos_txt.value = f"🔥 {p.get('dias_limpos', 0)}d"
        xp_txt.value = f"⚔️ {p.get('xp_forja', 0)}xp"
        nivel_txt.value = f"{g['icone']} {g['titulo']}"
        nivel_txt.color = g["cor_badge"]
        nivel_container.bgcolor = g["cor_bg"]
        nivel_container.border = ft.border.all(1, g["cor_badge"])
        nivel_container.tooltip = f"{g['fase']} | {g['passo_label']}\n'{g['texto_versiculo']}' ({g['versiculo']})"
        page.update()

    def set_tab(idx: int):
        nonlocal current_tab_index
        current_tab_index = idx
        if idx == 0:
            body_container.content = OrdemView(page, on_concluir=refresh_header).build()
        elif idx == 1:
            body_container.content = SentinelaView(page, on_vitoria=refresh_header).build()
        elif idx == 2:
            body_container.content = AliancaView(page).build()
        elif idx == 3:
            body_container.content = ConselheiroView(page).build()
        page.update()

    page.refresh_view = lambda: set_tab(current_tab_index)

    # Barra Superior (Header)
    header = ft.Container(
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=AppColors.BG_SURFACE,
        border=ft.border.only(bottom=ft.border.BorderSide(1, AppColors.BORDER_SUBTLE)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.Icon(ft.icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, color=AppColors.EMBER, size=22),
                        ft.Text(APP_NAME, style=AppStyles.TITLE_LARGE),
                    ]
                ),
                ft.Row(
                    spacing=8,
                    controls=[
                        nivel_container,
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            border_radius=8,
                            bgcolor=AppColors.EMBER_BG,
                            border=ft.border.all(1, AppColors.EMBER),
                            content=dias_limpos_txt
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                            border_radius=8,
                            bgcolor=AppColors.BG_SURFACE_ALT,
                            border=ft.border.all(1, AppColors.BORDER_SUBTLE),
                            content=xp_txt
                        ),
                    ]
                )
            ]
        )
    )

    # Barra Inferior (Bottom Navigation)
    nav_bar = ft.NavigationBar(
        bgcolor=AppColors.BG_SURFACE,
        indicator_color=AppColors.BG_SURFACE_HOVER,
        selected_index=0,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.SUNNY, label="Ordem"),
            ft.NavigationDestination(icon=ft.icons.SHIELD, label="Sentinela"),
            ft.NavigationDestination(icon=ft.icons.HANDSHAKE_OUTLINED, label="Aliança"),
            ft.NavigationDestination(icon=ft.icons.CHAT_BUBBLE_OUTLINE, label="Conselheiro"),
        ],
        on_change=lambda e: set_tab(e.control.selected_index),
    )

    # Inicializa com a primeira aba
    set_tab(0)

    page.add(
        ft.Column(
            expand=True,
            spacing=0,
            controls=[
                header,
                body_container,
                nav_bar,
            ]
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
