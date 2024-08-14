import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def match_prediction():
    df = pd.read_csv('data/processed/merged_data.csv')
    # Basit bir maç tahmini modeli
    X = df[['shots', 'possession']]
    y = df['match_result']  # 1: Win, 0: Loss or Draw
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    print(f'Match Prediction Accuracy: {accuracy:.2f}')

if __name__ == '__main__':
    match_prediction()