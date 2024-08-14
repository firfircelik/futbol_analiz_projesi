import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_radar_chart():
    df = pd.read_csv('data/processed/merged_data.csv')
    player_name = 'Sample Player'
    metrics = ['dribbling', 'passing', 'shooting', 'defense', 'pace']
    
    player_stats = df[df['player_name'] == player_name][metrics].mean()
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    stats = player_stats.values.flatten().tolist()
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, stats, color='green', alpha=0.25)
    ax.plot(angles, stats, color='green', linewidth=2)
    ax.set_yticklabels([])
    plt.title(f'Radar Chart: {player_name}')
    plt.show()

if __name__ == '__main__':
    create_radar_chart()