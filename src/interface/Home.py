import customtkinter as ctk
from tkinter import filedialog
import threading

from organizador.scanner import Scanner
from organizador.classifier import classify


class Home(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.s = Scanner()
        self.etapa = 0

        # Menu lateral
        menuLateral = ctk.CTkFrame(self, width=200)
        menuLateral.pack(side="left", fill="y")
        menuLateral.pack_propagate(False)

        label = ctk.CTkLabel(
            menuLateral,
            text="Organize Aí",
            fg_color="transparent",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label.pack(pady=20, side="top", anchor="n", padx=20)

        from interface.Statistics import Statistics
        ctk.CTkButton(
            menuLateral,
            text="Relatórios",
            command=lambda: master.mostrarPagina(Statistics)
        ).pack(pady=10)

        # Entrada para caminho
        selecaoPasta = ctk.CTkFrame(self, fg_color="transparent")
        selecaoPasta.pack(pady=20, padx=10)

        self.entrada = ctk.CTkEntry(
            selecaoPasta,
            width=650,
            height=30,
            placeholder_text="Escolha um caminho..."
        )
        self.entrada.pack(side="left", padx=10)

        ctk.CTkButton(
            selecaoPasta,
            width=30,
            height=30,
            text="...",
            command=self.selectDir
        ).pack(side="left")

        # Botão principal
        ctk.CTkButton(
            self,
            text="Scannear sistema",
            command=self.iniciarThreadScan
        ).pack(pady=10)

        # PROGRESSO AGORA É NO FRAME CERTO
        self.progresso = ctk.CTkProgressBar(self, width=700)
        self.progresso.pack(pady=10)
        self.progresso.set(0)

        # Caixa de logs
        self.logBox = ctk.CTkTextbox(
            self,
            width=700,
            height=350,
            corner_radius=10
        )
        self.logBox.pack(pady=20)
        self.logBox.configure(state="disabled")

        self.entrada.configure(state="readonly")

    # ========================================================
    # THREAD
    # ========================================================

    def iniciarThreadScan(self):
        threading.Thread(target=self.scanCompleto, daemon=True).start()

    # ========================================================
    # PROCESSAMENTO PRINCIPAL (RODA DENTRO DA THREAD)
    # ========================================================

    def scanCompleto(self):
        caminho = self.entrada.get()

        if caminho == "":
            self.log("[ERRO] Nenhum caminho inserido.")
            return

        self.log(f"[INFO] Scaneando: {caminho}")
        self.atualizarProgresso(0)

        try:
            # 1) Scanner
            arquivos = self.s.run(caminho)
            total = len(arquivos)

            if total == 0:
                self.log("[INFO] Nenhum arquivo encontrado.")
                self.atualizarProgresso(1)
                return

            self.log(f"[OK] {total} arquivos encontrados.")

            # 2) Classificação com progressão proporcional
            categorias = []
            for i, info in enumerate(classify(arquivos), start=1):
                categorias.append(info)

                # progressão proporcional
                self.atualizarProgresso(i / total)

                # log opcional
                self.log(f" • {info['nome']}  →  {info['category']}")

            self.atualizarProgresso(1)
            self.log("[OK] Processo concluído!")

        except Exception as e:
            self.log(f"[ERRO] {e}")

    # ========================================================
    # INTERFACE
    # ========================================================

    def atualizarProgresso(self, valor):
        """valor deve estar entre 0 e 1"""
        self.progresso.set(valor)

    def log(self, msg):
        self.logBox.configure(state="normal")
        self.logBox.insert("end", msg + "\n")
        self.logBox.configure(state="disabled")
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
            self.log(f"[INFO] Caminho selecionado: {caminho}")
