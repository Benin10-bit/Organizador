from pathlib import Path
import os

class Scanner:

    def __init__(self):
        self._arquivos = []

        self.LINUX_SYSTEM_DIRS = ["/bin", "/sbin", "/usr", "/lib", "/lib64", "/etc", "/boot", "/var", "/proc", "/sys", "/dev", "/run", "/snap", "/opt"]

        self.WINDOWS_SYSTEM_DIRS = ["c:/windows", "c:/windows/system32","c:/program files","c:/program files (x86)","c:/programdata","c:/users/all users"]

        self.BASEPATH = Path(__file__).parent

    def isSystem(self, caminho):
        p = caminho.resolve()
        p_str = str(p).lower().replace("\\", "/")

        if os.name == "posix":
            # checar pastas do sistema
            if any(p_str.startswith(folder) for folder in self.LINUX_SYSTEM_DIRS):
                return True

            # UID 0 = root
            try:
                if p.stat().st_uid == 0:
                    return True
            except PermissionError:
                return True

        elif os.name == "nt":
            if any(p_str.startswith(folder) for folder in self.WINDOWS_SYSTEM_DIRS):
                return True

            # Arquivo bloqueado ou protegido
            try:
                if not os.access(p, os.W_OK):
                    return True
            except:
                return True

        return False

    def scan(self, caminhos, bloqueadas=None):
        self._arquivos = []

        if isinstance(caminhos, (str, Path)):
            caminhos = [caminhos]

        pastasBloqueadas = set(Path(p).resolve() for p in (bloqueadas or []))

        for caminho in caminhos:
            for arquivo in Path(caminho).rglob("*"):

                # BLACKLIST verdadeira
                if any(b in arquivo.resolve().parents for b in pastasBloqueadas):
                    continue

                # Windows only — corrigido
                if hasattr(arquivo, "is_reserved") and arquivo.is_reserved():
                    self._arquivos.append("arquivo do sistema")
                    continue

                # ERRO QUE VOCÊ COMETEU — agora corrigido!
                if arquivo.is_symlink():
                    self._arquivos.append("arquivo do sistema")
                    continue

                if self.isSystem(arquivo):
                    self._arquivos.append("arquivo do sistema")
                    continue

                if arquivo.is_file():
                    self._arquivos.append(arquivo)

        return self._arquivos

    def __len__(self):
        return len(self._arquivos)
    
#Depuração    
def run():
    
    pass
    
