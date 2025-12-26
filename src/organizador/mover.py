import shutil
from pathlib import Path
from organizador.rules import Ruler


class Mover:
    def __init__(self):
        self.rules = Ruler()

    def specialRules(self, file: Path):
        """Retorna destino especial (string) ou None"""
        rules = self.rules.loadRules()
        if not rules:
            return None
        return self.rules.matchRules(rules=rules, filePath=file)

    def fileMove(self, fileList):
        """
        fileList: lista de dicts {'path': str(path), 'category': Optional[str]}
        Move cada arquivo para home/<category> ou para destino especial definido em rules.
        Ignora categorias definidas como não-mover.
        """
        home = Path.home()
        skip_categories = {"Sistemas", "Configurações", "Outros"}

        for item in fileList:
            try:
                # normaliza entrada
                if isinstance(item, dict):
                    path_str = item.get("path") or item.get("file")
                    category = item.get("category")
                else:
                    path_str = str(item)
                    category = None

                if not path_str:
                    continue

                file_path = Path(path_str)
                if not file_path.exists():
                    # arquivo não existe - pula e log será tratado pelo chamador
                    continue

                # aplica regras especiais para determinar categoria/destino, se houver
                special = self.specialRules(file_path)  # retorna string ou None
                if special:
                    destino = home / str(special)
                else:
                    destino_cat = category or "Outros"
                    destino = home / destino_cat

                # ignora categorias pré-definidas
                if destino.name in skip_categories:
                    continue

                destino.mkdir(parents=True, exist_ok=True)
                target = destino / file_path.name
                # usa shutil.move (pode sobrescrever) — quem chamar pode decidir sobre políticas adicionais
                shutil.move(str(file_path), str(target))
                # não retornar aqui: continuar processando o restante da lista
            except Exception:
                # não levantar exceção aqui para não interromper lote; chamador pode logar
                continue
