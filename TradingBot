import json
import requests
import time
import datetime

class TradingBot(object):
    def __init__(self, pair, interval, cutoff):
        self.pair = pair
        self.interval = interval
        self.cutoff = cutoff
        self.base_url = 'https://api.uphold.com/v0/ticker'
        self.price_prev = None
        self.price_initial = None

    def get_price(self):
        url = f'{self.base_url}/{self.pair}'
        response = requests.get(url)
        data = simplejson.loads(response.text)
        bid = float(data['bid'])
        ask = float(data['ask'])
        mid = (bid + ask) / 2
        return mid

    def is_big_move(self, price):
        change = abs((price - self.price_initial) / self.price_initial)
        flag = change > self.cutoff
        change = '%.1f' % change
        return flag, change

    def alert(self, ts, change, price):
        print(f'!!!!! As of {ts}, the price {price} has move {change} is larger than cutoff!')

    def run(self):
        while True:
            ts = datetime.datetime.utcnow()
            price = self.get_price()
            if self.price_initial is None:
                print(f'### Setting up initial price={price}')
                self.price_initial = price
            else:
                flag, change = self.is_big_move(price)
                if flag:
                    self.price_initial = self.price_prev  # price
                    self.alert(ts, flag, change, price)
                else:
                    print(f'### As of {ts}, the price {price} has move {change} is smaller than cutoff!')

            self.price_prev = price
            time.sleep(self.interval)


bot = TradingBot('BTC-USD', 3, 0.0005)
bot.run()
