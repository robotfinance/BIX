import websocket
import time
import sys
import json
import redis
#import hashlib
import zlib
#import base64

def on_open(self):
    self.send("{'event':'addChannel','channel':'ok_sub_spotusd_btc_ticker','binary':'true'}")

def on_message(self,evt):
    data = inflate(evt) 
    print (data)
    ticker = data.split(':')
    if len(ticker) > 4:
        ask_split = ticker[7].split(',')
        bid_split = ticker[3].split(',')
        okc_ticker = {}
        okc_ticker['source'] = 'okc'
        okc_ticker['ask'] = float(ask_split[0])
        okc_ticker['bid'] = float(bid_split[0])
        okc_ticker['mid'] = round((okc_ticker['ask']+okc_ticker['bid'])/2, 2)
        okc_ticker['ts'] = time.time()
        okc = json.dumps(okc_ticker, ensure_ascii=False)
        print "OKC: ", okc
        print r.set('okc', okc)
        print r.publish('bix-usd', okc)

def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

def on_error(self,evt):
    print (evt)

def on_close(self,evt):
    print ('DISCONNECT')

if __name__ == "__main__":

    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    url = "wss://real.okcoin.com:10440/websocket/okcoinapi"

    websocket.enableTrace(False)
    if len(sys.argv) < 2:
        host = url
    else:
        host = sys.argv[1]
    ws = websocket.WebSocketApp(host,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
