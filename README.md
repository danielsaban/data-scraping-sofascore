# README -  SofaScore Scraper

This Data Engineering project performs some detailed Data Mining operations, reaching the website [SofaScore](https://www.sofascore.com/) and scraping data about football players and managers of the main european leagues. 

Then, it makes sure all the data is safely stored in a Relational Database, ready to be exploited by the user.

## Data

For the selected football leagues, all the team names are collected.

For every team, each player is scraped and a series of information is stored in a database:

```
1. Name
2. Nationality
3. Date of Birth
4. Height
5. Preferred Foot
6. Position on the Pitch
7. Shirt Number
```

Information about managers is parsed as well:

```
1. Name
2. Date of Birth
3. Nationality
4. Preferred Formation
5. Average Points per Game
6. Games Won
7. Games Drawn
8. Games Lost
```

Moreover, extra data about the various teams is obtained and stored in the DB:

```
1. Name
2. Short Name
3. Alternative Name
4. Foundation Year
5. Stadium Name
6. Stadium Picture URL
7. Stadium Description
8. Stadium Location
9. Stadium Capacity
10. Team Website
11. Team Facebook
12. Team Twitter
13. Team Instagram
14. Team Description
```

If the data related to a certain league hasn't been scraped before, it will be simply added to the database.

If otherwise the data from the selected league is already present in the database, this data will be overwritten by the current one.

## Usage

As a first step it's important to write the correct username and password in "config.py".

```
pip install -r requirements.txt
```

```
python main.py -s -p -l -b
```

CLI Arg | Action
------------ | ------------- 
-s | scrapes teams and players from Serie A
-p | scrapes teams and players from Premier League
-l | scrapes teams and players from La Liga
-b | scrapes teams and players from Bundesliga

The user can choose which league or combination of leagues to scrape and to create/update the database with.

Created by:
- `Daniel Saban`
- `Sagi Elfassi`
