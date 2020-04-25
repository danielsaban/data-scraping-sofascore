import json
import requests
import config as cfg


def get_info_from_api(team_name):
    """
    getting some additional information about the teams and enriching our database
    thanks to the free API from thesportsdb.com/api.php
    :param team_name: team of the name to download more info to
    :return: a dictionary with some extra info about the team.
    """
    if "-" in team_name:
        team_name = team_name.replace("-", "+")
    if "brighton" in team_name:     # some teams has different names than in sofa-score
        team_name = "brighton"
    if "leicester" in team_name:
        team_name = "leicester"
    if "norwich" in team_name:
        team_name = "norwich"
    if "mallorca" in team_name:
        team_name = "mallorca"
    if "parma" in team_name:
        team_name = "parma+calcio"
    if "bayern" in team_name:
        team_name = "bayern"
    if "koln" in team_name:
        team_name = "fc+koln"
    print(team_name)
    response = requests.get(cfg.API_URL + team_name)
    team_data = json.loads(response.text)
    return team_data['teams'][0]

