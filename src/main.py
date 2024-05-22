import src.crawl as crawl, src.parse as parse

from datetime import datetime

d = {}
n_songs = 50
# save the datetime of scraping
# multiply by n_songs so dt arrays have the same shape as other data
datetimes = [datetime.now().isoformat(timespec="hours")] * n_songs
d['datetimes']=datetimes

for genre in ['rap','pop','r&b','rock','country']:
    d[genre] = {}
    d_crawl = crawl.get_html(50)

    d[genre]['html'] = d_crawl['html']

for genre in d.keys():
	for html in d[genre]['html']:
		d = parse.parse_html(html)
print(d)
