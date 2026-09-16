"""
Aba 02: A Sentinela (Protocolo SOS Anti-Recaída).
O Botão de Emergência para as horas críticas da noite.
Corta o pico de dopamina em 180 segundos através de respiração, choque térmico e firmeza bíblica.
"""
import flet as ft
import time
import threading
from core.theme import AppColors, AppStyles
from services.db_service import DatabaseService

class SentinelaView:
    def __init__(self, page: ft.Page, on_vitoria=None):
        self.page = page
        self.on_vitoria = on_vitoria
        self.db = DatabaseService()
        self.em_alerta = False
        self.tempo_restante = 180  # 3 minutos (tempo da onda da dopamina)

    def build(self) -> ft.Control:
        if not self.em_alerta:
            return self._build_tela_vigilia()
        else:
            return self._build_tela_sos()

    def _build_tela_vigilia(self) -> ft.Control:
        progresso = self.db.get_progresso()
        return ft.ListView(
            spacing=16,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            controls=[
                # Painel de Status
                ft.Container(
                    padding=20,
                    border_radius=12,
                    bgcolor=AppColors.BG_SURFACE_ALT,
                    border=ft.border.all(1, AppColors.BORDER_SUBTLE),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            ft.Icon(ft.icons.SHIELD, color=AppColors.EMBER, size=40),
                            ft.Text("SISTEMA DE VIGÍLIA ATIVO", style=AppStyles.CAPTION, color=AppColors.EMBER),
                            ft.Text(f"{progresso.get('dias_limpos', 0)} DIAS", style=ft.TextStyle(size=36, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE)),
                            ft.Text("SOBRIEDADE RADICAL // RECONSTRUÇÃO NEURAL", style=AppStyles.CAPTION),
                        ]
                    )
                ),

                # Regra das 22h às 02h
                ft.Container(
                    padding=16,
                    border_radius=12,
                    bgcolor=AppColors.BG_SURFACE,
                    border=ft.border.all(1, AppColors.BORDER_SUBTLE),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text("A ZONA CRÍTICA: 22H ÀS 02H", style=AppStyles.CAPTION, color=AppColors.EMBER),
                            ft.Text("87% das recaídas ocorrem quando o homem está cansado, sozinho e no escuro. A batalha não é de força de vontade; é de cortar o estímulo antes que ele vire ato.", style=AppStyles.BODY_TEXT),
                        ]
                    )
                ),

                # O Botão Vermelho de Emergência
                ft.Container(
                    padding=ft.padding.only(top=20),
                    content=ft.ElevatedButton(
                        text="⚡ ESTOU SOB ATAQUE / FISSURA",
                        style=ft.ButtonStyle(
                            bgcolor=AppColors.RED_ALERT,
                            color=AppColors.TEXT_WHITE,
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=ft.padding.symmetric(vertical=20),
                        ),
                        on_click=self._ativar_sos,
                    )
                ),
                ft.Text("Toque se sentir a vontade subindo. Não tente negociar com a carne.", style=AppStyles.CAPTION, text_align=ft.TextAlign.CENTER)
            ]
        )

    def _build_tela_sos(self) -> ft.Control:
        return ft.ListView(
            spacing=16,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            controls=[
                # Alerta SOS
                ft.Container(
                    padding=20,
                    border_radius=12,
                    bgcolor=AppColors.RED_ALERT_BG,
                    border=ft.border.all(2, AppColors.RED_ALERT),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            ft.Text("PROTOCOLO DE DESCOMPRESSÃO ATIVO", style=AppStyles.CAPTION, color=AppColors.RED_ALERT),
                            ft.Text(f"{self.tempo_restante // 60}:{self.tempo_restante % 60:02d}", style=ft.TextStyle(size=44, weight=ft.FontWeight.BOLD, color=AppColors.TEXT_WHITE)),
                            ft.Text("A onda atinge o pico e quebra em 3 minutos. Não ceda.", style=AppStyles.BODY_MUTED),
                        ]
                    )
                ),

                # Instruções Imediatas
                ft.Container(
                    padding=16,
                    border_radius=12,
                    bgcolor=AppColors.BG_SURFACE_ALT,
                    content=ft.Column(
                        spacing=12,
                        controls=[
                            ft.Text("ORDENS IMEDIATAS:", style=AppStyles.CAPTION, color=AppColors.EMBER),
                            ft.Text("1. LARGUE O CELULAR NA MESA AGORA.", style=AppStyles.BODY_TEXT, weight=ft.FontWeight.BOLD),
                            ft.Text("2. Vá até a pia e lave o rosto com água gelada (ativa o reflexo vagal e desacelera o coração).", style=AppStyles.BODY_TEXT),
                            ft.Text("3. Faça 20 flexões no chão imediatamente para redirecionar o fluxo sanguíneo.", style=AppStyles.BODY_TEXT),
                            ft.Text("4. Dobre os joelhos e diga em voz alta: 'Cristo me comprou. Eu não sou escravo da tela'.", style=AppStyles.BODY_TEXT),
                        ]
                    )
                ),

                # Botão de Vitória
                ft.Container(
                    padding=ft.padding.only(top=10),
                    content=ft.ElevatedButton(
                        text="VENCEI A ONDA // SALVEI MINHA HONRA",
                        style=ft.ButtonStyle(
                            bgcolor=AppColors.SUCCESS_GREEN,
                            color=AppColors.TEXT_WHITE,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.padding.symmetric(vertical=16),
                        ),
                        on_click=self._vencer_sos,
                    )
                )
            ]
        )

    def _ativar_sos(self, e):
        self.em_alerta = True
        self.db.registrar_sos("Fissura Noturna", vitoria=False)
        self.page.views.clear()
        self.page.update()
        if hasattr(self.page, "refresh_view"):
            self.page.refresh_view()

    def _vencer_sos(self, e):
        self.em_alerta = False
        self.db.registrar_sos("Fissura Noturna", vitoria=True)
        if self.on_vitoria:
            self.on_vitoria()
        self.page.snack_bar = ft.SnackBar(
            ft.Text("Honra preservada! +50 XP de Guerra adicionados.", color=AppColors.TEXT_WHITE),
            bgcolor=AppColors.SUCCESS_GREEN
        )
        self.page.snack_bar.open = True
        if hasattr(self.page, "refresh_view"):
            self.page.refresh_view()
        self.page.update()
