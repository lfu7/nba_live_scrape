from bs4 import BeautifulSoup
import requests

# Used to spoof ESPN's bot detection
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_espn_nba_games():
    # URL of the ESPN NBA scoreboard page
    url = 'https://www.espn.com/nba/scoreboard'

    # Send a GET request to the page
    response = requests.get(url, headers=HEADERS)

    # Check if the request was successful
    if response.status_code != 200:
        print(f'Failed to fetch data: HTTP {response.status_code}')
        return

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all game containers
    games = soup.find_all('section', class_='Scoreboard')

    # Extract data for each game
    for game in games:
        try:
            # Get the names of the teams
            gamecast_links = game.find_all('a', href=True)


            # TODO: make this code more robust.
            # - check to make sure that the gameId is strictly numerical (ex 401704990/cavaliers-nuggets)
            team1 = ''
            team2 = ''
            game_id = ''
            for link in gamecast_links:
                href = link['href']
                if 'team' in href:
                    if team1 == '':
                        team1 = href.split('/')[-1]
                    else:
                        team2 = href.split('/')[-1]
                
                if 'gameId' in href:
                    game_id = href.split('gameId/')[-1]
                    

        except Exception as e:
            print(f"Error processing game: {e}")


def get_active_players(game_id):
    url = f'https://www.espn.com/nba/game/_/{game_id}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all("div", class_="OnTheCourtTableWrapper")

    rows = []
    for element in elements:
        team = element.img.get('alt')
        for link_html in element.find_all("table", class_=["Table", "Table--align-right"])[0].find_all("a", href=True):
            # If you already have BeautifulSoup Tag objects (e.g., from find_all), skip re-parsing
            # link_soup = BeautifulSoup(link_html, "html.parser").find("a")

            name = link_html.get_text(strip=True)
            player_url = link_html.get("href")
            player_id = player_url.split('/')[-2]
            rows.append({"Player Name": name, "Player ID": player_id, "Team": team})
            print(player_id)
            
    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    scrape_espn_nba_games()
