import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def evaluate_strength_profile():
    df = pd.read_csv('data/processed/merged_data.csv')
    player_name = 'Sample Player'
    metrics = ['dribbling', 'passing', 'shooting', 'defense', 'pace']
    
    player_stats = df[df['player_name'] == player_name][metrics].mean()
    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    stats = player_stats.values.flatten().tolist()
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, stats, color='blue', alpha=0.25)
    ax.plot(angles, stats, color='blue', linewidth=2)
    ax.set_yticklabels([])
    plt.title(f'Strength Profile Evaluation: {player_name}')
    plt.show()

if __name__ == '__main__':
    evaluate_strength_profile()