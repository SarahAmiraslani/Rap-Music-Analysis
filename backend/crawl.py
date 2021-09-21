# utility
from datetime import datetime
import re

# web crawling
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



def get_html(num_songs:int)->str:
	"""[summary]

	Args:
		num_songs ([int]): number of songs to get lyrics for from the site.

	Returns:
		[str]: html
	"""

	# TODO: I don't think tab is a good name for this
	tabs = num_songs//10
	if num_songs%10 != 0:
		tabs+=1

	# prepare xpaths
	top_songs_xpath = '//*[@id="top-songs"]/div/div[2]/div/div/'
	dd_xpath = top_songs_xpath + 'div[1]/div'
	rap_xpath = top_songs_xpath + 'div[2]/div[2]/div[3]/div'
	load_css = "div[class^='SquareButton-sc']"

	# ------------------- Navigating -------------------------------------------

	# initilaize chrome driver
	driver = webdriver.Chrome(ChromeDriverManager().install())

	#TODO: headless browser would be better
	# navigate to website
	driver.get("https://genius.com/#top-songs")
	driver.maximize_window()

	# ------------- Page interactions ------------------------------------------

	# click on drop down once it is clickable, timeout if not clickable in 30s
	WebDriverWait(driver,30).until(
		EC.element_to_be_clickable((By.XPATH,dd_xpath))
		)
	drop_down = driver.find_elements_by_xpath(dd_xpath)[0]
	drop_down.click()

	# click on rap button once it is clickable, timeout if not clickable in 30s
	WebDriverWait(driver,30).until(
		EC.element_to_be_clickable((By.XPATH,rap_xpath))
		)
	rap_button = driver.find_elements_by_xpath(rap_xpath)[0]
	rap_button.click()

	# load more songs (10 at a time) until requested number of songs reached
	counter=0
	while counter < tabs:
		#TODO: is there a reason to use css and not xpath
		# load an extra tab, timeout if not clickable in 30s
		WebDriverWait(driver,30).until(
		EC.element_to_be_clickable((By.XPATH,load_css))
		)
		load_more = driver.find_element_by_css_selector(load_css)
		load_more.click()

		counter += 1

	'''
	Getting page html
	'''
	html = driver.page_source

	driver.quit()

	return html



# class rap_driver(object):

#     dd_xpath:str ='//*[@id="top-songs"]/div/div[2]/div/div/div[1]/div'
#     rap_xpath:str = '//*[@id="top-songs"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div'
#     load_css:str ="div[class^='SquareButton-sc']"

#     def __init__(self,song_num):
#         self.num_last_page:int = divmod(song_num,10)[-1]
#         self.num_pages:int = round(song_num/10)



#     def parse_page(html):

#         # parse html page
#         soup = BeautifulSoup(html,'html.parser')

#         # find the div where id == "top-songs"
#         songs = soup.find("div",{"id":"top-songs"})

#         # get song title, artist, and links to song lyrics page
#         hits = [hit.get_text() for hit in BeautifulSoup.findAll(
#             songs, attrs={
#                 'class': re.compile('^ChartSongdesktop__Title-sc.*')
#                 }
#             )
#                 ]
#         artists = [artist.get_text() for artist in BeautifulSoup.findAll(
#             songs, attrs={
#                 'class': re.compile('^ChartSongdesktop__Artist-sc.*')
#                 }
#             )
#                 ]
#         links = [link['href'] for link in songs.find_all(
#             'a', href=True
#             )
#                 ]

#         # TODO: create rank and return
#         #todo: this doesn't seem like the best approach, can just use numpy
#         rank = list(range(1,len(hits)))

#         # we multiply by len(lyrics) so that the lyrics and datetimes arrays are the same shape
#         datetimes = [datetime.now().isoformat(timespec='hours')]*len(hits)

#         return hits, artists, links, rank, datetimes