"""
Aba 04: O Conselheiro de Guerra (IA Especializada).
Acolhimento em momentos de crise, esclarecimento de dúvidas sobre vício e neurociência,
e exortação bíblica firme.
"""
import flet as ft
from core.theme import AppColors, AppStyles
from services.ai_advisor import AIAdvisorService

class ConselheiroView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.mensagens_col = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO, expand=True)
        self.input_chat = ft.TextField(
            hint_text="Desabafe ou pergunte sobre sua luta...",
            hint_style=ft.TextStyle(color=AppColors.TEXT_MUTED, size=13),
            text_size=13,
            color=AppColors.TEXT_WHITE,
            bgcolor=AppColors.BG_SURFACE_ALT,
            border_color=AppColors.BORDER_SUBTLE,
            focused_border_color=AppColors.EMBER,
            border_radius=10,
            content_padding=ft.padding.symmetric(horizontal=14, vertical=12),
            expand=True,
            on_submit=lambda _: self._enviar(),
        )

    def build(self) -> ft.Control:
        # Mensagem inicial do Conselheiro
        if len(self.mensagens_col.controls) == 0:
            self.mensagens_col.controls.append(
                self._criar_balao(
                    "Irmão, aqui não há hipocrisia e nem julgamento farisaico. O que você está enfrentando? Uma crise de fissura, uma recaída recente ou dúvidas sobre como blindar sua mente?",
                    is_user=False
                )
            )

        # Sugestões rápidas
        sugestoes = ft.Row(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                self._criar_chip_sugestao("Recaí ontem, o que fazer?"),
                self._criar_chip_sugestao("Como vencer a fissura da meia-noite?"),
                self._criar_chip_sugestao("A pornografia causa disfunção erétil?"),
            ]
        )

        return ft.Column(
            expand=True,
            spacing=10,
            controls=[
                # Área de Sugestões
                ft.Container(padding=ft.padding.symmetric(horizontal=16), content=sugestoes),
                
                # Lista de Mensagens
                ft.Container(
                    expand=True,
                    padding=ft.padding.symmetric(horizontal=16),
                    content=self.mensagens_col
                ),

                # Barra de Envio
                ft.Container(
                    padding=ft.padding.only(left=16, right=16, bottom=16, top=8),
                    bgcolor=AppColors.BG_SURFACE,
                    border=ft.border.only(top=ft.border.BorderSide(1, AppColors.BORDER_SUBTLE)),
                    content=ft.Row(
                        controls=[
                            self.input_chat,
                            ft.IconButton(
                                icon=ft.icons.ARROW_UPWARD_ROUNDED,
                                icon_color=AppColors.TEXT_DARK,
                                bgcolor=AppColors.PRIMARY,
                                icon_size=20,
                                on_click=lambda _: self._enviar(),
                            )
                        ]
                    )
                )
            ]
        )

    def _criar_chip_sugestao(self, texto: str) -> ft.Control:
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=20,
            bgcolor=AppColors.BG_SURFACE_ALT,
            border=ft.border.all(1, AppColors.BORDER_SUBTLE),
            content=ft.Text(texto, style=AppStyles.CAPTION, color=AppColors.TEXT_WHITE),
            on_click=lambda _: self._usar_sugestao(texto),
        )

    def _usar_sugestao(self, texto: str):
        self.input_chat.value = texto
        self._enviar()

    def _enviar(self):
        texto = self.input_chat.value.strip()
        if not texto:
            return

        self.input_chat.value = ""
        self.mensagens_col.controls.append(self._criar_balao(texto, is_user=True))
        self.page.update()

        # Resposta da IA especializada
        resposta = AIAdvisorService.responder(texto)
        self.mensagens_col.controls.append(self._criar_balao(resposta, is_user=False))
        self.page.update()

    def _criar_balao(self, texto: str, is_user: bool) -> ft.Control:
        return ft.Container(
            alignment=ft.alignment.center_right if is_user else ft.alignment.center_left,
            content=ft.Container(
                padding=12,
                border_radius=12,
                bgcolor=AppColors.BG_SURFACE_ALT if is_user else AppColors.BG_SURFACE,
                border=ft.border.all(1, AppColors.EMBER if not is_user else AppColors.BORDER_SUBTLE),
                width=320,
                content=ft.Column(
                    spacing=4,
                    controls=[
                        ft.Text("VOCÊ" if is_user else "CONSELHEIRO DE GUERRA", style=AppStyles.CAPTION, color=AppColors.TEXT_MUTED if is_user else AppColors.EMBER),
                        ft.Text(texto, style=AppStyles.BODY_TEXT),
                    ]
                )
            )
        )
