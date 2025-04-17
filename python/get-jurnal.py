import requests
import pandas as pd
import random
import time

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "paperId,title,abstract"

TOPIC_LIST = [
    "Teknologi", "Kesehatan", "Ekonomi"
]

def get_jurnal(min_abstract=200):
    jurnal = []
    
    topic_offsets = {topic: 0 for topic in TOPIC_LIST}
    topics_exhausted = {topic: False for topic in TOPIC_LIST}
    limit = 100 
    
    while len(jurnal) < min_abstract and not all(topics_exhausted.values()):
        for topic in TOPIC_LIST:
            if topics_exhausted[topic]:
                continue

            params = {
                "query": topic,
                "fields": FIELDS,
                "limit": limit,
                "offset": topic_offsets[topic],
            }
            print(f"Mengambil data untuk topik '{topic}' dengan offset {topic_offsets[topic]}...")
            
            # response = requests.get(SEMANTIC_SCHOLAR_URL, params=params)
            # if response.status_code == 429:
            #     print(f"Error 429 terjadi pada topik '{topic}'. Mohon tunggu beberapa saat sebelum mencoba kembali...")
            #     time.sleep(10)
            #     continue

            try:
                response = requests.get(SEMANTIC_SCHOLAR_URL, params=params)
            except requests.exceptions.RequestException as e:
                print(f"Terjadi kesalahan saat mengambil data untuk topik '{topic}': {e}")
                topics_exhausted[topic] = True
                time.sleep(10)
                continue

            if response.status_code != 200:
                print(f"Terjadi error anomali saat mengambil data untuk topik '{topic}': {response.status_code}")
                topics_exhausted[topic] = True
                continue

            data = response.json()
            papers = data.get("data", [])
            if not papers:
                print(f"Tidak ada data lagi untuk topik '{topic}'.")
                topics_exhausted[topic] = True
                continue

            for paper in papers:
                title = paper.get("title")
                abstract = paper.get("abstract")
                if abstract and len(abstract.split()) >= 30:
                    jurnal.append((title, abstract))
                if len(jurnal) >= min_abstract:
                    break

            topic_offsets[topic] += limit
            time.sleep(1)  
            
            if len(jurnal) >= min_abstract:
                break

    print(f"Jumlah jurnal terkumpul: {len(jurnal)}")
    return jurnal

def make_dataset(abstract):
    if len(abstract) < 200:
        raise ValueError("Jumlah abstrak kurang dari 200. Mohon kumpulkan abstrak yang cukup!")
    
    abstracts_sample = random.sample(abstract, 200)
    random.shuffle(abstracts_sample)
    
    paired = []
    for i in range(0, 200, 2):
        paired.append({
            "title1": abstracts_sample[i][0],
            "abstract1": abstracts_sample[i][1],
            "title2": abstracts_sample[i+1][0],
            "abstract2": abstracts_sample[i+1][1]
        })
    
    df = pd.DataFrame(paired)
    df.to_csv("dataset/dataset-jurnal.csv", index=False)
    print("Dataset berhasil disimpan ke dataset.csv")

def main():
    abstracts = get_jurnal(min_abstract=200)
    
    try:
        make_dataset(abstracts)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()