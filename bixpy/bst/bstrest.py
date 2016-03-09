import time
import redis
import json
import requests


global r
global status


def getBSTTicker():

	url = 'https://www.bitstamp.net/api/ticker/'

	while status == True:

		req = requests.get(url)

		print "Status: ", req.status_code
		print "Headers: ", req.headers['content-type']
		#print "Json: ", req.json
		print "Text: ", req.text

		if req.status_code == 200:
			req.ticker = json.loads(req.text)

			ticker = {}
			ticker['source'] = 'bst-rest'
			ticker['ask'] = float(req.ticker['ask'])
			ticker['bid'] = float(req.ticker['bid'])
        	ticker['mid'] = round((ticker['ask']+ticker['bid'])/2, 2)
        	ticker['ts'] = time.time()
        	bst_rest = json.dumps(ticker, ensure_ascii=False)
        	print "BST REST: ", bst_rest
        	print r.set('bst-rest', bst_rest)
        	print r.publish('bix-usd', bst_rest)

		time.sleep(1)


if __name__ == '__main__':

	r = redis.StrictRedis(host='localhost', port=6379, db=0)

	status = True

	getBSTTicker()


