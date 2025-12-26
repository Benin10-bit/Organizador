import customtkinter as ctk
from tkinter import filedialog
import threading
import time

from organizador.scanner import Scanner
from organizador.classifier import classify
from organizador.mover import Mover

class Home(ctk.CTkFrame):
    def __init__(self, master):
        # Inicializa o frame principal com fundo preto
        super().__init__(master, fg_color="#000000")
        self.master = master
        
        # ========================= VARIÁVEIS DE CONTROLE =========================
        self.caminho_selecionado = None  # Armazena o caminho da pasta selecionada
        self.operacao_em_andamento = False  # Flag para controlar se há operação rodando
        self.tempo_inicio = None  # Marca o tempo de início da operação
        self.arquivos_varridos = 0  # Contador de arquivos processados
        
        # Stages configuráveis: (nome, peso relativo no progresso total)
        # Para adicionar etapas, basta alterar esta lista.
        self.stages = [
            ("Varredura de Arquivos", 0.3),
            ("Classificação de Arquivos", 0.3),
            ("Movimentação de Arquivos", 0.4)  
        ]
        self.stage_index = 0
        self.stage_progress = 0.0  # 0..1 dentro da etapa atual

        # ========================= ÁREA PRINCIPAL COM SCROLL =========================
        # Frame com scroll para todo o conteúdo principal
        scroll = ctk.CTkScrollableFrame(self, 
                                       fg_color="#000000", 
                                       corner_radius=0,
                                       scrollbar_button_color="#1a1a1a",
                                       scrollbar_button_hover_color="#2a2a2a")
        scroll.pack(side="left", fill="both", expand=True)

        # Container centralizado para todo o conteúdo
        content = ctk.CTkFrame(scroll, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)

        # ========================= HEADER =========================
        # Cabeçalho da página com título e descrição
        header_frame = ctk.CTkFrame(content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 30))

        # Container do ícone principal com borda
        icon_container = ctk.CTkFrame(header_frame, width=80, height=80, 
                                     fg_color="#0a0a0a", 
                                     corner_radius=20,
                                     border_width=2,
                                     border_color="#3b82f6")
        icon_container.pack()
        icon_container.pack_propagate(False)
        
        # Ícone de pasta
        icon = ctk.CTkLabel(icon_container, text="📁", font=ctk.CTkFont(size=40))
        icon.place(relx=0.5, rely=0.5, anchor="center")

        # Título principal da página
        titulo = ctk.CTkLabel(header_frame, 
                             text="Organizador de Arquivos",
                             font=ctk.CTkFont(size=40, weight="bold"),
                             text_color="#ffffff")
        titulo.pack(pady=(20, 8))

        # Subtítulo descritivo
        subtitulo = ctk.CTkLabel(header_frame,
                                text="Selecione uma pasta e organize seus arquivos automaticamente",
                                font=ctk.CTkFont(size=18),
                                text_color="#9ca3af")
        subtitulo.pack()

        # ========================= SELEÇÃO DE PASTA =========================
        # Card para seleção do caminho da pasta
        selecao_card = ctk.CTkFrame(content, 
                                   fg_color="#0a0a0a", 
                                   corner_radius=12, 
                                   border_width=1, 
                                   border_color="#1a1a1a")
        selecao_card.pack(fill="x", pady=(0, 20))

        selecao_inner = ctk.CTkFrame(selecao_card, fg_color="transparent")
        selecao_inner.pack(fill="x", padx=30, pady=25)

        # Label do campo de seleção
        selecao_label = ctk.CTkLabel(selecao_inner,
                                     text="📂  Pasta para Organizar",
                                     font=ctk.CTkFont(size=18, weight="bold"),
                                     text_color="#ffffff")
        selecao_label.pack(anchor="w", pady=(0, 15))

        # Frame horizontal para input e botão
        selecao_row = ctk.CTkFrame(selecao_inner, fg_color="transparent")
        selecao_row.pack(fill="x")

        # Campo de texto mostrando o caminho selecionado
        self.entrada_caminho = ctk.CTkEntry(selecao_row,
                                           placeholder_text="Nenhuma pasta selecionada...",
                                           height=45,
                                           font=ctk.CTkFont(size=14),
                                           fg_color="#000000",
                                           border_color="#1a1a1a",
                                           state="disabled")  # Desabilitado para não editar manualmente
        self.entrada_caminho.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Botão para abrir o seletor de pasta
        btn_selecionar = ctk.CTkButton(selecao_row,
                                      text="Selecionar Pasta",
                                      command=self.selecionar_pasta,
                                      width=180,
                                      height=45,
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      fg_color="#3b82f6",
                                      hover_color="#2563eb")
        btn_selecionar.pack(side="left")

        # ========================= BARRAS DE PROGRESSO =========================
        # Card contendo as etapas de progresso (USANDO UMA BARRA UNIFICADA)
        progresso_card = ctk.CTkFrame(content, 
                                     fg_color="#0a0a0a", 
                                     corner_radius=12, 
                                     border_width=1, 
                                     border_color="#1a1a1a")
        progresso_card.pack(fill="x", pady=(0, 20))

        progresso_inner = ctk.CTkFrame(progresso_card, fg_color="transparent")
        progresso_inner.pack(fill="x", padx=30, pady=25)

        # Título da seção de progresso
        progresso_titulo = ctk.CTkLabel(progresso_inner,
                                       text="📊  Progresso da Operação",
                                       font=ctk.CTkFont(size=18, weight="bold"),
                                       text_color="#ffffff")
        progresso_titulo.pack(anchor="w", pady=(0, 20))

        # Label que mostra a etapa atual (visível acima da barra unificada)
        self.label_etapa = ctk.CTkLabel(progresso_inner,
                                       text="Etapa: Aguardando",
                                       font=ctk.CTkFont(size=14),
                                       text_color="#d1d5db")
        self.label_etapa.pack(anchor="w", pady=(0, 8))

        # Barra de progresso unificada (total)
        self.progress_total = ctk.CTkProgressBar(progresso_inner,
                                                height=20,
                                                fg_color="#1a1a1a",
                                                progress_color="#3b82f6")
        self.progress_total.pack(fill="x", pady=(0, 25))
        self.progress_total.set(0)

        # ========================= CARDS DE ESTATÍSTICAS =========================
        # Container horizontal para os 3 cards de info
        stats_row = ctk.CTkFrame(content, fg_color="transparent")
        stats_row.pack(fill="x", pady=(0, 20))

        # --- CARD 1: TEMPO DECORRIDO ---
        card_tempo = ctk.CTkFrame(stats_row, 
                                 fg_color="#0a0a0a", 
                                 corner_radius=12,
                                 border_width=1,
                                 border_color="#1a1a1a")
        card_tempo.pack(side="left", expand=True, fill="both", padx=(0, 10))

        tempo_inner = ctk.CTkFrame(card_tempo, fg_color="transparent")
        tempo_inner.pack(fill="both", padx=25, pady=20)

        # Ícone de relógio
        tempo_icon = ctk.CTkLabel(tempo_inner, text="⏱️", font=ctk.CTkFont(size=32))
        tempo_icon.pack(pady=(0, 10))

        # Valor do tempo (atualizado dinamicamente)
        self.label_tempo_valor = ctk.CTkLabel(tempo_inner,
                                             text="0.0s",
                                             font=ctk.CTkFont(size=28, weight="bold"),
                                             text_color="#3b82f6")
        self.label_tempo_valor.pack()

        # Descrição do card
        tempo_desc = ctk.CTkLabel(tempo_inner,
                                 text="Tempo Decorrido",
                                 font=ctk.CTkFont(size=13),
                                 text_color="#9ca3af")
        tempo_desc.pack(pady=(5, 0))

        # --- CARD 2: ARQUIVOS VARRIDOS ---
        card_arquivos = ctk.CTkFrame(stats_row, 
                                    fg_color="#0a0a0a", 
                                    corner_radius=12,
                                    border_width=1,
                                    border_color="#1a1a1a")
        card_arquivos.pack(side="left", expand=True, fill="both", padx=5)

        arquivos_inner = ctk.CTkFrame(card_arquivos, fg_color="transparent")
        arquivos_inner.pack(fill="both", padx=25, pady=20)

        # Ícone de documentos
        arquivos_icon = ctk.CTkLabel(arquivos_inner, text="📄", font=ctk.CTkFont(size=32))
        arquivos_icon.pack(pady=(0, 10))

        # Valor da quantidade (atualizado dinamicamente)
        self.label_arquivos_valor = ctk.CTkLabel(arquivos_inner,
                                                text="0",
                                                font=ctk.CTkFont(size=28, weight="bold"),
                                                text_color="#10b981")
        self.label_arquivos_valor.pack()

        # Descrição do card
        arquivos_desc = ctk.CTkLabel(arquivos_inner,
                                    text="Arquivos Varridos",
                                    font=ctk.CTkFont(size=13),
                                    text_color="#9ca3af")
        arquivos_desc.pack(pady=(5, 0))

        # --- CARD 3: STATUS DA OPERAÇÃO ---
        card_status = ctk.CTkFrame(stats_row, 
                                  fg_color="#0a0a0a", 
                                  corner_radius=12,
                                  border_width=1,
                                  border_color="#1a1a1a")
        card_status.pack(side="left", expand=True, fill="both", padx=(10, 0))

        status_inner = ctk.CTkFrame(card_status, fg_color="transparent")
        status_inner.pack(fill="both", padx=25, pady=20)

        # Ícone de status (muda conforme o estado)
        self.status_icon = ctk.CTkLabel(status_inner, text="⏸️", font=ctk.CTkFont(size=32))
        self.status_icon.pack(pady=(0, 10))

        # Valor do status (atualizado dinamicamente)
        self.label_status_valor = ctk.CTkLabel(status_inner,
                                              text="Aguardando",
                                              font=ctk.CTkFont(size=28, weight="bold"),
                                              text_color="#f59e0b")
        self.label_status_valor.pack()

        # Descrição do card
        status_desc = ctk.CTkLabel(status_inner,
                                  text="Status",
                                  font=ctk.CTkFont(size=13),
                                  text_color="#9ca3af")
        status_desc.pack(pady=(5, 0))

        # ========================= BOTÃO INICIAR =========================
        # Botão grande para iniciar a operação
        self.btn_iniciar = ctk.CTkButton(content,
                                        text="▶  Iniciar Organização",
                                        command=self.iniciar_organizacao,
                                        height=55,
                                        font=ctk.CTkFont(size=16, weight="bold"),
                                        fg_color="#10b981",
                                        hover_color="#059669",
                                        corner_radius=10)
        self.btn_iniciar.pack(fill="x", pady=(0, 20))

        # ========================= LOG DE OPERAÇÕES =========================
        # Card contendo o log de todas as operações
        log_card = ctk.CTkFrame(content, 
                               fg_color="#0a0a0a", 
                               corner_radius=12, 
                               border_width=1, 
                               border_color="#1a1a1a")
        log_card.pack(fill="both", expand=True)

        log_inner = ctk.CTkFrame(log_card, fg_color="transparent")
        log_inner.pack(fill="both", padx=30, pady=25)

        # Cabeçalho do log
        log_header = ctk.CTkFrame(log_inner, fg_color="transparent")
        log_header.pack(fill="x", pady=(0, 15))

        log_titulo = ctk.CTkLabel(log_header,
                                 text="📝  Log de Operações",
                                 font=ctk.CTkFont(size=18, weight="bold"),
                                 text_color="#ffffff")
        log_titulo.pack(side="left")

        # Botão para limpar o log
        btn_limpar_log = ctk.CTkButton(log_header,
                                      text="Limpar Log",
                                      command=self.limpar_log,
                                      width=120,
                                      height=32,
                                      font=ctk.CTkFont(size=12),
                                      fg_color="transparent",
                                      hover_color="#1a1a1a",
                                      border_width=1,
                                      border_color="#1a1a1a")
        btn_limpar_log.pack(side="right")

        # Caixa de texto para o log (somente leitura)
        self.log_textbox = ctk.CTkTextbox(log_inner,
                                         height=300,
                                         font=ctk.CTkFont(family="Consolas", size=12),
                                         fg_color="#000000",
                                         border_width=1,
                                         border_color="#1a1a1a",
                                         text_color="#d1d5db",
                                         wrap="word")
        self.log_textbox.pack(fill="both", expand=True)
        
        # Adiciona mensagem inicial ao log
        self.adicionar_log("Sistema iniciado. Aguardando seleção de pasta...")

    # ========================= MÉTODOS DE CONTROLE =========================
    
    def selecionar_pasta(self):
        """Abre o diálogo para selecionar uma pasta e atualiza a interface"""
        # Abre o file dialog para escolher uma pasta
        pasta = filedialog.askdirectory(title="Selecione a pasta para organizar")
        
        if pasta:  # Se o usuário selecionou algo
            self.caminho_selecionado = pasta
            # Habilita temporariamente o campo para atualizar o texto
            self.entrada_caminho.configure(state="normal")
            self.entrada_caminho.delete(0, "end")
            self.entrada_caminho.insert(0, pasta)
            self.entrada_caminho.configure(state="disabled")
            
            # Registra no log
            self.adicionar_log(f"✓ Pasta selecionada: {pasta}")
    
    def adicionar_log(self, mensagem):
        """Adiciona uma mensagem ao log com timestamp"""
        # Formata a hora atual
        timestamp = time.strftime("%H:%M:%S")
        # Insere no textbox
        self.log_textbox.insert("end", f"[{timestamp}] {mensagem}\n")
        # Faz scroll automático para o fim
        self.log_textbox.see("end")
    
    def limpar_log(self):
        """Limpa todo o conteúdo do log"""
        self.log_textbox.delete("1.0", "end")
        self.adicionar_log("Log limpo.")
    
    def atualizar_status(self, status, cor, icone):
        """Atualiza o card de status com novo texto, cor e ícone"""
        self.label_status_valor.configure(text=status, text_color=cor)
        self.status_icon.configure(text=icone)
    
    # ----------------- Helpers para stages/progresso unificado -----------------
    def _set_stage(self, index):
        """Seleciona a etapa atual pelo índice e zera o progresso interno."""
        self.stage_index = index
        self.stage_progress = 0.0
        nome = self.stages[index][0] if 0 <= index < len(self.stages) else "Desconhecido"
        self.after(0, lambda n=nome: self.label_etapa.configure(text=f"Etapa: {n}"))
        # atualiza barra total imediatamente (reflete que etapa atual está em 0)
        self._calculate_total_progress()

    def _set_stage_progress(self, percentual):
        """Atualiza progresso dentro da etapa atual (0..1)."""
        self.stage_progress = max(0.0, min(1.0, percentual))
        self._calculate_total_progress()

    def _calculate_total_progress(self):
        """Calcula progresso total ponderado e aplica na barra unificada."""
        progresso = 0.0
        for i, (_, peso) in enumerate(self.stages):
            if i < self.stage_index:
                progresso += peso
            elif i == self.stage_index:
                progresso += peso * self.stage_progress
            else:
                break
        # garante 0..1
        progresso = max(0.0, min(1.0, progresso))
        self.after(0, lambda p=progresso: self.progress_total.set(p))

    # ----------------- Fim helpers -----------------

    def iniciar_organizacao(self):
        """Inicia o processo de organização em uma thread separada"""
        # Verifica se já há uma operação rodando
        if self.operacao_em_andamento:
            self.adicionar_log("⚠ Já existe uma operação em andamento!")
            return
        
        # Verifica se uma pasta foi selecionada
        if not self.caminho_selecionado:
            self.adicionar_log("⚠ Por favor, selecione uma pasta primeiro!")
            return
        
        # Desabilita o botão para evitar cliques múltiplos
        self.btn_iniciar.configure(state="disabled", text="Operação em Andamento...")
        
        # Inicia a operação em uma thread separada para não travar a interface
        thread = threading.Thread(target=self.executar_organizacao, daemon=True)
        thread.start()
    
    def executar_organizacao(self):
        """Executa todo o processo de organização (roda em thread separada)"""
        try:
            # Marca início da operação
            self.operacao_em_andamento = True
            self.tempo_inicio = time.time()
            self.arquivos_varridos = 0
            
            # Reseta barra unificada e seleciona primeira etapa
            self.after(0, lambda: self.progress_total.set(0))
            self._set_stage(0)
            
            # Atualiza status
            self.after(0, lambda: self.atualizar_status("Processando", "#3b82f6", "⚙️"))
            self.adicionar_log("\n" + "="*60)
            self.adicionar_log("🚀 INICIANDO ORGANIZAÇÃO")
            self.adicionar_log("="*60)
            
            # ===== ETAPA 1: SCAN =====
            self.adicionar_log("\n📂 ETAPA 1: Iniciando varredura de arquivos...")
            
            # Cria instância do scanner
            scanner = Scanner()
            
            # Realiza o scan (isso pode demorar dependendo da pasta)
            arquivos = scanner.scan(self.caminho_selecionado)
            self.arquivos_varridos = len(arquivos)
            
            # marca varredura como concluída (progresso interno = 1)
            self.after(0, lambda: self.label_arquivos_valor.configure(text=str(self.arquivos_varridos)))
            self._set_stage_progress(1.0)
            self.adicionar_log(f"✓ Varredura concluída: {self.arquivos_varridos} arquivos encontrados")
            
            # passa para próxima etapa (classificação)
            next_index = min(self.stage_index + 1, len(self.stages) - 1)
            self._set_stage(next_index)
            
            # ===== ETAPA 2: CLASSIFICAÇÃO =====
            self.adicionar_log("\n🏷️ ETAPA 2: Iniciando classificação...")
            
            # Normaliza resultados da classificação em uma lista de dicts:
            # {'path': '/full/path', 'category': 'Categoria opcional'}
            results = []
            arquivos_lista = list(arquivos)
            total = len(arquivos_lista)

            # Tenta chamada "bulk" primeiro (se classifier aceitar lista e retornar resultados)
            try:
                bulk_res = classify(arquivos_lista)
                if isinstance(bulk_res, list):
                    # assume lista de dicts ou categorias; normaliza
                    for entry in bulk_res:
                        if isinstance(entry, dict):
                            path = str(entry.get("path") or entry.get("file") or "")
                            results.append({"path": path, "category": entry.get("category")})
                        elif isinstance(entry, (str,)):
                            # se classifier retornou apenas caminhos or categories, tentamos mapear por posição
                            results.append({"path": str(entry), "category": None})
                    # marca etapa completa
                    self._set_stage_progress(1.0)
                else:
                    # Se bulk_res não é lista, considera que classify fez side-effect sem retorno util
                    results = []
            except TypeError:
                # classify não aceita lista: itera por arquivo, captura retorno possível
                if total == 0:
                    self._set_stage_progress(1.0)
                else:
                    batch = max(1, total // 200)
                    for i, arquivo in enumerate(arquivos_lista):
                        try:
                            res = classify(arquivo)
                            if isinstance(res, dict):
                                results.append({"path": str(arquivo), "category": res.get("category")})
                            elif isinstance(res, str):
                                results.append({"path": str(arquivo), "category": res})
                            else:
                                results.append({"path": str(arquivo), "category": None})
                        except Exception as e:
                            self.adicionar_log(f"⚠ Erro ao classificar '{arquivo}': {e}")
                            results.append({"path": str(arquivo), "category": None})
                        if (i % batch) == 0 or (i == total - 1):
                            self._set_stage_progress((i + 1) / total)

            # Se bulk não retornou resultados e results está vazio, ainda assim produz lista básica
            if not results:
                results = [{"path": str(p), "category": None} for p in arquivos_lista]

            self.adicionar_log(f"✓ Classificação concluída")

            #==== ETAPA 3: MOVIMENTAÇÃO =====
            self._set_stage(next_index + 1)
            self.adicionar_log("\n🚚 ETAPA 3: Iniciando movimentação")

            # Cria instância do mover e passa a lista padronizada
            mover = Mover()
            try:
                mover.fileMove(results)
                self.adicionar_log("✓ Movimentação concluída")
            except Exception as e:
                self.adicionar_log(f"⚠ Erro ao mover arquivos: {e}")
            self._set_stage_progress(1.0)   

            # ===== FINALIZAÇÃO =====
            tempo_total = time.time() - self.tempo_inicio
            
            # Atualiza tempo final usando after
            self.after(0, lambda t=tempo_total: self.label_tempo_valor.configure(text=f"{t:.1f}s"))
            
            self.adicionar_log("\n" + "="*60)
            self.adicionar_log(f"✅ OPERAÇÃO CONCLUÍDA COM SUCESSO!")
            self.adicionar_log(f"⏱️ Tempo total: {tempo_total:.2f} segundos")
            self.adicionar_log(f"📄 Total de arquivos: {self.arquivos_varridos}")
            self.adicionar_log("="*60 + "\n")
            
            # Atualiza status final usando after
            self.after(0, lambda: self.atualizar_status("Concluído", "#10b981", "✅"))
            
        except Exception as e:
            # Em caso de erro, registra no log
            self.adicionar_log(f"\n❌ ERRO: {str(e)}")
            self.after(0, lambda: self.atualizar_status("Erro", "#ef4444", "❌"))
        
        finally:
            # Sempre reabilita o botão ao final usando after
            self.operacao_em_andamento = False
            self.after(0, lambda: self.btn_iniciar.configure(state="normal", text="▶  Iniciar Organização"))
    
    def update(self):
        """Atualiza os valores em tempo real (chamado periodicamente)"""
        # Atualiza o tempo decorrido se houver operação em andamento
        if self.operacao_em_andamento and self.tempo_inicio:
            tempo_decorrido = time.time() - self.tempo_inicio
            self.label_tempo_valor.configure(text=f"{tempo_decorrido:.1f}s")
        
        # Atualiza contador de arquivos
        self.label_arquivos_valor.configure(text=str(self.arquivos_varridos))
        
        # Agenda próxima atualização (a cada 100ms)
        self.after(100, self.update)