from src.data_collection.statsbomb_data_collection import collect_statsbomb_data
from src.data_collection.football_data_collection import collect_football_data
from src.data_processing.data_processor import main as process_data
from src.analysis.team_analysis import main as analyze_teams
from src.visualization.plot_generator import main as generate_plots

def main():
    print("Veri toplama başlıyor...")
    collect_statsbomb_data(competition_id=11, season_id=90)
    collect_football_data()
    
    print("Veri işleme başlıyor...")
    process_data()
    
    print("Takım analizi başlıyor...")
    analyze_teams()
    
    print("Görselleştirmeler oluşturuluyor...")
    generate_plots()
    
    print("Futbol maç analizi tamamlandı.")

if __name__ == '__main__':
    main()
