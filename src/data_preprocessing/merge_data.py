import pandas as pd

def combine_datasets():
    # Dataset'leri yükleyin
    statsbomb_df = pd.read_csv('/Users/firatcelik/Documents/futbol_analiz_projesi/data/processed/statsbomb_matches_clean.csv')
    football_data_df = pd.read_csv('/Users/firatcelik/Documents/futbol_analiz_projesi/data/processed/football_data_matches_clean.csv')
    
    # Lig bilgisini ekleyin
    statsbomb_df['league'] = 'La Liga'
    football_data_df['league'] = 'Bundesliga'
    
    # Tarih formatını standartlaştırın
    football_data_df['utcDate'] = pd.to_datetime(football_data_df['utcDate']).dt.date
    football_data_df.rename(columns={
        'utcDate': 'match_date',
        'homeTeam.name': 'home_team',
        'awayTeam.name': 'away_team'
    }, inplace=True)

    # Dataset'leri birleştirin
    combined_df = pd.concat([statsbomb_df, football_data_df], ignore_index=True)
    
    # Birleştirilmiş dataset'i kaydedin
    combined_df.to_csv('/Users/firatcelik/Documents/futbol_analiz_projesi/data/processed/combined_matches.csv', index=False)
    print("Datasets combined and saved successfully.")

if __name__ == '__main__':
    combine_datasets()
