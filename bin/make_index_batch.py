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

# 親ディレクトリの設定
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# パスの読み込み
sys.path.append(os.path.join(app_home, "models"))
sys.path.append(os.path.join(app_home, "setting"))

# モジュール、設定系の読み込み
from coincheck_ticker import CoincheckTicker
from coincheck_6tema_16dema import Coincheck6tema16dema
from db_setting import session
from logger import logger
from coincheck_ccxt import coincheck


def get_tciker_info(coincheck):
    ticker = coincheck.fetch_ticker("BTC/JPY")
    return ticker["info"]


if __name__ == "__main__" :

    try:
        logger.info("=== make_index_batch start ===")

        request_nonce = datetime.now().strftime("%Y%m%d%H%M%S")

        ### tickerを取得 & index価格を作成
        ticker_info = get_tciker_info(coincheck)
        index_price = (ticker_info["ask"] +ticker_info["bid"])/2

        ### tickerデータを保存
        CoincheckTicker.insert(session, request_nonce, ticker_info, index_price)

        ### emaデータを取得
        indexs_desc = Coincheck6tema16dema.get_limit_record_order_desc(30)
        
        ### 取得したデータを元に、emaデータを加工
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

        if len(long_index_list) != 0:
            long_index_list.reverse()
            short_index_list.reverse()

        long_index_list.append(index_price)
        short_index_list.append(index_price)

        short_ema = round(float(talib.TEMA(np.array(short_index_list), timeperiod = 6)[-1]), 4)
        long_ema = round(float(talib.DEMA(np.array(long_index_list), timeperiod = 16)[-1]), 4)

        if (np.isnan(short_ema)):
            short_ema = 0
        if (np.isnan(long_ema)):
            long_ema = 0

        ### emaデータからGクロス、Dクロスを判定
        gcross = bool((short_ema > long_ema) & (prev_short_ema < prev_long_ema))
        dcross = bool((short_ema < long_ema) & (prev_short_ema > prev_long_ema))

        ### emaデータを取得
        Coincheck6tema16dema.insert(session, ticker_info["timestamp"], index_price, short_ema, long_ema, gcross, dcross)
        
        logger.info("=== make_index_batch finish ===")

    # キャッチして例外をログに記録
    except Exception as e:
        logger.exception(e)
        sys.exit(1)

