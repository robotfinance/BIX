import time
import redis
import json
import requests


global r
global status


def getBFXTicker():

	url = 'https://api.bitfinex.com/v1/ticker/btcusd'

	while status == True:

		req = requests.get(url)

		print "Status: ", req.status_code
		print "Headers: ", req.headers['content-type']
		#print "Json: ", req.json
		print "Text: ", req.text

		if req.status_code == 200:
			req.ticker = json.loads(req.text)

			ticker = {}
			ticker['source'] = 'bfx-rest'
			ticker['ask'] = float(req.ticker['ask'])
			ticker['bid'] = float(req.ticker['bid'])
        	ticker['mid'] = round((ticker['ask']+ticker['bid'])/2, 2)
        	ticker['ts'] = time.time()
        	bfx_rest = json.dumps(ticker, ensure_ascii=False)
        	print "BFX REST: ", bfx_rest
        	print r.set('bfx-rest', bfx_rest)
        	print r.publish('bix-usd', bfx_rest)

		time.sleep(1)


if __name__ == '__main__':

	r = redis.StrictRedis(host='localhost', port=6379, db=0)

	status = True

	getBFXTicker()


