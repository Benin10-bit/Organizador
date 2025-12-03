import customtkinter as ctk
from tkinter import filedialog

from organizador.scanner import Scanner
from organizador.classifier import classify

class Home(ctk.CTkFrame, Scanner):
    def __init__(self, master):
        ctk.CTkFrame.__init__(self, master, fg_color="#08090d")
        Scanner.__init__(self) 
        self.master = master

        # Menu lateral
        menuLateral = ctk.CTkFrame(self, width=200, fg_color="#0A0C16")
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
        botao = ctk.CTkButton(menuLateral, text="Relatorios",
                              command=lambda: master.mostrarPagina(Statistics))
        botao.pack(pady=10)

        # Entrada para o caminho
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
            command=self.iniciar_scan
        ).pack(pady=10)

        # Caixa de log
        self.logBox = ctk.CTkTextbox(
            self,
            width=700,
            height=350,
            corner_radius=10
        )
        self.logBox.pack(pady=20)
        self.logBox.configure(state="disabled")

        self.entrada.configure(state="readonly")

    def iniciar_scan(self):
        caminho = self.entrada.get()

        if caminho == "":
            self.log("[ERRO] Nenhum caminho inserido.")
            return

        self.log(f"[INFO] Scaneando: {caminho}")

        try:
            arquivos = self.run(caminho)  # lista de Path

            categorias = classify(arquivos)

            self.log(f"[OK] Total de arquivos encontrados: {len(arquivos)}")
            for arq in categorias:
                self.log(" • " + arq["nome"] + " - " + arq["category"])

        except Exception as e:
            self.log(f"[ERRO] {e}")

            self.log(f"[ERRO] {e}")

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


