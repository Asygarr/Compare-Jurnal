import pandas as pd
import re
import unicodedata
import argparse
import sys

def clean_text(text):
    """
    Membersihkan teks dari karakter khusus, baris baru, dan karakter non-ASCII
    dengan penanganan khusus untuk karakter-karakter umum dalam teks akademik
    """
    if not text or pd.isna(text):
        return ""
    text = str(text)
    
    # Normalisasi karakter unicode - gunakan NFKC untuk kompatibilitas
    text = unicodedata.normalize('NFKC', text)
    
    # Dekode karakter yang salah di-encode (misal: UTF-8 yang diinterpretasikan sebagai Latin-1)
    try:
        text = text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    
    replacements = {
        # Karakter UTF-8 yang salah diinterpretasikan , 
        'â€™': "'",    'â€œ': '"',    'â€': '"',     'â€“': '-',
        'â€”': '—',    'â€˜': "'",    'â€¢': '•',     'â€¦': '...',
        'Ã©': 'é',     'Ã¨': 'è',     'Ã±': 'ñ',      'Ã¶': 'ö',
        'Ã¡': 'á',     'Ã³': 'ó',     'Ãº': 'ú',      'Ã¼': 'ü',
        'Ã¢': 'â',     'Ã£': 'ã',     'Ã§': 'ç',      'Ãª': 'ê',
        'Ã®': 'î',     'Ã´': 'ô',     'Ã»': 'û',      'Ã¤': 'ä',
        'Ã«': 'ë',     'Ã¯': 'ï',     'Ã¶': 'ö',      'Ã¼': 'ü',
        'Ã¿': 'ÿ',     'Ã ': 'à',     'Ã¡': 'á',      'Ã©': 'é',
        'Ã¨': 'è',     'Ã¬': 'ì',     'Ã³': 'ó',      'Ã²': 'ò',
        'Ã¹': 'ù',     'Ãº': 'ú',     'Ã±': 'ñ',      'â€': '',
        
        # Karakter kutipan khusus
        '‘': "'",      '’': "'",      '“': '"',       '”': '"',
        '„': '"',      '‟': '"',      '‹': "'",       '›': "'",
        
        # Dash dan hyphen
        '–': '-',      '—': '-',      '―': '-',       '−': '-',
        
        # Karakter khusus lainnya
        '•': '-',      '·': '-',      '…': '...',     '®': '',
        '©': '',       '™': '',       '§': '',        '¶': '',
        
        # Whitespace
        '\n': ' ',     '\r': ' ',     '\t': ' ',      '�': '',
        '\xa0': ' ',   ' ': ' ',      '\u200b': '',   '\ufeff': '',
        '\u200e': '',  '\u200f': '',  '\u202a': '',   '\u202c': '',
    }
    
    # Lakukan penggantian karakter
    for pattern, replacement in replacements.items():
        text = text.replace(pattern, replacement)

    # Hapus SEMUA varian â€*
    text = re.sub(r'â€[\w\d]?', '', text)  # regex baru
    
    # Hapus karakter kontrol lainnya
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    
    # Normalisasi spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def clean_csv_file(input_file, output_file=None):
    """
    Membersihkan kolom spesifik dalam file CSV dengan encoding yang benar
    """
    try:
        # Baca dengan encoding UTF-8 dan fallback ke latin1 jika perlu
        try:
            df = pd.read_csv(input_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(input_file, encoding='latin1')
    except FileNotFoundError:
        print(f"Error: File '{input_file}' tidak ditemukan!")
        sys.exit(1)
    except Exception as e:
        print(f"Error membaca file: {e}")
        sys.exit(1)
    
    # Daftar kolom yang akan dibersihkan
    target_columns = ['title1', 'abstract1', 'title2', 'abstract2']
    
    # Cek kolom yang ada di file
    available_columns = [col for col in target_columns if col in df.columns]
    missing_columns = [col for col in target_columns if col not in df.columns]
    
    if not available_columns:
        print("Error: Tidak ada kolom target yang ditemukan di file CSV!")
        print(f"Kolom yang dicari: {', '.join(target_columns)}")
        print(f"Kolom yang ada: {', '.join(df.columns)}")
        sys.exit(1)
    
    if missing_columns:
        print(f"Peringatan: Kolom berikut tidak ditemukan: {', '.join(missing_columns)}")
    
    # Bersihkan kolom yang tersedia
    for column in available_columns:
        print(f"Membersihkan kolom '{column}'...")
        df[column] = df[column].apply(clean_text)
    
    # Tentukan nama file output
    if output_file is None:
        output_file = input_file
    
    # Simpan hasil dengan encoding UTF-8
    try:
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\nFile berhasil dibersihkan dan disimpan sebagai: {output_file}")
        print(f"Jumlah baris yang diproses: {len(df)}")
        print(f"Kolom yang dibersihkan: {', '.join(available_columns)}")
        print("\nContoh hasil pembersihan:")
        for col in available_columns:
            sample = df[col].iloc[0][:100] + "..." if len(df[col].iloc[0]) > 100 else df[col].iloc[0]
            print(f"- {col}: {sample}")
    except Exception as e:
        print(f"Error menyimpan file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Membersihkan kolom title dan abstract dalam file CSV',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('input', help='Path ke file CSV input')
    parser.add_argument('-o', '--output', help='Path untuk file CSV output (opsional)\n'
                        'Jika tidak ditentukan, file input akan ditimpa')
    
    args = parser.parse_args()
    
    print(f"Memulai pembersihan file: {args.input}")
    clean_csv_file(
        input_file=args.input,
        output_file=args.output
    )

if __name__ == "__main__":
    main()