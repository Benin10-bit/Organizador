import customtkinter as ctk
from interface.Sidebar import Sidebar
from interface.Home import Home
from interface.Config import Config


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Organize Aí")
        self.geometry("1280x1000")

        self.sidebar = Sidebar(self)

        self.container = ctk.CTkFrame(self, fg_color="#000000")
        self.container.pack(side="left", fill="both", expand=True)

        self.prev = None

        self.paginascriadas = dict()

        self.mostrarPagina(Home)

    def mostrarPagina(self, pagina):
        self.trocarBotaoAtivo(pagina)

        frame = self.paginascriadas.get(pagina)
        if frame is None:
            frame = pagina(self.container)
            frame.place(relwidth=1, relheight=1)
            self.paginascriadas[pagina] = frame

        # abaixa a anterior (se for diferente) e traz a nova para frente
        if self.prev is not None and self.prev is not frame:
            self.prev.lower()
        frame.lift()  
        self.prev = frame

    def trocarBotaoAtivo(self, pagina):
        self.sidebar._setBotaoAtivo(pagina)


def run():
    app = App()
    app.mainloop()