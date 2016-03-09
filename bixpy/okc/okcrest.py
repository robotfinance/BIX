import time
import redis
import json
import requests


global r
global status


def getOKCTicker():

	url = 'https://www.okcoin.com/api/v1/ticker.do?symbol=btc_usd'

	while status == True:

		req = requests.get(url)

		print "Status: ", req.status_code
		print "Headers: ", req.headers['content-type']
		#print "Json: ", req.json
		print "Text: ", req.text

		if req.status_code == 200:
			req.ticker = json.loads(req.text)

			ticker = {}
			ticker['source'] = 'okc-rest'
			ticker['ask'] = float(req.ticker['ticker']['sell'])
			ticker['bid'] = float(req.ticker['ticker']['buy'])
        	ticker['mid'] = round((ticker['ask']+ticker['bid'])/2, 2)
        	ticker['ts'] = time.time()
        	okc_rest = json.dumps(ticker, ensure_ascii=False)
        	print "OKC REST: ", okc_rest
        	print r.set('okc-rest', okc_rest)
        	print r.publish('bix-usd', okc_rest)

		time.sleep(1)


if __name__ == '__main__':

	r = redis.StrictRedis(host='localhost', port=6379, db=0)

	status = True

	getOKCTicker()


