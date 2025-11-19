import pandas as pd
import re
import joblib
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Stopwords
STOPWORDS_PT = [
    "a","o","as","os","e","é","de","do","da","dos","das",
    "que","em","um","uma","para","por","com","na","no","nas","nos",
    "se","sua","seu","suas","seus","como","mas","ou","ao","aos",
    "à","às","ser","ter","há","isso","isto","aquele","aquela",
    "eles","elas","ele","ela","tudo","toda","todo","todas",
]

# Função para limpar textos
def limpar_texto(t):
    t = str(t).lower()
    t = re.sub(r"http\S+", "", t)
    t = re.sub(r"\d+", " ", t)
    t = re.sub(r"[^a-záéíóúàâêîôûçãõ\s]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()

def predict(texto: str):
    base_dir = Path(__file__).resolve().parent

    modelo_path = base_dir / "classificador.joblib"

    if not modelo_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {modelo_path}")

    modelo = joblib.load(modelo_path)

    texto_limpo = limpar_texto(texto)

    pred = modelo.predict([texto_limpo])[0]

    return pred

def run():
    # Caminho da pasta onde este arquivo está
    base_dir = Path(__file__).resolve().parent

    # Caminho correto do CSV dentro da pasta IA
    csv_path = base_dir / "treino.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")

    print(f"Lendo dataset: {csv_path}")

    # Carregar dados
    df = pd.read_csv(csv_path)

    df["text_clean"] = df["text"].apply(limpar_texto)

    X = df["text_clean"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Pipeline com TF-IDF + NB
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1,2),
            sublinear_tf=True,
            min_df=2,
        )),
        ("model", MultinomialNB(alpha=0.3))
    ])

    # Treinar
    pipeline.fit(X_train, y_train)

    # Predizer
    y_pred = pipeline.predict(X_test)

    # Acurácia
    acc = accuracy_score(y_test, y_pred)
    print(f"Acurácia: {acc*100:.2f}%")

    # Salvar dentro da pasta IA
    modelo_path = base_dir / "classificador.joblib"
    joblib.dump(pipeline, modelo_path)

    print(f"Modelo salvo em:\n{modelo_path}")

if __name__ == "__main__":
    print("Treinando IA:")
    run()
