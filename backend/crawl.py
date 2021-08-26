# web crawling
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# parsing page contents
from bs4 import BeautifulSoup

# utility
from datetime import datetime
import re

class rap_driver(object):
    dd_xpath:str ='//*[@id="top-songs"]/div/div[2]/div/div/div[1]/div'
    rap_xpath:str = '//*[@id="top-songs"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div'
    load_css:str ="div[class^='SquareButton-sc']"

    def __init__(self,song_num):
        self.num_last_page:int = divmod(song_num,10)[-1]
        self.num_pages:int = round(song_num/10)


    def get_page_source(self):

        '''
        Navigating
        '''
        # use Chrome to acess web
        driver = webdriver.Chrome(ChromeDriverManager().install())

        # navigare to the website
        driver.get("https://genius.com/#top-songs")
        driver.maximize_window()

        '''
        Page interactions
        '''

        # click on drop down once it is clickable
        _ = WebDriverWait(driver,30).until(
            EC.element_to_be_clickable((By.XPATH,rap_driver.dd_xpath))
            )
        drop_down = driver.find_elements_by_xpath(rap_driver.dd_xpath)[0]
        drop_down.click()

        # click on rap button once it is clickable
        _ = WebDriverWait(driver,30).until(
            EC.element_to_be_clickable((By.XPATH,rap_driver.rap_xpath))
            )
        rap_button = driver.find_elements_by_xpath(rap_driver.rap_xpath)[0]
        rap_button.click()

        # load more songs (10 at a time) until requested number of songs reached
        counter=0
        while counter < self.num_pages:
            #todo: IS THERE ARE A REASON WE ARE USING CSS AND NOT XPATH
            _ = WebDriverWait(driver,30).until(
            EC.element_to_be_clickable((By.XPATH,rap_driver.load_css))
            )
            load_more = driver.find_element_by_css_selector(rap_driver.load_css)
            load_more.click()

        '''
        Getting page html
        '''
        html = driver.page_source

        driver.quit()

        return html

    def parse_page(html):

        # parse html page
        soup = BeautifulSoup(html,'html.parser')

        # find the div where id == "top-songs"
        songs = soup.find("div",{"id":"top-songs"})

        # get song title, artist, and links to song lyrics page
        hits = [hit.get_text() for hit in BeautifulSoup.findAll(
            songs, attrs={
                'class': re.compile('^ChartSongdesktop__Title-sc.*')
                }
            )
                ]
        artists = [artist.get_text() for artist in BeautifulSoup.findAll(
            songs, attrs={
                'class': re.compile('^ChartSongdesktop__Artist-sc.*')
                }
            )
                ]
        links = [link['href'] for link in songs.find_all(
            'a', href=True
            )
                ]

        # TODO: create rank and return
        #todo: this doesn't seem like the best approach, can just use numpy
        rank = list(range(1,len()))

        # we multiply by len(lyrics) so that the lyrics and datetimes arrays are the same shape
        datetimes = [datetime.now().isoformat(timespec='hours')]*len(hits)

        return hits, artists, links, rank, datetimes