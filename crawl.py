"""Genius crawler

This script uses a chrome driver to navigate to the genius website and load the songs that rank the highest at that time. The script supports all genres (All, Rap, Pop, R&B, Rock, and Country). After loading information about top songs of a requested genre, it will return the html content of the page to be later parsed.

This script requires that `selenium` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
function:

	* get_html - returns html content of the requested genius page
"""

# utility
from datetime import datetime

# webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_html(n_songs:int,genre:str='rap')->dict:
	"""Get HTML data from genius for a specified (n_num) number of songs.
	Args:
		num_songs (int): number of songs to get lyrics for from the site.
	Returns:
		str: html of page, not parsed
	"""

	# serves as our data dict
	d = {}

	# calculate the number of pages to open given that the UI displays 10 songs per page
	pages = n_songs//10

	# if n_songs is not a multiple of 10, add 1 to page count
	if n_songs%10 != 0:
		pages+=1

	# ==== Prepare Xpaths ====

	# identify the top songs container and the genre column in drop down menu
	# to be used to generate xpaths of interest
	id_songs = '//*[@id="top-songs"]'
	genre_selections = id_songs + '/div/div[2]/div/div/div[2]/div[2]/'

	# identify drop down menu xpath and load button xpath
	# dd_xpath will be used to change genres, load_xpath to get more song data
	dd_xpath = id_songs + '/div/div[2]/div/div/div[1]'
	load_xpath = id_songs + '/div/div[4]/div'

	# prepare genre xpath
	if genre == 'all':
		genre_xpath = genre_selections + 'div[2]/div'
	elif genre == 'rap':
		genre_xpath = genre_selections + 'div[3]/div'
	elif genre == 'pop':
		genre_xpath = genre_selections + 'div[4]/div'
	elif genre == 'r&b':
		genre_xpath = genre_selections + 'div[5]/div'
	elif genre == 'rock':
		genre_xpath = genre_selections + 'div[6]/div'
	elif genre == 'country':
		genre_xpath = genre_selections + 'div[7]/div'

	# ==== Navigating ====

	# initilaize chrome driver
	driver = webdriver.Chrome(ChromeDriverManager().install())

	#TODO: headless browser would be better once we know that everything is working
	# navigate to website and maximize window for visibility
	driver.get("https://genius.com/#top-songs")
	driver.maximize_window()

	# ==== Page interactions ====

	# click on drop down once clickable, timeout if not clickable in 30s
	WebDriverWait(driver,30).until(
		EC.element_to_be_clickable((By.XPATH,dd_xpath))
		)
	drop_down = driver.find_elements_by_xpath(dd_xpath)[0]
	drop_down.click()

	# click on genre button once clickable, timeout if not clickable in 30s
	WebDriverWait(driver,30).until(
		EC.element_to_be_clickable((By.XPATH,genre_xpath))
		)
	genre_button = driver.find_elements_by_xpath(genre_xpath)[0]
	genre_button.click()

	# load 10 more songs until requested number of songs reached
	counter=0
	while counter < pages:
		# click on load more button once clickable, timeout in 30s
  		WebDriverWait(driver,30).until(
			EC.element_to_be_clickable(By.XPATH,load_xpath)
		)

		load_more = driver.find_elements_by_xpath(load_xpath)
		load_more.click()

		counter += 1

	# ==== save page html and stop driver ====

	# at this point we have n_songs+ listed, get html source code and save data
	html = driver.page_source
	d['html'] = html

	# close the driver and browser
	driver.quit()

	return d
