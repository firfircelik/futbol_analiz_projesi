from statsbombpy import sb

def collect_statsbomb_data(competition_id, season_id):
    # Maçları çek
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    matches.to_csv('data/raw/statsbomb_matches.csv', index=False)
    
    # Her maç için olay verilerini çek
    for match_id in matches['match_id']:
        events = sb.events(match_id=match_id)
        events.to_csv(f'data/raw/events_{match_id}.csv', index=False)

if __name__ == '__main__':
    collect_statsbomb_data(competition_id=11, season_id=90)