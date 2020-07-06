# Stock Scripts

> This repository calculates trending indicators MACD, Relative Strength Index (RSI), and MFI (Money Flow Index) and outputs a list of stocks that are considered overvalued or oversold.

## Installation

Use pip install for the following packages:
- BeautifulSoup
- yfinance
- pandas

### Clone

- Clone this repo to your local machine using `https://github.com/mschlesinger19/StockScripts.git`

### Setup

Use the file `getStonks.py > tmp.txt` to update the default stocks list that is pulled from http://gurufocus.com
The default `tmp.txt` should have enough updated stock symbols for setup.

## Running Script

### All Technical Indicators
Run the oversold/overbought screener by running this command `python macd.py > macd_output.csv`
The `macd.py` script outputs the data in a friendly csv format which can then be sorted in Excel.

### RSI/MFI
To only produce a report for RSI and MFI, use the `MFI.py` file.

## Technicals

*MACD* - MACD is considered bullish when the current MACD (difference between the 12 day EMA and the 26 day EMA) is greater than the 9 day EMA. If today's MACD value dips below the 9 day EMA then the stock is considered bearish.

*RSI* - RSI is considered oversold/undervalued when the value is below 30 and overbought/overvalued when the value is above 70.

*MFI* - MFI is considered oversold/undervalued when the value is below 20 and overbought/overvalued when the value is above 80.

## Improvements

Features to come:
- Using python arguments to determind which technical indicators to include
- Using python arguments for files to use for input/output