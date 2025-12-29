import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, ):
        super().__init__(master, width=220, fg_color="#0a0a0a", corner_radius=0)
        self.pack(side="left", fill="y")
        self.pack_propagate(False)
        self.botoes = {}

        self._logo()
        self._buttons(master)
        self._version()

        # self.atual = atual

    def _logo(self):
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=30, padx=20)

        ctk.CTkLabel(logo_frame, text="⚡", font=ctk.CTkFont(size=40)).pack()

        ctk.CTkLabel(
            self,
            text="Organize Aí",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#3b82f6"
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            self,
            text="File Organizer",
            font=ctk.CTkFont(size=12),
            text_color="#6b7280"
        ).pack(pady=(0, 40))

        ctk.CTkFrame(self, height=1, fg_color="#1a1a1a").pack(
            fill="x", padx=20, pady=10
        )

    def _buttons(self, app):
        from interface.Home import Home
        self._btn("🏠  Início", Home, app)
        from interface.Config import Config
        self._btn("⚙️  Config", Config, app)

    def _btn(self, text, page, app, active=False, bordered=False):
        btn = ctk.CTkButton(
            self,
            text=text,
            command=lambda: app.mostrarPagina(page),
            font=ctk.CTkFont(size=15),
            fg_color="#1a1a1a" if active else "transparent",
            hover_color="#2a2a2a",
            anchor="w",
            height=45,
            border_width=1 if bordered else 0,
            border_color="#3b82f6" if bordered else None
        )
        btn.pack(pady=5, padx=20, fill="x")
        self.botoes[page] = btn

    def _version(self):
        ctk.CTkLabel(
            self,
            text="v2.0",
            font=ctk.CTkFont(size=11),
            text_color="#3a3a3a"
        ).pack(side="bottom", pady=20)
    
    def _setBotaoAtivo(self, pagina):
        for page, button in self.botoes.items():
            ativo = pagina == page

            if ativo:
                button.configure(
                    fg_color="#1a1a1a",
                    border_width=1,
                    border_color="#3b82f6"
                )
            else:
                button.configure(
                    fg_color="transparent",
                    border_width=0
                )
