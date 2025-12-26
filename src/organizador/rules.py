import json
from pathlib import Path
import re

class Ruler:

    def __init__(self):
        # Caminho padrão do arquivo de regras (resolvido relativo ao pacote)
        # evita problemas com different working directories
        self.RULESPATH = Path(__file__).resolve().parent.parent / "data" / "rules.json"

    def loadRules(self):
        if not self.RULESPATH.exists():
            return []
        try:
            text = self.RULESPATH.read_text(encoding="utf-8")
            # remove comentários // ... e blocos /* ... */
            text_clean = re.sub(r'//.*?$|/\*.*?\*/', '', text, flags=re.MULTILINE | re.DOTALL)
            return json.loads(text_clean)
        except Exception:
            # erro ao ler/parsear -> retorna lista vazia para não quebrar fluxo
            return []

    def saveRules(self, rules):
        # garante que a pasta exista
        self.RULESPATH.parent.mkdir(parents=True, exist_ok=True)
        with open(self.RULESPATH, "w", encoding="utf-8") as f:
            json.dump(rules, f, indent=4)

    def matchRules(self, rules, filePath):
        name = filePath.name.lower()
        # normaliza extensão sem o ponto ('.txt' -> 'txt')
        ext = filePath.suffix.lower().lstrip('.')
        # stat pode falhar se o arquivo sumiu; tratar com segurança
        try:
            size = filePath.stat().st_size
        except Exception:
            size = 0

        for rule in rules:

            # Regra: nome contém texto específico
            if "contem" in rule:
                val = str(rule.get("contem", "")).lower()
                if val and val in name:
                    return rule.get("move_to")

            # Regra: extensão exata
            if "ext" in rule:
                rule_ext = str(rule.get("ext", "")).lower().lstrip('.')
                if rule_ext and rule_ext == ext:
                    return rule.get("move_to")

            # Regra: tamanho mínimo
            if "tam_min" in rule:
                try:
                    tam_min = int(rule.get("tam_min"))
                except Exception:
                    try:
                        tam_min = float(rule.get("tam_min"))
                    except Exception:
                        tam_min = None
                if tam_min is not None and tam_min <= size:
                    return rule.get("move_to")

        # Nenhuma regra correspondeu
        return None
