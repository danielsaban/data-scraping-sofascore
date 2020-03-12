import requests
from selenium import webdriver
from bs4 import BeautifulSoup

TOP3_LEAGUES_URLS = [r"https://www.sofascore.com/tournament/football/italy/serie-a/23",
                     r"https://www.sofascore.com/tournament/football/spain/laliga/8"
                     r"https://www.sofascore.com/tournament/football/england/premier-league/17"]


def extract_player_info(player_url):
    """
    Starting from the url of a player's page on https://www.sofascore.com, the function extracts
    the most interesting infos about him, if available, and returns them in a list.
    :param player_url: url of the player on https://www.sofascore.com site.
    :return: list ordered in the following way: [Name, Team, Nationality, Age, Height, Preferred Foot, Position, Shirt Number, Market Value]
    """
    player_html = BeautifulSoup(requests.get(player_url).text, 'html.parser')       # beautifulsoup of the player
    player_panel_html = player_html.find_all("h2", class_="styles__DetailBoxTitle-sc-1ss54tr-5 enIhhc")     # html of the most interesting data
    team_name_raw = player_html.find_all("h3", class_="styles__TeamLink-sc-1ss54tr-7 hUZGuP")
    team_name = str(team_name_raw).replace("<", ">").split(">")[-3]     # name of the team the player plays in
    details = str(player_panel_html).replace("<", ">").split(">")
    raw_nationality = player_html.find_all("span", class_="u-pL8")
    nationality = str(raw_nationality).replace("<", ">").split(">")[-3]
    player_name = player_url.split("/")[-2]
    player_data = [player_name, team_name, nationality]      # initiating player's data list
    for i in range(len(details)):
        if (r"h2 class=" in details[i] or r"span style" in details[i]) and details[i + 1] != '':        # adding data to the list
            player_data.append(details[i + 1])
    return player_data


def extract_players_urls(team_url):
    # TODO: fill docstring
    """
    :param team_url:
    :return:
    """
    team_html = BeautifulSoup(requests.get(team_url).text, 'html.parser')
    all_players_html = team_html.find_all("a", class_="squad__player squad-player u-tC js-show-player-modal ff-medium")
    html_list = str(all_players_html).split()
    for line in html_list:
        if "href" in line:
            print(extract_player_info("https://www.sofascore.com" + line.split("\"")[1]))


def extract_teams_urls(league_url):
    team_list = []
    driver = webdriver.Chrome()
    driver.get(league_url)
    team_html = BeautifulSoup(driver.page_source, 'html.parser')
    all_teams_html = team_html.find_all("a", class_="js-link")
    html_list = str(all_teams_html).split()
    for line in html_list:
        if "href=\"/team" in line and not line.endswith("img"):
            team_list.append("https://www.sofascore.com" + line.replace("\"", "").split("=")[-1].split(">")[0])
    sorted_teams = sorted(list(set(team_list)))
    return sorted_teams


def main():
    league_cnt = 1
    all_team_url = []
    for league_url in TOP3_LEAGUES_URLS:
        print("getting teams from league #" + str(league_cnt))
        all_team_url += extract_teams_urls(league_url)
        league_cnt += 1

    for team_url in all_team_url:
        extract_players_urls(team_url)


if __name__ == '__main__':
    main()
