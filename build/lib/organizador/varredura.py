from pathlib import Path
import time

def varredura(caminhos, bloqueadas=None):
    arquivos = list()
    pastasBloqueadas = set(bloqueadas or [])

    for caminho in caminhos:
        for arquivo in Path(caminho).rglob("*"):
            if any(b in arquivo.parts for b in pastasBloqueadas):
                continue
            if arquivo.is_file():
                arquivos.append(arquivo)
    
    return arquivos


def run():
    inicio = time.time()

    caminhos = [
        "/home/beni/"
    ]
    
    varrido = varredura(caminhos=caminhos)

    for i in varrido:
        print(i)

    fim = time.time()

    print(f"o programa finalizou em {(fim - inicio)*1000:.2f} ms")
    print(len(varrido))

if __name__ == "__main__":
    run()
