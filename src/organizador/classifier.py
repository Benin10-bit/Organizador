from pathlib import Path
import mimetypes

CATEGORIES = {
    "Imagens": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    "Vídeos": [".mp4", ".avi", ".mov", ".mkv"],
    "Documentos": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx"],
    "Áudio": [".mp3", ".wav", ".ogg"],
    "Executáveis": [".exe", ".msi", ".sh"],
    "Compactados": [".zip", ".rar", ".7z"],
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
                    "nome": file.name,
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
