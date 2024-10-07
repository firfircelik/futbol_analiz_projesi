import pandas as pd
import os

def calculate_team_stats(events):
    team_stats = events.groupby('team').agg({
        'type': 'count',
        'shot': 'sum',
        'goal': 'sum',
        'pass': 'sum'
    }).rename(columns={'type': 'total_events'})
    team_stats['shot_accuracy'] = team_stats['goal'] / team_stats['shot']
    return team_stats

def analyze_team_performance(merged_data):
    team_performance = merged_data.groupby('team_name').agg({
        'score': 'mean',
        'possession': 'mean'
    })
    return team_performance

def main():
    merged_data = pd.read_csv('data/processed/merged_matches.csv')
    events = pd.read_csv('data/raw/all_events.csv')
    
    team_stats = calculate_team_stats(events)
    team_performance = analyze_team_performance(merged_data)
    
    result = pd.merge(team_stats, team_performance, left_index=True, right_index=True)
    
    os.makedirs('data/processed', exist_ok=True)
    result.to_csv('data/processed/team_analysis.csv')
    print("Takım analizi tamamlandı.")

if __name__ == '__main__':
    main()
