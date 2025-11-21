import shutil
from pathlib import Path
from organizador.rules import Ruler


class Mover():
    def __init__(self):
        pass
    
    def fileMove(category, filePath, basePath):
        base = Path(basePath)
        file = Path(filePath) 

        destino = base / category
        destino.mkdir(parents=True, exist_ok=True)

        shutil.move(str(file), str(destino / file.name))
