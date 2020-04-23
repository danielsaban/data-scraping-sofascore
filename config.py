DB_NAME = "sofa_score"
PASSWD = "Sofa_Score_2020"
USERNAME = "Sagi"
HOST = "localhost"

API_URL = r"https://www.thesportsdb.com/api/v1/json/1/searchteams.php?t="

POSSIBLE_FOOT = ['Right', 'Left', 'Both']
POSSIBLE_POSITION = ['G', 'D', 'M', 'F']
PLAYER_FIELDS = ['birth_date', 'height', 'prefd_foot', 'position',
                 'shirt_num', 'market_val_million_euro', 'nationality']
# MANAGER_FIELDS = ['birth_date', 'nationality', 'pref_formation', 'avg_points_per_game',
#                   'games_won', 'games_drawn', 'games_lost']


TOP3_LEAGUES_URLS = {"seriea": r"https://www.sofascore.com/tournament/football/italy/serie-a/23",
                     "laliga": r"https://www.sofascore.com/tournament/football/spain/laliga/8",
                     "premier": r"https://www.sofascore.com/tournament/football/england/premier-league/17"}
