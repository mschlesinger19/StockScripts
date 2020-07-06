import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

print("Indicator,Symbol,Close,macd-hist,rsi,mfi")
def rsi_mfi(stonk):
    stock = yf.Ticker(stonk)

    # get historical market data
    twoWeeks = datetime.today() - timedelta(days=250)

    # Get closing prices
    history = stock.history(start=twoWeeks)
    df = pd.DataFrame(history)
    if not df.empty:
        closings = df['Close'].to_numpy()
        volumes = df['Volume'].to_numpy()
        highs = df['High'].to_numpy()
        lows = df['Low'].to_numpy()
        # Make sure we are trading stocks that are older than 15 days and with a volume of at least 400000
        if volumes[-1] > 400000 and len(closings) >= 15 and closings[-1] > 1:

            # calculate RSI First Averages
            firstAvgGain = 0;
            sumGain = 0;
            firstAvgLoss = 0;
            sumLoss = 0;
            moneyFlow = 0;
            prevTypicalPrice = 0;
            rawMoneyFlow = 0;
            positiveMoneyFlow = []
            negativeMoneyFlow = []

            # Loop through first 14 values for RSI Calculation
            for i in range(0, 14):
                change = closings[i] - closings[i - 1]
                if (change >= 0):
                    sumGain += change
                elif (change < 0):
                    sumLoss += abs(change)
                # MFI Calculations
                typicalPrice = (highs[i] + lows[i] + closings[i]) / 3
                rawMoneyFlow = typicalPrice * volumes[i]
                if typicalPrice >= prevTypicalPrice:
                    positiveMoneyFlow.append(rawMoneyFlow)
                    negativeMoneyFlow.append(0.0)
                else:
                    negativeMoneyFlow.append(rawMoneyFlow)
                    positiveMoneyFlow.append(0.0)
                prevTypicalPrice = typicalPrice
            # Do calculations needed for RSI estimations
            firstAvgGain = sumGain / 14
            firstAvgLoss = sumLoss / 14
            if firstAvgLoss == 0.0:
                rs = 100
            else:
                rs = firstAvgGain / firstAvgLoss
            rsi = 100
            if rs != 0:
                rsi = 100-(100/(1+rs))
            avgGain = firstAvgGain
            avgLoss = firstAvgLoss
            # MFI Last 14
            sumPositiveMF = sum(positiveMoneyFlow)
            sumNegativeMF = sum(negativeMoneyFlow)
            if sumNegativeMF == 0.0:
                moneyFlowRatio = 100.0
            else:
                moneyFlowRatio = sumPositiveMF / sumNegativeMF
            mfi = 100 - (100 / (1 + moneyFlowRatio))
            # Loop through rest of data
            for i in range (14, len(closings)):
                # RSI Calculations
                change = closings[i] - closings[i - 1]
                if change >= 0:
                    avgGain = (avgGain * 13 + change) / 14
                    avgLoss = (avgLoss * 13 + 0) / 14
                elif change < 0:
                    avgGain = (avgGain * 13 + 0) / 14
                    avgLoss = (avgLoss * 13 + abs(change)) / 14
                # MFI Calculations
                positiveMoneyFlow.pop(0)
                negativeMoneyFlow.pop(0)
                typicalPrice = (highs[i] + lows[i] + closings[i]) / 3
                rawMoneyFlow = typicalPrice * volumes[i]
                if typicalPrice >= prevTypicalPrice:
                    positiveMoneyFlow.append(typicalPrice)
                    negativeMoneyFlow.append(0.0)
                else:
                    negativeMoneyFlow.append(typicalPrice)
                    positiveMoneyFlow.append(0.0)
                prevTypicalPrice = typicalPrice
            if avgLoss == 0.0:
                rs = 100
            else:
                rs = avgGain / avgLoss
            rsi = 100 - (100 /( 1 + rs))
            # MFI Calculations
            sumPositiveMF = sum(positiveMoneyFlow)
            sumNegativeMF = sum(negativeMoneyFlow)
            if sumNegativeMF == 0.0:
                moneyFlowRatio = 100
            else:
                moneyFlowRatio = sumPositiveMF / sumNegativeMF
            mfi = 100 - (100 / (1 + moneyFlowRatio))
            return rsi, mfi


SMOOTH_12 = 2 / (1 + 12)
SMOOTH_26 = 2 / (1 + 26)
SMOOTH_9 = 2 / (1 + 9)
# Read stocks file from getStonks.py
with open('tmp.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
stonks = [x.strip() for x in content] 

for stonk in stonks:
    stock = yf.Ticker(stonk)

    # get historical market data
    twoWeeks = datetime.today() - timedelta(days=100)

    # Get closing prices
    history = stock.history(start=twoWeeks)
    df = pd.DataFrame(history)
    if not df.empty:
        closings = df['Close'].to_numpy()
        volumes = df['Volume'].to_numpy()
        # Make sure we are trading stocks that are older than 26 days and with a volume of at least 400000
        if volumes[-1] > 400000 and len(closings) >= 36 and closings[-1] > 1:
            sum12 = 0.0
            sum26 = 0.0
            ema_12 = 0.0
            prevEMA_12 = 0.0
            prevEMA_26 = 0.0
            ema_26 = 0.0
            prevEMA_9 = 0.0
            ema_9 = 0.0
            macd = []
            # Calculate 12 day EMA
            for i in range(0, 12):
                sum12 += closings[i]
                sum26 += closings[i]
            # Get first EMA of 12-day
            prevEMA_12 = sum12 / 12
            for i in range (12, 26):
                ema_12 = (closings[i] * SMOOTH_12) + (prevEMA_12 * (1 - SMOOTH_12))
                prevEMA_12 = ema_12
                sum26 += closings[i]
            # Get first EMA of 26-day
            prevEMA_26 = sum26 / 26
            # Calculate MACD
            macd_today = ema_12 - prevEMA_26
            macd.append(macd_today)
            for i in range(26, 34):
                ema_12 = (closings[i] * SMOOTH_12) + (prevEMA_12 * (1 - SMOOTH_12))
                prevEMA_12 = ema_12
                ema_26 = (closings[i] * SMOOTH_26) + (prevEMA_26 * (1 - SMOOTH_26))
                prevEMA_26 = ema_26
                macd_today = ema_12 - ema_26
                macd.append(macd_today)
            prevEMA_9 = sum(macd) / 9
            for i in range(34, len(closings)):
                ema_12 = (closings[i] * SMOOTH_12) + (prevEMA_12 * (1 - SMOOTH_12))
                prevEMA_12 = ema_12
                ema_26 = (closings[i] * SMOOTH_26) + (prevEMA_26 * (1 - SMOOTH_26))
                prevEMA_26 = ema_26
                macd_today = ema_12 - ema_26
                macd.pop(0)
                macd.append(macd_today)
                ema_9 = (macd_today * SMOOTH_9) + (prevEMA_9 * (1 - SMOOTH_9))
                prevEMA_9 = ema_9
            if (macd[-2] > ema_9 and macd[-1] < ema_9):
                rsi, mfi = rsi_mfi(stonk)
                print("Bearish," + stonk + "," + str(closings[-1]) + "," + str(macd[-1] - ema_9) + "," + str(rsi) + "," + str(mfi))
            elif (macd[-2] < ema_9 and macd[-1] > ema_9):
                rsi, mfi = rsi_mfi(stonk)
                print("Bullish," + stonk + "," + str(closings[-1]) + "," + str(macd[-1] - ema_9) + "," + str(rsi) + "," + str(mfi))