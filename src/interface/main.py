import customtkinter as ctk
from interface.Sidebar import Sidebar
from interface.Home import Home
from interface.Statistics import Statistics
from interface.About import Resumo
from interface.Config import Config


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Organize Aí")
        self.geometry("1280x1000")

        self.sidebar = Sidebar(self)

        self.container = ctk.CTkFrame(self, fg_color="#000000")
        self.container.pack(side="left", fill="both", expand=True)

        self.pages = {}
        for Page in (Home, Statistics, Resumo, Config):
            frame = Page(self.container)
            self.pages[Page] = frame
            frame.place(relwidth=1, relheight=1)
            frame.lower()

        self.mostrarPagina(Home)

    def mostrarPagina(self, pagina):
        self.trocarBotaoAtivo(pagina)
        self.pages[pagina].lift()


    def trocarBotaoAtivo(self, pagina):
        self.sidebar._setBotaoAtivo(pagina)
        






def run():
    app = App()
    app.mainloop()