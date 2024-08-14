import unittest
from src.analysis.live_match_analysis import analyze_live_match
from src.analysis.player_trend_analysis import analyze_player_trend
from src.analysis.match_prediction import match_prediction

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

if __name__ == '__main__':
    unittest.main()