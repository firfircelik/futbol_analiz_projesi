import psycopg2

def create_tables():
    commands = [
        """
        CREATE TABLE IF NOT EXISTS matches (
            match_id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            team_home VARCHAR(255),
            team_away VARCHAR(255),
            goals_home INT,
            goals_away INT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS players (
            player_id SERIAL PRIMARY KEY,
            player_name VARCHAR(255),
            team_name VARCHAR(255),
            position VARCHAR(50)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS events (
            event_id SERIAL PRIMARY KEY,
            match_id INT REFERENCES matches(match_id),
            player_id INT REFERENCES players(player_id),
            event_type VARCHAR(50),
            minute INT,
            x_coordinate FLOAT,
            y_coordinate FLOAT
        )
        """
    ]
    
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="football_db", user="youruser", password="yourpassword"
        )
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()