# utility
from datetime import datetime
import re
import json
import time
import requests
import os

# script execution
from typing import NoReturn

# webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# lyrics generation
import lyricsgenius
from bs4 import BeautifulSoup

# TODO: get historical data for songs

TOKEN = "F4xSKCMmA7mpolFgbIrdAPPBw67u6ae_p19dSs0rqDcZNrhBSzVt9hMn5Xan0_aq"


def get_page_source(song_num: int) -> str:

    # TODO: consider css selector approach for find_elements_by_xpath

    load_clicks: int = song_num % 10

    # Using Chrome to acess web
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Open the website
    driver.get("https://genius.com/#top-songs")

    # Setting up the page for scraping, we need to load top 50 and choose the rap genre

    # Set up top 50 songs
    drop_d_xpath = '//*[@id="top-songs"]/div/div[2]/div/div/div[1]/div'
    drop_down = driver.find_elements_by_xpath(drop_d_xpath)[0]
    drop_down.click()
    time.sleep(3)  # TODO: change this

    rap_xpath = '//*[@id="top-songs"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div'
    rap_button = driver.find_elements_by_xpath(rap_xpath)[0]
    rap_button.click()
    time.sleep(5)

    # adjust range accordingly depending on how many songs you would like
    for i in range(4):
        load_xpath = "div[class^='SquareButton-sc']"
        load_more = driver.find_element_by_css_selector(load_xpath)
        load_more.click()
        time.sleep(5)

    # getting page html
    html = driver.page_source

    driver.quit()

    # TODO: find out how to return without printing html

    return html


def parse_page(html: str) -> list:

    # parsing the entire html page, creates BS4 object
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

    token = "F4xSKCMmA7mpolFgbIrdAPPBw67u6ae_p19dSs0rqDcZNrhBSzVt9hMn5Xan0_aq"
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


# TODO: we should get comments and page views
