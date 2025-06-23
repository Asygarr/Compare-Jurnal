import requests
import pandas as pd
import random
import time
import os
import json

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "paperId,title,abstract"

TOPIC_LIST = [
    "Technology", "Health", "Economy"
]

# File untuk menyimpan state dan data sementara
STATE_FILE = 'state.json'
TEMP_ABSTRACTS_FILE = 'temp_abstracts.csv'
DATASET_FILE = 'dataset/dataset-journal.csv'

def get_jurnal(required_count, state):
    """Mengambil abstrak jurnal sesuai kebutuhan, melanjutkan dari state"""
    jurnal = []
    topics_exhausted = {topic: False for topic in TOPIC_LIST}
    limit = 100

    current_state = state.copy()
    
    while len(jurnal) < required_count and not all(topics_exhausted.values()):
        for topic in TOPIC_LIST:
            if topics_exhausted[topic] or len(jurnal) >= required_count:
                continue

            params = {
                "query": topic,
                "fields": FIELDS,
                "limit": limit,
                "offset": current_state[topic],
            }
            print(f"Mengambil data untuk topik '{topic}' dengan offset {current_state[topic]}...")

            # Retry mechanism untuk handle rate limit
            retry_count = 0
            max_retries = 3
            success = False
            while retry_count < max_retries and not success:
                try:
                    response = requests.get(SEMANTIC_SCHOLAR_URL, params=params)
                    if response.status_code == 200:
                        success = True
                    elif response.status_code == 429:
                        wait_time = 10 + (2 ** retry_count)  # Exponential backoff
                        print(f"Rate limit exceeded. Menunggu {wait_time} detik...")
                        time.sleep(wait_time)
                        retry_count += 1
                    else:
                        print(f"Error {response.status_code} untuk topik '{topic}'. Melewati topik ini.")
                        topics_exhausted[topic] = True
                        break
                except requests.exceptions.RequestException as e:
                    print(f"Terjadi kesalahan: {e}. Melewati topik ini.")
                    topics_exhausted[topic] = True
                    break

            if not success:
                topics_exhausted[topic] = True
                continue

            data = response.json()
            papers = data.get("data", [])
            if not papers:
                print(f"Tidak ada data lagi untuk topik '{topic}'.")
                topics_exhausted[topic] = True
                continue

            # Proses semua paper dalam satu halaman
            for paper in papers:
                title = paper.get("title")
                abstract = paper.get("abstract")
                # Periksa apakah title dan abstract memenuhi syarat
                if (title and len(title.split()) >= 10 and 
                    abstract and len(abstract.split()) >= 50):
                    jurnal.append((title, abstract))

            # Update state setelah berhasil memproses satu halaman
            current_state[topic] += limit
            time.sleep(1)  # Menghindari request terlalu cepat

    return jurnal, current_state

def make_dataset(abstracts):
    """Membuat dataset dari kumpulan abstrak"""
    if len(abstracts) < 200:
        raise ValueError(f"Jumlah abstrak ({len(abstracts)}) kurang dari 200. Kumpulkan ulang!")

    # Acak dan pilih 200 abstrak
    abstracts_sample = random.sample(abstracts, 200)
    random.shuffle(abstracts_sample)
    
    # Buat pasangan
    paired = []
    for i in range(0, 200, 2):
        paired.append({
            "title1": abstracts_sample[i][0],
            "abstract1": abstracts_sample[i][1],
            "title2": abstracts_sample[i+1][0],
            "abstract2": abstracts_sample[i+1][1]
        })
    
    # Simpan ke CSV
    df = pd.DataFrame(paired)
    os.makedirs('dataset', exist_ok=True)
    df.to_csv(DATASET_FILE, index=False)
    print(f"Dataset berhasil disimpan ke {DATASET_FILE}")

def main():
    """Fungsi utama dengan mekanisme melanjutkan state"""
    # Muat state sebelumnya jika ada
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    else:
        state = {topic: 0 for topic in TOPIC_LIST}
    
    # Muat abstrak sementara jika ada
    if os.path.exists(TEMP_ABSTRACTS_FILE):
        df_temp = pd.read_csv(TEMP_ABSTRACTS_FILE)
        existing_abstracts = [(row.title, row.abstract) for _, row in df_temp.iterrows()]
    else:
        existing_abstracts = []
    
    print(f"Abstrak yang tersedia: {len(existing_abstracts)}")
    
    # Hitung kebutuhan tambahan
    min_abstract = 200
    required_count = max(0, min_abstract - len(existing_abstracts))
    
    if required_count > 0:
        print(f"Membutuhkan tambahan {required_count} abstrak...")
        new_abstracts, updated_state = get_jurnal(required_count, state)
        
        # Gabung dengan data existing
        all_abstracts = existing_abstracts + new_abstracts
        
        # Simpan data baru ke file sementara
        if new_abstracts:
            df_new = pd.DataFrame(new_abstracts, columns=['title', 'abstract'])
            if os.path.exists(TEMP_ABSTRACTS_FILE):
                df_new.to_csv(TEMP_ABSTRACTS_FILE, mode='a', index=False, header=False)
            else:
                df_new.to_csv(TEMP_ABSTRACTS_FILE, index=False)
        
        # Update state
        state = updated_state
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    else:
        all_abstracts = existing_abstracts
    
    # Buat dataset jika cukup
    if len(all_abstracts) >= min_abstract:
        make_dataset(all_abstracts)
        # Hapus file sementara setelah berhasil
        if os.path.exists(TEMP_ABSTRACTS_FILE):
            os.remove(TEMP_ABSTRACTS_FILE)
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
    else:
        print(f"Total abstrak terkumpul: {len(all_abstracts)}. Masih kurang dari 200")

if __name__ == "__main__":
    main()