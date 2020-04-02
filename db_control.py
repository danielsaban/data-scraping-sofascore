import mysql.connector
from config import DB_NAME


def connector():
    return mysql.connector.connect(
        host="localhost",
        user="Sagi",
        password="Eilat2012",
        database=DB_NAME
    )


def create():
    my_db = mysql.connector.connect(
        host="localhost",
        user="Sagi",
        password="Eilat2012",
    )
    cur = my_db.cursor()
    cur.execute('''CREATE DATABASE IF NOT EXISTS ''' + DB_NAME)

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
                        mngr_name CHAR NOT NULL,
                        age INT,
                        nationality CHAR,
                        pref_formation CHAR,
                        avg_points_per_game REAL,
                        games_won INT,
                        games_drawn INT,
                        games_lost INT,
                        FOREIGN KEY (team_id) REFERENCES teams(team_id))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS players (
                        player_id INT PRIMARY KEY AUTO_INCREMENT,
                        team_id INT,
                        player_name CHAR NOT NULL,
                        nationality CHAR,
                        age INT,
                        height_cm INT,
                        prefd_foot CHAR,
                        position CHAR,
                        shirt_num INT,
                        market_val_million_euro REAL,
                        FOREIGN KEY (team_id) REFERENCES teams(team_id))''')
    cur.close()


def write_league(league_info):
    my_db = connector()
    cur = my_db.cursor()
    cur.execute("INSERT INTO leagues (league_name, number_of_teams) VALUES (%s, %s)"
                "ON DUPLICATE KEY UPDATE league_name=league_name",
                (league_info[0], league_info[1]))
    my_db.commit()
    cur.close()


def write_teams(teams_info, lg_name):
    my_db = connector()
    cur = my_db.cursor()
    cur.execute("INSERT INTO teams (team_name, number_of_players, league_id) VALUES "
                "(%s, %s, (SELECT league_id FROM leagues WHERE league_name='"+lg_name+"'))"
                """ON DUPLICATE KEY UPDATE team_name=team_name""",
                (teams_info[0], teams_info[1]))
    my_db.commit()
    cur.close()


def write_players(players_info, team_n):
    my_db = connector()
    cur = my_db.cursor()
    for player in players_info:
        cur.execute("INSERT INTO players (team_id, player_name, nationality, age, height_cm, prefd_foot,"
                    "position, shirt_num)"
                    "VALUES ((SELECT team_id FORM teams WHERE team_name='"+team_n+"' LIMIT 1),%s, %s, %s, %s, %s, %s, %s)",
                    [player[0], player[1], int(player[2]), int(player[3].split()[0]),
                     player[4], player[5], int(player[6])])
    my_db.commit()
    cur.close()
