import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium.webdriver.chrome.options import Options
import config as cfg

arrow_manipu = lambda x: x.replace("<", ">").split(">")


def extract_player_info(player_url):
    """
    Starting from the url of a player's page on https://www.sofascore.com, the function extracts
    the most interesting infos about him, if available, and returns them in a dict.
    :param player_url: url of the player on https://www.sofascore.com site.
    :return: dict with this keys: [Name, Nationality, birth-date, Height, Preferred Foot, Position, Shirt Number, Market Value]
    """
    player_dict = {}
    # beautiful_soup of the player
    player_html = BeautifulSoup(requests.get(player_url).text, 'html.parser')
    # html of the most interesting data
    player_panel_html = player_html.find_all("h2", class_="styles__DetailBoxTitle-sc-1ss54tr-5 enIhhc")
    details = arrow_manipu(str(player_panel_html))
    player_fields_html = player_html.find_all("div", class_="styles__DetailBoxContent-sc-1ss54tr-6 iAORZR")
    fields_list = arrow_manipu(str(player_fields_html))

    player_dict['name'] = player_url.split("/")[-2].replace('-', ' ').title()
    if "Nationality" in fields_list:
        raw_nationality = player_html.find_all("span", class_="u-pL8")
        player_dict['nationality'] = arrow_manipu(str(raw_nationality))[-3]
    for field in fields_list:
        try:
            b_day = parse(field, fuzzy=False)
            player_dict['birth_date'] = b_day
        except ValueError:
            continue
    for i in range(len(details)):
        is_a_detail = (r"h2 class=" in details[i] or r"span style" in details[i]) and details[i + 1] != ''
        if is_a_detail:
            if 'cm' in details[i + 1]:
                player_dict['height'] = int(details[i + 1].split()[0])
            elif '€' in details[i + 1]:
                player_dict['market_val_million_euro'] = details[i + 1].split()[0]
                if 'M' in player_dict['market_val_million_euro']:
                    player_dict['market_val_million_euro'] = float(player_dict['market_val_million_euro'][:-1])
                else:
                    player_dict['market_val_million_euro'] = float(player_dict['market_val_million_euro'][:-1]) / 1000
            elif details[i + 1] in cfg.POSSIBLE_FOOT:
                player_dict['prefd_foot'] = details[i + 1]
            elif details[i + 1] in cfg.POSSIBLE_POSITION:
                player_dict['position'] = details[i + 1]
            elif "Shirt number" in fields_list:
                player_dict['shirt_num'] = int(details[i + 1])

    for key in cfg.PLAYER_FIELDS:
        if key not in player_dict.keys():
            player_dict[key] = None
    return player_dict


def extract_players_urls(team_url):
    """
    this function fet url of a team and extract all of the players url list out of it.
    then it send the player url to extract player info func to get all info about the player
    :param team_url: a url to a team page as a string
    """
    players_list = []
    # using bs4 & requests to retrieve html as text
    team_html = BeautifulSoup(requests.get(team_url).text, 'html.parser')
    # looking for the player info inside the page
    all_players_html = team_html.find_all("a", class_="squad__player squad-player u-tC js-show-player-modal ff-medium")
    # manipulating the text to extract player links
    html_list = str(all_players_html).split()
    for line in html_list:
        if "href" in line:
            players_list.append(extract_player_info("https://www.sofascore.com" + line.split("\"")[1]))
    return players_list


def extract_mgr_url(team_url):
    mgr_link = ""
    soup = BeautifulSoup(requests.get(team_url).text, 'html.parser')
    mgr_html = soup.find('td', class_="ff-medium")
    for line in str(mgr_html).split():
        if "href" in line:
            mgr_link = "https://www.sofascore.com" + line.split("\"")[1]
    return mgr_link


def extract_mgr_info(manager_url):
    """
    this function gets a manager url and extract all desired data from the source html
    :param manager_url: a manger url
    :return: a dictionary that contains all the dat about a manager.
    """
    mgr_dict = {}
    mgr_soup = BeautifulSoup(requests.get(extract_mgr_url(manager_url)).text, 'html.parser')
    mgr_dict['name'] = mgr_soup.find('div', class_="Content-sc-1o55eay-0 gYsVZh u-fs25 fw-medium").get_text()
    mgr_dict['nationality'] = mgr_soup.find('span', style="padding-left:6px").get_text()
    field_list = arrow_manipu(str(mgr_soup.find_all('div', class_="Content-sc-1o55eay-0 gYsVZh u-txt-2")))
    for field in field_list:
        try:
            b_day = parse(field, fuzzy=False)
            mgr_dict['birth_date'] = b_day
        except ValueError:
            continue
    values_list = arrow_manipu(str(mgr_soup.find_all('div', class_="Content-sc-1o55eay-0 gYsVZh u-fs21 fw-medium")))
    mgr_dict['pref_formation'] = values_list[12]
    mgr_dict['avg_points_per_game'] = values_list[20]
    mgr_dict['games_won'] = mgr_soup.find('div', class_="Section-sc-1a7xrsb-0 dPyKtM u-txt-green").get_text()
    mgr_dict['games_drawn'] = mgr_soup.find('div', class_="Section-sc-1a7xrsb-0 dPyKtM u-txt-2").get_text()
    mgr_dict['games_lost'] = mgr_soup.find('div', class_="Section-sc-1a7xrsb-0 dPyKtM u-txt-red").get_text()

    return mgr_dict


def extract_teams_urls(league_url):
    """
    this function extract teams url out of league home page
    :param league_url: league url as a string
    :return: all teams urlss unique and alphabetically sorted in a list
    """
    team_list = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        options=chrome_options)  # working with selenium google driver as the data is not in the bs4 html
    driver.get(league_url)  # mimicking human behaviour and opening league url
    team_html = BeautifulSoup(driver.page_source, 'html.parser')  # getting the source with selenium, parsing with bs4
    driver.close()
    # looking after all teams urls
    all_teams_html = team_html.find_all("div", class_="Content-sc-1o55eay-0 gYsVZh u-pL8 fw-medium")
    html_list = str(all_teams_html).split()  # splitting the string by spaces
    for line in html_list:
        is_line_with_link = "href=\"/team" in line and not line.endswith("img")
        if is_line_with_link:
            # appending it to a list
            team_list.append("https://www.sofascore.com" + line.replace("\"", "").split("=")[-1].split(">")[0])
    sorted_teams = sorted(list(set(team_list)))  # sorting and removing duplicates
    return sorted_teams
