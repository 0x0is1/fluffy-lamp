import requests, json, os, base64
from bs4 import BeautifulSoup as scraper

BASE_URL = base64.b64decode("aHR0cHM6Ly94bWFzY2hpcm1hc3QuY29tLwo=").decode("utf-8")

def fetch_home(url):
    response = requests.get(url)
    return response.content

def get_season_list(raw_data):
    container = []
    soup = scraper(raw_data, 'html.parser')
    seasons = soup.find_all('a', {'role': 'button'})
    for i in seasons[:-1]:
        season_name = str(i.text).replace("\n", "")
        season_url = i.get("href")
        container.append((season_name, season_url))
    return container

def get_episode_list(raw_data):
    container = []
    soup = scraper(raw_data, 'html.parser')
    episodes = soup.find_all('a', {'class': 'post-permalink'})
    for i in episodes:
        episode_name = i.get("title")
        episode_url = i.get("href")
        container.append((episode_name, episode_url))
    return container

def get_episode(raw_data):
    container = []
    soup = scraper(raw_data, 'html.parser')
    video_elem = soup.find_all('video', {'class': 'video-js position-absolute videojs-streamtube vjs-theme-forest'})[0]
    json_raw_data = video_elem.get("data-setup")
    return json.loads(json_raw_data)['sources'][0]['src']

def play(url, name):
    os.system(f"ffplay -window_title '{name}' '{url}'")

def main():
    season_list = get_season_list(fetch_home(BASE_URL))
    for i,j in enumerate(season_list):
        print(f'{i+1}. {j[0]}')
    season_idx = int(input("Select Season: "))-1
    os.system('clear')
    episode_list = get_episode_list(fetch_home(season_list[season_idx][1]))
    for i,j in enumerate(episode_list):
        print(f'{i+1}. {j[0]}')
    episode_idx = int(input("Select Episode: "))-1
    os.system('clear')
    episode = episode_list[episode_idx]
    stream_url = get_episode(fetch_home(episode[1]))
    play(stream_url, episode[0])

while True:
    main()
