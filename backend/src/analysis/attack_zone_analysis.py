import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_attack_zones():
    df = pd.read_csv('data/processed/merged_data.csv')
    # xT haritalarını ve atak bölgesi analizlerini yapma
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.pivot_table(index='y_coordinate', columns='x_coordinate', values='xT', aggfunc='mean'), cmap='viridis')
    plt.title('Attack Zone xT Analysis')
    plt.show()

if __name__ == '__main__':
    analyze_attack_zones()