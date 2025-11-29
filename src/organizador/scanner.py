from pathlib import Path

class Scanner:

    def __init__(self):
        self._arquivos = []

    def scan(self, caminhos, bloqueadas=None):
        self._arquivos = []

        if isinstance(caminhos, (str, Path)):
            caminhos = [caminhos]

        pastasBloqueadas = set(Path(p) for p in (bloqueadas or []))

        for caminho in caminhos:
            for arquivo in Path(caminho).rglob("*"):

                if any(str(b) in str(arquivo) for b in pastasBloqueadas):
                    continue

                if arquivo.is_file():
                    self._arquivos.append(arquivo)

        return self._arquivos

    def __len__(self):
        return len(self._arquivos)
    
    def run(self, caminho):
        return (self.scan(caminho))




if __name__ == "__main__":
    pass