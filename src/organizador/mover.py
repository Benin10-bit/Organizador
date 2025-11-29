import shutil
from pathlib import Path
from organizador.rules import Ruler


class Mover:
    
    def __init__(self):
        pass  # Mantido para compatibilidade futura caso precise de estados internos

    @staticmethod
    def fileMove(category, filePath, basePath):
        base = Path(basePath)
        file = Path(filePath)

        # Criar diretório da categoria caso não exista
        destino = base / category
        destino.mkdir(parents=True, exist_ok=True)

        # Mover arquivo para o destino final
        shutil.move(str(file), str(destino / file.name))
