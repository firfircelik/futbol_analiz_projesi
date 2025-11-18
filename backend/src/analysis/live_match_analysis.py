import pandas as pd
import matplotlib.pyplot as plt

def analyze_live_match():
    df = pd.read_csv('data/processed/merged_data.csv')
    # Örnek analiz işlemleri
    df['xG'] = df['shots'] * 0.1  # Basit bir xG hesaplama örneği
    plt.plot(df['minute'], df['xG'])
    plt.title('Live Match xG Analysis')
    plt.show()

if __name__ == '__main__':
    analyze_live_match()