import psycopg2
import json
import uuid

class Database:
    def __init__(self, hostname, database, username, pwd, port_id) :
        self.conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)
        self.cursor = self.conn.cursor()

    def drop_table(self):
        with self.conn:
            self.cursor.execute('DROP TABLE IF EXISTS binance_data')
            self.conn.commit()

    def create_table(self):
        with self.conn:
            table = '''CREATE TABLE IF NOT EXISTS binance_data (
                id text PRIMARY KEY,
                symbol text,
                interval text,
                klineStart bigint,
                klineClose bigint, 
                firstID bigint,
                lastID bigint,
                isCandleClose boolean,
                openPrice real,
                closePrice real,
                highPrice real,
                lowPrice real,
                volume real,
                numTrades bigint, 
                quoteAsset real,
                buyBase real,
                buyQuote real) '''
            self.cursor.execute(table)
            self.conn.commit()

    def insert_data(self, message):
        with self.conn:
            json_message = json.loads(message)
            candle = json_message['k']

            id = str(uuid.uuid4().hex) 
            klineStart = int(candle['t'])
            klineClose = int(candle['T'])
            symbol = candle['s']
            interval = candle['i']
            firstId = int(candle['f'])
            lastId = int(candle['L'])
            isCandleClosed = bool(candle['x'])
            openPrice = float(candle['o'])
            closePrice = float(candle['c'])
            highPrice = float(candle['h'])
            lowPrice = float(candle['l'])
            volume = float(candle['v'])
            numTrades = int(candle['n'])
            quoteAsset = float(candle['q'])
            buyBase = float(candle['V'])
            buyQuote = float(candle['Q'])

            data = (id, symbol, interval, klineStart, klineClose, firstId, lastId, isCandleClosed, openPrice, closePrice, highPrice, lowPrice, volume, numTrades, quoteAsset, buyBase, buyQuote)

            sql = 'INSERT INTO binance_data (id, symbol, interval, klineStart, klineClose, firstID, lastID, isCandleClose, openPrice, closePrice, highPrice, lowPrice, volume, numTrades, quoteAsset, buyBase, buyQuote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            self.cursor.execute(sql, data)
            self.conn.commit()