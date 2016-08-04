import time
import redis
import json
import threading
from pubnub import Pubnub

r = redis.StrictRedis(host='localhost', port=6379, db=0)
pubnub = Pubnub(publish_key='YOUR-PUB-KEY', subscribe_key='YOUR-SUB-KEY')
api_path = '/var/www/yourdomain.org/htdocs/api/v1/bix/yourfile.json'
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
bmx_new = r.get('bmx-rest')



def PubNubcallback(message):
     print(message)



def calculateBIX(bfx_new, okc_new, bst_new, rest_bfx_new, rest_okc_new, rest_bst_new, bmx_new):
    global api_path
    global bix_old
    bfx_weight = 0.5
    bst_weight = 0.22
    okc_weight = 0.28
    
    bfx_ticker = json.loads(bfx_new)
    okc_ticker = json.loads(okc_new)
    bst_ticker = json.loads(bst_new)
    rest_bfx_ticker = json.loads(rest_bfx_new)
    rest_okc_ticker = json.loads(rest_okc_new)
    rest_bst_ticker = json.loads(rest_bst_new)
    bmx_ticker = json.loads(bmx_new)

    time_now = time.time()
    bfx_ticker_age = round((time_now - bfx_ticker['ts'])*1000, 2)
    bfx_rest_ticker_age = round((time_now - rest_bfx_ticker['ts'])*1000, 2)
    okc_ticker_age = round((time_now - okc_ticker['ts'])*1000, 2)
    okc_rest_ticker_age = round((time_now - rest_okc_ticker['ts'])*1000, 2)
    bst_ticker_age = round((time_now - bst_ticker['ts'])*1000, 2)
    bst_rest_ticker_age = round((time_now - rest_bst_ticker['ts'])*1000, 2)
    #print "Age in ms - BFX: ", bfx_ticker_age, "BFX REST: ", bfx_rest_ticker_age, "OKC: ", okc_ticker_age, "OKC REST: ", okc_rest_ticker_age, "BST: ", bst_ticker_age, "BST REST: ", bst_rest_ticker_age  

    if bfx_ticker_age > 10000 and bfx_ticker_age > bfx_rest_ticker_age:
           print "BFX websocket data possibly outdated. Failover to REST."
           bfx_ticker = rest_bfx_ticker
    if okc_ticker_age > 10000 and okc_ticker_age > okc_rest_ticker_age:
           print "OKC websocket data possibly outdated. Failover to REST."
           okc_ticker = rest_okc_ticker
    if bst_ticker_age > 10000 and bst_ticker_age > bst_rest_ticker_age:
           print "BST websocket data possibly outdated. Failover to REST."
           bst_ticker = rest_bst_ticker

    # Adjusting Weightings / Dynamic De-Weighting Mechanism 
    
    av_price = (bmx_ticker['mid']+bfx_ticker['mid']+okc_ticker['mid']+bst_ticker['mid']-max([bfx_ticker['mid'],okc_ticker['mid'],bst_ticker['mid'], bmx_ticker['mid']])-min([bfx_ticker['mid'],okc_ticker['mid'],bst_ticker['mid'],bmx_ticker['mid']]))/2
    bfx_dev = max([av_price, bfx_ticker['mid']]) - min([av_price, bfx_ticker['mid']])
    okc_dev = max([av_price, okc_ticker['mid']]) - min([av_price, okc_ticker['mid']])
    bst_dev = max([av_price, bst_ticker['mid']]) - min([av_price, bst_ticker['mid']])
    
    dev_sum = bfx_dev + okc_dev + bst_dev
    bfx_dev_rel = round(bfx_dev/dev_sum, 2)
    okc_dev_rel = round(okc_dev/dev_sum, 2)
    bst_dev_rel = round(bst_dev/dev_sum, 2)

    bfx_weight_adj = 1-min([1, max([0, (bfx_dev_rel-0.66)*3.5])])
    okc_weight_adj = 1-min([1, max([0, (okc_dev_rel-0.66)*3.5])])
    bst_weight_adj = 1-min([1, max([0, (bst_dev_rel-0.66)*3.5])])

    if bfx_weight_adj < 1:
        adj_bfx_weight = bfx_weight*bfx_weight_adj
        adj_okc_weight = (1-adj_bfx_weight)*okc_weight/(okc_weight+bst_weight)
        adj_bst_weight = (1-adj_bfx_weight)*bst_weight/(okc_weight+bst_weight)
    elif okc_weight_adj < 1:
        adj_okc_weight = okc_weight*okc_weight_adj
        adj_bfx_weight = (1-adj_okc_weight)*bfx_weight/(bfx_weight+bst_weight)
        adj_bst_weight = (1-adj_okc_weight)*bst_weight/(bfx_weight+bst_weight)
    elif bst_weight_adj < 1:
        adj_bst_weight = bst_weight*bst_weight_adj
        adj_bfx_weight = (1-adj_bst_weight)*bfx_weight/(bfx_weight+okc_weight)
        adj_okc_weight = (1-adj_bst_weight)*okc_weight/(bfx_weight+okc_weight)
    else:
        adj_okc_weight = okc_weight
        adj_bfx_weight = bfx_weight
        adj_bst_weight = bst_weight

    print "BFX DEV: ", bfx_dev, bfx_dev_rel, bfx_weight_adj, bfx_weight, adj_bfx_weight
    print "OKC DEV: ", okc_dev, okc_dev_rel, okc_weight_adj, okc_weight, adj_okc_weight
    print "BST DEV: ", bst_dev, bst_dev_rel, bst_weight_adj, bst_weight, adj_bst_weight

    bix_ticker = {}
    bix_ticker['ask'] = round((bfx_ticker['ask']*adj_bfx_weight + okc_ticker['ask']*adj_okc_weight + bst_ticker['ask']*adj_bst_weight), 2)
    bix_ticker['bid'] = round((bfx_ticker['bid']*adj_bfx_weight + okc_ticker['bid']*adj_okc_weight + bst_ticker['bid']*adj_bst_weight), 2)
    bix_ticker['mid'] = round((bix_ticker['ask']+ bix_ticker['bid'])/2, 2)

    if bix_old['ask'] != bix_ticker['ask'] or bix_old['bid'] != bix_ticker['bid']:
    	bix_ticker['ts'] = time.time()
    	bix = json.dumps(bix_ticker, ensure_ascii=False)
    	bix_old['ask'] = bix_ticker['ask']
    	bix_old['bid'] = bix_ticker['bid']
    	print "BIX: ", bix
    	print r.set('bix', bix)
        with open(api_path, 'w') as outfile:
            json.dump(bix_ticker, outfile)
        message = {}
        message['eon'] = {}
        message['eon']['bix'] = bix_ticker['mid']
        message['eon']['bfx'] = bfx_ticker['mid']
        message['eon']['okc'] = okc_ticker['mid']
        message['eon']['bst'] = bst_ticker['mid']
        message['eon']['bmx'] = bmx_ticker['mid']

        pubnub.publish('bix-chart', message, callback=PubNubcallback, error=PubNubcallback)


def main():
    global r, bfx_new, okc_new, bst_new, rest_bfx_new, rest_okc_new, rest_bst_new, bmx_new
    sub = r.pubsub()
    sub.subscribe('bix-usd')
    while True:
        for m in sub.listen():
            if m['data'] != 1:
                print m['data']
                ticker = json.loads(m['data'])
                if ticker['source'] == 'bfx':
                    bfx_new = m['data']
                    calculateBIX(bfx_new, okc_new, bst_new, rest_bfx_new, rest_okc_new, rest_bst_new, bmx_new)
                if ticker['source'] == 'okc':
                    okc_new = m['data']
                    calculateBIX(bfx_new, okc_new, bst_new, rest_bfx_new, rest_okc_new, rest_bst_new, bmx_new)
                if ticker['source'] == 'bst':
                    bst_new = m['data']
                    calculateBIX(bfx_new, okc_new, bst_new, rest_bfx_new, rest_okc_new, rest_bst_new, bmx_new)
                if ticker['source'] == 'bmx-rest':
                    bmx_new = m['data']
            else:
                print m


if __name__ == '__main__':
    main()
