# -*- coding: utf-8 -*-
import sys
import os
from backports import configparser
import json
from datetime import datetime
import talib
import numpy as np
import pymysql.cursors
from sqlalchemy import desc

# set home directory
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# set models path
sys.path.append(os.path.join(app_home, "models"))

# road self models
from coincheck_ticker import CoincheckTicker
from coincheck_6tema_16dema import Coincheck6tema16dema

# set setting path
sys.path.append(os.path.join(app_home, "setting"))

# road self settings
#TODO try-exception at settings file
from db_setting import session
from logger import logger
from coincheck_ccxt import coincheck

if __name__ == "__main__" :

    # start
    try:
        ### make self nonce
        request_nonce = datetime.now().strftime("%Y%m%d%H%M%S")

        ### get ticker data from api & make index_price
        ticker = coincheck.fetch_ticker("BTC/JPY")
        ticker_info = ticker["info"]
        index_price = (ticker_info["ask"] +ticker_info["bid"])/2

        ### insert & commit coincheck_ticker
        session.add(
            CoincheckTicker(
                request_nonce = request_nonce,
                last = ticker_info["last"],
                bid = ticker_info["bid"],
                ask = ticker_info["ask"],
                high = ticker_info["high"],
                low = ticker_info["low"],
                volume = ticker_info["volume"],
                timestamp = ticker_info["timestamp"],
                server_nonce = datetime.fromtimestamp(ticker_info["timestamp"]).strftime("%Y%m%d%H%M%S"),
                index_price = index_price,
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        session.commit()

        #### get data from coincheck_6tema_16dema at 15period
        indexs_desc = session.query(Coincheck6tema16dema).order_by(desc(Coincheck6tema16dema.id)).limit(30).all()
        
        short_index_list = []
        long_index_list = []
        prev_short_ema = 0
        prev_long_ema = 0

        for index in indexs_desc:
            if prev_short_ema == 0:
                prev_short_ema = float(index.short_ema)
                prev_long_ema = float(index.long_ema)

            long_index_list.append(float(index.index_price))
            
            if (len(short_index_list) < 15):
                short_index_list.append(float(index.index_price))

        # sort asc
        if len(long_index_list) != 0:
            long_index_list.reverse()
            short_index_list.reverse()

        #### make index
        long_index_list.append(index_price)
        short_index_list.append(index_price)

        short_ema = round(float(talib.TEMA(np.array(short_index_list), timeperiod = 6)[-1]), 4)
        long_ema = round(float(talib.DEMA(np.array(long_index_list), timeperiod = 16)[-1]), 4)

        gcross = bool((short_ema > long_ema) & (prev_short_ema < prev_long_ema))
        dcross = bool((short_ema < long_ema) & (prev_short_ema > prev_long_ema))

        # cast to decimal from nan
        if (np.isnan(short_ema)):
            short_ema = 0
        if (np.isnan(long_ema)):
            long_ema = 0

        #### insert coincheck_6tema_16dema
        session.add(
            Coincheck6tema16dema(
                server_nonce = datetime.fromtimestamp(ticker_info["timestamp"]).strftime("%Y%m%d%H%M%S"),
                index_price = index_price,
                short_ema = short_ema,
                long_ema = long_ema,
                gcross = gcross,
                dcross = dcross,
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        session.commit()

    except Exception as e:
        # err
        print(e)
        print("err!!!!!!")


