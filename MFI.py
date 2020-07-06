import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Read stocks file from getStonks.py
with open('tmp.txt') as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
stonks = [x.strip() for x in content] 

print("Value,Symbol,Closing,RSI,MFI")
for stonk in stonks:
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
            if rsi >= 70 and mfi >= 80:
                print("OVERVALUED," + stonk + "," + str(closings[-1]) + "," + str(rsi) + "," + str(mfi))
            elif rsi <= 30 and mfi <= 20:
                print("UNDERVALUED," + stonk + "," + str(closings[-1]) + "," + str(rsi) + "," + str(mfi))  