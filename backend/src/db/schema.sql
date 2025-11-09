-- Opta Replacement Database Schema
-- PostgreSQL 14+

-- =====================================================
-- CORE ENTITIES
-- =====================================================

-- Leagues
CREATE TABLE IF NOT EXISTS leagues (
    league_id SERIAL PRIMARY KEY,
    league_code VARCHAR(50) UNIQUE NOT NULL,  -- 'EPL', 'LALIGA', 'NBA'
    league_name VARCHAR(200) NOT NULL,
    sport VARCHAR(50) NOT NULL,  -- 'football', 'basketball'
    country VARCHAR(100),
    level INT DEFAULT 1,  -- 1=top tier, 2=second tier, etc.
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Teams
CREATE TABLE IF NOT EXISTS teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(200) NOT NULL,
    team_short_name VARCHAR(100),
    league_id INT REFERENCES leagues(league_id),
    stadium VARCHAR(200),
    founded_year INT,
    manager VARCHAR(200),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Players
CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY,
    player_name VARCHAR(200) NOT NULL,
    full_name VARCHAR(300),
    date_of_birth DATE,
    nationality VARCHAR(100),
    height_cm INT,
    weight_kg INT,
    preferred_foot VARCHAR(20),  -- 'right', 'left', 'both'
    position VARCHAR(50),
    current_team_id INT REFERENCES teams(team_id),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seasons
CREATE TABLE IF NOT EXISTS seasons (
    season_id SERIAL PRIMARY KEY,
    season_name VARCHAR(50) NOT NULL,  -- '2023-2024'
    league_id INT REFERENCES leagues(league_id),
    start_date DATE,
    end_date DATE,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- MATCHES & EVENTS
-- =====================================================

-- Matches
CREATE TABLE IF NOT EXISTS matches (
    match_id SERIAL PRIMARY KEY,
    season_id INT REFERENCES seasons(season_id),
    home_team_id INT REFERENCES teams(team_id),
    away_team_id INT REFERENCES teams(team_id),
    match_date TIMESTAMP NOT NULL,
    venue VARCHAR(200),
    home_score INT,
    away_score INT,
    match_status VARCHAR(50),  -- 'scheduled', 'live', 'finished', 'postponed'
    attendance INT,
    referee VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Match Events (passes, shots, tackles, etc.)
CREATE TABLE IF NOT EXISTS match_events (
    event_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES matches(match_id),
    player_id INT REFERENCES players(player_id),
    team_id INT REFERENCES teams(team_id),
    event_type VARCHAR(50) NOT NULL,  -- 'pass', 'shot', 'tackle', 'foul', 'goal', etc.
    minute INT,
    second INT,
    x_coordinate DECIMAL(10,2),  -- Pitch coordinates
    y_coordinate DECIMAL(10,2),
    end_x DECIMAL(10,2),  -- For passes, shots
    end_y DECIMAL(10,2),
    outcome VARCHAR(50),  -- 'complete', 'incomplete', 'goal', 'saved', etc.
    body_part VARCHAR(50),  -- 'right_foot', 'left_foot', 'head', etc.
    metadata JSONB,  -- Additional event-specific data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_events_match ON match_events(match_id);
CREATE INDEX idx_events_player ON match_events(player_id);
CREATE INDEX idx_events_type ON match_events(event_type);

-- =====================================================
-- PLAYER STATISTICS
-- =====================================================

-- Player Match Stats (per match)
CREATE TABLE IF NOT EXISTS player_match_stats (
    stat_id SERIAL PRIMARY KEY,
    match_id INT REFERENCES matches(match_id),
    player_id INT REFERENCES players(player_id),
    team_id INT REFERENCES teams(team_id),
    minutes_played INT,

    -- Offensive
    goals INT DEFAULT 0,
    assists INT DEFAULT 0,
    shots INT DEFAULT 0,
    shots_on_target INT DEFAULT 0,
    key_passes INT DEFAULT 0,
    dribbles_attempted INT DEFAULT 0,
    dribbles_successful INT DEFAULT 0,

    -- Passing
    passes_attempted INT DEFAULT 0,
    passes_completed INT DEFAULT 0,
    pass_accuracy DECIMAL(5,2),
    progressive_passes INT DEFAULT 0,
    crosses_attempted INT DEFAULT 0,
    crosses_successful INT DEFAULT 0,

    -- Defensive
    tackles INT DEFAULT 0,
    interceptions INT DEFAULT 0,
    clearances INT DEFAULT 0,
    blocks INT DEFAULT 0,
    duels_won INT DEFAULT 0,
    duels_lost INT DEFAULT 0,

    -- Discipline
    fouls_committed INT DEFAULT 0,
    fouls_won INT DEFAULT 0,
    yellow_cards INT DEFAULT 0,
    red_cards INT DEFAULT 0,

    -- Advanced metrics (calculated)
    xg DECIMAL(10,3),  -- Expected goals
    xa DECIMAL(10,3),  -- Expected assists
    opta_index DECIMAL(5,1),  -- Opta performance index

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_player_match_stats_match ON player_match_stats(match_id);
CREATE INDEX idx_player_match_stats_player ON player_match_stats(player_id);

-- Player Season Stats (aggregated)
CREATE TABLE IF NOT EXISTS player_season_stats (
    stat_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    season_id INT REFERENCES seasons(season_id),
    team_id INT REFERENCES teams(team_id),
    matches_played INT,
    minutes_played INT,

    -- Offensive
    goals INT DEFAULT 0,
    assists INT DEFAULT 0,
    shots INT DEFAULT 0,
    shots_on_target INT DEFAULT 0,
    goals_per_90 DECIMAL(10,2),
    assists_per_90 DECIMAL(10,2),

    -- Passing
    passes_attempted INT DEFAULT 0,
    passes_completed INT DEFAULT 0,
    pass_accuracy DECIMAL(5,2),
    progressive_passes INT DEFAULT 0,

    -- Defensive
    tackles INT DEFAULT 0,
    interceptions INT DEFAULT 0,
    clearances INT DEFAULT 0,

    -- Discipline
    yellow_cards INT DEFAULT 0,
    red_cards INT DEFAULT 0,

    -- Advanced metrics
    total_xg DECIMAL(10,2),
    total_xa DECIMAL(10,2),
    average_opta_index DECIMAL(5,1),
    performance_rating VARCHAR(50),  -- 'EXCEPTIONAL', 'EXCELLENT', etc.

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(player_id, season_id)
);

CREATE INDEX idx_player_season_stats_player ON player_season_stats(player_id);
CREATE INDEX idx_player_season_stats_season ON player_season_stats(season_id);

-- =====================================================
-- TEAM STATISTICS
-- =====================================================

-- Team Season Stats
CREATE TABLE IF NOT EXISTS team_season_stats (
    stat_id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(team_id),
    season_id INT REFERENCES seasons(season_id),
    matches_played INT,
    wins INT DEFAULT 0,
    draws INT DEFAULT 0,
    losses INT DEFAULT 0,
    goals_for INT DEFAULT 0,
    goals_against INT DEFAULT 0,
    goal_difference INT DEFAULT 0,
    points INT DEFAULT 0,
    position INT,  -- League position

    -- Advanced metrics
    total_xg DECIMAL(10,2),
    total_xga DECIMAL(10,2),  -- xG against
    ppda DECIMAL(10,2),  -- Passes per defensive action
    possession_avg DECIMAL(5,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(team_id, season_id)
);

-- =====================================================
-- MARKET DATA & VALUATIONS
-- =====================================================

-- Player Market Values
CREATE TABLE IF NOT EXISTS player_market_values (
    value_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    market_value DECIMAL(12,2),  -- In millions
    currency VARCHAR(10) DEFAULT 'EUR',
    valuation_date DATE NOT NULL,
    source VARCHAR(100),  -- 'transfermarkt', 'calculated', etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_market_values_player ON player_market_values(player_id);

-- Transfer History
CREATE TABLE IF NOT EXISTS transfers (
    transfer_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    from_team_id INT REFERENCES teams(team_id),
    to_team_id INT REFERENCES teams(team_id),
    transfer_date DATE NOT NULL,
    transfer_fee DECIMAL(12,2),  -- In millions
    contract_length_years INT,
    loan BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- ANALYTICS & INSIGHTS
-- =====================================================

-- Opta Performance Index History
CREATE TABLE IF NOT EXISTS opta_index_history (
    record_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    match_id INT REFERENCES matches(match_id),
    season_id INT REFERENCES seasons(season_id),
    opta_index DECIMAL(5,1),
    rating VARCHAR(50),  -- 'EXCEPTIONAL', 'EXCELLENT', etc.
    performance_level VARCHAR(50),
    breakdown JSONB,  -- Detailed breakdown scores
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Team Fit Analysis Results
CREATE TABLE IF NOT EXISTS team_fit_analyses (
    analysis_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    target_team_id INT REFERENCES teams(team_id),
    fit_score DECIMAL(5,1),  -- 0-100
    fit_rating VARCHAR(50),  -- 'EXCELLENT_FIT', 'GOOD_FIT', etc.
    recommendation VARCHAR(100),  -- 'STRONG_BUY', 'BUY', etc.
    breakdown JSONB,  -- Detailed fit breakdown
    analysis_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Moneyball Valuations
CREATE TABLE IF NOT EXISTS moneyball_valuations (
    valuation_id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(player_id),
    season_id INT REFERENCES seasons(season_id),
    calculated_value DECIMAL(12,2),  -- Model-calculated value
    market_value DECIMAL(12,2),  -- Actual market value
    value_ratio DECIMAL(10,2),  -- Calculated / Market
    value_category VARCHAR(50),  -- 'UNDERVALUED', 'FAIR', 'OVERVALUED'
    roi_potential DECIMAL(10,2),  -- Potential return on investment
    calculation_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- DATA SOURCE TRACKING
-- =====================================================

-- Data Sources Metadata
CREATE TABLE IF NOT EXISTS data_sources (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) UNIQUE NOT NULL,
    source_type VARCHAR(50),  -- 'api', 'scraper', 'manual'
    reliability_score DECIMAL(3,2),  -- 0-1
    priority INT,  -- Lower = higher priority
    active BOOLEAN DEFAULT true,
    last_sync TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data Collection Log
CREATE TABLE IF NOT EXISTS data_collection_log (
    log_id SERIAL PRIMARY KEY,
    source_id INT REFERENCES data_sources(source_id),
    collection_type VARCHAR(100),  -- 'player_stats', 'match_events', etc.
    records_collected INT,
    success BOOLEAN,
    error_message TEXT,
    collection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Player Full Profile View
CREATE OR REPLACE VIEW player_profiles AS
SELECT
    p.player_id,
    p.player_name,
    p.date_of_birth,
    EXTRACT(YEAR FROM AGE(p.date_of_birth)) as age,
    p.nationality,
    p.position,
    p.height_cm,
    p.weight_kg,
    t.team_name as current_team,
    l.league_name as current_league,
    pss.average_opta_index,
    pss.goals as season_goals,
    pss.assists as season_assists,
    pmv.market_value as current_market_value
FROM players p
LEFT JOIN teams t ON p.current_team_id = t.team_id
LEFT JOIN leagues l ON t.league_id = l.league_id
LEFT JOIN player_season_stats pss ON p.player_id = pss.player_id
    AND pss.season_id = (SELECT MAX(season_id) FROM seasons WHERE active = true)
LEFT JOIN LATERAL (
    SELECT market_value
    FROM player_market_values
    WHERE player_id = p.player_id
    ORDER BY valuation_date DESC
    LIMIT 1
) pmv ON true;

-- League Standings View
CREATE OR REPLACE VIEW league_standings AS
SELECT
    s.season_id,
    l.league_name,
    s.season_name,
    t.team_name,
    tss.position,
    tss.matches_played,
    tss.wins,
    tss.draws,
    tss.losses,
    tss.goals_for,
    tss.goals_against,
    tss.goal_difference,
    tss.points,
    tss.total_xg,
    tss.total_xga
FROM team_season_stats tss
JOIN teams t ON tss.team_id = t.team_id
JOIN seasons s ON tss.season_id = s.season_id
JOIN leagues l ON s.league_id = l.league_id
ORDER BY s.season_id DESC, tss.position ASC;

-- Top Performers View
CREATE OR REPLACE VIEW top_performers AS
SELECT
    p.player_name,
    t.team_name,
    l.league_name,
    s.season_name,
    pss.goals,
    pss.assists,
    pss.average_opta_index,
    pss.performance_rating
FROM player_season_stats pss
JOIN players p ON pss.player_id = p.player_id
JOIN seasons s ON pss.season_id = s.season_id
JOIN teams t ON pss.team_id = t.team_id
JOIN leagues l ON s.league_id = l.league_id
WHERE s.active = true
ORDER BY pss.average_opta_index DESC;

-- =====================================================
-- FUNCTIONS & TRIGGERS
-- =====================================================

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update trigger to relevant tables
CREATE TRIGGER update_leagues_updated_at BEFORE UPDATE ON leagues
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_teams_updated_at BEFORE UPDATE ON teams
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_players_updated_at BEFORE UPDATE ON players
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_matches_updated_at BEFORE UPDATE ON matches
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- INITIAL DATA
-- =====================================================

-- Insert default data sources
INSERT INTO data_sources (source_name, source_type, reliability_score, priority) VALUES
    ('StatsBomb', 'api', 0.95, 1),
    ('Understat', 'scraper', 0.90, 2),
    ('FBref', 'scraper', 0.85, 3),
    ('Transfermarkt', 'scraper', 0.80, 4),
    ('TheSportsDB', 'api', 0.70, 5)
ON CONFLICT (source_name) DO NOTHING;

-- Insert major football leagues
INSERT INTO leagues (league_code, league_name, sport, country, level) VALUES
    ('EPL', 'English Premier League', 'football', 'England', 1),
    ('LALIGA', 'La Liga', 'football', 'Spain', 1),
    ('BUNDESLIGA', 'Bundesliga', 'football', 'Germany', 1),
    ('SERIEA', 'Serie A', 'football', 'Italy', 1),
    ('LIGUE1', 'Ligue 1', 'football', 'France', 1),
    ('UEFA_CHAMPIONS_LEAGUE', 'UEFA Champions League', 'football', 'Europe', 1),
    ('NBA', 'National Basketball Association', 'basketball', 'USA', 1)
ON CONFLICT (league_code) DO NOTHING;

COMMENT ON TABLE players IS 'Core player information';
COMMENT ON TABLE player_match_stats IS 'Detailed statistics for each player in each match';
COMMENT ON TABLE match_events IS 'Event-level data (passes, shots, tackles) - Opta equivalent';
COMMENT ON TABLE opta_index_history IS 'Historical Opta Performance Index values';
COMMENT ON TABLE team_fit_analyses IS 'Team fit analysis results - unique feature';
COMMENT ON TABLE moneyball_valuations IS 'Moneyball-style player valuations - unique feature';
