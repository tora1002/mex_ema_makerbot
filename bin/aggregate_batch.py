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
from coincheck_ema_trade_history import CoincheckEmaTradeHistory
from db_setting import session
from logger import logger
from coincheck_ccxt import coincheck

if __name__ == "__main__" :

    logger.info("=== aggregate_batch start ===")
    
    try:
        #statusがcloseのレコードを取得する
        close_positions = CoincheckEmaTradeHistory.get_record_filter_status(session, "close")

        if close_positions is not None:
        
            # 直近の取引履歴25件をcoincheckから取得する
            my_trades = coincheck.get_my_trades()
            
            # 1件ずつ、order_idをキーに突合し、抜けているデータを保存する
            for trade_history in close_positions:
                # 変数初期化
                open_time = None
                open_rate = None
                open_price = None
                close_time = None
                close_rate = None
                close_price = None
 
                for my_trade in my_trades:
                    if my_trade["info"]["order_id"] == trade_history.open_order_id:
                        open_time = my_trade["info"]["created_at"]
                        open_rate = my_trade["info"]["rate"]
                        open_price = my_trade["info"]["funds"]["jpy"]
                    if my_trade["info"]["order_id"] == trade_history.close_order_id:
                        close_time = my_trade["info"]["created_at"]
                        close_rate = my_trade["info"]["rate"]
                        close_price = my_trade["info"]["funds"]["jpy"]
 
                # データ整形
                sharping_open_time = open_time.split(".")[0].replace("T", " ")
                sharping_close_time = close_time.split(".")[0].replace("T", " ")
                profit = float(close_price) + float(open_price)
                print(close_price)
                print(open_price)
 
                # update
                trade_history.status = "agregated"
                trade_history.open_time = datetime.strptime(sharping_open_time, "%Y-%m-%d %H:%M:%S")
                trade_history.open_rate = open_rate
                trade_history.close_time =datetime.strptime(sharping_close_time, "%Y-%m-%d %H:%M:%S")
                trade_history.close_rate = close_rate
                trade_history.profit = profit
                trade_history.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                session.commit()
    
    # キャッチして例外をログに記録
    except Exception as e:
        logger.exception(e)
        sys.exit(1)

    logger.info("=== aggregate_batch finish ===")


