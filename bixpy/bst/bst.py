import sys
sys.path.append('..')
import time
import pusherclient
import json
import redis

import logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

global pusher

def channel_callback(data):
    ticker = json.loads(data)
    bst_ticker = {}
    bst_ticker['source'] = 'bst'
    bst_ticker['ask'] = float(ticker['asks'][0][0])
    bst_ticker['bid'] = float(ticker['bids'][0][0])
    bst_ticker['mid'] = round((bst_ticker['ask']+bst_ticker['bid'])/2, 2)
    bst_ticker['ts'] = time.time()
    bst = json.dumps(bst_ticker, ensure_ascii=False)
    print "BST: ", bst
    print r.set('bst', bst)
    print r.publish('bix-usd', bst)

def connect_handler(data):
    channel = pusher.subscribe("order_book")

    channel.bind('data', channel_callback)
    

if __name__ == '__main__':

    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    appkey = 'de504dc5763aeef9ff52'

    pusher = pusherclient.Pusher(appkey)

    pusher.connection.bind('pusher:connection_established', connect_handler)
    pusher.connect()

    while True:
        time.sleep(0.1)
