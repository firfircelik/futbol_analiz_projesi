from statsbombpy import sb
import pandas as pd
import os

def collect_statsbomb_data(competition_id, season_id):
    try:
        # Maçları çek
        matches = sb.matches(competition_id=competition_id, season_id=season_id)
        
        # Klasörü oluştur (eğer yoksa)
        os.makedirs('data/raw', exist_ok=True)
        
        matches.to_csv('data/raw/statsbomb_matches.csv', index=False)
        
        # Her maç için olay verilerini çek
        for match_id in matches['match_id']:
            events = sb.events(match_id=match_id)
            events.to_csv(f'data/raw/events_{match_id}.csv', index=False)
        
        print("Veri toplama işlemi başarıyla tamamlandı.")
    except Exception as e:
        print(f"Veri toplama sırasında bir hata oluştu: {str(e)}")

if __name__ == '__main__':
    collect_statsbomb_data(competition_id=11, season_id=90)