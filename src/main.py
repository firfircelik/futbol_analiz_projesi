import sys
from src.data_collection.statsbomb_data_collection import collect_statsbomb_data
from src.data_collection.football_data_collection import collect_football_data
from src.data_processing.data_processor import main as process_data
from src.analysis.team_analysis import main as analyze_teams
from src.visualization.plot_generator import main as generate_plots

def main():
    print("Veri toplama başlıyor...")
    statsbomb_matches, statsbomb_events = collect_statsbomb_data(competition_id=11, season_id=90)
    
    if statsbomb_matches is None:
        print("Error: StatsBomb data collection failed. Exiting.")
        sys.exit(1)
        
    football_data_result = collect_football_data()
    
    if football_data_result is None:
        print("Error: Football Data collection failed. Exiting.")
        sys.exit(1)
    
    print("Veri işleme başlıyor...")
    process_data()
    
    print("Takım analizi başlıyor...")
    analyze_teams()
    
    print("Görselleştirmeler oluşturuluyor...")
    generate_plots()
    
    print("Futbol maç analizi tamamlandı.")

if __name__ == '__main__':
    main()
