# standard library imports
from datetime import datetime
import json
import os
import re
import time

# third-party libraries
from bs4 import BeautifulSoup
import lyricsgenius
import requests
import spacy


def results_csv(df_hits):
    """
    Export the dataframe to a CSV file.

    Args:
        df_hits (pandas.DataFrame): The dataframe to be exported.

    Returns:
        None
    """
    csv_path = os.path.join(os.getcwd(), "assets", "csv")
    os.makedirs(csv_path, exist_ok=True)
    csv_name = f'{df_hits["Date"][0]}{datetime.now()}.csv'
    df_hits.to_csv(os.path.join(csv_path, csv_name), encoding="utf-8")


nlp = spacy.load("en_core_web_sm")


# plan to apply this function to a column using pandas .apply()
def clean_text(lyrics):

    # remove lyric annotations that exist in brackets
    new_lyrics = re.sub(r"\[.*\]", "", lyrics)

    # remove extra space between paragaphs


# TODO: we should get comments and page views


# ==== Get Data ====


def parse_html(html: str) -> dict[str, list[str]]:

    # create BeautifulSoup object
    soup = BeautifulSoup(html, "html.parser")

    # find the div where id = "top-songs"
    songs = soup.find("div", {"id": "top-songs"})

    # Check if songs is not None
    if songs:
        # create a dictionary to store the song information
        song_info = {
            "hits": [
                hit.get_text()
                for hit in songs.findAll(
                    attrs={"class": re.compile("^ChartSongdesktop__Title-sc.*")}
                )
            ],
            "artists": [
                artist.get_text()
                for artist in songs.findAll(
                    attrs={"class": re.compile("^ChartSongdesktop__Artist-sc.*")}
                )
            ],
            "links": [
                link["href"]
                for link in songs.find_all("a", href=True)
                ],
            "rank": list(range(0, len(songs))),
            "genre": ["rap"] * len(songs),
        }
    else:
        print("No div with id 'top-songs' found")
        song_info = {}

    return song_info


def get_lyrics(token: str, d: dict) -> list:
    """Append lyrics information to the data dictionary using the lyricsgenius library.

    A combination of artist and song is used in API requests because there exists a many-many relationship between song names and artists

    Args:
        token (str): secret genius token
        hits (list[str]): a list of song names
        artists (list[str]): a list of artist names

    Returns:
        d:
    """
    # create lyricsgenius object
    genius = lyricsgenius.Genius(token)
    d = {}
    for hit, artist in zip(d["hits"], d["artists"]):
        d[hit]=genius.search_song(hit, artist).lyrics
        time.sleep(15)
    return d


def get_artist_info(arists: list[str], token: str) -> list[str]:

    # prep for api request
    base_url = "https://api.genius.com/search"
    headers = {"Authorization": "Bearer " + token}

    # for each artist, make an api request and append strings to artist_info
    artist_info = []
    for artist in arists:
        params = {"q": str(artist)}
        r = requests.get(base_url, params=params, headers=headers)
        r = json.loads(r.text)
        artist_info.append(r["response"])

    return artist_info
