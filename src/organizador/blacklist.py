import json

class BlackList():
    def __init__(self):
        pass

    def addToBlackList(self, path):
        BLACKLISTPATH = self.BASEPATH / "data/blacklist.json"
        if BLACKLISTPATH.exists:
            with open(BLACKLISTPATH, "r") as blacklist:
                conteudo = json.load(blacklist)
        else:
                conteudo = []
            
        conteudo.append(path)
        
        with open(BLACKLISTPATH, "w") as blacklist:
            json.dump(conteudo, blacklist, indent=4)