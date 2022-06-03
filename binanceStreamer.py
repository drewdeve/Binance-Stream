import json
import time
import requests
import websocket
from dbWorker import Database
from config import *

db = Database(HOSTNAME, DATABASE, USERNANE, PWD, PORT)
URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

class Binance:
    def __init__(self):
        self.chat_id, self.coin, self.interval = self.get_last_chat_id_and_text(self.get_updates())
        try:
            self.stream_kline()
        except Exception as e:
            print(e)

    def stream_kline(self):
        websocket.enableTrace(False)
        self.socket = f'wss://stream.binance.com:9443/ws/{self.coin}@kline_{self.interval}'
        self.ws = websocket.WebSocketApp(self.socket, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.ws.run_forever()

    def on_message(self, ws, message):
        db.insert_data(message)
        json_message = json.loads(message)
        candle = json_message['k']

        symbol = candle['s']
        interval = candle['i']
        openPrice = float(candle['o'])
        closePrice = float(candle['c'])
        highPrice = float(candle['h'])
        lowPrice = float(candle['l'])
        volume = float(candle['v'])

        text = f'Symbol: {symbol}\nInterval: {interval}\nOpen Price: {openPrice}\nClose Price: {closePrice}\nHigh Price: {highPrice}\nLow Price: {lowPrice}\nVolume: {volume}'
        self.send_message(text, self.chat_id)
        time.sleep(2)

        stop = self.check_for_stop(self.get_updates())
        if stop == '/stop':
            self.ws.close()
          
    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print('Connection Closed')
        print("Retry : %s" % time.ctime())
        time.sleep(10)
        self.stream_kline()

    def get_url(self, url):
        response = requests.get(url)
        return response.text

    def get_json(self, url):
        content_json = json.loads(self.get_url(url))
        return content_json
    
    def get_updates(self):
        url = URL + 'getUpdates'
        content_json = self.get_json(url)
        return content_json

    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates['result'])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        coin = text.split(', ')[0].lower()
        interval = text.split(', ')[1]
        return chat_id, coin, interval
    
    def check_for_stop(self, updates):
        num_updates = len(updates['result'])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        return text

    def send_message(self, text, chat_id):
        url = URL + f'sendMessage?text={text}&chat_id={chat_id}'
        self.get_url(url)

# if __name__ == "__main__":
#     db.drop_table()
#     db.create_table()
#     coin = input('Enter the coin: ').lower()   
#     interval = input('Enter the interval(1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M): ') 
#     Binance()
