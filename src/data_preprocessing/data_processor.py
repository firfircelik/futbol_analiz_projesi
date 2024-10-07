import pandas as pd
import json
import os

def process_statsbomb_data():
    matches = pd.read_csv('data/raw/statsbomb_matches.csv')
    events = pd.read_csv('data/raw/all_events.csv')
    return matches, events

def process_football_data():
    with open('data/raw/football_data_matches.json', 'r') as f:
        data = json.load(f)
    matches = pd.json_normalize(data['matches'])
    return matches

def merge_data(statsbomb_matches, football_data_matches):
    merged_data = pd.merge(statsbomb_matches, football_data_matches, left_on='match_date', right_on='utcDate')
    return merged_data

def main():
    statsbomb_matches, statsbomb_events = process_statsbomb_data()
    football_data_matches = process_football_data()
    merged_data = merge_data(statsbomb_matches, football_data_matches)
    
    os.makedirs('data/processed', exist_ok=True)
    merged_data.to_csv('data/processed/merged_matches.csv', index=False)
    print("Veri işleme tamamlandı.")

if __name__ == '__main__':
    main()
