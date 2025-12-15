import customtkinter as ctk
import os

from interface.Statistics import Statistics
from interface.About import Resumo
from interface.provi import Home


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")

        # Configurações da janela
        self.title("Organize Aí")
        self.geometry("1280x1000")

        self.pages = dict()

        for F in (Home, Resumo ,Statistics):
            frame = F(self)
            self.pages[F] = frame
            frame.place(x=0,y=0, relwidth=1, relheight=1)
        
        self.mostrarPagina(Home)
    
    def mostrarPagina(self, pagina):
        frame = self.pages[pagina]
        frame.lift()





def run():
    app = App()
    app.mainloop()