import json
from pathlib import Path

class Ruler:

    def __init__(self):
        # Caminho padrão do arquivo de regras
        self.RULESPATH = Path("data/rules.json")
    def loadRules(self):
        if self.RULESPATH.exists():
            with open(self.RULESPATH, "r", encoding="utf-8") as file:
                return json.load(file)

    def saveRules(self, rules):
        with open(self.RULESPATH, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=4)

    def matchRules(self, rules, filePath):
        name = filePath.name.lower()           
        ext = filePath.suffix.lower()          
        size = filePath.stat().st_size         

        for rule in rules:

            # Regra: nome contém texto específico
            if "contem" in rule:
                if rule["contem"].lower() in name:
                    return rule.get("mover_para") or rule.get("move_to")

            # Regra: extensão exata
            if "ext" in rule:
                if rule["ext"].lower() == ext:
                    return rule.get("move_to") or rule.get("mover_para")

            # Regra: tamanho mínimo
            if "tam_min" in rule:
                if rule["tam_min"] <= size:
                    return rule.get("move_to") or rule.get("mover_para")

        # Nenhuma regra correspondeu
        return None
