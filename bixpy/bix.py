import time
import redis
import json
import threading
import pprint

r = redis.StrictRedis(host='localhost', port=6379, db=0)
api_path = '/var/www/robotfinance.org/htdocs/api/v1/bix/usd/index.html'
bix_old = {}
bix_old['ask'] = 0
bix_old['bid'] = 0

bfx_old = ''
okc_old = ''
bst_old = ''
rest_bfx_old = ''
rest_okc_old = ''
rest_bst_old = ''

bfx_new = r.get('bfx')
okc_new = r.get('okc')
bst_new = r.get('bst')
rest_bfx_new = r.get('bfx-rest')
rest_okc_new = r.get('okc-rest')
rest_bst_new = r.get('bst-rest')

def callback():
    global r, bfx_new, okc_new, bst_new, rest_bfx_new, rest_okc_new, rest_bst_new
    sub = r.pubsub()
    sub.subscribe('bix-usd')
    while True:
        for m in sub.listen():
            if m['data'] != 1:
                print m['data']
                ticker = json.loads(m['data'])
                if ticker['source'] == 'bfx':
                    bfx_new = m['data']
                    calculateBIX(bfx_new, okc_new, bst_new, rest_bfx_new, rest_okc_new, rest_bst_new)
                if ticker['source'] == 'okc':
                    okc_new = m['data']
                    calculateBIX(bfx_new, okc_new, bst_new, rest_bfx_new, rest_okc_new, rest_bst_new)
                if ticker['source'] == 'bst':
                    bst_new = m['data']
                    calculateBIX(bfx_new, okc_new, bst_new, rest_bfx_new, rest_okc_new, rest_bst_new)
            else:
                print m



def calculateBIX(bfx_new, okc_new, bst_new, rest_bfx_new, rest_okc_new, rest_bst_new):
    global api_path
    global bix_old
    bfx_ticker = json.loads(bfx_new)
    okc_ticker = json.loads(okc_new)
    bst_ticker = json.loads(bst_new)
    rest_bfx_ticker = json.loads(rest_bfx_new)
    rest_okc_ticker = json.loads(rest_okc_new)
    rest_bst_ticker = json.loads(rest_bst_new)

    time_now = time.time()
    bfx_ticker_age = round((time_now - bfx_ticker['ts'])*1000, 2)
    bfx_rest_ticker_age = round((time_now - rest_bfx_ticker['ts'])*1000, 2)
    okc_ticker_age = round((time_now - okc_ticker['ts'])*1000, 2)
    okc_rest_ticker_age = round((time_now - rest_okc_ticker['ts'])*1000, 2)
    bst_ticker_age = round((time_now - bst_ticker['ts'])*1000, 2)
    bst_rest_ticker_age = round((time_now - rest_bst_ticker['ts'])*1000, 2)
    #print "Age in ms - BFX: ", bfx_ticker_age, "BFX REST: ", bfx_rest_ticker_age, "OKC: ", okc_ticker_age, "OKC REST: ", okc_rest_ticker_age, "BST: ", bst_ticker_age, "BST REST: ", bst_rest_ticker_age  

    if bfx_ticker_age > 10000 and bfx_rest_ticker_age < 5000:
    	print "BFX websocket data possibly outdated. Failover to REST."
    	bfx_ticker = rest_bfx_ticker
    if okc_ticker_age > 10000 and okc_rest_ticker_age < 5000:
    	print "OKC websocket data possibly outdated. Failover to REST."
    	okc_ticker = rest_okc_ticker
    if bst_ticker_age > 10000 and bst_rest_ticker_age < 5000:
    	print "BST websocket data possibly outdated. Failover to REST."
    	bst_ticker = rest_bst_ticker

    bix_ticker = {}
    bix_ticker['ask'] = round((bfx_ticker['ask']*45 + okc_ticker['ask']*35 + bst_ticker['ask']*20)/100, 2)
    bix_ticker['bid'] = round((bfx_ticker['bid']*45 + okc_ticker['bid']*35 + bst_ticker['bid']*20)/100, 2)

    if bix_old['ask'] != bix_ticker['ask'] or bix_old['bid'] != bix_ticker['bid']:
    	bix_ticker['mid'] = round((bix_ticker['ask']+ bix_ticker['bid'])/2, 2)
    	bix_ticker['ts'] = time.time()
    	bix = json.dumps(bix_ticker, ensure_ascii=False)
    	bix_old['ask'] = bix_ticker['ask']
    	bix_old['bid'] = bix_ticker['bid']
    	print "BIX: ", bix
    	print r.set('bix', bix)
        with open(api_path, 'w') as outfile:
            json.dump(bix_ticker, outfile)


def main():
        
    t = threading.Thread(target=callback)
    t.setDaemon(True)
    t.start()

    while True:
        print 'Listening...'
        time.sleep(10)
    	



if __name__ == '__main__':
    main()