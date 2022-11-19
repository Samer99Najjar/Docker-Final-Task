import time


import redis
from flask import Flask, render_template
from datetime import datetime
import requests

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_bit_coin_price():
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        # requesting data from url
        data = requests.get(key)
        data = data.json()
        print(f"{data['symbol']} price is {data['price']}")
        price = data['price']
        print(price)
        cache.set('price_of_Bitcoin', price)
    except Exception as exp:
        print(exp)
    return price

def get_last_avg():
    bitcoin_history = []
    #key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    while True:
        price= get_bit_coin_price()
        date= datetime.now()
        bitcoin_history.append({'date': date, 'price': price})
        if len(bitcoin_history) ==3 :
            break
        time.sleep(5)
    #print(bitcoin_history)
    sum=0
    for bit in bitcoin_history:
        sum+=float(bit['price'])
    sum=sum/10
    print(sum)
    return sum



@app.route('/')
def hello():
    #count = get_hit_count()
    sum=get_last_avg()
    mystr= "the average pice in last 10 mins is :" +str(sum)
    return mystr

if __name__ == "__main__":
    app.run(host = "0.0.0.0")