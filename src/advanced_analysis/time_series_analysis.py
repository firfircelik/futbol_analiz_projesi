import pandas as pd
import matplotlib.pyplot as plt

def analyze_time_series():
    df = pd.read_csv('data/processed/merged_data.csv')
    df['cumulative_goals'] = df['goals_home'].cumsum()
    plt.plot(df['date'], df['cumulative_goals'])
    plt.title('Zaman Serisi Analizi: Gol Performansı')
    plt.show()

if __name__ == '__main__':
    analyze_time_series()