"""
Free API Configuration for Multi-Sport Analytics
Uses only free endpoints - no API keys required for most features
"""

# Free API Endpoints

FREE_APIS = {
    'football': {
        'thesportsdb': {
            'base_url': 'https://www.thesportsdb.com/api/v1/json/3',
            'endpoints': {
                'leagues': '/all_leagues.php',
                'teams': '/lookup_all_teams.php?id={league_id}',
                'fixtures': '/eventsnextleague.php?id={league_id}',
                'results': '/eventspastleague.php?id={league_id}',
                'standings': '/lookuptable.php?l={league_id}&s={season}',
                'team_details': '/lookupteam.php?id={team_id}',
                'player': '/lookupplayer.php?id={player_id}',
                'team_players': '/lookup_all_players.php?id={team_id}',
                'live_scores': '/livescore.php?l={league_id}',
            },
            'requires_key': False,
            'rate_limit': '1 request per 2 seconds',
        },
        'api_football': {
            'base_url': 'https://v3.football.api-sports.io',
            'endpoints': {
                'leagues': '/leagues',
                'teams': '/teams',
                'fixtures': '/fixtures',
                'standings': '/standings',
                'players': '/players',
                'live': '/fixtures?live=all',
            },
            'requires_key': True,
            'free_tier': '100 requests/day',
        },
    },
    'basketball': {
        'thesportsdb': {
            'base_url': 'https://www.thesportsdb.com/api/v1/json/3',
            'endpoints': {
                'leagues': '/all_leagues.php',
                'teams': '/lookup_all_teams.php?id={league_id}',
                'fixtures': '/eventsnextleague.php?id={league_id}',
                'results': '/eventspastleague.php?id={league_id}',
                'standings': '/lookuptable.php?l={league_id}&s={season}',
                'live_scores': '/livescore.php?l={league_id}',
            },
            'requires_key': False,
            'rate_limit': '1 request per 2 seconds',
        },
        'balldontlie': {
            'base_url': 'https://www.balldontlie.io/api/v1',
            'endpoints': {
                'teams': '/teams',
                'players': '/players',
                'games': '/games',
                'stats': '/stats',
                'season_averages': '/season_averages',
            },
            'requires_key': False,
            'note': 'NBA data only',
        },
        'nba_api_free': {
            'base_url': 'https://data.nba.net/prod/v1',
            'endpoints': {
                'scoreboard': '/{date}/scoreboard.json',
                'standings': '/current/standings_all.json',
                'team_roster': '/{season}/teams/{team}/roster.json',
            },
            'requires_key': False,
            'note': 'Official NBA data feed',
        },
    }
}

# League IDs for TheSportsDB
THESPORTSDB_LEAGUE_IDS = {
    'football': {
        'EPL': '4328',           # English Premier League
        'LALIGA': '4335',        # La Liga
        'BUNDESLIGA': '4331',    # Bundesliga
        'SERIEA': '4332',        # Serie A
        'LIGUE1': '4334',        # Ligue 1
        'EREDIVISIE': '4337',    # Eredivisie
        'PRIMEIRALIGA': '4344',  # Primeira Liga
        'BRASILEIRAO': '4351',   # Brasileirão
        'MLS': '4346',           # MLS
        'CHAMPIONSHIP': '4329',  # Championship
    },
    'basketball': {
        'NBA': '4387',           # NBA
        'EUROLEAGUE': '4427',    # EuroLeague
        'SPANISH_ACB': '4424',   # Liga ACB
        'TURKISH_BSL': '4425',   # Turkish BSL
        'GREEK_BASKET': '4428',  # Greek Basket
    }
}

# API-Football League IDs (if user has API key)
API_FOOTBALL_LEAGUE_IDS = {
    'EPL': 39,
    'LALIGA': 140,
    'BUNDESLIGA': 78,
    'SERIEA': 135,
    'LIGUE1': 61,
}
