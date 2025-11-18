from statsbombpy import sb
import pandas as pd
import os

RAW_DATA_DIR = 'data/raw'
MATCHES_CSV_PATH = os.path.join(RAW_DATA_DIR, 'statsbomb_matches.csv')
ALL_EVENTS_CSV_PATH = os.path.join(RAW_DATA_DIR, 'all_events.csv')

def collect_statsbomb_data(competition_id, season_id):
    try:
        matches = sb.matches(competition_id=competition_id, season_id=season_id)
        if matches is None or matches.empty:
            print(f"No matches found for competition_id {competition_id} and season_id {season_id}.")
            return None, None
            
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        matches.to_csv(MATCHES_CSV_PATH, index=False)
        
        all_events = []
        for match_id in matches['match_id']:
            try:
                events = sb.events(match_id=match_id)
                if events is None or events.empty:
                    print(f"No events found for match_id {match_id}.")
                    continue
                # Assuming sb.events returns a DataFrame or can be converted
                events_df = pd.DataFrame(events) 
                all_events.append(events_df)
                events_df.to_csv(f'{RAW_DATA_DIR}/events_{match_id}.csv', index=False)
            except Exception as e:
                print(f"Error collecting events for match_id {match_id}: {str(e)}")
                continue
        
        if not all_events:
            print("No events collected, skipping combined events file generation.")
            combined_events = pd.DataFrame() # Return an empty DataFrame
        else:
            combined_events = pd.concat(all_events, ignore_index=True)
            combined_events.to_csv(ALL_EVENTS_CSV_PATH, index=False)
            print("All event data collected and saved.")

        print("StatsBomb data collection process completed.")
        return matches, combined_events
    except Exception as e:
        print(f"An error occurred during the main StatsBomb data collection process: {str(e)}")
        return None, None

if __name__ == '__main__':
    collect_statsbomb_data(competition_id=11, season_id=90)