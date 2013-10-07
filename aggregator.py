import facebook
import json
import time
import datetime
import csv, sys, urlparse

graph = facebook.GraphAPI('CAAB8StE8fOEBAJHd2dbCLAJpZAkVZAtrjf5ihL3Q4Y2JZA7Fc0z1VP7A6jVMrZCYNPCe8jocu6WZA3xsSYFZCzADG1SjzYItoOh0wOekrU66oWhPZBHPP8sZCFXLzmeswdSSimErcnoMlRRtgEoP0Xyi2G09lpBd5SNXYBRdugMqAUQlHlLHzsf4kKZCvC4jQKbFqm2auQCBPEgZDZD')
records = []
count = 1
pageid = 'wsj'
fromname = 'The Wall Street Journal'
posts = graph.get_connections(pageid, 'posts', date_format='U', limit=50)

flag = 1
while True:
	print len(posts['data'])
	for post in posts['data']:
		post['likes'] = {}
		post['comments'] = {}

		print "\nPost #", count, "\n", post, "\n"
		count = count + 1
		if post['from']['name'] == fromname and 'status_type' in post and 'message' in post or 'caption' in post:
			likes = graph.get_connections(post['id'], 'likes', summary=1)
			comments = graph.get_connections(post['id'], 'comments', summary=1)

			rec = {}

			rec['likes'] = likes['summary']['total_count']
			rec['comments'] = comments['summary']['total_count']
			rec['type'] = str(post['type'])
			if 'status_type' in post:
				rec['status_type'] = str(post['status_type'])
			else:
				rec['status_type'] = 'unknown'
			rec['age'] = post['created_time']
			rec['date'] = datetime.datetime.fromtimestamp(int(post['created_time'])).strftime('%Y-%m-%d %H:%M:%S')
			if 'message' in post:
				rec['text'] = unicode(post['message']).encode("utf-8")
			else:
				rec['text'] = unicode(post['caption']).encode("utf-8")

			if 'shares' in post:
				rec['shares'] = post['shares']['count']
			else:
				rec['shares'] = 0

			records.append(rec)
			print rec
			print '\n=======================================\n'

	with open('wsj2.csv', 'wb') as f:  # Just use 'w' mode in 3.x
	    w = csv.DictWriter(f, records[0].keys())

	    if flag:
	    	w.writeheader()
	    	flag = 0

	    w.writerows(records)

	if 'paging' in posts:
		nxt = urlparse.parse_qs(posts['paging']['next'])
		untilVal = nxt['until'][0]
		posts = graph.get_connections(pageid, 'posts', until=untilVal, date_format='U', limit=50)
		print "\nGetting data until", untilVal, datetime.datetime.fromtimestamp(int(untilVal)).strftime('%Y-%m-%d %H:%M:%S')
	else:
		break



