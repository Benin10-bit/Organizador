import customtkinter as ctk
from interface.Home import Home


class Resumo(ctk.CTkFrame):
    def __init__(self, master):
        # Inicializa o frame principal com fundo preto
        super().__init__(master, fg_color="#000000")
        self.master = master

        # ========================= SIDEBAR =========================
        # Barra lateral fixa à esquerda
        sidebar = ctk.CTkFrame(self, width=220, fg_color="#0a0a0a", corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)  # Impede redimensionamento interno

        # Frame do logo
        logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo_frame.pack(pady=30, padx=20)
        
        # Ícone grande do logo
        logo_icon = ctk.CTkLabel(logo_frame, text="⚡", font=ctk.CTkFont(size=40))
        logo_icon.pack()
        
        # Título da aplicação
        title = ctk.CTkLabel(sidebar, text="Organize Aí", 
                            font=ctk.CTkFont(size=24, weight="bold"),
                            text_color="#3b82f6")
        title.pack(pady=(0, 5))
        
        # Subtítulo
        subtitle = ctk.CTkLabel(sidebar, text="File Organizer", 
                               font=ctk.CTkFont(size=12),
                               text_color="#6b7280")
        subtitle.pack(pady=(0, 40))

        # Linha separadora
        separator = ctk.CTkFrame(sidebar, height=1, fg_color="#1a1a1a")
        separator.pack(fill="x", padx=20, pady=10)

        # Botão: voltar ao início
        btn_home = ctk.CTkButton(sidebar, 
                                text="🏠  Início",
                                command=lambda: master.mostrarPagina(Home),
                                font=ctk.CTkFont(size=15),
                                fg_color="transparent",
                                hover_color="#1a1a1a",
                                anchor="w",
                                height=45)
        btn_home.pack(pady=5, padx=20, fill="x")

        # Botão: ir para estatísticas
        from interface.Statistics import Statistics
        btn_relatorios = ctk.CTkButton(sidebar, 
                                      text="📊  Relatórios",
                                      command=lambda: master.mostrarPagina(Statistics),
                                      font=ctk.CTkFont(size=15),
                                      fg_color="transparent",
                                      hover_color="#1a1a1a",
                                      anchor="w",
                                      height=45)
        btn_relatorios.pack(pady=5, padx=20, fill="x")
        
        # Botão atual: Sobre
        btn_sobre = ctk.CTkButton(sidebar, 
                                 text="ℹ️  Sobre",
                                 command=lambda: master.mostrarPagina(Resumo),
                                 font=ctk.CTkFont(size=15),
                                 fg_color="#1a1a1a",
                                 hover_color="#2a2a2a",
                                 anchor="w",
                                 height=45,
                                 border_width=1,
                                 border_color="#3b82f6")
        btn_sobre.pack(pady=5, padx=20, fill="x")

        # Versão no rodapé da sidebar
        version_label = ctk.CTkLabel(sidebar, text="v2.0", 
                                    font=ctk.CTkFont(size=11),
                                    text_color="#3a3a3a")
        version_label.pack(side="bottom", pady=20)

        # ========================= ÁREA COM SCROLL =========================
        # Área principal com scroll
        scroll = ctk.CTkScrollableFrame(self, 
                                       fg_color="#000000", 
                                       corner_radius=0,
                                       scrollbar_button_color="#1a1a1a",
                                       scrollbar_button_hover_color="#2a2a2a")
        scroll.pack(side="left", fill="both", expand=True)

        # Container centralizado
        content = ctk.CTkFrame(scroll, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)

        # ========================= HEADER =========================
        # Header da página Sobre
        header_frame = ctk.CTkFrame(content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 40))

        # Container do ícone principal
        icon_container = ctk.CTkFrame(header_frame, width=80, height=80, 
                                     fg_color="#0a0a0a", 
                                     corner_radius=20,
                                     border_width=2,
                                     border_color="#3b82f6")
        icon_container.pack()
        icon_container.pack_propagate(False)
        
        # Ícone informativo
        icon = ctk.CTkLabel(icon_container, text="ℹ️", font=ctk.CTkFont(size=40))
        icon.place(relx=0.5, rely=0.5, anchor="center")

        # Título da página
        titulo = ctk.CTkLabel(header_frame, 
                             text="Sobre o Organize Aí",
                             font=ctk.CTkFont(size=40, weight="bold"),
                             text_color="#ffffff")
        titulo.pack(pady=(20, 8))

        # Subtítulo da página
        subtitulo = ctk.CTkLabel(header_frame,
                                text="Um organizador de pastas eficiente, rápido e inteligente",
                                font=ctk.CTkFont(size=18),
                                text_color="#9ca3af")
        subtitulo.pack()

        # ========================= HERO SECTION =========================
        self._make_hero_section(content)
        
        # ========================= SEÇÕES PRINCIPAIS =========================
        self._make_section(
            content,
            "📁",
            "O que é o Organize Aí?",
            "O Organize Aí é uma ferramenta desenvolvida para analisar pastas, "
            "identificar arquivos e organizar tudo de maneira automática e eficiente. "
            "Ideal para manter seu computador limpo e organizado, economizando tempo "
            "e aumentando sua produtividade no dia a dia."
        )

        self._make_section(
            content,
            "⚙️",
            "Como funciona?",
            "O processo é simples e intuitivo: você seleciona uma pasta e o sistema "
            "realiza uma varredura completa de todos os arquivos dentro dela. "
            "Cada arquivo é analisado e classificado automaticamente por tipo, extensão "
            "ou categoria personalizada, tornando a organização muito mais ágil e precisa."
        )

        # ========================= CARD DE RECURSOS =========================
        recursos_card = ctk.CTkFrame(content, 
                                    fg_color="#0a0a0a", 
                                    corner_radius=12, 
                                    border_width=1, 
                                    border_color="#1a1a1a")
        recursos_card.pack(fill="x", pady=15)

        rec_header = ctk.CTkFrame(recursos_card, fg_color="transparent")
        rec_header.pack(fill="x", padx=30, pady=(25, 15))

        # Cabeçalho do card de recursos
        icon_rec = ctk.CTkLabel(rec_header, text="✨", font=ctk.CTkFont(size=28))
        icon_rec.pack(side="left", padx=(0, 10))

        title_rec = ctk.CTkLabel(rec_header,
                                text="Recursos Principais",
                                font=ctk.CTkFont(size=24, weight="bold"),
                                text_color="#ffffff")
        title_rec.pack(side="left")

        # Grid interno para os recursos
        recursos_grid = ctk.CTkFrame(recursos_card, fg_color="transparent")
        recursos_grid.pack(fill="x", padx=30, pady=(0, 25))

        # Lista de recursos exibidos
        recursos = [
            ("🚀", "Scanner Rápido", "Varredura recursiva de alta performance"),
            ("🎯", "Classificação Inteligente", "Organização automática por extensão"),
            ("📝", "Log Detalhado", "Registro completo de todas as operações"),
            ("🎨", "Interface Moderna", "Design limpo com CustomTkinter"),
            ("🔧", "Sistema Modular", "Arquitetura pronta para expansão"),
            ("⚡", "Alto Desempenho", "Processamento otimizado e eficiente")
        ]

        # Monta o grid de forma dinâmica (2 colunas)
        for i, (emoji, titulo_rec, desc) in enumerate(recursos):
            col = i % 2
            row = i // 2
            self._make_feature_card(recursos_grid, emoji, titulo_rec, desc).grid(
                row=row, column=col, padx=10, pady=10, sticky="ew"
            )

        # Configura colunas com peso para distribuírem igualmente
        recursos_grid.grid_columnconfigure(0, weight=1)
        recursos_grid.grid_columnconfigure(1, weight=1)

        # ========================= CARD DO DESENVOLVEDOR =========================
        dev_card = ctk.CTkFrame(content, 
                               fg_color="#0a0a0a", 
                               corner_radius=12, 
                               border_width=1, 
                               border_color="#1a1a1a")
        dev_card.pack(fill="x", pady=15)

        dev_inner = ctk.CTkFrame(dev_card, fg_color="transparent")
        dev_inner.pack(fill="x", padx=30, pady=25)

        dev_header = ctk.CTkFrame(dev_inner, fg_color="transparent")
        dev_header.pack(fill="x")

        icon_dev = ctk.CTkLabel(dev_header, text="👨‍💻", font=ctk.CTkFont(size=28))
        icon_dev.pack(side="left", padx=(0, 10))

        title_dev = ctk.CTkLabel(dev_header,
                                text="Desenvolvedor",
                                font=ctk.CTkFont(size=24, weight="bold"),
                                text_color="#ffffff")
        title_dev.pack(side="left")

        separator_dev = ctk.CTkFrame(dev_inner, height=1, fg_color="#1a1a1a")
        separator_dev.pack(fill="x", pady=15)

        info_frame = ctk.CTkFrame(dev_inner, fg_color="transparent")
        info_frame.pack(fill="x")

        # Caixa com informações do desenvolvedor
        dev_info = ctk.CTkFrame(info_frame, fg_color="#000000", corner_radius=8)
        dev_info.pack(fill="x", pady=5)
        
        dev_label = ctk.CTkLabel(dev_info,
                                text="Criado por: namorado de kalyne ❤️",
                                font=ctk.CTkFont(size=16),
                                text_color="#e0e0e0")
        dev_label.pack(pady=12, padx=15)

        # Caixa com a versão da aplicação
        version_info = ctk.CTkFrame(info_frame, fg_color="#000000", corner_radius=8)
        version_info.pack(fill="x", pady=5)
        
        version_text = ctk.CTkLabel(version_info,
                                   text="Versão da aplicação: 1.0.0",
                                   font=ctk.CTkFont(size=16),
                                   text_color="#e0e0e0")
        version_text.pack(pady=12, padx=15)

        # ========================= BOTÃO VOLTAR =========================
        btn_voltar = ctk.CTkButton(content,
                                  text="← Voltar ao Início",
                                  command=lambda: master.mostrarPagina(Home),
                                  width=200,
                                  height=50,
                                  font=ctk.CTkFont(size=15, weight="bold"),
                                  fg_color="#3b82f6",
                                  hover_color="#2563eb",
                                  corner_radius=10,
                                  text_color="#ffffff")
        btn_voltar.pack(pady=40)

    # ========================= FUNÇÕES DE COMPONENTES =========================
    def _make_hero_section(self, parent):
        """Cria uma seção hero com estatísticas"""
        hero = ctk.CTkFrame(parent, fg_color="#0a0a0a", corner_radius=12, 
                           border_width=1, border_color="#1a1a1a")
        hero.pack(fill="x", pady=(0, 15))

        hero_inner = ctk.CTkFrame(hero, fg_color="transparent")
        hero_inner.pack(fill="x", padx=30, pady=25)

        hero_title = ctk.CTkLabel(hero_inner,
                                 text="Por que escolher o Organize Aí?",
                                 font=ctk.CTkFont(size=20, weight="bold"),
                                 text_color="#ffffff")
        hero_title.pack(pady=(0, 20))

        stats_row = ctk.CTkFrame(hero_inner, fg_color="transparent")
        stats_row.pack(fill="x")

        # Lista de estatísticas
        stats = [
            ("⚡", "Velocidade", "10x mais rápido"),
            ("🎯", "Precisão", "100% automático"),
            ("💡", "Simplicidade", "Interface intuitiva")
        ]

        # Cria cards lado a lado
        for emoji, label, value in stats:
            stat_card = ctk.CTkFrame(stats_row, fg_color="#000000", corner_radius=8)
            stat_card.pack(side="left", expand=True, fill="x", padx=5)

            emoji_label = ctk.CTkLabel(stat_card, text=emoji, font=ctk.CTkFont(size=32))
            emoji_label.pack(pady=(15, 5))

            value_label = ctk.CTkLabel(stat_card, text=value, 
                                      font=ctk.CTkFont(size=18, weight="bold"),
                                      text_color="#3b82f6")
            value_label.pack()

            label_label = ctk.CTkLabel(stat_card, text=label, 
                                      font=ctk.CTkFont(size=13),
                                      text_color="#9ca3af")
            label_label.pack(pady=(0, 15))

    # Cria seção completa de texto com ícone
    def _make_section(self, parent, icon, titulo, texto):
        card = ctk.CTkFrame(parent, 
                           fg_color="#0a0a0a", 
                           corner_radius=12, 
                           border_width=1, 
                           border_color="#1a1a1a")
        card.pack(fill="x", pady=15)

        card_inner = ctk.CTkFrame(card, fg_color="transparent")
        card_inner.pack(fill="both", padx=30, pady=25)

        # Cabeçalho da seção
        header = ctk.CTkFrame(card_inner, fg_color="transparent")
        header.pack(fill="x", pady=(0, 15))

        icon_label = ctk.CTkLabel(header, text=icon, font=ctk.CTkFont(size=28))
        icon_label.pack(side="left", padx=(0, 10))

        titulo_label = ctk.CTkLabel(header,
                                    text=titulo,
                                    font=ctk.CTkFont(size=24, weight="bold"),
                                    text_color="#ffffff")
        titulo_label.pack(side="left")

        # Linha separadora
        separator = ctk.CTkFrame(card_inner, height=1, fg_color="#1a1a1a")
        separator.pack(fill="x", pady=(0, 15))

        # Texto explicativo
        texto_label = ctk.CTkLabel(card_inner,
                                   text=texto,
                                   justify="left",
                                   wraplength=850,
                                   font=ctk.CTkFont(size=16),
                                   text_color="#d1d5db")
        texto_label.pack(anchor="w")

    # Cria pequenos cards para os recursos
    def _make_feature_card(self, parent, icon, titulo, desc):
        card = ctk.CTkFrame(parent, 
                           fg_color="#000000", 
                           corner_radius=8,
                           border_width=1,
                           border_color="#1a1a1a")
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", padx=15, pady=15)

        icon_label = ctk.CTkLabel(inner, text=icon, font=ctk.CTkFont(size=24))
        icon_label.pack(pady=(0, 8))

        titulo_label = ctk.CTkLabel(inner,
                                   text=titulo,
                                   font=ctk.CTkFont(size=15, weight="bold"),
                                   text_color="#ffffff")
        titulo_label.pack()

        desc_label = ctk.CTkLabel(inner,
                                 text=desc,
                                 font=ctk.CTkFont(size=12),
                                 text_color="#9ca3af")
        desc_label.pack(pady=(5, 0))

        return card
