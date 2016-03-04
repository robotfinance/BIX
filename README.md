# BIX

<i>this is a very early experimental alpha release of BIX (this version does neither support concurrent connections nor websockets and uses a hardcoded USDCNY exchange rate) a more advanced python version will follow soon. we are looking forward to receiving your feedback via mail (bix@robotfinance.org) or Twitter (https://twitter.com/RobotFinance)</i>

BIX is a decentralized global Bitcoin price index<br>
it's open, fast and free

<p><b>Our Goal:</b> building an open source alternative to TradeBlock's XBX (see https://tradeblock.com/markets/index/). A proprietary index like XBX could have negative effects on Bitcoin market quality, because<br>
1. it can easily be manipulated by a central entity<br>
2. it can't be rebuilt at your own machine, so it does not only cost more money to consume Tradeblock's feed, it also adds latency to use data via TradeBlock's proxy server in NYC</p>

<p><b>Current exchange weightings:</b><br>
50% Bitfinex USD<br>
30% Bitstamp USD<br>
14% Kraken EUR (USD equivalent)<br>
6% Huobi CNY (USD equivalent)<p>

<p><b>Dynamic de-weighting:</b><br>
Exchanges will be de-weighted on a short term basis when<br>
a) order book data does not update for more than 59 seconds<br>
b) it takes more than 1 second to connect to the exchange / the exchange is down</p>

<p>We calculate a <code>Virtual Price</code> as soon as there is a problem on an exchange. The Virtual Price is based on the last premium/discount and the last spread of the de-weighted exchange and the price movements of the other exchanges that deliver up-to-date data.</p>

<p><b>Websocket GUI Demo: (powered by pusher.com)</b><br>
https://robotfinance.org/bix/</p>

<p><b>Websocket API JS Demo: (Los Angeles datacenter)</b><br>
<code>var pusher = new Pusher('cf8d2e4ae29bb0960db7', {encrypted: true});</code><br>
<code>var channel = pusher.subscribe('bix_alpha');</code><br>
<code>channel.bind('price_update', function(data) { alert(data.message); });</code></p>

<p><b>Websocket API JS Demo: (Frankfurt datacenter)</b><br>
<code>var pusher = new Pusher('87a8acb3a5c184357a38', { cluster: 'eu', encrypted: true });</code><br>
<code>var channel = pusher.subscribe('bix_alpha');</code><br>
<code>channel.bind('price_update', function(data) { alert(data.message); });</code></p>

<p><b>REST API Demo:</b><br>
https://la.robotfinance.org/api/bix_alpha/<br>
https://frankfurt.robotfinance.org/api/bix_alpha/</p>
<p>Choose a close location to minimize latency. You can test the response time by using this CURL command:</p>
<p><code>curl -s -w "%{time_total}\n" -o /dev/null https://la.robotfinance.org/api/bix_alpha/</code></p>
<p><code>curl -s -w "%{time_total}\n" -o /dev/null https://frankfurt.robotfinance.org/api/bix_alpha/</code></p>


