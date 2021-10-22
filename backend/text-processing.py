# import spacy and load the english language library
import spacy
import re
nlp = spacy.load('en_core_web_sm')

# plan to apply this function to a column using pandas .apply()
def clean_text(lyrics):

    # remove lyric annotations that exist in brackets
	new_lyrics = re.sub('\[.*\]','',lyrics)

	# remove extra space between paragaphs
	





# create doc object for each song