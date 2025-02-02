import os
import requests
from bs4 import BeautifulSoup
import json
import gzip

# File e URL statici
daddyLiveChannelsFileName = '247channels.html'
daddyLiveChannelsURL = 'https://thedaddy.to/24-7-channels.php'


STATIC_LOGOS = {
    "sky uno": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-uno-it.png",
    "rai 1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-1-it.png",
    "rai 2": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-2-it.png",
    "rai 3": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-3-it.png",
    "eurosport 1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/spain/eurosport-1-es.png",
    "eurosport 2": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/spain/eurosport-2-es.png",
    "italia 1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/italia1-it.png",
    "la7": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/la7-it.png",
    "la7d": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/la7d-it.png",
    "rai sport": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-sport-it.png",
    "rai premium": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-premium-it.png",
    "sky sports golf": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-golf-it.png",
    "sky sport motogp": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-motogp-it.png",
    "sky sport tennis": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-tennis-it.png",
    "sky sport f1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-f1-it.png",
    "sky sport football": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-football-it.png",
    "sky sport uno": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-uno-it.png",
    "sky sport arena": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-arena-it.png",
    "sky cinema collection": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-collection-it.png",
    "sky cinema uno": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-uno-it.png",
    "sky cinema action": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-action-it.png",
    "sky cinema comedy": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-comedy-it.png",
    "sky cinema uno +24": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-uno-plus24-it.png",
    "sky cinema romance": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-romance-it.png",
    "sky cinema family": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-family-it.png",
    "sky cinema due +24": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-due-plus24-it.png",
    "sky cinema drama": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-drama-it.png",
    "sky cinema suspense": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-suspense-it.png",
    "sky sport 24": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-24-it.png",
    "sky sport calcio": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-calcio-it.png",
    "sky calcio 1": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-1-alt-de.png",
    "sky calcio 2": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-2-alt-de.png",
    "sky calcio 3": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-3-alt-de.png",
    "sky calcio 4": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-4-alt-de.png",
    "sky calcio 5": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-5-alt-de.png",
    "sky calcio 6": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-6-alt-de.png",
    "sky calcio 7": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/germany/sky-select-7-alt-de.png",
    "sky serie": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-serie-it.png",
    "20 mediaset": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/20-it.png"
}

STATIC_TVG_IDS = {
    "sky uno": "skyuno.it",
    "rai 1": "rai1.it",
    "rai 2": "rai2.it",
    "rai 3": "rai3.it",
    "eurosport 1": "eurosport1.it",
    "eurosport 2": "eurosport2.it",
    "italia 1": "italia1.it",
    "la7": "la7.it",
    "la7d": "la7d.it",
    "rai sport": "raisport.it",
    "rai premium": "raipremium.it",
    "sky sports golf": "skysportsgolf.it",
    "sky sport motogp": "skysportmotogp.it",
    "sky sport tennis": "skysporttennis.it",
    "sky sport f1": "skysportf1.it",
    "sky sport football": "skysportfootball.it",
    "sky sport uno": "skysportuno.it",
    "sky sport arena": "skysportarena.it",
    "sky cinema collection": "skycinemacollection.it",
    "sky cinema uno": "skycinemauno.it",
    "sky cinema action": "skycinemaaction.it",
    "sky cinema comedy": "skycinemacomedy.it",
    "sky cinema uno +24": "skycinemaunoPlus24.it",
    "sky cinema romance": "skycinemaromance.it",
    "sky cinema family": "skycinemafamily.it",
    "sky cinema due +24": "SkyCinemaDuePlus24.it",
    "sky cinema drama": "skycinemadrama.it",
    "sky cinema suspense": "skycinemasuspense.it",
    "sky sport 24": "skysport24.it",
    "sky sport calcio": "SkySportCalcio.it",
    "sky calcio 1": "SkySport1.it",
    "sky calcio 2": "SkySport2.it",
    "sky calcio 3": "skysport3.it",
    "sky calcio 4": "skysport4.it",
    "sky calcio 5": "skysport5.it",
    "sky calcio 6": "skysport6.it",
    "sky calcio 7": "skysport7.it",
    "sky serie": "skyserie.it",
    "20 mediaset": "20.it",
}


