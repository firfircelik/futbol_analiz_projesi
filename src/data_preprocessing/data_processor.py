import pandas as pd
import json
import os

RAW_DATA_DIR = 'data/raw'
PROCESSED_DATA_DIR = 'data/processed'
STATSbomb_MATCHES_CSV_IN_PATH = os.path.join(RAW_DATA_DIR, 'statsbomb_matches.csv')
ALL_EVENTS_CSV_IN_PATH = os.path.join(RAW_DATA_DIR, 'all_events.csv') # Path for reading all_events.csv
FOOTBALL_DATA_MATCHES_JSON_IN_PATH = os.path.join(RAW_DATA_DIR, 'football_data_matches.json')
COMBINED_PROCESSED_MATCHES_CSV_OUT_PATH = os.path.join(PROCESSED_DATA_DIR, 'combined_processed_matches.csv')
PROCESSED_STATSbomb_EVENTS_CSV_OUT_PATH = os.path.join(PROCESSED_DATA_DIR, 'processed_statsbomb_events.csv')

def process_statsbomb_data():
    matches = pd.read_csv(STATSbomb_MATCHES_CSV_IN_PATH)
    # Assuming events are still needed, read them. If not, this line can be removed.
    try:
        events = pd.read_csv(ALL_EVENTS_CSV_IN_PATH) 
    except FileNotFoundError:
        print(f"Warning: File not found at {ALL_EVENTS_CSV_IN_PATH}. Returning None for events.")
        events = None # Or pd.DataFrame() if preferred for type consistency downstream
    except pd.errors.EmptyDataError:
        print(f"Warning: No data in file at {ALL_EVENTS_CSV_IN_PATH}. Returning empty DataFrame for events.")
        events = pd.DataFrame()

    matches['league'] = 'La Liga'
    return matches, events

def process_football_data():
    with open(FOOTBALL_DATA_MATCHES_JSON_IN_PATH, 'r') as f:
        data = json.load(f)
    matches = pd.json_normalize(data['matches'])
    matches['league'] = 'Bundesliga'
    matches['utcDate'] = pd.to_datetime(matches['utcDate']).dt.date
    matches.rename(columns={
        'utcDate': 'match_date',
        'homeTeam.name': 'home_team',
        'awayTeam.name': 'away_team'
    }, inplace=True)
    return matches

def main():
    statsbomb_matches, statsbomb_events = process_statsbomb_data()
    football_data_matches = process_football_data()
    
    # Concatenate the two dataframes
    combined_df = pd.concat([statsbomb_matches, football_data_matches], ignore_index=True)
    
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    combined_df.to_csv(COMBINED_PROCESSED_MATCHES_CSV_OUT_PATH, index=False)
    print("Veri işleme tamamlandı ve birleştirilmiş dosya kaydedildi.")

    if statsbomb_events is not None and not statsbomb_events.empty:
        statsbomb_events.to_csv(PROCESSED_STATSbomb_EVENTS_CSV_OUT_PATH, index=False)
        print("StatsBomb events data saved.")
    elif statsbomb_events is not None and statsbomb_events.empty:
        print("StatsBomb events data is empty, not saving processed events file.")
    else:
        print("StatsBomb events data is None, not saving processed events file.")

if __name__ == '__main__':
    main()
