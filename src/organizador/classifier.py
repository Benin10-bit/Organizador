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

def classify(pathFile):
    ext = Path(pathFile).suffix.lower()

    for category, exts in CATEGORIES.items():
        if ext == exts:
            return category
    
    mime, _ = mimetypes.guess_type(pathFile)
    if mime:
        return mime.split('/')[0].capitalize()
    
    return "Outros"