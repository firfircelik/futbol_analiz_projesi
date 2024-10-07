from statsbombpy import sb
import pandas as pd
import os

def collect_statsbomb_data(competition_id, season_id):
    try:
        matches = sb.matches(competition_id=competition_id, season_id=season_id)
        
        os.makedirs('data/raw', exist_ok=True)
        
        matches.to_csv('data/raw/statsbomb_matches.csv', index=False)
        
        all_events = []
        for match_id in matches['match_id']:
            events = sb.events(match_id=match_id)
            all_events.append(events)
            events.to_csv(f'data/raw/events_{match_id}.csv', index=False)
        
        combined_events = pd.concat(all_events, ignore_index=True)
        combined_events.to_csv('data/raw/all_events.csv', index=False)
        
        print("Veri toplama işlemi başarıyla tamamlandı.")
        return matches, combined_events
    except Exception as e:
        print(f"Veri toplama sırasında bir hata oluştu: {str(e)}")
        return None, None

if __name__ == '__main__':
    collect_statsbomb_data(competition_id=11, season_id=90)