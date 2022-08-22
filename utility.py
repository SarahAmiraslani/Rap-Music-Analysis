# utility
import os

# pylance: ignore reportMissingImports, reportMissingModuleSource

# utility
import re
import time
from datetime import datetime
import json

# getting data
import requests
import lyricsgenius

# parsing page contents
from bs4 import BeautifulSoup


def results_csv(df_hits):

    current_datetime_str = datetime.today().strftime("%m/%d/%Y")

    repo = os.getcwd()
    csv_path = "results_csv"

    if csv_path not in os.listdir():
        os.mkdir(repo + os.sep + csv_path)
    # file naming/ path convention:
    import datetime

    current_datetime_str = str(datetime.datetime.now())
    csv_path = "/results_csv/"
    df_hits_time = str(df_hits["Date"][0])
    csv_name = df_hits_time + current_datetime_str + ".csv"

    # export dataframe:
    df_hits.to_csv(csv_path + os.sep + csv_name, encoding="utf-8")

# import spacy and load the english language library
import spacy
import re
nlp = spacy.load('en_core_web_sm')

# plan to apply this function to a column using pandas .apply()
def clean_text(lyrics):

    # remove lyric annotations that exist in brackets
	new_lyrics = re.sub('\[.*\]','',lyrics)

	# remove extra space between paragaphs


# TODO: we should get comments and page views


# ==== Get Data ====

def parse_html(html: str) -> list[list[str]]:

    d = {}

    # create BeautifulSoup object
    soup = BeautifulSoup(html, "html.parser")

    # ==== Parse and Save Data ====

    # finds the div where id = "top-songs"
    songs = soup.find("div", {"id": "top-songs"})

    # get song title for each song, save to hits list
    hits = [
        hit.get_text()
        for hit in BeautifulSoup.findAll(
            songs, attrs={"class": re.compile("^ChartSongdesktop__Title-sc.*")}
        )
    ]
    d['hits']=hits

    # get artist name for each song, save to artists list
    artists = [
        artist.get_text()
        for artist in BeautifulSoup.findAll(
            songs, attrs={"class": re.compile("^ChartSongdesktop__Artist-sc.*")}
        )
    ]
    d['artists']=artists

    # get links to the genius page for each top song
    links = [link["href"] for link in songs.find_all("a", href=True)]
    d['links']=links

    # save how the songs ranked at the time of scraping
    rank = list(range(0,len(songs)))
    d['rank']=rank

    # save the genre of the songs
    genre = ['rap'] * len(songs)
    d['genre'] = genre


    return d

# todo: figure out how to type hint with dict
def get_lyrics(token:str,d:dict)-> dict:
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

    # get lyrics for each song artist combination
    lyrics = []
    for hit, artist in zip(d['hits'], d['artists']):
        lyrics.append(genius.search_song(hit, artist).lyrics)
        time.sleep(15) #TODO: why do we have sleep?

    d['lyrics']=lyrics

    return d


def get_artist_info(arists:list[str],token:str)->list[str]:

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


def get_song_info(hits):
    """
    # TODO: add better documentation

    """

    # TODO: make this more robust so that it gets the right song even when there
    # are multiple songs with the same name

    base_url = "https://api.genius.com/search"
    headers = {"Authorization": "Bearer " + TOKEN}

    hits_info = []
    for hit in hits:
        params = {"q": str(hit)}
        r = requests.get(base_url, params=params, headers=headers)
        r = json.loads(r.text)

        hits_info.append(r["response"])

    return hits_info


def get_comments(hits):
    NotImplementedError

# ==== Clean Data ====

def clean_lyrics(lyrics:list)-> list:

    NotImplementedError

    return lyrics


def clean_comments(comments:list)-> list:

    NotImplementedError

    return comments
