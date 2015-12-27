# BIX

<i>this is a very early experimental alpha release of BIX (this version does neither support concurrent connections nor websockets and uses a hardcoded USDCNY exchange rate) a more advanced python version will follow soon. we are looking forward to receiving your feedback via mail (bix@robotfinance.org) or Twitter (https://twitter.com/RobotFinance)</i>

BIX is an open, fast and free 
global Bitcoin price index

<p><b>Our Goal:</b> building an open source alternative to TradeBlock's XBX (see https://tradeblock.com/markets/index/). A proprietary index like XBX could have negative effects on Bitcoin market quality, because<br>
1. it can easily be manipulated by a central entity<br>
2. it can't be rebuilt at your own machine, so it does not only cost more money to consume Tradeblock's feed, it also adds latency to use data via TradeBlock's proxy server in NYC</p>

<p><b>Current exchange weightings:</b><br>
50% Bitfinex USD<br>
30% Bitstamp USD<br>
12% Huobi CNY (USD equivalent)<br>
8% Kraken EUR (USD equivalent)<p>

<p><b>Dynamic de-weighting:</b><br>
Exchanges will be de-weighted on a short term basis when<br>
a) order book data does not update for more than 59 seconds<br>
b) it takes more than 1 second to connect to the exchange / the exchange is down</p>

<p>We calculate a <code>Virtual Price</code> as soon as there is a problem on an exchange. The Virtual Price is based on the last premium/discount and the last spread of the de-weighted exchange and the price movements of the other exchanges that deliver up-to-date data.</p>

<p><b>Demo:</b><br>
https://robotfinance.org/api/bix_alpha/</p>

