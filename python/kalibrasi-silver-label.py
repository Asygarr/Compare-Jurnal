from sklearn.isotonic import IsotonicRegression
import pandas as pd
import matplotlib.pyplot as plt

silver = pd.read_csv("./dataset/silver-label.csv", encoding="latin-1")
gold   = pd.read_csv("./dataset/gold-label.csv",   encoding="latin-1")

silver["key"] = silver["title1"].str.strip() + "||" + silver["title2"].str.strip()
gold["key"]   = gold["title1"].str.strip()   + "||" + gold["title2"].str.strip()

merged = pd.merge(
    silver[["key", "cosine_similarity"]],
    gold[["key", "cosine_similarity"]],
    on="key",
    suffixes=("_silver", "_gold")
)

silver_scores_gold = merged["cosine_similarity_silver"].tolist()
gold_scores        = merged["cosine_similarity_gold"].tolist()

ir = IsotonicRegression(out_of_bounds="clip")
ir.fit(silver_scores_gold, gold_scores)

plt.figure()
plt.scatter(silver_scores_gold, gold_scores)
plt.plot([0,1], [0,1], linestyle='--')      # garis y=x
plt.xlabel('Silver Scores')
plt.ylabel('Gold Scores')
plt.title('Before Calibration')
plt.show()

plt.figure()
x_sorted = sorted(silver_scores_gold)
y_calib  = ir.transform(x_sorted)
plt.plot(x_sorted, y_calib)
plt.xlabel('Silver Scores')
plt.ylabel('Calibrated Scores')
plt.title('Calibration Function')
plt.show()

all_silver = silver["cosine_similarity"].tolist()
all_calib  = ir.transform(all_silver)

plt.figure()
plt.scatter(all_silver, all_calib)
plt.xlabel('Original Silver Scores')
plt.ylabel('Calibrated Scores')
plt.title('All Silver Scores After Calibration')
plt.show()

silver["calibrated_similarity"] = [round(x, 2) for x in all_calib]
silver.drop(columns=["key"], inplace=True)
silver.to_csv("./dataset/silver-label-calibrated.csv", index=False)

print("Kalibrasi selesai! File disimpan sebagai silver-label-calibrated.csv")
