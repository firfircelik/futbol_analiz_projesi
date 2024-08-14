import pandas as pd
import json

def preprocess_football_data():
    with open('data/raw/football_data_matches.json', 'r') as f:
        data = json.load(f)

    df = pd.json_normalize(data['matches'])

    # Drop columns that are not needed
    df = df.drop(columns=['group', 'season.winner'])

    # Inspect missing data
    missing_data_summary = df.isnull().sum()
    print("Missing data summary:\n", missing_data_summary)

    # Drop rows with missing values in critical columns only if necessary
    df_clean = df.dropna(subset=['id', 'utcDate', 'homeTeam.name', 'awayTeam.name'])

    # Optionally, select relevant columns
    relevant_columns = ['id', 'utcDate', 'status', 'matchday', 'homeTeam.name', 'awayTeam.name', 'score.fullTime.home', 'score.fullTime.away']
    df_clean = df_clean[relevant_columns]

    # Save to CSV
    df_clean.to_csv('data/processed/football_data_matches_clean.csv', index=False)

if __name__ == '__main__':
    preprocess_football_data()
