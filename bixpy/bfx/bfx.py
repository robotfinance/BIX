import ssl
from websocket import create_connection
import time
import json
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

if __name__ == "__main__":

    url = 'wss://api2.bitfinex.com:3000/ws'

    channel = 'ticker'
    pair = 'BTCUSD'
    msg = '{"event":"subscribe","channel":"' + channel + '","pair":"'+ pair +'"}'

    sslopt={'cert_reqs': ssl.CERT_NONE, 'check_hostname': False}
            
    ws = create_connection(url, sslopt=sslopt)
    
    ws.send(msg)
    
    while True:
	tick = ws.recv()
	ticker = tick.split(',')

	if len(ticker) > 4:
            bfx_ticker = {}
            bfx_ticker['source'] = 'bfx'
            bfx_ticker['ask'] = float(ticker[3])
            bfx_ticker['bid'] = float(ticker[1])
            bfx_ticker['mid'] = round((bfx_ticker['ask']+bfx_ticker['bid'])/2, 2)
            bfx_ticker['ts'] = time.time()
            bfx = json.dumps(bfx_ticker, ensure_ascii=False)
            print "BFX: ", bfx
            print r.set('bfx', bfx)
            print r.publish('bix-usd', bfx)
