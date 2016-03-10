# BIX

<i>this is an experimental beta release of BIX. we are looking forward to receiving your feedback via mail (bix@robotfinance.org) or Twitter (https://twitter.com/RobotFinance)</i>

BIX is a distributed Bitcoin price index<br>
it's open, fast and free

<p><b>Our Goal:</b> building a distributed price feed with<br>
- 100% up-time (no single point of failure)<br>
- no single source of the truth </p>

<p>BIX is an open source alternative to <a href="https://tradeblock.com/markets/index/">TradeBlock's XBX index</a>. We believe that proprietary indices like XBX  have negative effects on market quality, because<br>
1. they can easily be manipulated by a central entity<br>
2. they can't be rebuilt locally, so it does not only cost more money to consume Tradeblock's feed, it also adds latency to receive data via TradeBlock's proxy server in NYC</p>

<p><b>Current exchange weightings:</b><br>
45% Bitfinex USD<br>
35% OKCoin USD<br>
20% Bitstamp USD<br>

<p>BIX uses the mid price calculated from the best bid and ask as reference. Using bids and offers from market makers and other liquidity providers instead of trade data guarantees more regular price updates especially when trade volume is low.</p>

<p><b>Real-Time Fontend Demo:</b> (powered by pubnub.com and D3)<br>
https://robotfinance.org/bix/beta</p>

<p><b>REST API Demo:</b><br>
https://robotfinance.org/api/v1/bix/usd</p>

<p><b>Setup:</b><br><br>
BIXPY follows a multiprocessing rather than a multithreading approach. Redis is used as message broker. You can setup Redis within a few seconds. Here is a short example how to install it on Debian/Ubuntu:</p>

<p><code>$ sudo apt-get install redis-server</code></p>

<p><code>$ sudo pip install redis</code></p>

<p>To push updates to a front-end with PubNub you have to setup the library:</p>

<p><code>$ sudo pip install pubnub</code></p>

Before you start running BIX you have to add your PubNub keys and modify the path for your web server's REST api in the <code>bix.py</code> file:

<p><code>pubnub = Pubnub(publish_key='YOUR-PUB-KEY', subscribe_key='YOUR-SUB-KEY')</code><br>
<code>api_path = '/var/www/yourdomain.org/htdocs/api/v1/bix/yourfile.json'</code></p>

<p><b>Next steps:</b><br>
running BIX on multiple nodes: <br>
- distributed price index calculation<br>
- cross node verification</p>

