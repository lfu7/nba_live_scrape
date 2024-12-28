import json

from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import requests

# Used to spoof ESPN's bot detection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# URL of the ESPN NBA scoreboard page
NBA_SCOREBOARD_URL = 'https://www.espn.com/nba/scoreboard'

NBA_GAMES_URL = 'https://www.espn.com/nba/game/_/{}'

app = Flask(__name__)

@app.route('/nba_games', methods=['GET'])
def nba_games():
    try:
        active_games = scrape_espn_nba_games()
        return [json.dumps(item) for item in list_of_maps]
    except Exception as e:
        print(f"Failed to retrieve live NBA games: {e}")

@app.route('/nba_games/<string:id>', methods=['GET'])
def nba_game_details(id):
    try:
        active_players = get_active_players(id)
        game_details = {
            "activePlayers": active_players,
        }

        return json.dumps(game_details)
    
    except Exception as e:
        print(f'Failed to retrieve NBA game details: {e}')




def scrape_espn_nba_games():
    """
    Scrapes the NBA games from the ESPN scoreboard

    Returns:
    A list of NBA game details, including:
    - 'home': the name of the home team
    - 'away': the name of the away team
    - 'id': the ESPN id of the game
    """

    # Send a GET request to the page
    response = requests.get(NBA_SCOREBOARD_URL, headers=HEADERS)

    # Check if the request was successful
    if response.status_code != 200:
        print(f'Failed to fetch data: HTTP {response.status_code}')
        return

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all game containers
    games = soup.find_all('section', class_='Scoreboard')

    # Extract data for each game
    active_games = []
    for game in games:
        try:
            # Get the names of the teams
            gamecast_links = game.find_all('a', href=True)


            # TODO: make this code more robust.
            # - check to make sure that the gameId is strictly numerical (ex 401704990/cavaliers-nuggets)
            # - verify logic for home and away teams
            away = ''
            home = ''
            game_id = ''
            for link in gamecast_links:
                href = link['href']
                if 'team' in href:
                    if away == '':
                        away = href.split('/')[-1]
                    else:
                        home = href.split('/')[-1]
                
                if 'gameId' in href:
                    game_id = href.split('gameId/')[-1]

                active_games.append({
                    "away": away,
                    "home": home,
                    "id": game_id,
                })

        except Exception as e:
            print(f"Error processing game: {e}")

    return active_games


def get_active_players(game_id):

    """
    Scrapes the active players an NBA game on ESPN. 

    Returns:
    A list of NBA player details, including:

    """

    url = NBA_GAMES_URL.format(game_id)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all("div", class_="OnTheCourtTableWrapper")

    active_players = []
    for element in elements:
        team = element.img.get('alt')
        for link_html in element.find_all("table", class_=["Table", "Table--align-right"])[0].find_all("a", href=True):
            # If you already have BeautifulSoup Tag objects (e.g., from find_all), skip re-parsing
            # link_soup = BeautifulSoup(link_html, "html.parser").find("a")

            name = link_html.get_text(strip=True)
            player_url = link_html.get("href")
            player_id = player_url.split('/')[-2]

            active_players.append({
                "name": name,
                "id": player_id,
                "team": team,
            })
            
    return active_players

if __name__ == "__main__":
    app.run(debug=True)
