import pandas as pd
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import lightgbm as lgb
import os

# ------------------------------
# Função de pré-processamento
# ------------------------------
def run():
    def preprocess_text(text):
        text = str(text).strip().lower()
        return text

    # Carregar dataset
    BASEPATH = os.path.dirname(__file__)
    CSVPATH = os.path.join(BASEPATH, "textos_para_predicao.csv")
    df = pd.read_csv(CSVPATH)

    # Remover classes com poucos exemplos
    min_examples = 10
    counts = df['materia'].value_counts()
    df = df[df['materia'].isin(counts[counts >= min_examples].index)]

    X = df['texto'].apply(preprocess_text).tolist()
    y = df['materia'].tolist()

    # Treino / teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Carregar modelo MiniLM
    print("Carregando MiniLM...")
    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    # Gerar embeddings
    print("Gerando embeddings de treino...")
    emb_train = model.encode(X_train, batch_size=32, show_progress_bar=True)
    print("Gerando embeddings de teste...")
    emb_test = model.encode(X_test, batch_size=32, show_progress_bar=True)

    # Normalizar embeddings
    scaler = StandardScaler()
    emb_train = scaler.fit_transform(emb_train)
    emb_test = scaler.transform(emb_test)

    # Treinar LightGBM Classifier
    clf = lgb.LGBMClassifier(
        objective='multiclass',
        num_class=len(set(y)),
        boosting_type='gbdt',
        max_depth=10,
        n_estimators=500,
        learning_rate=0.05,
        class_weight='balanced'
    )
    clf.fit(emb_train, y_train)

    # Avaliação detalhada
    y_pred = clf.predict(emb_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAcurácia geral: {acc*100:.2f}%")
    print("\nRelatório detalhado por classe:\n")
    print(classification_report(y_test, y_pred))

    # Salvar modelo + scaler
    joblib.dump({
        "bert": model,
        "clf": clf,
        "scaler": scaler
    }, os.path.join(BASEPATH, "classificador.joblib"))

    print("\nModelo salvo como 'classificador.joblib'")

if __name__ == "__main__":
    run()