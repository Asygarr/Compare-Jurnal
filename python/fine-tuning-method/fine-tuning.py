from sentence_transformers import SentenceTransformer, losses, InputExample, evaluation
from torch.utils.data import DataLoader
import pandas as pd

df = pd.read_csv("../dataset/silver-label-calibrated.csv", encoding="latin-1")

examples = [
    InputExample(texts=[row["abstract1"], row["abstract2"]],
                 label=row["calibrated_similarity"])
    for _, row in df.iterrows()
]

gold = pd.read_csv("../dataset/gold-label.csv", encoding="latin-1")
gold_examples = [
    InputExample(texts=[row["abstract1"], row["abstract2"]],
                 label=row["cosine_similarity"])
    for _, row in gold.iterrows()
]
evaluator = evaluation.EmbeddingSimilarityEvaluator.from_input_examples(
    gold_examples, name='gold-eval'
)

model_name = "distilbert-base-nli-stsb-mean-tokens"
model = SentenceTransformer(model_name)

print("=== Evaluasi sebelum fine-tuning ===")
resultBefore = model.evaluate(evaluator)
pearson_score, spearman_score = resultBefore['gold-eval_pearson_cosine'], resultBefore['gold-eval_spearman_cosine']
print(f"Pearson : {pearson_score:.4f}")
print(f"Spearman: {spearman_score:.4f}")

transformer = model._first_module().auto_model
for layer in transformer.transformer.layer[:4]:
    for param in layer.parameters():
        param.requires_grad = False

train_loader = DataLoader(examples, shuffle=True, batch_size=8)
train_loss  = losses.CosineSimilarityLoss(model)

model.fit(
    train_objectives=[(train_loader, train_loss)],
    evaluator=evaluator,           
    epochs=3,
    warmup_steps=50,
    evaluation_steps=100,
    output_path="./fine_tuned_model",
    use_amp=True
)

print("=== Evaluasi setelah fine-tuning ===")
fine_tuned = SentenceTransformer("./fine_tuned_model")
resultAfter = fine_tuned.evaluate(evaluator)
pearson_score, spearman_score = resultAfter['gold-eval_pearson_cosine'], resultAfter['gold-eval_spearman_cosine']
print(f"Pearson : {pearson_score:.4f}")
print(f"Spearman: {spearman_score:.4f}")
