"""
Aba 01: A Ordem Matinal (Protocolo dos 7 Minutos).
A Forja dos 90 Dias: O Texto Cru (Bíblia sem filtro) + O Áudio da Ordem + O Princípio Biológico + A Missão do Dia.
"""
import flet as ft
from core.theme import AppColors, AppStyles
from services.db_service import DatabaseService

class OrdemView:
    def __init__(self, page: ft.Page, on_concluir=None):
        self.page = page
        self.on_concluir = on_concluir
        self.db = DatabaseService()
        self.dia_selecionado = 1
        self.licao_atual = self.db.get_licao_do_dia(self.dia_selecionado)
        self.audio_tocando = False

    def mudar_dia(self, delta: int):
        novo_dia = max(1, min(90, self.dia_selecionado + delta))
        if novo_dia != self.dia_selecionado:
            self.dia_selecionado = novo_dia
            self.licao_atual = self.db.get_licao_do_dia(novo_dia)
            if hasattr(self.page, "refresh_view"):
                self.page.refresh_view()
            self.page.update()

    def _tocar_audio(self, e):
        self.audio_tocando = not self.audio_tocando
        dia = self.licao_atual['dia'] if self.licao_atual else 1
        msg = f"🎧 Áudio da Ordem (Dia {dia}): Reproduzindo narração solene. Ouça no fone enquanto arruma a cama!" if self.audio_tocando else "Áudio pausado."
        self.page.snack_bar = ft.SnackBar(
            ft.Text(msg, color=AppColors.TEXT_WHITE),
            bgcolor=AppColors.EMBER if self.audio_tocando else AppColors.BG_SURFACE_ALT
        )
        self.page.snack_bar.open = True
        self.page.update()

    def build(self) -> ft.Control:
        if not self.licao_atual:
            return ft.Text("Nenhuma lição disponível.", color=AppColors.TEXT_MUTED)

        fase_nome = self.licao_atual.get("fase", "A FORJA")
        graduacao_nome = self.licao_atual.get("graduacao", "O RESGATADO")

        return ft.ListView(
            spacing=16,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            controls=[
                # Cabeçalho da Ordem com Navegação
                ft.Container(
                    padding=16,
                    border_radius=12,
                    bgcolor=AppColors.BG_SURFACE_ALT,
                    border=ft.border.all(1, AppColors.BORDER_SUBTLE),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(f"{fase_nome} // {graduacao_nome}", style=AppStyles.CAPTION, color=AppColors.EMBER),
                                    ft.Row(
                                        spacing=4,
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.icons.CHEVRON_LEFT,
                                                icon_size=18,
                                                icon_color=AppColors.TEXT_WHITE if self.dia_selecionado > 1 else AppColors.TEXT_MUTED,
                                                on_click=lambda _: self.mudar_dia(-1),
                                                tooltip="Dia Anterior"
                                            ),
                                            ft.Text(f"DIA {self.licao_atual['dia']}/90", style=AppStyles.CAPTION, weight=ft.FontWeight.BOLD),
                                            ft.IconButton(
                                                icon=ft.icons.CHEVRON_RIGHT,
                                                icon_size=18,
                                                icon_color=AppColors.TEXT_WHITE if self.dia_selecionado < 90 else AppColors.TEXT_MUTED,
                                                on_click=lambda _: self.mudar_dia(1),
                                                tooltip="Próximo Dia"
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                            ft.Text(self.licao_atual["titulo"], style=AppStyles.TITLE_MEDIUM),
                        ]
                    )
                ),

                # Widget Audio-First (Combate à Fadiga de Leitura / Abismo do Dia 14)
                ft.Container(
                    padding=12,
                    border_radius=10,
                    bgcolor=AppColors.BG_SURFACE_HOVER,
                    border=ft.border.all(1, AppColors.BORDER_SUBTLE),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=10,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.PLAY_CIRCLE_FILLED if not self.audio_tocando else ft.icons.PAUSE_CIRCLE_FILLED,
                                        icon_color=AppColors.EMBER,
                                        icon_size=32,
                                        on_click=self._tocar_audio,
                                        tooltip="Ouvir Narração da Ordem"
                                    ),
                                    ft.Column(
                                        spacing=2,
                                        controls=[
                                            ft.Text("ÁUDIO DA ORDEM // 2 MIN", style=AppStyles.CAPTION, color=AppColors.TEXT_WHITE, weight=ft.FontWeight.BOLD),
                                            ft.Text("Narração de comando militar e oração guiada", style=AppStyles.CAPTION, color=AppColors.TEXT_MUTED),
                                        ]
                                    )
                                ]
                            ),
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=6,
                                bgcolor=AppColors.BG_SURFACE,
                                content=ft.Text("🎧 2:15", style=AppStyles.CAPTION, color=AppColors.EMBER)
                            )
                        ]
                    )
                ),

                # Seção 1: O Texto Cru (A Espada da Palavra)
                ft.Container(
                    padding=16,
                    border_radius=12,
                    bgcolor=AppColors.BG_SURFACE,
                    border=ft.border.all(1, AppColors.BORDER_SUBTLE),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text("01. A PALAVRA SEM FILTRO", style=AppStyles.CAPTION, color=AppColors.TEXT_MUTED),
                            ft.Text(f"\"{self.licao_atual['texto_biblico']}\"", style=AppStyles.VERSE_TEXT),
                            ft.Text(f"— {self.licao_atual['versiculo_referencia']}", style=AppStyles.CAPTION, color=AppColors.EMBER),
                        ]
                    )
                ),

                # Seção 2: O Princípio Neurocientífico
                ft.Container(
                    padding=16,
                    border_radius=12,
                    bgcolor=AppColors.BG_SURFACE,
                    border=ft.border.all(1, AppColors.BORDER_SUBTLE),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Text("02. A REALIDADE BIOLÓGICA", style=AppStyles.CAPTION, color=AppColors.TEXT_MUTED),
                            ft.Text(self.licao_atual["principio_neurocientifico"], style=AppStyles.BODY_TEXT),
                        ]
                    )
                ),

                # Seção 3: A Missão Prática do Dia
                ft.Container(
                    padding=16,
                    border_radius=12,
                    bgcolor=AppColors.BG_SURFACE_ALT,
                    border=ft.border.all(1, AppColors.EMBER),
                    content=ft.Column(
                        spacing=8,
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.SHIELD_OUTLINED, color=AppColors.EMBER, size=18),
                                    ft.Text("03. SUA ORDEM DE MISSÃO HOJE", style=AppStyles.CAPTION, color=AppColors.EMBER),
                                ]
                            ),
                            ft.Text(self.licao_atual["missao_pratica"], style=AppStyles.BODY_TEXT, weight=ft.FontWeight.W_500),
                        ]
                    )
                ),

                # Botão de Conclusão da Ordem
                ft.Container(
                    padding=ft.padding.only(top=10, bottom=20),
                    content=ft.ElevatedButton(
                        text=f"SELAR A ORDEM DE HOJE (+{self.licao_atual.get('xp_recompensa', 30)} XP)",
                        style=ft.ButtonStyle(
                            bgcolor=AppColors.PRIMARY,
                            color=AppColors.TEXT_DARK,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.padding.symmetric(vertical=16),
                        ),
                        on_click=self._concluir,
                    )
                )
            ]
        )

    def _concluir(self, e):
        self.db.concluir_licao(self.licao_atual["dia"])
        if self.on_concluir:
            self.on_concluir()
        self.page.snack_bar = ft.SnackBar(
            ft.Text("Ordem Matinal selada. Vá para o mundo e mantenha seus olhos puros!", color=AppColors.TEXT_WHITE),
            bgcolor=AppColors.SUCCESS_GREEN
        )
        self.page.snack_bar.open = True
        self.page.update()
