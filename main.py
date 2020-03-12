import requests
from selenium import webdriver
from bs4 import BeautifulSoup

TOP3_LEAGUES_URLS = [r"https://www.sofascore.com/tournament/football/italy/serie-a/23",     # Serie A as the first
                     r"https://www.sofascore.com/tournament/football/spain/laliga/8"
                     r"https://www.sofascore.com/tournament/football/england/premier-league/17"]


def extract_player_info(player_url):
    player_html = BeautifulSoup(requests.get(player_url).text, 'html.parser')
    player_panel_html = player_html.find_all("h2", class_="styles__DetailBoxTitle-sc-1ss54tr-5 enIhhc")
    team_name_raw = player_html.find_all("h3", class_="styles__TeamLink-sc-1ss54tr-7 hUZGuP")
    team_name = str(team_name_raw).replace("<", ">").split(">")[-3]
    details = str(player_panel_html).replace("<", ">").split(">")
    player_name = player_url.split("/")[-2]
    det = [player_name, team_name]
    for i in range(len(details)):
        if (r"h2 class=" in details[i] or r"span style" in details[i]) and details[i + 1] != '':
            det.append(details[i + 1])
    return det


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
