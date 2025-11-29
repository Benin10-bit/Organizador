import customtkinter as ctk
from tkinter import filedialog
import os

from organizador.scanner import Scanner
from organizador.classifier import classify

scan = Scanner()

BASEPATH = os.path.dirname(__file__)
THEMEPATH = os.path.join(BASEPATH, "themes/organize.json")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme(THEMEPATH)

janela = ctk.CTk()
janela.title("Organize Aí")
janela.geometry("1024x650")
# --- Log visual ---------------------------------------------------------
def log(msg):
    logBox.configure(state="normal")
    logBox.insert("end", msg + "\n")
    logBox.configure(state="disabled")
    logBox.see("end")


# --- Seleção de diretório -----------------------------------------------
def selectDir():
    caminho = filedialog.askdirectory(
        parent= janela,
        title="Escolha uma pasta",
        initialdir="~",  
        mustexist=True
    )
    if caminho:
        entrada.configure(state="normal")
        entrada.delete(0, ctk.END)
        entrada.insert(0, caminho)
        entrada.configure(state="readonly")
        log(f"[INFO] Caminho selecionado: {caminho}")


# --- Ação do Scan --------------------------------------------------------
def iniciar_scan():
    caminho = entrada.get()

    if caminho == "":
        log("[ERRO] Nenhum caminho inserido.")
        raise ValueError("Caminho Vazio")

    log(f"[INFO] Scaneando: {caminho}")

    try:
        arquivos = scan.run(caminho)
        log(f"[OK] Total de arquivos encontrados: {len(arquivos)}")

        for arq in arquivos:
            log(" • " + str(arq))

    except Exception as e:
        log(f"[ERRO] {e}")


# --- Interface -----------------------------------------------------------

menuLateral = ctk.CTkFrame(janela, width=200)
menuLateral.pack(side="left", fill="y")
menuLateral.pack_propagate(False)  

label = ctk.CTkLabel(menuLateral, text="Organize Aí", fg_color="transparent", font=ctk.CTkFont(size=20, weight="bold"))
label.pack(pady=20, side="top",anchor="n", padx=20)

# Entrada para o caminho
selecaoPasta = ctk.CTkFrame(janela, fg_color="transparent")
selecaoPasta.pack(pady=20, padx=10)

entrada = ctk.CTkEntry(
    selecaoPasta,
    width=650,
    height=30,
    placeholder_text="Escolha um caminho..."
)
entrada.pack(side="left", padx=10)

ctk.CTkButton(
    selecaoPasta,
    width=30,
    height=30,
    text="...",
    command=selectDir
).pack(side="left")

# Botão principal
ctk.CTkButton(
    janela,
    text="Scannear sistema",
    command=iniciar_scan
).pack(pady=10)

# Caixa de log
logBox = ctk.CTkTextbox(
    janela,
    width=700,
    height=350,
    corner_radius=10
)
logBox.pack(pady=20)
logBox.configure(state="disabled")

entrada.configure(state="readonly")

# --- Mainloop ------------------------------------------------------------
def run():
    janela.mainloop()
