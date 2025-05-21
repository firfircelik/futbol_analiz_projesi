import unittest
import tempfile
import os
import shutil
import json
import pandas as pd
from unittest import mock

# Import functions to be tested or used in tests
from src.analysis.live_match_analysis import analyze_live_match
from src.analysis.player_trend_analysis import analyze_player_trend
from src.analysis.match_prediction import match_prediction
# Import the main function from data_processor.py
from src.data_preprocessing.data_processor import main as data_processor_main

class TestAnalysisModules(unittest.TestCase):
    def test_analyze_live_match(self):
        try:
            analyze_live_match()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"analyze_live_match failed: {str(e)}")

    def test_analyze_player_trend(self):
        try:
            analyze_player_trend()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"analyze_player_trend failed: {str(e)}")

    def test_match_prediction(self):
        try:
            match_prediction()
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"match_prediction failed: {str(e)}")

    def test_import_dotenv(self):
        try:
            import dotenv
            self.assertTrue(True, "dotenv module imported successfully.")
        except ImportError:
            self.fail("Failed to import dotenv")

    @mock.patch('src.data_preprocessing.data_processor.PROCESSED_STATSbomb_EVENTS_CSV_OUT_PATH')
    @mock.patch('src.data_preprocessing.data_processor.COMBINED_PROCESSED_MATCHES_CSV_OUT_PATH')
    @mock.patch('src.data_preprocessing.data_processor.FOOTBALL_DATA_MATCHES_JSON_IN_PATH')
    @mock.patch('src.data_preprocessing.data_processor.ALL_EVENTS_CSV_IN_PATH')
    @mock.patch('src.data_preprocessing.data_processor.STATSbomb_MATCHES_CSV_IN_PATH')
    @mock.patch('src.data_preprocessing.data_processor.PROCESSED_DATA_DIR')
    @mock.patch('src.data_preprocessing.data_processor.RAW_DATA_DIR')
    def test_data_processor_main_execution(self, 
                                           mock_raw_dir_const, 
                                           mock_processed_dir_const,
                                           mock_statsbomb_matches_in_const,
                                           mock_all_events_in_const,
                                           mock_football_data_in_const,
                                           mock_combined_out_const,
                                           mock_processed_events_out_const):
        # b. Set up temporary directories
        with tempfile.TemporaryDirectory() as temp_base_dir_name:
            raw_dir_path = os.path.join(temp_base_dir_name, 'data', 'raw')
            processed_dir_path = os.path.join(temp_base_dir_name, 'data', 'processed')
            os.makedirs(raw_dir_path, exist_ok=True)
            os.makedirs(processed_dir_path, exist_ok=True)

            # c. Define paths for dummy input files
            dummy_statsbomb_matches_csv = os.path.join(raw_dir_path, 'statsbomb_matches.csv')
            dummy_all_events_csv = os.path.join(raw_dir_path, 'all_events.csv')
            dummy_football_data_json = os.path.join(raw_dir_path, 'football_data_matches.json')
            
            # Define expected output file paths
            expected_combined_csv = os.path.join(processed_dir_path, 'combined_processed_matches.csv')
            expected_events_csv = os.path.join(processed_dir_path, 'processed_statsbomb_events.csv')

            # d. Mock the path constants in src.data_preprocessing.data_processor
            mock_raw_dir_const.return_value = raw_dir_path
            mock_processed_dir_const.return_value = processed_dir_path
            mock_statsbomb_matches_in_const.return_value = dummy_statsbomb_matches_csv
            mock_all_events_in_const.return_value = dummy_all_events_csv
            mock_football_data_in_const.return_value = dummy_football_data_json
            mock_combined_out_const.return_value = expected_combined_csv
            mock_processed_events_out_const.return_value = expected_events_csv
            
            # Create dummy input files
            # Statsbomb matches CSV
            statsbomb_headers = ['match_id', 'match_date', 'kick_off', 'competition', 'season', 'home_team', 'away_team', 'home_score', 'away_score']
            statsbomb_dummy_data = [[1, '2023-01-01', '12:00', 'Test Comp', '2023', 'Team H', 'Team A', 1, 0]]
            pd.DataFrame(statsbomb_dummy_data, columns=statsbomb_headers).to_csv(dummy_statsbomb_matches_csv, index=False)

            # All events CSV
            pd.DataFrame(columns=['event_id', 'match_id', 'event_type']).to_csv(dummy_all_events_csv, index=False)

            # Football data JSON
            football_dummy_json_content = {
                "matches": [{
                    "utcDate": "2023-01-01T12:00:00Z", 
                    "homeTeam": {"name": "Team A"}, 
                    "awayTeam": {"name": "Team B"}
                }]
            }
            with open(dummy_football_data_json, 'w') as f:
                json.dump(football_dummy_json_content, f)

            # e. Run the data processor main function
            data_processor_main()

            # f. Assert output files exist
            self.assertTrue(os.path.exists(expected_combined_csv), 
                            f"Expected combined output file not found: {expected_combined_csv}")
            self.assertTrue(os.path.exists(expected_events_csv),
                            f"Expected processed events output file not found: {expected_events_csv}")

if __name__ == '__main__':
    unittest.main()