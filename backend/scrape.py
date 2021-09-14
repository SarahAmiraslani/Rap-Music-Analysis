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

def parse_page(html: str) -> list:
    """[summary]

    Args:
        html ([str]): [description]

    Returns:
        [list]: [description]
    """

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

    # TODO: create rank and return
    #TODO: can probably use range for this
    rank = [i for i, hit in enumerate(hits)]

    # we multiply by len(lyrics) so that the lyrics and datetimes arrays are the same shape
    datetimes = [datetime.now().isoformat(timespec="hours")] * len(hits)

    return [hits, artists, links, rank, datetimes]



def get_lyrics(hits:list, artists:list)-> list:
    """[summary]

    Args:
        hits (list): [description]
        artists (list): [description]

    Returns:
        list: [description]
    """

    token = os.environ.get('genius_token')
    genius = lyricsgenius.Genius(token)

    lyrics = []
    for hit, artist in zip(hits, artists):
        lyrics.append(genius.search_song(hit, artist).lyrics)
        time.sleep(15)

    return lyrics


def clean_lyrics(lyrics:list)-> list:
    """[summary]

    Args:
        lyrics (list): [description]

    Returns:
        list: [description]
    """


    return lyrics


def clean_comments(comments:list)-> list:
    """[summary]

    Args:
        lyrics (list): [description]

    Returns:
        list: [description]
    """

    return comments


def get_artist_info(arists):
    """
    # TODO: add better documentation
    """

    base_url = "https://api.genius.com/search"
    #TODO: set this to env vars
    headers = {"Authorization": "Bearer " + TOKEN}

    artist_info = []
    for artist in arists:
        params = {"q": str(artist)}
        r = requests.get(base_url, params=params, headers=headers)
        r = json.loads(r.text)

        artist_info.append(r["response"])

    return artist_info
