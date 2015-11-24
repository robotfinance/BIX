<?php


$rootDir = "/home/";	
$apiDir = "/var/www/robotfinance.org/htdocs/api/bix_alpha/index.php";
$cny_price = 6.3857;

function curl_get_contents($URL)
    {
        $c = curl_init();
        curl_setopt($c, CURLOPT_RETURNTRANSFER, TRUE);
        curl_setopt($c, CURLOPT_SSL_VERIFYPEER, FALSE);
        curl_setopt($c, CURLOPT_TIMEOUT, 1);
        
        curl_setopt($c, CURLOPT_URL, $URL);
        $contents = curl_exec($c);
        curl_close($c);

        if ($contents) return $contents;
            else return $contents = '{"status":0}';
    }



function get_ticker() {

global $rootDir, $apiDir, $cny_price;


// get data from Bitstamp

echo time()." - connecting to Bitstamp....".PHP_EOL.PHP_EOL;

$bitstamp_data = json_decode(curl_get_contents('https://www.bitstamp.net/api/ticker/'));

$ticker_bstmp['bid'] = $bitstamp_data->bid;
$ticker_bstmp['ask'] = $bitstamp_data->ask;
$ticker_bstmp['timestamp'] = $bitstamp_data->timestamp;

	$commFile = $rootDir."comm/bitstamp.last";
	$comm = fopen($commFile, "r");
	$last_bstmp = fread($comm,filesize($commFile));
	fclose($comm);
	$last_bstmp = json_decode($last_bstmp);
	$oldticker_bstmp['bid'] = $last_bstmp->bid;
	$oldticker_bstmp['ask'] = $last_bstmp->ask;
	$oldticker_bstmp['timestamp'] = $last_bstmp->timestamp;
	$oldticker_bstmp['premium'] = $last_bstmp->premium;
	
	$commFile = $apiDir;
	$comm = fopen($apiDir, "r");
	$last_bix = fread($comm,filesize($commFile));
	fclose($comm);
	$last_bix = json_decode($last_bix);
	$oldticker_bix['bid'] = $last_bix->bid;
	$oldticker_bix['ask'] = $last_bix->ask;
	$oldticker_bix['mid'] = $last_bix->mid;
	$oldticker_bix['timestamp'] = $last_bix->ts;

if($ticker_bstmp['bid']>0 && $ticker_bstmp['ask']>0){

	 
	$time_now = time();
	$lastchange_bstmp = $time_now-intval($oldticker_bstmp['timestamp']);

	if($oldticker_bstmp['bid'] == $ticker_bstmp['bid'] && $oldticker_bstmp['ask'] == $ticker_bstmp['ask']) {

		echo time()." - Bitstamp price did not change for ".$lastchange_bstmp." seconds.".PHP_EOL; 
		echo time()." - Bitstamp Ticker: ".json_encode($ticker_bstmp).PHP_EOL.PHP_EOL;

		if($lastchange_bstmp > 59){

		$ticker_bstmp['status'] ='error';	
		
		$ticker_bstmp['spread'] = $oldticker_bstmp['ask'] - $oldticker_bstmp['bid'];
		$ticker_bstmp['ask'] = $oldticker_bix['mid'] + $ticker_bstmp['spread']/2 + $oldticker_bstmp['premium'];
		$ticker_bstmp['bid'] = $oldticker_bix['mid'] - $ticker_bstmp['spread']/2 + $oldticker_bstmp['premium'];
		$ticker_bstmp['timestamp'] = $oldticker_bix['timestamp'];

		echo time()." - Error - Setting virtual price for Bitstamp".PHP_EOL;
		echo time()." - Virtual Bitstamp Ticker: ".json_encode($ticker_bstmp).PHP_EOL;

		} else {

		$ticker_bstmp['status'] ='ok';	
			
		}


	}else{

	$ticker_bstmp['status'] ='ok';		

	$ticker_bstmp['mid'] = ($oldticker_bstmp['bid'] + $oldticker_bstmp['ask'])/2;
	$ticker_bstmp['premium'] = round($ticker_bstmp['mid'] - $oldticker_bix['mid'], 2);

	echo time()." - New Bitstamp Ticker: ".json_encode($ticker_bstmp).PHP_EOL.PHP_EOL;

	$comm = fopen($rootDir."comm/bitstamp.last", "w");
	$comm_message = json_encode($ticker_bstmp);
	fwrite($comm, $comm_message);
	fclose($comm);

	}


}else{

	$ticker_bstmp['status'] ='error';	

	$ticker_bstmp['spread'] = $oldticker_bstmp['ask'] - $oldticker_bstmp['bid'];
	$ticker_bstmp['ask'] = $oldticker_bix['mid'] + $ticker_bstmp['spread']/2 + $oldticker_bstmp['premium'];
	$ticker_bstmp['bid'] = $oldticker_bix['mid'] - $ticker_bstmp['spread']/2 + $oldticker_bstmp['premium'];
	$ticker_bstmp['timestamp'] = $oldticker_bix['timestamp'];

	echo time()." Error - Setting virtual price for Bitstamp".PHP_EOL;
	echo time()." Virtual Bitstamp Ticker: ".json_encode($ticker_bstmp).PHP_EOL.PHP_EOL;

}



// get data from Bitfinex

echo time()." - connecting to Bitfinex....".PHP_EOL.PHP_EOL;

$bitfinex_data = json_decode(curl_get_contents('https://api.bitfinex.com/v1/pubticker/btcusd'));

$ticker_bfx['bid'] = $bitfinex_data->bid;
$ticker_bfx['ask'] = $bitfinex_data->ask;
$ticker_bfx['timestamp'] = $bitfinex_data->timestamp;


	$commFile = $rootDir."comm/bitfinex.last";
	$comm = fopen($commFile, "r");
	$last_bfx = fread($comm,filesize($commFile));
	fclose($comm);
	$last_bfx = json_decode($last_bfx);
	$oldticker_bfx['bid'] = $last_bfx->bid;
	$oldticker_bfx['ask'] = $last_bfx->ask;
	$oldticker_bfx['timestamp'] = $last_bfx->timestamp;
	$oldticker_bfx['premium'] = $last_bfx->premium;
	
	$commFile = $apiDir;
	$comm = fopen($apiDir, "r");
	$last_bix = fread($comm,filesize($commFile));
	fclose($comm);
	$last_bix = json_decode($last_bix);
	$oldticker_bix['bid'] = $last_bix->bid;
	$oldticker_bix['ask'] = $last_bix->ask;
	$oldticker_bix['mid'] = $last_bix->mid;
	$oldticker_bix['timestamp'] = $last_bix->ts;


if($ticker_bfx['bid']>0 && $ticker_bfx['ask']>0){

	 
	$time_now = time();
	$lastchange_bfx = $time_now-intval($oldticker_bfx['timestamp']);

	if($oldticker_bfx['bid'] == $ticker_bfx['bid'] && $oldticker_bfx['ask'] == $ticker_bfx['ask']) {

		echo time()." - Bitfinex price did not change for ".$lastchange_bfx." seconds.".PHP_EOL; 
		echo time()." - Bitfinex Ticker: ".json_encode($ticker_bfx).PHP_EOL.PHP_EOL;

		if($lastchange_bfx > 59){

		$ticker_bfx['status'] ='error';	

		$ticker_bfx['spread'] = $oldticker_bfx['ask'] - $oldticker_bfx['bid'];
		$ticker_bfx['ask'] = $oldticker_bix['mid'] + $ticker_bfx['spread']/2 + $oldticker_bfx['premium'];
		$ticker_bfx['bid'] = $oldticker_bix['mid'] - $ticker_bfx['spread']/2 + $oldticker_bfx['premium'];
		$ticker_bfx['timestamp'] = $oldticker_bix['timestamp'];

		echo time()." - Error - Setting virtual price for Bitfinex".PHP_EOL;
		echo time()." - Virtual Bitfinex Ticker: ".json_encode($ticker_bfx).PHP_EOL;

		} else {

		$ticker_bfx['status'] ='ok';	
			
		}


	}else{

	$ticker_bfx['status'] ='ok';		

	$ticker_bfx['mid'] = ($oldticker_bfx['bid'] + $oldticker_bfx['ask'])/2;
	$ticker_bfx['premium'] = round($ticker_bfx['mid'] - $oldticker_bix['mid'], 2);

	echo time()." - New Bitfinex Ticker: ".json_encode($ticker_bfx).PHP_EOL.PHP_EOL;

	$comm = fopen($rootDir."comm/bitfinex.last", "w");
	$comm_message = json_encode($ticker_bfx);
	fwrite($comm, $comm_message);
	fclose($comm);

	}


}else{


	$ticker_bfx['status'] ='error';	

	$ticker_bfx['spread'] = $oldticker_bfx['ask'] - $oldticker_bfx['bid'];
	$ticker_bfx['ask'] = $oldticker_bix['mid'] + $ticker_bfx['spread']/2 + $oldticker_bfx['premium'];
	$ticker_bfx['bid'] = $oldticker_bix['mid'] - $ticker_bfx['spread']/2 + $oldticker_bfx['premium'];
	$ticker_bfx['timestamp'] = $oldticker_bix['timestamp'];

	echo time()." Error - Setting virtual price for Bitfinex".PHP_EOL;
	echo time()." Virtual Bitfinex Ticker: ".json_encode($ticker_bfx).PHP_EOL.PHP_EOL;



}




// get data from Huobi

echo time()." - connecting to Huobi....".PHP_EOL.PHP_EOL;

$huobi_data = json_decode(curl_get_contents('https://api.huobi.com/staticmarket/ticker_btc_json.js'));

if(isset($huobi_data->ticker->buy)){
$ticker_huobi['bid'] = $huobi_data->ticker->buy;
$ticker_huobi['ask'] = $huobi_data->ticker->sell;
$ticker_huobi['bid'] = round($ticker_huobi['bid']/$cny_price, 2);
$ticker_huobi['ask'] = round($ticker_huobi['ask']/$cny_price, 2);
$ticker_huobi['timestamp'] = $huobi_data->time;
}


	$commFile = $rootDir."comm/huobi.last";
	$comm = fopen($commFile, "r");
	$last_huobi = fread($comm,filesize($commFile));
	fclose($comm);
	$last_huobi = json_decode($last_huobi);
	$oldticker_huobi['bid'] = $last_huobi->bid;
	$oldticker_huobi['ask'] = $last_huobi->ask;
	$oldticker_huobi['timestamp'] = $last_huobi->timestamp;
	$oldticker_huobi['premium'] = $last_huobi->premium;
	
	$commFile = $apiDir;
	$comm = fopen($apiDir, "r");
	$last_bix = fread($comm,filesize($commFile));
	fclose($comm);
	$last_bix = json_decode($last_bix);
	$oldticker_bix['bid'] = $last_bix->bid;
	$oldticker_bix['ask'] = $last_bix->ask;
	$oldticker_bix['mid'] = $last_bix->mid;
	$oldticker_bix['timestamp'] = $last_bix->ts;


if($ticker_huobi['bid']>0 && $ticker_huobi['ask']>0){
	
	 
	$time_now = time();
	$lastchange_huobi = $time_now-intval($oldticker_huobi['timestamp']);

	if($oldticker_huobi['bid'] == $ticker_huobi['bid'] && $oldticker_huobi['ask'] == $ticker_huobi['ask']) {

		echo time()." - Huobi price did not change for ".$lastchange_huobi." seconds.".PHP_EOL;
		echo time()." - New Huobi Ticker: ".json_encode($ticker_huobi).PHP_EOL.PHP_EOL;

		if($lastchange_huobi > 59){

		$ticker_huobi['status'] ='error';	

		$ticker_huobi['spread'] = $oldticker_huobi['ask'] - $oldticker_huobi['bid'];
		$ticker_huobi['ask'] = $oldticker_bix['mid'] + $ticker_huobi['spread']/2 + $oldticker_huobi['premium'];
		$ticker_huobi['bid'] = $oldticker_bix['mid'] - $ticker_huobi['spread']/2 + $oldticker_huobi['premium'];
		$ticker_huobi['timestamp'] = $oldticker_bix['timestamp'];

		echo time()." - Error - Setting virtual price for Huobi".PHP_EOL;
		echo time()." - Last Huobi Ticker: ".json_encode($oldticker_huobi).PHP_EOL;
		echo time()." - Virtual Huobi Ticker: ".json_encode($ticker_huobi).PHP_EOL;

		} else {

		$ticker_huobi['status'] ='ok';	
			
		}


	}else{

	$ticker_huobi['status'] ='ok';		

	$ticker_huobi['mid'] = ($oldticker_huobi['bid'] + $oldticker_huobi['ask'])/2;
	$ticker_huobi['premium'] = round($ticker_huobi['mid'] - $oldticker_bix['mid'], 2);

	echo time()." - New Huobi Ticker: ".json_encode($ticker_huobi).PHP_EOL.PHP_EOL;

	$comm = fopen($rootDir."comm/huobi.last", "w");
	$comm_message = json_encode($ticker_huobi);
	fwrite($comm, $comm_message);
	fclose($comm);

	}



}else{



	$ticker_huobi['status'] ='error';	

	$ticker_huobi['spread'] = $oldticker_huobi['ask'] - $oldticker_huobi['bid'];
	$ticker_huobi['ask'] = $oldticker_bix['mid'] + $ticker_huobi['spread']/2 + $oldticker_huobi['premium'];
	$ticker_huobi['bid'] = $oldticker_bix['mid'] - $ticker_huobi['spread']/2 + $oldticker_huobi['premium'];
	$ticker_huobi['timestamp'] = $oldticker_bix['timestamp'];

	echo time()." - Error - Setting virtual price for Huobi".PHP_EOL;
	echo time()." - Last Huobi Ticker: ".json_encode($oldticker_huobi).PHP_EOL;
	echo time()." - Virtual Huobi Ticker: ".json_encode($ticker_huobi).PHP_EOL.PHP_EOL;

}




// check data and calculate the average best bid and ask price 

$time_now = time();
$latency_bfx = $time_now-intval($ticker_bfx['timestamp']);
$latency_bstmp = $time_now-intval($ticker_bstmp['timestamp']);
$latency_huobi = $time_now-intval($ticker_huobi['timestamp']);
echo time()." - Last Trade - Bitfinex: ".$latency_bfx." / Bitstamp: ".$latency_bstmp." / Huobi: ".$latency_huobi.PHP_EOL;

$ticker['ask'] = round(($ticker_bfx['ask']*3 + $ticker_bstmp['ask']*2 + $ticker_huobi['ask']*1)/6, 2);
$ticker['bid'] = round(($ticker_bfx['bid']*3 + $ticker_bstmp['bid']*2 + $ticker_huobi['bid']*1)/6, 2);
$ticker['mid'] = round(($ticker['ask'] + $ticker['bid'])/2, 2);
$ticker['ts'] = time();

	$comm = fopen($apiDir, "w");
	$comm_message = json_encode($ticker);
	fwrite($comm, $comm_message);
	fclose($comm);

return $ticker;


}



while(true){

	usleep(10000);

    $bix = get_ticker();
 
    echo PHP_EOL.time()." - BIX Ticker: " .json_encode($bix).PHP_EOL;

} 


