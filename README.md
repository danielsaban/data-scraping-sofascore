# README -  SofaScore Scraper

The program reaches the website [SofaScore](https://www.sofascore.com/) and scrapes data for the football players of the main european leagues.

## Data

For the selected football leagues, all the team names are collected.

For every team, each player is scraped and a series of information is stored in a database:

```
1. Name
2. Nationality
3. Age
4. Height
5. Preferred Foot
6. Position on the Pitch
7. Shirt Number
8. Market Value
```

If the data related to a certain league hasn't been scraped before, it will be simply added to the database.

If otherwise the data from the selected league is already present in the database, this data will be overwritten by the current one.

## Usage

As a first step it's important to write the correct username and password in "config.py".

```
pip install -r requirements.txt
```

```
python main.py -s -p -l
```

CLI Arg | Action
------------ | ------------- 
-s | scrapes teams and players from Serie A
-p | scrapes teams and players from Premier League
-l | scrapes teams and players from La Liga

The user can choose which league or combination of leagues to scrape and to create/update the database with.

