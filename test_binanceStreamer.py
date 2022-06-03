import unittest
import websocket
import json

class TestStreamMessage(unittest.TestCase):
    def test_stream_message(self):
        def stream(coin, interval):
            socket = f'wss://stream.binance.com:9443/ws/{coin}@kline_{interval}'

            ws = websocket.create_connection(socket)
            json_message = json.loads(ws.recv())
            symbol = json_message['s']
            print(symbol)
            ws.close()
            return symbol

        self.assertEqual(stream('btcusdt', '1m'), 'BTCUSDT')
        self.assertEqual(stream('ethusdt', '1m'), 'ETHUSDT')
        self.assertEqual(stream('solusdt', '1m'), 'SOLUSDT')