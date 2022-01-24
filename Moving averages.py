import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web

dir(plt)

plt.style.use('dark_background')

ma1 = 5
ma2 = 22

start = dt.datetime.now() - dt.timedelta(days=365 * 1)
end = dt.datetime.now()

data = web.DataReader('TSLA', 'yahoo', start, end)
print(data)

data[f'SMA_{ma1}'] = data['Adj Close'].rolling(window=ma1).mean()
data[f'SMA_{ma2}'] = data['Adj Close'].rolling(window=ma2).mean()


data = data.iloc[ma2:]


buy_signals = []
sell_signals = []

trigger = 0

for x in range(len(data)):
    if data[f'SMA_{ma1}'].iloc[x] > data[f'SMA_{ma2}'].iloc[x] and trigger != 1:
        buy_signals.append(data['Adj Close'].iloc[x])
        sell_signals.append(float('nan'))
        trigger = 1
    elif data[f'SMA_{ma1}'].iloc[x] < data[f'SMA_{ma2}'].iloc[x] and trigger != -1:
        buy_signals.append(float('nan'))
        sell_signals.append(data['Adj Close'].iloc[x])
        trigger = -1
    else:
        buy_signals.append(float('nan'))
        sell_signals.append(float('nan'))

data['Buy Signals'] = buy_signals
data['Sell Signals'] = sell_signals

print(data)

plt.plot(data['Adj Close'], label='Share Price', alpha=0.5)
plt.plot(data[f'SMA_{ma1}'], label=f'SMA_{ma1}', color='orange', linestyle='--')
plt.plot(data[f'SMA_{ma2}'], label=f'SMA_{ma2}', color='pink', linestyle='--')
plt.scatter(data.index, data['Buy Signals'], label='Buy Signals', marker='^', color='#00ff00', lw=3)
plt.scatter(data.index, data['Sell Signals'], label='Sell Signals', marker='v', color='#ff0000', lw=3)
plt.legend(loc='upper left')
plt.show()
