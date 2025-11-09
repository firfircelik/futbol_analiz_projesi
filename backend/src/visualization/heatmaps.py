import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_heatmap():
    df = pd.read_csv('data/processed/merged_data.csv')
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.pivot_table(index='y_coordinate', columns='x_coordinate', values='passes', aggfunc='sum'), cmap='coolwarm')
    plt.title('Heatmap of Passes')
    plt.show()

if __name__ == '__main__':
    create_heatmap()