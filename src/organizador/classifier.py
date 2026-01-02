from pathlib import Path
import mimetypes
import os

CATEGORIES = {
    "Imagens": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".svg", ".webp",
        ".ico", ".psd", ".ai", ".xcf"
    ],

    "Vídeos": [
        ".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".mpeg", ".mpg",
        ".webm", ".ogv", ".3gp"
    ],

    "Documentos": [
        ".pdf", ".docx", ".docx#", ".doc", ".pptx", ".ppt", ".xlsx", ".xls",
        ".rtf", ".txt", ".md", ".csv", ".json", ".xml", ".yaml", ".yml",
        ".odt", ".ods", ".odp", ".epub"
    ],

    "Áudio": [
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".oga", ".wma", ".m4a"
    ],

    "Executáveis": [
        ".exe", ".msi", ".bat", ".cmd", ".com", ".ps1",
        ".sh", ".bin", ".run", ".AppImage", ".desktop"
    ],

    "Compactados": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
        ".tar.gz", ".tgz"
    ],

    "Atalhos": [
        ".lnk", ".url", ".library-ms"
    ],

    "Configurações": [
        ".conf", ".ini", ".service", ".rule", ".mount", ".reg"
    ],

    "Fontes": [
        ".ttf", ".otf", ".woff", ".woff2"
    ],

    "Sistemas": [
        ".dll", ".sys", ".inf", ".so", ".iso", ".img", ".log", ".lock"
    ]
}


def classify(files: list[Path]) -> list:
    """
    Classifica arquivos APENAS quando receber uma lista.
    Retorna lista de dicts: { nome: str, category: str }
    """
    categorizados = []

    for file in files:

        # Segurança: ignorar itens inválidos
        if not isinstance(file, Path):
            continue

        ext = file.suffix.lower()
        found = False

        # Verificar por extensão
        for category, exts in CATEGORIES.items():
            if ext in exts:
                categorizados.append({
                    "path": file,
                    "category": category
                })
                found = True
                break

        if found:
            continue

        # Verificar por MIME
        mime, _ = mimetypes.guess_type(str(file))
        if mime:
            categorizados.append({
                "nome": file.name,
                "category": mime.split("/")[0].capitalize()
            })
            continue

        # Caso nada encaixe
        categorizados.append({
            "nome": file.name,
            "category": "Outros"
        })

    return categorizados
