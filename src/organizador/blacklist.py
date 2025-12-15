import json
from pathlib import Path

class BlackList():
    def __init__(self):
        self.BASEPATH = Path(__file__).parent
        self.BLACKLISTPATH = self.BASEPATH.parent / "data/blackList.json"

    def addToBlackList(self, path):
        conteudo = self.readBlackList()
        conteudo.append(str(path))
        
        with open(self.BLACKLISTPATH, "w") as blacklist:
            json.dump(conteudo, blacklist, indent=4, ensure_ascii=False)

    def readBlackList(self):
        try:
            with open(self.BLACKLISTPATH, "r", encoding="utf-8") as blacklist:
                raw = blacklist.read().strip()

                # arquivo vazio ou só espaços
                if not raw:
                    return []

                return json.loads(raw)

        except FileNotFoundError:
            return []

        except json.JSONDecodeError:
            print("Arquivo corrompido! Resetando...")
            return []

#Depuração
def add():
    p = Path(__file__)
    b = BlackList()
    b.addToBlackList(path=p)