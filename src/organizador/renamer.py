from pathlib import Path

def rename(filePath):
    file = Path(filePath)
    safe = file.stem.replace(" ", "_")

    finalName = f"{safe}.{file.suffix}"
    counter = 1

    while (file.parent / finalName).exists():
        finalName = f"{safe}_{counter}.{file.suffix}"
        counter += 1
    
    file.rename(file.parent / finalName)