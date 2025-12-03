from pathlib import Path
import sqlite3


def sql(comando):
    
    BASEPATH = Path(__file__).parent.parent.parent
    MODELPATH = BASEPATH / "data/historico.db" 
    conexao = sqlite3.connect(MODELPATH)
    cursor = conexao.cursor()

    cursor.execute(comando)
    
    conexao.commit()

