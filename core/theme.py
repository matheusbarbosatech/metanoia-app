"""
Design System Dark Brutalist / Obsidian Minimalist para o METANOIA.
Cores sóbrias, foco absoluto em contraste, sem poluição visual.
"""
import flet as ft

# Compatibilidade garantida com todas as versões do Flet (0.2x a 0.86+)
if not hasattr(ft.padding, "symmetric") and hasattr(ft, "Padding"):
    ft.padding.symmetric = ft.Padding.symmetric
    ft.padding.all = ft.Padding.all
    ft.padding.only = ft.Padding.only

if not hasattr(ft.border, "all") and hasattr(ft, "Border"):
    ft.border.all = ft.Border.all
    ft.border.only = ft.Border.only
    ft.border.symmetric = ft.Border.symmetric
    if hasattr(ft, "BorderSide"):
        ft.border.BorderSide = ft.BorderSide

if hasattr(ft, "Icons"):
    ft.icons = ft.Icons

if not hasattr(ft, "colors") and hasattr(ft, "Colors"):
    ft.colors = ft.Colors

if hasattr(ft, "Alignment"):
    ft.alignment.center_left = ft.Alignment.CENTER_LEFT
    ft.alignment.center_right = ft.Alignment.CENTER_RIGHT
    ft.alignment.center = ft.Alignment.CENTER
    ft.alignment.top_left = ft.Alignment.TOP_LEFT
    ft.alignment.top_right = ft.Alignment.TOP_RIGHT
    ft.alignment.bottom_left = ft.Alignment.BOTTOM_LEFT
    ft.alignment.bottom_right = ft.Alignment.BOTTOM_RIGHT

if not hasattr(ft, "NavigationDestination") and hasattr(ft, "NavigationBarDestination"):
    ft.NavigationDestination = ft.NavigationBarDestination

# Compatibilidade para botões: mapeia 'text' para 'content' no Flet 0.80+
def _patch_btn(btn_cls):
    if hasattr(btn_cls, "__init__"):
        orig_init = btn_cls.__init__
        def new_init(self, *args, **kwargs):
            if "text" in kwargs and "content" not in kwargs:
                kwargs["content"] = kwargs.pop("text")
            orig_init(self, *args, **kwargs)
        btn_cls.__init__ = new_init

for _b in [getattr(ft, "ElevatedButton", None), getattr(ft, "OutlinedButton", None), getattr(ft, "TextButton", None), getattr(ft, "FilledButton", None), getattr(ft, "Button", None)]:
    if _b:
        _patch_btn(_b)

class AppColors:
    # Fundo e Superfícies
    BG_DARK = "#050505"         # Preto Absoluto
    BG_SURFACE = "#0E0E10"      # Superfície Elevada
    BG_SURFACE_ALT = "#16161A"  # Cartões e Inputs
    BG_SURFACE_HOVER = "#222227"

    # Bordas e Linhas de Separação
    BORDER_SUBTLE = "#232328"
    BORDER_STRONG = "#383842"

    # Tipografia
    TEXT_WHITE = "#FAFAFA"      # Texto Principal
    TEXT_MUTED = "#8A8A93"      # Texto Secundário / Legendas
    TEXT_DARK = "#121214"

    # Acentos Funcionais
    PRIMARY = "#FAFAFA"         # Branco Puro para botões de impacto
    EMBER = "#EA580C"           # Laranja Brasa (Chama do Altar / Alerta de Guerra)
    EMBER_BG = "#2B1408"        # Fundo suave para alertas de brasa
    RED_ALERT = "#EF4444"       # Botão SOS / Pânico
    RED_ALERT_BG = "#2B0B0B"    # Fundo de pânico
    SUCCESS_GREEN = "#10B981"   # Dia Cumprido / Aliança Selada
    SUCCESS_BG = "#06231A"

class AppStyles:
    TITLE_LARGE = ft.TextStyle(size=22, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE, letter_spacing=0.5)
    TITLE_MEDIUM = ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE, letter_spacing=0.3)
    BODY_TEXT = ft.TextStyle(size=13, color=AppColors.TEXT_WHITE, height=1.4)
    BODY_MUTED = ft.TextStyle(size=12, color=AppColors.TEXT_MUTED, height=1.4)
    CAPTION = ft.TextStyle(size=11, color=AppColors.TEXT_MUTED, letter_spacing=0.5)
    VERSE_TEXT = ft.TextStyle(size=14, weight=ft.FontWeight.W_500, italic=True, color=AppColors.TEXT_WHITE, height=1.5)
