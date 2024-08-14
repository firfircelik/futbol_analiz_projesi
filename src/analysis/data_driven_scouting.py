import pandas as pd

def scout_players():
    df = pd.read_csv('data/processed/merged_data.csv')
    # Oyuncuları veriye dayalı olarak scout etme
    top_scorers = df[df['goals'] > 10]
    top_scorers.to_csv('reports/figures/top_scorers.csv', index=False)
    print("Top Scorers scouted and saved.")

if __name__ == '__main__':
    scout_players()