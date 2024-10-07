import requests
import json
import os
from dotenv import load_dotenv

def collect_football_data():
    try:
        load_dotenv()  # .env dosyasından çevre değişkenlerini yükle
        api_key = os.getenv('FOOTBALL_DATA_API_KEY')
        
        if not api_key:
            raise ValueError("API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin.")
        
        url = 'https://api.football-data.org/v4/competitions/BL1/matches'
        headers = {'X-Auth-Token': api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP hatalarını kontrol et
        data = response.json()
        
        # Klasörü oluştur (eğer yoksa)
        os.makedirs('data/raw', exist_ok=True)
        
        with open('data/raw/football_data_matches.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"{len(data['matches'])} maç verisi başarıyla kaydedildi.")
        return data
    except requests.exceptions.RequestException as e:
        print(f"API isteği sırasında bir hata oluştu: {str(e)}")
    except json.JSONDecodeError:
        print("JSON verisi ayrıştırılırken bir hata oluştu.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {str(e)}")
    return None

if __name__ == '__main__':
    collect_football_data()