import db_control
import config as cfg
import html_parser as hp
from tqdm import tqdm
import argparse


def parsing():
    """
    using argparse to simplify the cli for the user
    """
    leagues = []
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--SerieA", help="download Italian league players", action="store_true")
    parser.add_argument("-p", "--PremierLeague", help="download English league players", action="store_true")
    parser.add_argument("-l", "--LaLiga", help="download Spanish league players", action="store_true")
    args = parser.parse_args()

    if args.PremierLeague:
        leagues.append("premier")
    if args.LaLiga:
        leagues.append("laliga")
    if args.SerieA:
        leagues.append("seriea")
    return leagues


def main():
    """
    this is main calling function to extract players data out of https://www.sofascore.com
    """
    # validating that the user changed the MySQL password and username to connect
    if cfg.PASSWD == "" or cfg.USERNAME == "":
        exit("Please read README.md!")

    leagues_to_download = parsing()  # getting commands from the cli
    db_control.create()  # will create database and tables that does not exists.

    for league in leagues_to_download:  # iterating league links
        league_name = cfg.TOP3_LEAGUES_URLS[league].split("/")[-2]
        db_control.check_and_delete(league_name)
        teams = hp.extract_teams_urls(cfg.TOP3_LEAGUES_URLS[league])  # extracting teams out of leagues tables
        print("getting teams from " + league_name)  # printing for user "loading" in addition to tqdm
        db_control.write_league([league_name, len(teams)])
        watch = tqdm(total=len(teams), position=0)
        for team_url in teams:  # iterating all teams urls
            players_list = hp.extract_players_urls(team_url)  # extracting player url which
            team_name = team_url.split('/')[-2]
            db_control.write_teams([team_name, len(players_list)], league_name)
            db_control.write_players(players_list, team_name)
            watch.update(1)


if __name__ == '__main__':
    main()
