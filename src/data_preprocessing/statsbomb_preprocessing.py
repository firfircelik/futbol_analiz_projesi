import pandas as pd

def preprocess_statsbomb_data():
    df = pd.read_csv('data/raw/statsbomb_matches.csv')
    # Temel veri temizleme ve ön işleme
    df_clean = df.dropna()  # Eksik değerleri temizle
    df_clean.to_csv('data/processed/statsbomb_matches_clean.csv', index=False)

if __name__ == '__main__':
    preprocess_statsbomb_data()