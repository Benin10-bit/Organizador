from pathlib import Path

def rename(filePath):
    file = Path(filePath)

    # Nome base sem extensão e sem espaços
    safe = file.stem.replace(" ", "_")

    # IMPORTANTE:
    # file.suffix já inclui o ".", então NÃO deve ser escrito como f".{file.suffix}"
    finalName = f"{safe}{file.suffix}"

    counter = 1

    while (file.parent / finalName).exists():
        finalName = f"{safe}_{counter}{file.suffix}"
        counter += 1

    # Renomear arquivo para o novo nome seguro
    file.rename(file.parent / finalName)
