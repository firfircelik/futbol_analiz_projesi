import pandas as pd
import matplotlib.pyplot as plt

def analyze_player_trend():
    df = pd.read_csv('data/processed/merged_data.csv')
    # Oyuncuların performans trendlerini analiz etme
    player_trend = df.groupby('player_name')['goals'].cumsum()
    plt.plot(player_trend)
    plt.title('Player Trend Analysis')
    plt.show()

if __name__ == '__main__':
    analyze_player_trend()