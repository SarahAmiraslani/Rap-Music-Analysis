# utility functions
from datetime import datetime

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



def get_html(n_songs:int,genre:str)->dict:
	"""Get HTML data from genius for a specified (n_num) number of songs.
	Args:
		num_songs ([int]): number of songs to get lyrics for from the site.
	Returns:
		[str]: html of page, not parsed
	"""

	# serves as our data dict
	d = {}

	# save the datetime of scraping
    # multiply by len(n_songs) so dt arrays have the same shape as other data
	datetimes = [datetime.now().isoformat(timespec="hours")] * len(n_songs)
	d['datetimes']=datetimes

	# calculate the number of pages to open given that the UI displays 10 songs per page
	pages = n_songs//10

	# if n_songs is not a multiple of 10, add 1 to page count
	if n_songs%10 != 0:
		pages+=1

	# prepare xpaths
	top_songs_xpath = '//*[@id="top-songs"]/div/div[2]/div/div/'
	dd_xpath = top_songs_xpath + 'div[1]/div'
	load_css = "div[class^='SquareButton-sc']"

	if genre == 'rap':
		genre_xpath = top_songs_xpath + 'div[2]/div[2]/div[3]/div'
	elif genre == 'pop':
		genre_xpath = NotImplementedError
	elif genre == 'r&b':
		rap_xpath = NotImplementedError


	# ==== Navigating ====

	# initilaize chrome driver
	driver = webdriver.Chrome(ChromeDriverManager().install())

	#TODO: headless browser would be better
	# navigate to website
	driver.get("https://genius.com/#top-songs")
	driver.maximize_window()

	# ==== Page interactions ====

	# click on drop down once it is clickable, timeout if not clickable in 30s
	WebDriverWait(driver,30).until(
		EC.element_to_be_clickable((By.XPATH,dd_xpath))
		)
	drop_down = driver.find_elements_by_xpath(dd_xpath)[0]
	drop_down.click()

	# click on rap button once it is clickable, timeout if not clickable in 30s
	WebDriverWait(driver,30).until(
		EC.element_to_be_clickable((By.XPATH,genre_xpath))
		)
	rap_button = driver.find_elements_by_xpath(rap_xpath)[0]
	rap_button.click()

	# load more songs (10 at a time) until requested number of songs reached
	counter=0
	while counter < pages:
		#TODO: is there a reason to use css and not xpath
		# load an extra tab, timeout if not clickable in 30s
		WebDriverWait(driver,30).until(
		EC.element_to_be_clickable((By.XPATH,load_css))
		)
		load_more = driver.find_element_by_css_selector(load_css)
		load_more.click()

		counter += 1

	# ==== save page html and stop driver ====

	html = driver.page_source
	d['html'] = html

	# close the browser
	driver.quit()

	return d
