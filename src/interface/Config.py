import customtkinter as ctk
from tkinter import filedialog

from organizador.blacklist import BlackList

class Config(ctk.CTkFrame):
    def __init__(self, master):
        # Inicializa o frame principal com fundo preto
        super().__init__(master, fg_color="#000000")
        self.master = master

        self.blacklist = BlackList()

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

        # ================================ CONFIGURAÇÕES ================================

        # --- input blacklist ---

        blacklistFrame = ctk.CTkFrame(content, 
                                   fg_color="#0a0a0a", 
                                   width=500,
                                   corner_radius=12, 
                                   border_width=1, 
                                   border_color="#1a1a1a")
        blacklistFrame.pack(fill="x", pady=30)

        blacklist_beforeinner = ctk.CTkFrame(blacklistFrame, fg_color="transparent")
        blacklist_beforeinner.pack(fill="x")

        blacklist_inner = ctk.CTkFrame(blacklistFrame, fg_color="transparent")
        blacklist_inner.pack(fill="x", padx=30, pady=25)


        blacklistLabel = ctk.CTkLabel(blacklist_beforeinner, 
                                      text= "Bloquear pastas",
                                      font=ctk.CTkFont(size=18, weight="bold"),
                                      text_color="#ffffff")
        blacklistLabel.pack(side="left",padx=30, pady=(20, 0))

        blacklist_row = ctk.CTkFrame(blacklist_inner, fg_color="transparent")
        blacklist_row.pack(fill="x")

        self.entrada_caminho = ctk.CTkEntry(blacklist_row,
                                           placeholder_text="Nenhuma pasta selecionada...",
                                           height=45,
                                           font=ctk.CTkFont(size=14),
                                           fg_color="#000000",
                                           border_color="#1a1a1a",
                                           state="disabled")  # Desabilitado para não editar manualmente
        self.entrada_caminho.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Botão para abrir o seletor de pasta
        btn_selecionar = ctk.CTkButton(blacklist_row,
                                      text="Selecionar Pasta",
                                      command=self.selecionar_pasta,
                                      width=180,
                                      height=45,
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      fg_color="#3b82f6",
                                      hover_color="#2563eb")
        btn_selecionar.pack(side="left")

        self.resultadoLabel = ctk.CTkLabel(blacklistFrame, text="")
        self.resultadoLabel.pack(pady=20, padx=30)
    
    def selecionar_pasta(self):
        """Abre o diálogo para selecionar uma pasta e atualiza a interface"""
        # Abre o file dialog para escolher uma pasta
        pasta = filedialog.askdirectory(title="Selecione a pasta para Bloquear")
        
        if pasta:  # Se o usuário selecionou algo
            self.caminho_selecionado = pasta
            # Habilita temporariamente o campo para atualizar o texto
            self.entrada_caminho.configure(state="normal")
            self.entrada_caminho.delete(0, "end")
            self.entrada_caminho.insert(0, pasta)
            self.entrada_caminho.configure(state="disabled")

            self.adicionarBlacklist(pasta)
    
    def adicionarBlacklist(self, pasta):
        res = self.blacklist.addToBlackList(pasta)
        self.resultadoLabel.configure(text=res if res else "Adicionado a blacklist com sucesso" , text_color="#10b981" if not res else "#ef4444")