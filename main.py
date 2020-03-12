import requests
from selenium import webdriver
from bs4 import BeautifulSoup

TOP3_LEAGUES_URLS = [r"https://www.sofascore.com/tournament/football/italy/serie-a/23",     # base urls of each league
                     r"https://www.sofascore.com/tournament/football/spain/laliga/8",    # can be expand to more leagues
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
    """
    this function fet url of a team and extract all of the players url list out of it.
    then it send the player url to extract player info func to get all info about the player
    :param team_url: a url to a team page as a string
    """
    team_html = BeautifulSoup(requests.get(team_url).text, 'html.parser')  # using bs4 & requests to retrieve html as text
    all_players_html = team_html.find_all("a", class_="squad__player squad-player u-tC js-show-player-modal ff-medium")  # looking for the player info inside the page
    html_list = str(all_players_html).split()       # manipulating the text to extract player links
    for line in html_list:
        if "href" in line:
            print(extract_player_info("https://www.sofascore.com" + line.split("\"")[1]))   # printing player info to the screen


def extract_teams_urls(league_url):
    """
    this function extract teams url out of league home page
    :param league_url: league url as a string
    :return: all teams urlss unique and alphabetically sorted in a list
    """
    team_list = []
    driver = webdriver.Chrome()         # working with selenium google driver as the data is not in the bs4 html
    driver.get(league_url)              # mimicking human behaviour and opening league url
    team_html = BeautifulSoup(driver.page_source, 'html.parser')    # getting the source with selenium, parsing with bs4
    all_teams_html = team_html.find_all("a", class_="js-link")     # looking after all teams urls
    html_list = str(all_teams_html).split()         # splitting the string by spaces
    for line in html_list:
        if "href=\"/team" in line and not line.endswith("img"):  # getting all lines containing links
            team_list.append("https://www.sofascore.com" + line.replace("\"", "").split("=")[-1].split(">")[0])  # appending it to a list
    sorted_teams = sorted(list(set(team_list)))  # sorting and removing duplicates
    return sorted_teams  # returning the list


def main():
    """
    this is main calling function to extract players data out of https://www.sofascore.com
    """
    league_cnt = 1
    all_team_url = []
    for league_url in TOP3_LEAGUES_URLS:        # iterating league links
        print("getting teams from league #" + str(league_cnt))      # printing for user "loading"
        all_team_url += extract_teams_urls(league_url)              # extracting teams out of leagues table
        league_cnt += 1

    for team_url in all_team_url:           # iterating all teams urls
        extract_players_urls(team_url)      # extracting player url which also print to screen player data


if __name__ == '__main__':
    main()
