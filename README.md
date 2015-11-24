# BIX
an open, fast and free Bitcoin (near) real-time price index

<p><b>Our Goal:</b> to build an open source alternative to TradeBlock's XBX (see https://tradeblock.com/markets/index/). A proprietary index like XBX could have negative effects, because<br>
1. it can easily be manipulated by a central entity<br>
2. it can't be rebuilt at your own machine, so it does not only cost more money to consume Tradeblock's feed, it also adds latency to use data via TradeBlock's "proxy server" in NYC</p>

<p><b>Current exchange weighting:</b><br>
50% Bitfinex, 33,33% Bitstamp and 16,67% Market in Chinese Yen (currently Huobi)<p>

<p><b>Dynamic de-weighting:</b><br>
Exchanges will be de-weighted on a short term basis when<br>
a) order book data does not update for more than 59 seconds<br>
b) it takes more than 1 second to connect to the exchange / the exchange is down</p>

<p>We calculate a <code>Virtual price</code> as soon as there is a problem on one exchange. The Virtual Price is based on the last premium/discount and the last spread of the exchange in drouble and the price movements of the other exchanges that deliver up-to-date data.</p>

<p><b>Demo:</b><br>
https://robotfinance.org/api/bix_alpha/</p>

