# -*- coding: utf-8 -*-
import sys
import os
from time import sleep
from datetime import datetime
from pathlib import Path
import pymysql.cursors
from sqlalchemy import desc

# 親ディレクトリの設定
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# パスの読み込み
sys.path.append(os.path.join(app_home, "models"))
sys.path.append(os.path.join(app_home, "setting"))

# モジュール、設定系の読み込み
from bitmex_ema_trade_history import BitmexEmaTradeHistory
from db_setting import session
from logger import logger
from bitmex_ccxt import bitmex

if __name__ == "__main__" :

    logger.info("=== aggregate_batch start ===")
    
    try:
        #statusがcloseのレコードを取得する
        close_positions = BitmexEmaTradeHistory.get_record_filter_status(session, "close")

        if close_positions is not None:
        
            my_trades = bitmex.fetch_my_trades()
            
            # 1件ずつ、order_idをキーに突合し、抜けているデータを保存する
            for trade_history in close_positions:
                # 変数初期化
                open_time = None
                open_rate = None
                open_order_type = None
                close_time = None
                close_rate = None
                close_order_type = None
 
                for my_trade in my_trades:
                    if my_trade["info"]["orderID"] == trade_history.open_order_id:
                        open_time = my_trade["datetime"].split(".")[0].replace("T", " ")
                        open_rate = my_trade["price"]
                        open_order_type = "maker" if my_trade["fee"]["rate"] < 0 else "taker"
                    if my_trade["info"]["orderID"] == trade_history.close_order_id:
                        close_time = my_trade["datetime"].split(".")[0].replace("T", " ")
                        close_rate = my_trade["price"]
                        close_order_type = "maker" if my_trade["fee"]["rate"] < 0 else "taker"
 
                profit = float(close_rate) - float(open_rate)
 
                # update
                trade_history.status = "agregated"
                trade_history.open_time = datetime.strptime(open_time, "%Y-%m-%d %H:%M:%S")
                trade_history.open_rate = open_rate
                trade_history.open_side = open_order_type
                trade_history.close_time =datetime.strptime(close_time, "%Y-%m-%d %H:%M:%S")
                trade_history.close_rate = close_rate
                trade_history.close_side = close_order_type
                trade_history.profit = profit
                trade_history.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                session.commit()
    
    # キャッチして例外をログに記録
    except Exception as e:
        logger.exception(e)
        sys.exit(1)

    logger.info("=== aggregate_batch finish ===")


