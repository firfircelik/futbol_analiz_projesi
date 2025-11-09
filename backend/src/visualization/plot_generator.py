import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def plot_team_stats(team_stats):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=team_stats.index, y='total_events', data=team_stats)
    plt.title('Takım Başına Toplam Olay Sayısı')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('data/visualizations/team_events.png')
    plt.close()

def plot_shot_accuracy(team_stats):
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x='shot', y='shot_accuracy', data=team_stats)
    plt.title('Şut Sayısı ve İsabet Oranı')
    for i, txt in enumerate(team_stats.index):
        plt.annotate(txt, (team_stats['shot'].iloc[i], team_stats['shot_accuracy'].iloc[i]))
    plt.tight_layout()
    plt.savefig('data/visualizations/shot_accuracy.png')
    plt.close()

def main():
    team_stats = pd.read_csv('data/processed/team_analysis.csv', index_col=0)
    
    os.makedirs('data/visualizations', exist_ok=True)
    plot_team_stats(team_stats)
    plot_shot_accuracy(team_stats)
    print("Görselleştirmeler oluşturuldu.")

if __name__ == '__main__':
    main()
