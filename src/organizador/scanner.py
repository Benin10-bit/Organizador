import os
from pathlib import Path

from organizador.blacklist import BlackList


class Scanner:

    def __init__(self):
        self._arquivos: list[Path] = []

        self.blacklist = BlackList()

        # normaliza blacklist vinda do arquivo
        self._bloqueadas = {
            Path(p).resolve()
            for p in self.blacklist.readBlackList()
        }

    def _scan_dir(self, base: Path):
        try:
            with os.scandir(base) as it:
                for entry in it:
                    try:
                        # ignora symlinks
                        if entry.is_symlink():
                            continue

                        entry_path = Path(entry.path).resolve()

                        # verifica blacklist (robusta)
                        if any(entry_path.is_relative_to(b) for b in self._bloqueadas):
                            continue

                        if entry.is_dir(follow_symlinks=False):
                            self._scan_dir(entry_path)

                        elif entry.is_file(follow_symlinks=False):
                            self._arquivos.append(entry_path)

                    except (PermissionError, OSError):
                        continue
        except (PermissionError, FileNotFoundError):
            pass

    def scan(self, caminhos, bloqueadas=None):
        self._arquivos.clear()

        if isinstance(caminhos, (str, Path)):
            caminhos = [caminhos]

        # adiciona bloqueadas passadas no scan()
        if bloqueadas:
            self._bloqueadas |= {
                Path(p).resolve()
                for p in bloqueadas
            }

        for caminho in caminhos:
            self._scan_dir(Path(caminho).resolve())

        return self._arquivos

    def __len__(self):
        return len(self._arquivos)