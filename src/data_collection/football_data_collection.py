import requests
import json

def collect_football_data(api_key):
    url = f'https://api.football-data.org/v4/competitions/BL1/matches'
    headers = {'X-Auth-Token': api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    
    with open('data/raw/football_data_matches.json', 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    collect_football_data('56770a4c0bf04cc5ad6d41a2bd1d0ba6')