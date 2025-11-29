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

def classify(*pathFile):
    classificados = list()

    for i in pathFile:
        # Extrair a extensão (ex: '.txt', '.jpg')
        ext = Path(pathFile).suffix.lower()

        # Verificar em cada categoria se a extensão está mapeada
        for category, exts in CATEGORIES.items():
            # Aqui deve verificar se ext está na lista 'exts'.
            if ext in exts:
                return category

        # Se não encontrou categoria pelas extensões, tentar via MIME
        mime, _ = mimetypes.guess_type(pathFile)
        if mime:
            # Exemplo: "image/png" → "Image"
            return mime.split('/')[0].capitalize()

        # Caso nenhuma classificação seja possível
        return "Outros"
    
