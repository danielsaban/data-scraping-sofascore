import mysql.connector
import config as cfg


def connector():
    """
    creating a connector to an existing db
    :return: return the valid connector
    """
    return mysql.connector.connect(
        host=cfg.HOST,
        user=cfg.USERNAME,
        password=cfg.PASSWD,
        database=cfg.DB_NAME
    )


def create():
    """
    creating an MySQL database
    """
    my_db = mysql.connector.connect(
        host=cfg.HOST,
        user=cfg.USERNAME,
        password=cfg.PASSWD,
    )
    cur = my_db.cursor()
    cur.execute('''CREATE DATABASE IF NOT EXISTS ''' + cfg.DB_NAME)

    my_db = connector()
    cur = my_db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS leagues (
                        league_id INT PRIMARY KEY AUTO_INCREMENT,
                        league_name VARCHAR(255) NOT NULL UNIQUE,
                        number_of_teams INT NOT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS teams (
                        team_id INT PRIMARY KEY AUTO_INCREMENT,
                        league_id INT,
                        team_name VARCHAR(255) NOT NULL UNIQUE,
                        number_of_players INT,
                        FOREIGN KEY (league_id) REFERENCES leagues(league_id))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS managers (
                        manager_id INT PRIMARY KEY AUTO_INCREMENT,
                        team_id INT,
                        mngr_name VARCHAR(255) NOT NULL,
                        age INT,
                        nationality VARCHAR(255),
                        pref_formation VARCHAR(255),
                        avg_points_per_game REAL,
                        games_won INT,
                        games_drawn INT,
                        games_lost INT,
                        FOREIGN KEY (team_id) REFERENCES teams(team_id))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS players (
                        player_id INT PRIMARY KEY AUTO_INCREMENT,
                        team_id INT,
                        player_name VARCHAR(255) NOT NULL,
                        nationality VARCHAR(255),
                        birth_date DATETIME,
                        height_cm INT,
                        prefd_foot VARCHAR(255),
                        position VARCHAR(255),
                        shirt_num INT,
                        market_val_million_euro REAL,
                        FOREIGN KEY (team_id) REFERENCES teams(team_id))''')
    cur.close()


def write_league(league_info):
    """
    writing the league info to the database
    :param league_info: a list with the league name and the number of teams in this league
    """
    my_db = connector()
    cur = my_db.cursor()
    cur.execute("INSERT INTO leagues (league_name, number_of_teams) VALUES (%s, %s)"
                "ON DUPLICATE KEY UPDATE league_name=league_name",
                (league_info[0], league_info[1]))
    my_db.commit()
    cur.close()


def write_teams(teams_info, lg_name):
    """
    writing a team info to the database
    :param teams_info: the team name, number of players in the team
    :param lg_name: the league which the teams belong to - foreign key
    """
    my_db = connector()
    cur = my_db.cursor()
    cur.execute("INSERT INTO teams (team_name, number_of_players, league_id) VALUES "
                "(%s, %s, (SELECT league_id FROM leagues WHERE league_name='"+lg_name+"'))"
                """ON DUPLICATE KEY UPDATE team_id=team_id""",
                (teams_info[0], teams_info[1]))
    my_db.commit()
    cur.close()


def write_players(players_info, team_n):
    """
    writing a list of players to the database
    :param players_info: a list of dictionaries, each dict stands for a player with several data fields.
    :param team_n: the name of the team which the players belong to
    """
    my_db = connector()
    cur = my_db.cursor()
    for player in players_info:
        cur.execute("INSERT INTO players (team_id, player_name, nationality, birth_date, height_cm, prefd_foot,"
                    "position, shirt_num, market_val_million_euro)"
                    "VALUES ((SELECT team_id FROM teams WHERE team_name='"+team_n+"' LIMIT 1),%s, %s, %s, %s, %s, %s, %s, %s)"
                    "ON DUPLICATE KEY UPDATE player_id=player_id",
                    (player['name'], player['nationality'], player['birth_date'], player['height'],
                     player['prefd_foot'], player['position'], player['shirt_num'], player['market_val_million_euro']))
    my_db.commit()
    cur.close()


def check_and_delete(league_name):
    """
    this function checks if the league already exists in the database, if so deletes it.
    :param league_name: getting the league name from user
    """
    my_db = connector()
    cur = my_db.cursor()
    cur.execute("SELECT league_id FROM leagues WHERE league_name ='"+league_name+"'")
    league_id = cur.fetchall()
    if len(league_id) != 0:
        cur.execute("SELECT team_id FROM teams WHERE league_id="+str(league_id[0][0]))
        team_ids = cur.fetchall()
        if len(team_ids) > 0:
            for team_id in team_ids:
                cur.execute("DELETE FROM players WHERE team_id = "+str(team_id[0]))
                my_db.commit()
            cur.execute("DELETE FROM teams WHERE league_id = "+str(league_id[0][0]))
            my_db.commit()
        cur.execute("DELETE FROM leagues WHERE league_id = "+str(league_id[0][0]))
        my_db.commit()
