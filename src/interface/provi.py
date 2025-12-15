import customtkinter as ctk
from tkinter import filedialog
import threading
import time

from organizador.scanner import Scanner
from organizador.classifier import classify
from organizador.blacklist import BlackList


class Home(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#000000")

        self.master = master
        self.scanner = Scanner()
        self.blacklist = BlackList()
        self.tempo_inicio = None
        self.tempo_decorrido = 0
        self.arquivos_scanneados = 0
        self.scanning = False

        # Container principal com gradiente simulado
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=25, pady=25)

        # Menu lateral
        self.criar_menu_lateral(container)

        # Área de conteúdo
        self.criar_area_conteudo(container)

    def criar_menu_lateral(self, parent):
        """Menu lateral com design premium"""
        menuLateral = ctk.CTkFrame(
            parent, 
            width=260, 
            fg_color="#0a0a0a", 
            corner_radius=20,
            border_width=1,
            border_color="#1a1a1a"
        )
        menuLateral.pack(side="left", fill="y", padx=(0, 25))
        menuLateral.pack_propagate(False)

        # Header do menu com gradiente visual
        headerFrame = ctk.CTkFrame(menuLateral, fg_color="transparent")
        headerFrame.pack(pady=40, padx=25)

        # Ícone com fundo
        iconFrame = ctk.CTkFrame(
            headerFrame, 
            fg_color="#1a1a1a",
            corner_radius=15,
            width=70,
            height=70
        )
        iconFrame.pack()
        iconFrame.pack_propagate(False)

        ctk.CTkLabel(
            iconFrame,
            text="📁",
            font=ctk.CTkFont(size=36)
        ).pack(expand=True)

        ctk.CTkLabel(
            headerFrame,
            text="Organize Aí",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            headerFrame,
            text="Sistema de Organização v2.0",
            font=ctk.CTkFont(size=11),
            text_color="#555555"
        ).pack()

        # Separador com gradiente
        separadorFrame = ctk.CTkFrame(menuLateral, fg_color="transparent", height=50)
        separadorFrame.pack(fill="x", padx=25)
        separadorFrame.pack_propagate(False)
        
        ctk.CTkFrame(
            separadorFrame, 
            height=1, 
            fg_color="#1a1a1a"
        ).pack(pady=25)

        # Seção de navegação
        ctk.CTkLabel(
            menuLateral,
            text="NAVEGAÇÃO",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#444444",
            anchor="w"
        ).pack(padx=25, pady=(0, 10), anchor="w")

        # Botão de navegação estilizado
        from interface.Statistics import Statistics
        
        btnRelatorios = ctk.CTkButton(
            menuLateral,
            text="📊  Relatórios",
            command=lambda: self.master.mostrarPagina(Statistics),
            fg_color="#1a1a1a",
            hover_color="#2a2a2a",
            text_color="#aaaaaa",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=50,
            anchor="w",
            corner_radius=12,
            border_width=1,
            border_color="#252525"
        )
        btnRelatorios.pack(pady=5, padx=25, fill="x")

        # Espaçador
        ctk.CTkFrame(menuLateral, fg_color="transparent").pack(expand=True)

        # Footer com info
        footerFrame = ctk.CTkFrame(menuLateral, fg_color="#0f0f0f", corner_radius=12, height=80)
        footerFrame.pack(fill="x", padx=25, pady=25)
        footerFrame.pack_propagate(False)

        ctk.CTkLabel(
            footerFrame,
            text="💡",
            font=ctk.CTkFont(size=20)
        ).pack(pady=(12, 5))

        ctk.CTkLabel(
            footerFrame,
            text="Organize seus arquivos\ncom inteligência",
            font=ctk.CTkFont(size=10),
            text_color="#555555",
            justify="center"
        ).pack()

    def criar_area_conteudo(self, parent):
        """Área principal de conteúdo"""
        areaConteudo = ctk.CTkFrame(parent, fg_color="transparent")
        areaConteudo.pack(side="left", fill="both", expand=True)

        # Header com título e subtítulo
        headerConteudo = ctk.CTkFrame(areaConteudo, fg_color="transparent", height=100)
        headerConteudo.pack(fill="x", pady=(0, 25))
        headerConteudo.pack_propagate(False)

        ctk.CTkLabel(
            headerConteudo,
            text="Scanner de Diretórios",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ffffff",
            anchor="w"
        ).pack(side="top", anchor="w", pady=(10, 0))

        ctk.CTkLabel(
            headerConteudo,
            text="Analise e organize seus arquivos de forma inteligente",
            font=ctk.CTkFont(size=13),
            text_color="#666666",
            anchor="w"
        ).pack(side="top", anchor="w", pady=(5, 0))

        # Cards de estatísticas
        self.criar_cards_stats(areaConteudo)

        # Seleção de pasta
        self.criar_selecao_pasta(areaConteudo)

        # Barra de progresso
        self.criar_barra_progresso(areaConteudo)

        # Área de logs
        self.criar_area_logs(areaConteudo)

    def criar_cards_stats(self, parent):
        """Cards com estatísticas premium"""
        cardsFrame = ctk.CTkFrame(parent, fg_color="transparent", height=140)
        cardsFrame.pack(fill="x", pady=(0, 25))
        cardsFrame.pack_propagate(False)

        # Card 1: Tempo
        card1 = ctk.CTkFrame(
            cardsFrame, 
            fg_color="#0a0a0a", 
            corner_radius=16,
            border_width=1,
            border_color="#1a1a1a"
        )
        card1.pack(side="left", fill="both", expand=True, padx=(0, 12))

        # Mini header do card
        ctk.CTkLabel(
            card1,
            text="TEMPO DECORRIDO",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#444444",
            anchor="w"
        ).pack(pady=(18, 5), padx=20, anchor="w")

        # Valor principal
        timeFrame = ctk.CTkFrame(card1, fg_color="transparent")
        timeFrame.pack(fill="x", padx=20)

        ctk.CTkLabel(
            timeFrame,
            text="⏱️",
            font=ctk.CTkFont(size=20)
        ).pack(side="left", padx=(0, 10))

        self.labelTempo = ctk.CTkLabel(
            timeFrame,
            text="00:00:00",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#3b82f6"
        )
        self.labelTempo.pack(side="left")

        # Card 2: Arquivos
        card2 = ctk.CTkFrame(
            cardsFrame, 
            fg_color="#0a0a0a", 
            corner_radius=16,
            border_width=1,
            border_color="#1a1a1a"
        )
        card2.pack(side="left", fill="both", expand=True, padx=(6, 12))

        ctk.CTkLabel(
            card2,
            text="ARQUIVOS PROCESSADOS",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#444444",
            anchor="w"
        ).pack(pady=(18, 5), padx=20, anchor="w")

        filesFrame = ctk.CTkFrame(card2, fg_color="transparent")
        filesFrame.pack(fill="x", padx=20)

        ctk.CTkLabel(
            filesFrame,
            text="📄",
            font=ctk.CTkFont(size=20)
        ).pack(side="left", padx=(0, 10))

        self.labelArquivos = ctk.CTkLabel(
            filesFrame,
            text="0",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#3b82f6"
        )
        self.labelArquivos.pack(side="left")

        # Card 3: Status
        card3 = ctk.CTkFrame(
            cardsFrame, 
            fg_color="#0a0a0a", 
            corner_radius=16,
            border_width=1,
            border_color="#1a1a1a"
        )
        card3.pack(side="left", fill="both", expand=True, padx=(6, 0))

        ctk.CTkLabel(
            card3,
            text="STATUS DO SISTEMA",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#444444",
            anchor="w"
        ).pack(pady=(18, 5), padx=20, anchor="w")

        statusFrame = ctk.CTkFrame(card3, fg_color="transparent")
        statusFrame.pack(fill="x", padx=20)

        self.statusIcon = ctk.CTkLabel(
            statusFrame,
            text="⚪",
            font=ctk.CTkFont(size=20)
        )
        self.statusIcon.pack(side="left", padx=(0, 10))

        self.labelStatus = ctk.CTkLabel(
            statusFrame,
            text="Aguardando",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#666666"
        )
        self.labelStatus.pack(side="left")

    def criar_selecao_pasta(self, parent):
        """Seleção de pasta com design premium"""
        selecaoFrame = ctk.CTkFrame(
            parent, 
            fg_color="#0a0a0a", 
            corner_radius=16,
            border_width=1,
            border_color="#1a1a1a",
            height=220
        )
        selecaoFrame.pack(fill="x", pady=(0, 25))
        selecaoFrame.pack_propagate(False)

        # Header interno
        ctk.CTkLabel(
            selecaoFrame,
            text="SELEÇÃO DE DIRETÓRIO",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#444444",
            anchor="w"
        ).pack(pady=(25, 5), padx=25, anchor="w")

        ctk.CTkLabel(
            selecaoFrame,
            text="Escolha o diretório que deseja organizar",
            font=ctk.CTkFont(size=12),
            text_color="#666666",
            anchor="w"
        ).pack(pady=(0, 15), padx=25, anchor="w")

        # Frame de entrada estilizado
        entradaContainer = ctk.CTkFrame(
            selecaoFrame, 
            fg_color="#050505",
            corner_radius=12,
            border_width=2,
            border_color="#1a1a1a",
            height=55
        )
        entradaContainer.pack(fill="x", padx=25, pady=(0, 15))
        entradaContainer.pack_propagate(False)

        self.entrada = ctk.CTkEntry(
            entradaContainer,
            placeholder_text="📂  Nenhum caminho selecionado...",
            fg_color="transparent",
            border_width=0,
            font=ctk.CTkFont(size=13),
            text_color="#ffffff",
            state="readonly"
        )
        self.entrada.pack(side="left", fill="both", expand=True, padx=15, pady=12)

        ctk.CTkButton(
            entradaContainer,
            width=120,
            height=40,
            text="Procurar",
            command=self.selectDir,
            fg_color="#1a1a1a",
            hover_color="#2a2a2a",
            font=ctk.CTkFont(size=12, weight="bold"),
            corner_radius=8,
            border_width=1,
            border_color="#2a2a2a"
        ).pack(side="right", padx=8, pady=8)

        # Botão de scan PREMIUM com efeito 3D
        btnContainer = ctk.CTkFrame(
            selecaoFrame,
            fg_color="transparent",
            height=90
        )
        btnContainer.pack(fill="x", padx=25, pady=(0, 25))
        btnContainer.pack_propagate(False)
        
        # Sombra do botão (efeito de profundidade)
        btnShadow = ctk.CTkFrame(
            btnContainer,
            fg_color="#1a3a5c",
            corner_radius=16,
            height=78
        )
        btnShadow.place(relx=0.5, rely=0.52, anchor="center", relwidth=1.0)
        
        # Botão principal
        self.btnScan = ctk.CTkButton(
            btnContainer,
            height=75,
            text="🚀  INICIAR SCANNER",
            command=self.iniciarThreadScan,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=ctk.CTkFont(size=18, weight="bold"),
            corner_radius=14,
            border_width=0
        )
        self.btnScan.place(relx=0.5, rely=0.48, anchor="center", relwidth=0.98)

    def criar_barra_progresso(self, parent):
        """Barra de progresso premium"""
        progressoFrame = ctk.CTkFrame(
            parent, 
            fg_color="#0a0a0a", 
            corner_radius=16,
            border_width=1,
            border_color="#1a1a1a",
            height=110
        )
        progressoFrame.pack(fill="x", pady=(0, 25))
        progressoFrame.pack_propagate(False)

        # Header
        headerProg = ctk.CTkFrame(progressoFrame, fg_color="transparent")
        headerProg.pack(fill="x", padx=25, pady=(20, 10))

        ctk.CTkLabel(
            headerProg,
            text="PROGRESSO DO SCANNER",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#444444",
            anchor="w"
        ).pack(side="left")

        self.labelProgresso = ctk.CTkLabel(
            headerProg,
            text="0%",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#3b82f6"
        )
        self.labelProgresso.pack(side="right")

        # Barra customizada com fundo
        progressoOuter = ctk.CTkFrame(
            progressoFrame,
            fg_color="#050505",
            corner_radius=10,
            height=30,
            border_width=1,
            border_color="#1a1a1a"
        )
        progressoOuter.pack(fill="x", padx=25, pady=(0, 20))
        progressoOuter.pack_propagate(False)

        self.progresso = ctk.CTkProgressBar(
            progressoOuter,
            height=20,
            corner_radius=8,
            fg_color="#050505",
            progress_color="#3b82f6",
            border_width=0
        )
        self.progresso.pack(fill="both", expand=True, padx=5, pady=5)
        self.progresso.set(0)

    def criar_area_logs(self, parent):
        """Área de logs estilo terminal profissional"""
        logsFrame = ctk.CTkFrame(
            parent, 
            fg_color="#0a0a0a", 
            corner_radius=16,
            border_width=1,
            border_color="#1a1a1a"
        )
        logsFrame.pack(fill="both", expand=True)

        # Header premium dos logs
        headerLogs = ctk.CTkFrame(
            logsFrame, 
            fg_color="#050505",
            corner_radius=0,
            height=65,
            border_width=0
        )
        headerLogs.pack(fill="x")
        headerLogs.pack_propagate(False)

        headerContent = ctk.CTkFrame(headerLogs, fg_color="transparent")
        headerContent.pack(fill="both", expand=True, padx=25, pady=15)

        leftHeader = ctk.CTkFrame(headerContent, fg_color="transparent")
        leftHeader.pack(side="left", fill="y")

        ctk.CTkLabel(
            leftHeader,
            text="REGISTRO DE ATIVIDADES",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#444444",
            anchor="w"
        ).pack(side="top", anchor="w")

        ctk.CTkLabel(
            leftHeader,
            text="Monitor em tempo real",
            font=ctk.CTkFont(size=10),
            text_color="#555555",
            anchor="w"
        ).pack(side="top", anchor="w", pady=(2, 0))

        # Botões de controle
        botoesFrame = ctk.CTkFrame(headerContent, fg_color="transparent")
        botoesFrame.pack(side="right")

        ctk.CTkButton(
            botoesFrame,
            text="🔄",
            width=40,
            height=35,
            command=self.scroll_to_bottom,
            fg_color="#1a1a1a",
            hover_color="#2a2a2a",
            font=ctk.CTkFont(size=14),
            corner_radius=8,
            border_width=1,
            border_color="#252525"
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            botoesFrame,
            text="🗑️  Limpar",
            width=100,
            height=35,
            command=self.limpar_logs,
            fg_color="#1a1a1a",
            hover_color="#2a2a2a",
            font=ctk.CTkFont(size=11, weight="bold"),
            corner_radius=8,
            border_width=1,
            border_color="#252525"
        ).pack(side="left")

        # Separador
        ctk.CTkFrame(logsFrame, height=1, fg_color="#1a1a1a").pack(fill="x")

        # Container do textbox
        logContainer = ctk.CTkFrame(logsFrame, fg_color="#000000", corner_radius=0)
        logContainer.pack(fill="both", expand=True, padx=2, pady=2)

        # Textbox estilizado
        self.logBox = ctk.CTkTextbox(
            logContainer,
            fg_color="#000000",
            corner_radius=0,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#94a3b8",
            wrap="word",
            border_width=0,
            scrollbar_button_color="#1a1a1a",
            scrollbar_button_hover_color="#2a2a2a"
        )
        self.logBox.pack(fill="both", expand=True, padx=20, pady=20)
        self.logBox.configure(state="disabled")

        # Log inicial estilizado
        self.log_styled("[SISTEMA]", "Sistema iniciado com sucesso", "#3b82f6")
        self.log_styled("[INFO]", "Aguardando seleção de diretório...", "#64748b")

    # ========================================================
    # THREAD E TIMER
    # ========================================================

    def iniciarThreadScan(self):
        if self.scanning:
            return
        threading.Thread(target=self.scanCompleto, daemon=True).start()
        threading.Thread(target=self.atualizar_timer, daemon=True).start()

    def atualizar_timer(self):
        """Atualiza o timer enquanto o scan está ativo"""
        while self.scanning:
            elapsed = time.time() - self.tempo_inicio
            horas = int(elapsed // 3600)
            minutos = int((elapsed % 3600) // 60)
            segundos = int(elapsed % 60)
            
            tempo_str = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            self.labelTempo.configure(text=tempo_str)
            time.sleep(0.5)

    # ========================================================
    # PROCESSAMENTO PRINCIPAL
    # ========================================================

    def scanCompleto(self):
        caminho = self.entrada.get()

        if caminho == "":
            self.log_styled("[ERRO]", "Nenhum caminho selecionado", "#ef4444")
            return

        self.scanning = True
        self.tempo_inicio = time.time()
        self.arquivos_scanneados = 0
        
        self.btnScan.configure(
            state="disabled", 
            text="⌛  SCANNEANDO...",
            fg_color="#334155",
            hover_color="#334155"
        )
        self.labelStatus.configure(text="Scanneando", text_color="#3b82f6")
        self.statusIcon.configure(text="🔵")
        
        self.log_styled("[INICIO]", f"Scanner iniciado em: {caminho}", "#3b82f6")
        self.atualizarProgresso(0)

        try:
            # 1) Scanner
            bloqueados = self.blacklist.readBlackList()
            arquivos = self.scanner.scan(caminho, bloqueados)
            total = len(arquivos)

            if total == 0:
                self.log_styled("[INFO]", "Nenhum arquivo encontrado no diretório", "#fbbf24")
                self.atualizarProgresso(1)
                self.finalizar_scan()
                return

            self.log_styled("[SUCESSO]", f"{total} arquivos encontrados", "#22c55e")
            self.log_styled("[PROCESSO]", "Iniciando classificação inteligente...", "#a78bfa")

            # 2) Classificação com progressão proporcional
            categorias = []
            for i, info in enumerate(classify(arquivos), start=1):
                categorias.append(info)
                
                self.arquivos_scanneados = i
                self.labelArquivos.configure(text=str(i))
                
                # progressão proporcional
                progresso = i / total
                self.atualizarProgresso(progresso)
                
                # log com cores
                categoria = info['category']
                nome = info['path'].name
                
                # Truncar nome se for muito longo
                if len(nome) > 50:
                    nome = nome[:47] + "..."
                
                self.log_styled("[SCAN]", f"{nome} → {categoria}", "#a78bfa")

            self.atualizarProgresso(1)
            self.log_styled("[CONCLUÍDO]", f"Processo finalizado! {total} arquivos processados", "#22c55e")
            self.labelStatus.configure(text="Concluído", text_color="#22c55e")
            self.statusIcon.configure(text="🟢")

        except Exception as e:
            self.log_styled("[ERRO]", str(e), "#ef4444")
            self.labelStatus.configure(text="Erro", text_color="#ef4444")
            self.statusIcon.configure(text="🔴")
        
        finally:
            self.finalizar_scan()

    def finalizar_scan(self):
        """Finaliza o processo de scan"""
        self.scanning = False
        self.btnScan.configure(
            state="normal", 
            text="🚀  INICIAR SCANNER",
            fg_color="#3b82f6",
            hover_color="#2563eb"
        )

    # ========================================================
    # INTERFACE
    # ========================================================

    def atualizarProgresso(self, valor):
        """valor deve estar entre 0 e 1"""
        self.progresso.set(valor)
        percentual = int(valor * 100)
        self.labelProgresso.configure(text=f"{percentual}%")

    def log_styled(self, tag, msg, cor):
        """Log estilizado profissional"""
        self.logBox.configure(state="normal")
        
        timestamp = time.strftime("%H:%M:%S")
        
        # Formatação premium
        linha = f"┌─ [{timestamp}]\n│\n├─ {tag}\n│  {msg}\n└{'─' * 70}\n\n"
        
        self.logBox.insert("end", linha)
        self.logBox.configure(state="disabled")
        self.logBox.see("end")

    def log(self, msg):
        """Mantido para compatibilidade - usa log_styled"""
        if "[ERRO]" in msg:
            self.log_styled("[ERRO]", msg.replace("[ERRO]", "").strip(), "#ef4444")
        elif "[SUCESSO]" in msg or "[OK]" in msg:
            tag = "[SUCESSO]" if "[SUCESSO]" in msg else "[OK]"
            self.log_styled(tag, msg.replace(tag, "").strip(), "#22c55e")
        elif "[INFO]" in msg:
            self.log_styled("[INFO]", msg.replace("[INFO]", "").strip(), "#64748b")
        elif "[SCAN]" in msg:
            self.log_styled("[SCAN]", msg.replace("[SCAN]", "").strip(), "#a78bfa")
        else:
            self.log_styled("[LOG]", msg, "#94a3b8")

    def limpar_logs(self):
        """Limpa a área de logs"""
        self.logBox.configure(state="normal")
        self.logBox.delete("1.0", "end")
        self.logBox.configure(state="disabled")
        self.log_styled("[SISTEMA]", "Logs limpos", "#3b82f6")

    def scroll_to_bottom(self):
        """Scroll para o final dos logs"""
        self.logBox.see("end")

    def selectDir(self):
        caminho = filedialog.askdirectory(
            parent=self.master,
            title="Escolha uma pasta",
            initialdir="~",
            mustexist=True
        )
        if caminho:
            self.entrada.configure(state="normal")
            self.entrada.delete(0, ctk.END)
            self.entrada.insert(0, caminho)
            self.entrada.configure(state="readonly")
            self.log_styled("[INFO]", f"Diretório selecionado: {caminho}", "#3b82f6")