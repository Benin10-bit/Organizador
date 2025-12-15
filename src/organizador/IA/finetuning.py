from pathlib import Path
import numpy as np
import pandas as pd
import evaluate

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)

from sklearn.metrics import classification_report, f1_score

def run():
    #Dataset
    BASEPATH = Path(__file__).parent
    df = pd.read_csv(BASEPATH / "dataset_balanceado_600.csv")

    df["materia"] = df["materia"].str.lower().str.strip().str.replace('"', '', regex=False)

    labels = sorted(df["materia"].unique())
    label2id = {l: i for i, l in enumerate(labels)}
    id2label = {i: l for l, i in label2id.items()}

    df["label"] = df["materia"].map(label2id)

    dataset = Dataset.from_pandas(df[["texto", "label"]])

    dataset = dataset.train_test_split(test_size=0.2, seed=42)

    train_dataset = dataset["train"]
    test_dataset = dataset["test"]

    #tokenizer

    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    def token(batch):
        return tokenizer(batch["texto"], truncation=True, padding="max_length", max_length=128)

    train_dataset = train_dataset.map(token, batched=True)
    test_dataset = test_dataset.map(token, batched=True)

    train_dataset = train_dataset.remove_columns("texto")
    test_dataset = test_dataset.remove_columns("texto")

    train_dataset.set_format("torch")
    test_dataset.set_format("torch")

    #modelo

    model = AutoModelForSequenceClassification.from_pretrained(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        num_labels=len(labels),
        id2label=id2label,
        label2id=label2id
    )

    #métricas

    accuracy_metric = evaluate.load("accuracy")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)

        return {
            "accuracy": accuracy_metric.compute(
                predictions=predictions,
                references=labels
            )["accuracy"],
            "f1": f1_score(labels, predictions, average="weighted")
        }

    #argumentoss de treinamento

    training_args = TrainingArguments(
        output_dir="./miniLM",
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=5,
        learning_rate=2e-5,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=50,
        load_best_model_at_end=True
    )

    #treinador

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics
    )

    #treino

    trainer.train()

    #salvar modelo

    model.save_pretrained("./miniLM")
    tokenizer.save_pretrained("./miniLM")

    #matriz de confusão

    preds = trainer.predict(train_dataset)

    y_true = preds.label_ids
    y_pred = np.argmax(preds.predictions, axis=1)

    unique_labels = np.unique(y_true)

    print(
        classification_report(
            y_true,
            y_pred,
            labels=unique_labels,
            target_names=[id2label[i] for i in unique_labels],
            digits=4
        )
    )

if __name__ == "__main__":
    run()