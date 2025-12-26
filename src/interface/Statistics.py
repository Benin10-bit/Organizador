import customtkinter as ctk


class Statistics(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#000000")
        self.master = master



        label = ctk.CTkLabel(self, text="EU QUERO COMER KALYNE COM FORÇA PQ ELA É MUITO GOSTOSA", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        from interface.Home import Home
        botao = ctk.CTkButton(self, text="Organizador", command=lambda: master.mostrarPagina(Home))
        botao.pack(pady=50)

        