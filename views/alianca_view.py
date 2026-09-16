"""
Aba 03: A Aliança (Pacto de Honra 1-to-1).
Prestação de contas real com consequência social direta no WhatsApp.
Sabatina diária das 21h30: 3 perguntas binárias e envio com 1 toque para o parceiro.
"""
import urllib.parse
import webbrowser
import flet as ft
from core.theme import AppColors, AppStyles
from services.db_service import DatabaseService

class AliancaView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = DatabaseService()
        self.parceiro = self.db.get_parceiro_alianca()
        self.q1_val = True
        self.q2_val = True
        self.q3_val = True

    def _abrir_dialogo_parceiro(self, e):
        nome_field = ft.TextField(
            label="Nome do Parceiro de Aliança",
            value=self.parceiro.get("nome", "Irmão de Guerra"),
            border_color=AppColors.BORDER_SUBTLE,
            focused_border_color=AppColors.EMBER,
            color=AppColors.TEXT_WHITE,
        )
        tel_field = ft.TextField(
            label="WhatsApp com DDD (apenas números, ex: 11999998888)",
            value=self.parceiro.get("telefone_whatsapp", ""),
            border_color=AppColors.BORDER_SUBTLE,
            focused_border_color=AppColors.EMBER,
            color=AppColors.TEXT_WHITE,
        )

        def salvar(evt):
            nome = nome_field.value.strip() or "Irmão de Guerra"
            tel = tel_field.value.strip()
            self.db.salvar_parceiro_alianca(nome, tel)
            self.parceiro = self.db.get_parceiro_alianca()
            dialog.open = False
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Parceiro de Aliança configurado com sucesso!", color=AppColors.TEXT_WHITE),
                bgcolor=AppColors.SUCCESS_GREEN
            )
            self.page.snack_bar.open = True
            if hasattr(self.page, "refresh_view"):
                self.page.refresh_view()
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Configurar Parceiro de Aliança", color=AppColors.TEXT_WHITE, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                tight=True,
                spacing=12,
                controls=[
                    ft.Text("Defina quem receberá seu relatório diário de honra às 21h30 (amigo, mentor, noiva ou pastor):", style=AppStyles.CAPTION),
                    nome_field,
                    tel_field,
                ]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: setattr(dialog, 'open', False) or self.page.update()),
                ft.ElevatedButton("Salvar Parceiro", bgcolor=AppColors.EMBER, color=AppColors.TEXT_DARK, on_click=salvar),
            ],
            bgcolor=AppColors.BG_SURFACE_ALT,
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _abrir_dialogo_graca(self, e):
        def confirmar_reinicio(evt):
            msg_restauracao = self.db.zerar_contador_com_graca("Reinício voluntário")
            dialog_graca.open = False
            self.page.snack_bar = ft.SnackBar(
                ft.Text(msg_restauracao, color=AppColors.TEXT_WHITE, size=13),
                bgcolor=AppColors.EMBER,
                duration=6000
            )
            self.page.snack_bar.open = True
            if hasattr(self.page, "refresh_view"):
                self.page.refresh_view()
            self.page.update()

        dialog_graca = ft.AlertDialog(
            title=ft.Text("A Graça de Cristo (Sem Condenação)", color=AppColors.EMBER, weight=ft.FontWeight.BOLD),
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[
                    ft.Text(
                        "Houve um tropeço hoje? Não se esconda e não aceite a mentira da culpa paralisante.",
                        style=AppStyles.BODY_TEXT
                    ),
                    ft.Text(
                        "\"O justo cai sete vezes e se levanta.\" (Provérbios 24:16)\n"
                        "Zere o contador com dignidade. Seu recorde é preservado e a forja continua hoje.",
                        style=AppStyles.CAPTION,
                        color=AppColors.TEXT_MUTED
                    ),
                ]
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: setattr(dialog_graca, 'open', False) or self.page.update()),
                ft.ElevatedButton("Zerar com Graça e Levantar", bgcolor=AppColors.PRIMARY, color=AppColors.TEXT_DARK, on_click=confirmar_reinicio),
            ],
            bgcolor=AppColors.BG_SURFACE_ALT,
        )
        self.page.dialog = dialog_graca
        dialog_graca.open = True
        self.page.update()

    def _transmitir_whatsapp(self, e):
        progresso = self.db.get_progresso()
        graduacao = self.db.get_graduacao_biblica()
        dias = progresso.get("dias_limpos", 0)
        tel = self.parceiro.get("telefone_whatsapp", "")

        q1_txt = "✅ SIM" if self.q1_val else "❌ NÃO (Preciso de oração)"
        q2_txt = "✅ SIM" if self.q2_val else "❌ NÃO"
        q3_txt = "✅ SIM" if self.q3_val else "❌ NÃO"

        if self.q1_val:
            msg = (
                f"🛡️ *METANOIA // SABATINA DA ALIANÇA (21H30)*\n"
                f"👤 *Guerreiro:* Homem de Honra\n"
                f"⚔️ *Graduação:* {graduacao.get('titulo', 'O RESGATADO')} ({graduacao.get('passo_label', '')})\n"
                f"🔥 *Dias Limpos:* {dias} dias na forja\n\n"
                f"*Relatório de Honra de Hoje:*\n"
                f"1. Olhos e pensamentos guardados? {q1_txt}\n"
                f"2. Ordem Matinal e joelhos no chão? {q2_txt}\n"
                f"3. Família honrada e trabalho diligente? {q3_txt}\n\n"
                f"_\"Como o ferro com o ferro se afia, assim o homem ao seu irmão.\" (Pv 27:17)_\n"
                f"Honra selada hoje! ⚔️"
            )
        else:
            msg = (
                f"⚠️ *METANOIA // ALERTA DE BATALHA & COBERTURA (21H30)*\n"
                f"👤 *Guerreiro:* Homem de Honra\n"
                f"⚔️ *Graduação:* {graduacao.get('titulo', 'O RESGATADO')}\n\n"
                f"Meu irmão, hoje enfrentei um combate duro e tropecei no item 1. Mas não me escondo nas sombras: "
                f"o sangue de Jesus me purifica e eu já estou de pé. "
                f"Peço sua oração e cobertura espiritual esta noite. Um guerreiro não fica no chão!\n\n"
                f"_\"Confessai as vossas culpas uns aos outros e orai uns pelos outros para que sareis.\" (Tg 5:16)_"
            )

        # Salva o checkin no banco
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO alianca_checkin (data, olhos_guardados, ordem_matinal, honrou_casa, observacao)
            VALUES (datetime('now'), ?, ?, ?, ?)
            """, (1 if self.q1_val else 0, 1 if self.q2_val else 0, 1 if self.q3_val else 0, "Transmitido via WhatsApp"))
            conn.commit()

        # Abre o WhatsApp via URL Scheme
        tel_limpo = "".join(filter(str.isdigit, tel))
        if tel_limpo:
            url = f"https://wa.me/{tel_limpo}?text={urllib.parse.quote(msg)}"
        else:
            url = f"https://wa.me/?text={urllib.parse.quote(msg)}"

        try:
            webbrowser.open(url)
        except Exception:
            pass

        self.page.snack_bar = ft.SnackBar(
            ft.Text(f"Relatório gerado! Abrindo WhatsApp de {self.parceiro.get('nome')}...", color=AppColors.TEXT_WHITE),
            bgcolor=AppColors.SUCCESS_GREEN
        )
        self.page.snack_bar.open = True
        self.page.update()

    def build(self) -> ft.Control:
        nome_parceiro = self.parceiro.get("nome", "Irmão de Guerra")
        tel_parceiro = self.parceiro.get("telefone_whatsapp", "Não configurado")

        return ft.ListView(
            spacing=16,
            padding=ft.padding.symmetric(horizontal=16, vertical=12),
            controls=[
                # Cartão de Padrinho / Parceiro de Guerra
                ft.Container(
                    padding=16,
                    border_radius=12,
                    bgcolor=AppColors.BG_SURFACE_ALT,
                    border=ft.border.all(1, AppColors.BORDER_SUBTLE),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                spacing=12,
                                expand=True,
                                controls=[
                                    ft.CircleAvatar(
                                        bgcolor=AppColors.EMBER,
                                        content=ft.Icon(ft.icons.SHIELD, color=AppColors.TEXT_DARK, size=22),
                                        radius=24,
                                    ),
                                    ft.Column(
                                        spacing=2,
                                        expand=True,
                                        controls=[
                                            ft.Text("PARCEIRO DE ALIANÇA 1-TO-1", style=AppStyles.CAPTION, color=AppColors.EMBER),
                                            ft.Text(nome_parceiro, style=AppStyles.TITLE_MEDIUM),
                                            ft.Text(f"WhatsApp: {tel_parceiro}", style=AppStyles.CAPTION, color=AppColors.TEXT_MUTED),
                                        ]
                                    )
                                ]
                            ),
                            ft.IconButton(
                                icon=ft.icons.EDIT_NOTE,
                                icon_color=AppColors.EMBER,
                                tooltip="Alterar Parceiro",
                                on_click=self._abrir_dialogo_parceiro
                            )
                        ]
                    )
                ),

                # As 3 Perguntas de Honra
                ft.Container(
                    padding=16,
                    border_radius=12,
                    bgcolor=AppColors.BG_SURFACE,
                    border=ft.border.all(1, AppColors.BORDER_SUBTLE),
                    content=ft.Column(
                        spacing=16,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("SABATINA DIÁRIA DE HONRA (21H30)", style=AppStyles.CAPTION, color=AppColors.TEXT_MUTED),
                                    ft.Container(
                                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                        border_radius=6,
                                        bgcolor=AppColors.BG_SURFACE_ALT,
                                        content=ft.Text("🔒 Sigilo Quebrado", style=AppStyles.CAPTION, color=AppColors.SUCCESS_GREEN)
                                    )
                                ]
                            ),
                            
                            # Pergunta 1
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(
                                        spacing=2,
                                        expand=True,
                                        controls=[
                                            ft.Text("1. Guardou seus olhos e mente puros hoje?", style=AppStyles.BODY_TEXT),
                                            ft.Text("Zero pornografia, zero espiar perfis ou frestas na carne.", style=AppStyles.CAPTION, color=AppColors.TEXT_MUTED),
                                        ]
                                    ),
                                    ft.Switch(value=self.q1_val, active_color=AppColors.SUCCESS_GREEN, on_change=lambda e: setattr(self, 'q1_val', e.control.value))
                                ]
                            ),
                            ft.Divider(color=AppColors.BORDER_SUBTLE, height=1),

                            # Pergunta 2
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(
                                        spacing=2,
                                        expand=True,
                                        controls=[
                                            ft.Text("2. Cumpriu a Ordem Matinal e joelhos no chão?", style=AppStyles.BODY_TEXT),
                                            ft.Text("Primícias do dia entregues a Deus antes das redes sociais.", style=AppStyles.CAPTION, color=AppColors.TEXT_MUTED),
                                        ]
                                    ),
                                    ft.Switch(value=self.q2_val, active_color=AppColors.SUCCESS_GREEN, on_change=lambda e: setattr(self, 'q2_val', e.control.value))
                                ]
                            ),
                            ft.Divider(color=AppColors.BORDER_SUBTLE, height=1),

                            # Pergunta 3
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(
                                        spacing=2,
                                        expand=True,
                                        controls=[
                                            ft.Text("3. Honrou sua família e foi diligente no trabalho?", style=AppStyles.BODY_TEXT),
                                            ft.Text("Presença masculina no lar, sem ira e com trabalho honesto.", style=AppStyles.CAPTION, color=AppColors.TEXT_MUTED),
                                        ]
                                    ),
                                    ft.Switch(value=self.q3_val, active_color=AppColors.SUCCESS_GREEN, on_change=lambda e: setattr(self, 'q3_val', e.control.value))
                                ]
                            ),
                        ]
                    )
                ),

                # Botão de Transmitir Status ao Parceiro
                ft.Container(
                    padding=ft.padding.only(top=6),
                    content=ft.ElevatedButton(
                        text="TRANSMITIR STATUS AO MEU PARCEIRO NO WHATSAPP",
                        icon=ft.icons.SEND,
                        style=ft.ButtonStyle(
                            bgcolor=AppColors.SUCCESS_GREEN,
                            color=AppColors.TEXT_DARK,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.padding.symmetric(vertical=18),
                        ),
                        on_click=self._transmitir_whatsapp,
                    )
                ),

                # Botão de Graça e Redenção (Se houve tropeço, sem humilhação)
                ft.Container(
                    padding=ft.padding.only(top=4),
                    content=ft.OutlinedButton(
                        text="Houve um tropeço hoje? Reiniciar com Graça",
                        icon=ft.icons.REFRESH,
                        style=ft.ButtonStyle(
                            color=AppColors.TEXT_MUTED,
                            shape=ft.RoundedRectangleBorder(radius=10),
                            side=ft.BorderSide(1, AppColors.BORDER_SUBTLE),
                        ),
                        on_click=self._abrir_dialogo_graca,
                    )
                ),

                ft.Text(
                    "O pecado se alimenta do sigilo. Quando a luz entra, o monstro morre.",
                    style=AppStyles.CAPTION,
                    text_align=ft.TextAlign.CENTER,
                    color=AppColors.TEXT_MUTED
                )
            ]
        )
