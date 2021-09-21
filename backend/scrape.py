# pylance: ignore reportMissingImports, reportMissingModuleSource
import os
import re
import lyricsgenius
import time
from datetime import datetime
import requests
import json

# parsing page contents
from bs4 import BeautifulSoup

# TODO: add type hints

def parse_page(html: str) -> list[list[str]]:

    # parse entire html page
    soup = BeautifulSoup(html, "html.parser")

    # finds the div where id = "top-songs", save to songs
    songs = soup.find("div", {"id": "top-songs"})

    # get song title and artist info
    hits = [
        hit.get_text()
        for hit in BeautifulSoup.findAll(
            songs, attrs={"class": re.compile("^ChartSongdesktop__Title-sc.*")}
        )
    ]
    artists = [
        artist.get_text()
        for artist in BeautifulSoup.findAll(
            songs, attrs={"class": re.compile("^ChartSongdesktop__Artist-sc.*")}
        )
    ]

    # get links to the genius page for each top song
    links = [link["href"] for link in songs.find_all("a", href=True)]
    rank = [i for i, _ in enumerate(hits)]

    # multiply by len(lyrics) so lyrics and datetimes arrays are the same shape
    datetimes = [datetime.now().isoformat(timespec="hours")] * len(hits)

    return [hits, artists, links, rank, datetimes]



def get_lyrics(hits:list[str], artists:list[str])-> list[str]:

    token = os.environ.get('genius_token')
    genius = lyricsgenius.Genius(token)

    lyrics = []
    for hit, artist in zip(hits, artists):
        lyrics.append(genius.search_song(hit, artist).lyrics)
        time.sleep(15)

    return lyrics


def clean_lyrics(lyrics:list)-> list:

    NotImplementedError

    return lyrics


def clean_comments(comments:list)-> list:

    NotImplementedError

    return comments


def get_artist_info(arists):

    base_url = "https://api.genius.com/search"
    headers = {"Authorization": "Bearer " + TOKEN}

    artist_info = []
    for artist in arists:
        params = {"q": str(artist)}
        r = requests.get(base_url, params=params, headers=headers)
        r = json.loads(r.text)

        artist_info.append(r["response"])

    return artist_info
