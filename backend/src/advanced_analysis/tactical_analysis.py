import pandas as pd
import matplotlib.pyplot as plt

def analyze_tactics():
    df = pd.read_csv('data/processed/merged_data.csv')
    plt.figure(figsize=(10, 6))
    plt.scatter(df['x_coordinate'], df['y_coordinate'], c='blue', alpha=0.5)
    plt.title('Taktiksel Yerleşim Analizi')
    plt.show()

if __name__ == '__main__':
    analyze_tactics()