def get_page_source(): 

    """ 
    #TODO: add better documentation
    """




    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    import time # for interaction latency

    # Using Chrome to acess web
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # Open the website
    driver.get("https://genius.com/#top-songs")

    #TODO: consider css selector approach for find_elements_by_xpath
    # Setting up the page for scraping
    drop_down = driver.find_elements_by_xpath('//*[@id="top-songs"]/div/div[2]/div/div/div[1]/div')[0]
    drop_down.click()
    time.sleep(3)

    rap_button = driver.find_elements_by_xpath('//*[@id="top-songs"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div')[0]
    rap_button.click()
    time.sleep(5)

    # adjust range accordingly depending on how many songs you would like
    for i in range(4):
        load_more = driver.find_element_by_css_selector("div[class^='SquareButton-sc']")
        load_more.click()
        time.sleep(5)

    # getting page html
    html = driver.page_source

    driver.quit()

    # TODO: find out how to return without printing html
    
    return html

def parse_page(html): 

    """
    # TODO: add better documentation
    """

    from bs4 import BeautifulSoup
    from datetime import datetime
    import re

    # parsing the entire html page, creates BS4 object
    soup = BeautifulSoup(html, 'html.parser')

    # finds the div where id = "top-songs", save to songs
    songs = soup.find("div",{"id":"top-songs"})

    # get song title and artist info
    hits = [hit.get_text() for hit in BeautifulSoup.findAll(songs, attrs={'class': re.compile('^ChartSongdesktop__Title-sc.*')})]
    artists = [artist.get_text() for artist in BeautifulSoup.findAll(songs, attrs={'class': re.compile('^ChartSongdesktop__Artist-sc.*')})]

    # get links to the genius page for each top song
    links = [link['href'] for link in songs.find_all('a', href=True)] 
    
    # TODO: create rank and return 
    rank = [i for i, hit in enumerate(hits)]

    # we multiply by len(lyrics) so that the lyrics and datetimes arrays are the same shape
    datetimes = [datetime.now().isoformat(timespec='hours')]*len(hits)

    return hits, artists, links, rank, datetimes

def get_lyrics(hits, artists): 

    """ 
    # TODO: add better documentation

    """
    import lyricsgenius
    import getpass # could be useful if we dont want our genius token to be public on github

    #TODO: consider using getpass to protect our API token

    token = 'F4xSKCMmA7mpolFgbIrdAPPBw67u6ae_p19dSs0rqDcZNrhBSzVt9hMn5Xan0_aq'
    genius = lyricsgenius.Genius(token)

    lyrics = []
    
    for hit, artist in zip(hits, artists):
        lyrics.append(genius.search_song(hit, artist).lyrics)
         time.sleep(15)

    return lyrics

def clean_lyrics(lyrics): 

    """Apply this to the the lyrics column to prepare lyrics for 
    natual lanaguage processing
    
    """


    return lyrics

def clean_comments(comments):

    return comments

def get_artist_info(arists):

    """
    # TODO: add better documentation
    """

    import requests
    import json

    base_url = 'https://api.genius.com/search'
    TOKEN = 'F4xSKCMmA7mpolFgbIrdAPPBw67u6ae_p19dSs0rqDcZNrhBSzVt9hMn5Xan0_aq'
    headers = {'Authorization': 'Bearer ' + TOKEN}
    
    artist_info = []
    for artist in arists: 
        params = {'q': str(artist)}
        r = requests.get(base_url, params=params, headers=headers)
        r = json.loads(r.text)
        
        artist_info.append(r['response'])

    return artist_info

def get_song_info(hits): 

    """
    # TODO: add better documentation

    """

    #TODO: make this more robust so that it gets the right song even when there 
    # are multiple songs with the same name

    import requests
    import json

    base_url = 'https://api.genius.com/search'

    TOKEN = 'F4xSKCMmA7mpolFgbIrdAPPBw67u6ae_p19dSs0rqDcZNrhBSzVt9hMn5Xan0_aq'
    headers = {'Authorization': 'Bearer ' + TOKEN}
    
    hits_info = []
    for hit in hits: 
        params = {'q': str(hit)}
        r = requests.get(base_url, params=params, headers=headers)
        r = json.loads(r.text)
        
        hits_info.append(r['response'])

    return hits_info

# TODO: we should get comments and page views
# TODO: create a quick diagram to see how functions interact with each other