import mysql.connector
import config as cfg
import unicodedata


def connector():
    """
    creating a connector to an existing db
    :return: return the valid connector
    """
    return mysql.connector.connect(
        host=cfg.HOST,
        user=cfg.USERNAME,
        password=cfg.PASSWD,
        database=cfg.DB_NAME,
        charset='utf8mb4',
        use_unicode=True
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
                        manager_name VARCHAR(255) NOT NULL,
                        birth_date DATETIME,
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
                        FOREIGN KEY (team_id) REFERENCES teams(team_id))''')
    cur.execute('''CREATE TABLE IF NOT EXISTS teams_extras (
                        id_Team INT PRIMARY KEY,
                        team_id INT,
                        team_name VARCHAR(45) NOT NULL,
                        team_name_short VARCHAR(45),
                        alternate_team_name VARCHAR(255),
                        formed_year INT,
                        stadium_name VARCHAR(45),
                        stadium_pic_url VARCHAR(255),
                        stadium_description LONGTEXT,
                        stadium_location VARCHAR(255),
                        stadium_capacity INT,
                        team_website VARCHAR(255),
                        team_facebook VARCHAR(255),
                        team_twitter VARCHAR(255),
                        team_instagram VARCHAR(255),
                        team_description LONGTEXT,
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
                "ON DUPLICATE KEY UPDATE league_id=league_id",
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
                    "position, shirt_num)"
                    "VALUES ((SELECT team_id FROM teams WHERE team_name='"+team_n+"' LIMIT 1),%s, %s, %s, %s, %s, %s, %s)"
                    "ON DUPLICATE KEY UPDATE player_id=player_id",
                    (player['name'], player['nationality'], player['birth_date'], player['height'],
                     player['prefd_foot'], player['position'], player['shirt_num']))
    my_db.commit()
    cur.close()


def write_manager(mgr_info, team_n):
    """
    writing a manager to the database
    :param mgr_info: a dictionary, that represent a manger with several data fields.
    :param team_n: the name of the team which the manager belong to
    """
    my_db = connector()
    cur = my_db.cursor()
    cur.execute("INSERT INTO managers (team_id, manager_name, birth_date, nationality, pref_formation,"
                "avg_points_per_game, games_won, games_drawn, games_lost)"
                "VALUES ((SELECT team_id FROM teams WHERE team_name='"+team_n+"' LIMIT 1),%s, %s, %s, %s, %s, %s, %s, %s)"
                "ON DUPLICATE KEY UPDATE manager_id=manager_id",
                (unicodedata.normalize('NFD', mgr_info['name']).encode('ascii', 'ignore')), mgr_info['birth_date'], mgr_info['nationality'], mgr_info['pref_formation'],
                mgr_info['avg_points_per_game'], mgr_info['games_won'], mgr_info['games_drawn'], mgr_info['games_lost'])
    my_db.commit()
    cur.close()


def write_team_extras(team_info, team_n):
    """
    writing an additional information about each team from an external API - thesportsdb.com/api.php
    :param team_info: a dictionary with the desired external data
    :param team_n: team name that the external data is belong to
    """
    my_db = connector()
    cur = my_db.cursor()
    cur.execute("INSERT INTO teams_extras (team_id, id_Team, team_name, team_name_short, alternate_team_name,"
                "formed_year, stadium_name, stadium_pic_url, stadium_description, stadium_location, stadium_capacity,"
                "team_website, team_facebook, team_twitter, team_instagram, team_description)"
                "VALUES ((SELECT team_id FROM teams WHERE team_name='"+team_n+"' LIMIT 1), %s, %s, %s, %s, %s, %s, %s,"
                "%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE id_Team = id_Team",
                (team_info['idTeam'], team_info['strTeam'], team_info['strTeamShort'], team_info['strAlternate'],
                 team_info['intFormedYear'], team_info['strStadium'], team_info['strStadiumThumb'],
                 team_info['strStadiumDescription'], team_info['strStadiumLocation'], team_info['intStadiumCapacity'],
                 team_info['strWebsite'], team_info['strFacebook'], team_info['strTwitter'], team_info['strInstagram'],
                 team_info['strDescriptionEN']))
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
                cur.execute("DELETE FROM managers WHERE team_id = "+str(team_id[0]))
                cur.execute("DELETE FROM teams_extras WHERE team_id = "+str(team_id[0]))
                my_db.commit()
            cur.execute("DELETE FROM teams WHERE league_id = "+str(league_id[0][0]))
            my_db.commit()
        cur.execute("DELETE FROM leagues WHERE league_id = "+str(league_id[0][0]))
        my_db.commit()