STATIC_CATEGORIES = {
    "sky uno": "Intrattenimento",
    "rai 1": "Intrattenimento",
    "rai 2": "Intrattenimento",
    "rai 3": "Intrattenimento",
    "eurosport 1": "Sport",
    "eurosport 2": "Sport",
    "italia 1": "Intrattenimento",
    "la7": "Intrattenimento",
    "la7d": "Intrattenimento",
    "rai sport": "Sport",
    "rai premium": "Intrattenimento",
    "sky sports golf": "Sport",
    "sky sport motogp": "Sport",
    "sky sport tennis": "Sport",
    "sky sport f1": "Sport",
    "sky sport football": "Sport",
    "sky sport uno": "Sport",
    "sky sport arena": "Sport",
    "sky cinema collection": "Cinema",
    "sky cinema uno": "Cinema",
    "sky cinema action": "Cinema",
    "sky cinema comedy": "Cinema",
    "sky cinema uno +24": "Cinema",
    "sky cinema romance": "Cinema",
    "sky cinema family": "Cinema",
    "sky cinema due +24": "Cinema",
    "sky cinema drama": "Cinema",
    "sky cinema suspense": "Cinema",
    "sky sport 24": "Sport",
    "sky sport calcio": "Sport",
    "sky calcio 1": "Sport",
    "sky calcio 2": "Sport",
    "sky calcio 3": "Sport",
    "sky calcio 4": "Sport",
    "sky calcio 5": "Sport",
    "sky calcio 6": "Sport",
    "sky calcio 7": "Sport",
    "sky serie": "Cinema",
    "20 mediaset": "Intrattenimento",
}


def delete_file_if_exists(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f'File {file_path} deleted.')

def fetch_with_debug(filename, url):
    try:
        print(f'Downloading {url}...')
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with open(filename, 'wb') as file:
            file.write(response.content)

        print(f'File {filename} downloaded successfully.')
    except requests.exceptions.RequestException as e:
        print(f'Error downloading {url}: {e}')


def search_category(channel_name):
    return STATIC_CATEGORIES.get(channel_name.lower().strip(), "Undefined")


def search_streams(file_path, keyword):
    matches = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            links = soup.find_all('a', href=True)

            for link in links:
                if keyword.lower() in link.text.lower():
                    href = link['href']
                    stream_number = href.split('-')[-1].replace('.php', '')
                    stream_name = link.text.strip()
                    match = (stream_number, stream_name)

                    if match not in matches:
                        matches.append(match)
    except FileNotFoundError:
        print(f'The file {file_path} does not exist.')
    return matches

def search_logo(channel_name):
    channel_name_lower = channel_name.lower().strip()
    for key, url in STATIC_LOGOS.items():
        if key in channel_name_lower:
            return url
    return "https://raw.githubusercontent.com/emaschi123/eventi/refs/heads/main/ddlive.png"

def search_tvg_id(channel_name):
    channel_name_lower = channel_name.lower().strip()
    for key, tvg_id in STATIC_TVG_IDS.items():
        if key in channel_name_lower:
            return tvg_id
    return "unknown"

def generate_m3u8(matches):
    if not matches:
        print("No matches found. Skipping M3U8 generation.")
        return

    with open("outworld.m3u8", 'w', encoding='utf-8') as file:
        file.write('#EXTM3U\n')

        for channel in matches:
            channel_id = channel[0]
            channel_name = channel[1].replace("Italy", "").replace("8", "").replace("(251)", "").replace("(252)", "").replace("(253)", "").replace("(254)", "").replace("(255)", "").replace("(256)", "").replace("(257)", "").replace("HD+", "").strip()
            tvicon_path = search_logo(channel_name)
            tvg_id = search_tvg_id(channel_name)
            category = search_category(channel_name)

            # Se tvg_id non è definito, usa channel_id al suo posto
            tvg_id_to_use = tvg_id if tvg_id != channel_name else channel_id

            file.write(f"#EXTINF:-1 tvg-id=\"{tvg_id_to_use}\" tvg-name=\"{channel_name}\" tvg-logo=\"{tvicon_path}\" group-title=\"{category}\", {channel_name}\n")
            file.write(f'#EXTVLCOPT:http-referrer=https://ilovetoplay.xyz/\n')
            file.write(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1\n')
            file.write(f'#EXTVLCOPT:http-origin=https://ilovetoplay.xyz\n')
            file.write(f"https://xyzdddd.mizhls.ru/lb/premium{channel_id}/index.m3u8\n\n")

    print("M3U8 file generated successfully.")

# Cleanup e Fetch dati
delete_file_if_exists(daddyLiveChannelsFileName)
fetch_with_debug(daddyLiveChannelsFileName, daddyLiveChannelsURL)

# Cancella anche out.m3u8 prima di crearne uno nuovo
delete_file_if_exists("outworld.m3u8")

# Elaborazione dati
matches = search_streams(daddyLiveChannelsFileName, "")
generate_m3u8(matches)

# Parte EPG commentata
"""
epgs = [
    {'filename': 'epgShare1.xml', 'url': 'https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz'}
]

for epg in epgs:
    delete_file_if_exists(epg['filename'])
    fetch_with_debug(epg['filename'], epg['url'])
"""
