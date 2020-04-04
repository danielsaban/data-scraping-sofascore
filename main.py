import db_control
import config as cfg
import html_parser as hp
from tqdm import tqdm


def main():
    """
    this is main calling function to extract players data out of https://www.sofascore.com
    """
    db_control.create()
    watch = tqdm(total=100, position=0)

    for league_url in cfg.TOP3_LEAGUES_URLS:  # iterating league links
        teams = hp.extract_teams_urls(league_url)  # extracting teams out of leagues tables
        league_name = league_url.split("/")[-2]
        print("\ngetting teams from " + league_name)  # printing for user "loading" in addition to tqdm
        db_control.write_league([league_name, len(teams)])

        for team_url in teams:  # iterating all teams urls
            players_list = hp.extract_players_urls(team_url)  # extracting player url which
            team_name = team_url.split('/')[-2]
            db_control.write_teams([team_name, len(players_list)], league_name)
            db_control.write_players(players_list, team_name)
            watch.update(1)


if __name__ == '__main__':
    main()
