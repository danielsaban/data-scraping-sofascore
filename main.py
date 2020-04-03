import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from dateutil.parser import parse
import db_control
from tqdm import tqdm

TOP3_LEAGUES_URLS = [r"https://www.sofascore.com/tournament/football/italy/serie-a/23",     # base urls of each league
                     r"https://www.sofascore.com/tournament/football/spain/laliga/8",    # can be expand to more leagues
                     r"https://www.sofascore.com/tournament/football/england/premier-league/17"]


def extract_player_info(player_url):
    """
    Starting from the url of a player's page on https://www.sofascore.com, the function extracts
    the most interesting infos about him, if available, and returns them in a list.
    :param player_url: url of the player on https://www.sofascore.com site.
    :return: list ordered in the following way: [Name, Team, Nationality, Age, Height, Preferred Foot, Position, Shirt Number, Market Value]
    """
    player_dict = {}
    player_html = BeautifulSoup(requests.get(player_url).text, 'html.parser')  # beautifulsoup of the player
    player_panel_html = player_html.find_all("h2",
                                             class_="styles__DetailBoxTitle-sc-1ss54tr-5 enIhhc")  # html of the most interesting data
    details = str(player_panel_html).replace("<", ">").split(">")
    player_fields_html = player_html.find_all("div", class_="styles__DetailBoxContent-sc-1ss54tr-6 iAORZR")
    fields_list = str(player_fields_html).replace("<", ">").split(">")

    player_dict['name'] = player_url.split("/")[-2].replace('-', ' ').title()
    if "Nationality" in fields_list:
        raw_nationality = player_html.find_all("span", class_="u-pL8")
        player_dict['nationality'] = str(raw_nationality).replace("<", ">").split(">")[-3]
    for field in fields_list:
        try:
            b_day = parse(field, fuzzy=False)
            player_dict['birth_date'] = b_day
        except ValueError:
            continue
    for i in range(len(details)):
        if (r"h2 class=" in details[i] or r"span style" in details[i]) and details[i + 1] != '':  # adding data to the list
            if 'cm' in details[i + 1]:
                player_dict['height'] = int(details[i + 1].split()[0])
            elif '€' in details[i + 1]:
                player_dict['market_val_million_euro'] = details[i + 1].split()[0]
                if 'M' in player_dict['market_val_million_euro']:
                    player_dict['market_val_million_euro'] = float(player_dict['market_val_million_euro'][: -1])
                else:
                    player_dict['market_val_million_euro'] = float(player_dict['market_val_million_euro'][: -1]) / 1000
            elif details[i + 1] in ['Right', 'Left', 'Both']:
                player_dict['prefd_foot'] = details[i + 1]
            elif details[i + 1] in ['G', 'D', 'M', 'F']:
                player_dict['position'] = details[i + 1]
            elif "Shirt number" in fields_list:
                player_dict['shirt_num'] = int(details[i + 1])

    dang_keys = ['birth_date', 'height', 'prefd_foot', 'position', 'shirt_num', 'market_val_million_euro', 'nationality']
    for key in dang_keys:
        if key not in player_dict.keys():
            player_dict[key] = None
    return player_dict


def extract_players_urls(team_url):
    """
    this function fet url of a team and extract all of the players url list out of it.
    then it send the player url to extract player info func to get all info about the player
    :param team_url: a url to a team page as a string
    """
    player_count = 0
    players_list = []
    team_html = BeautifulSoup(requests.get(team_url).text,
                              'html.parser')  # using bs4 & requests to retrieve html as text
    all_players_html = team_html.find_all("a",
                                          class_="squad__player squad-player u-tC js-show-player-modal ff-medium")  # looking for the player info inside the page
    html_list = str(all_players_html).split()  # manipulating the text to extract player links
    for line in html_list:
        if "href" in line:
            player_count += 1
            players_list.append(extract_player_info("https://www.sofascore.com" + line.split("\"")[1]))
    return player_count, players_list


def extract_teams_urls(league_url):
    """
    this function extract teams url out of league home page
    :param league_url: league url as a string
    :return: all teams urlss unique and alphabetically sorted in a list
    """
    team_list = []
    driver = webdriver.Chrome()  # working with selenium google driver as the data is not in the bs4 html
    driver.get(league_url)  # mimicking human behaviour and opening league url
    team_html = BeautifulSoup(driver.page_source, 'html.parser')  # getting the source with selenium, parsing with bs4
    all_teams_html = team_html.find_all("a", class_="js-link")  # looking after all teams urls
    html_list = str(all_teams_html).split()  # splitting the string by spaces
    for line in html_list:
        if "href=\"/team" in line and not line.endswith("img"):  # getting all lines containing links
            team_list.append("https://www.sofascore.com" + line.replace("\"", "").split("=")[-1].split(">")[
                0])  # appending it to a list
    sorted_teams = sorted(list(set(team_list)))  # sorting and removing duplicates
    return sorted_teams  # returning the list


def main():
    """
    this is main calling function to extract players data out of https://www.sofascore.com
    """
    db_control.create()
    watch = tqdm(total=100, position=0)

    for league_url in TOP3_LEAGUES_URLS:  # iterating league links
        teams = extract_teams_urls(league_url)  # extracting teams out of leagues tables
        league_name = league_url.split("/")[-2]
        print("\ngetting teams from " + league_name)  # printing for user "loading"
        db_control.write_league([league_name, len(teams)])

        for team_url in teams:  # iterating all teams urls
            player_count, players_list = extract_players_urls(
                team_url)  # extracting player url which also print to screen player data
            team_name = team_url.split('/')[-2]
            db_control.write_teams([team_name, player_count], league_name)
            db_control.write_players(players_list, team_name)
            watch.update(1)


if __name__ == '__main__':
    main()
