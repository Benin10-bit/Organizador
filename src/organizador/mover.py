import shutil
from pathlib import Path
from organizador.rules import Ruler


class Mover:
    
    def __init__(self):
        self.rules = Ruler()

    def specialRules(self, file: Path):
        rules = self.rules.loadRules()

        if not rules:
            return None
        
        return self.rules.matchRules(rules=rules, filePath=file)

    def fileMove(self, category, fileList):
        home = Path.home()  # mantém como Path

        for file in fileList:

            category = file["category"]

            if category in ["Sistemas", "Configurações", "Outros"]:
                continue

            file = Path(file)

            destino = home / category
            
            specialDestiny = self.specialRules(file)
            if specialDestiny is not None:
                destino = home / specialDestiny

            destino.mkdir(parents=True, exist_ok=True)

            shutil.move(str(file), str(destino / file.name))
