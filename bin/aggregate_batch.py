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
    
    # 直近の取引履歴25件をcoincheckから取得する
    my_trades = coincheck.get_my_trades()

    # 15分以上前の、statusがcloseのレコードを取得する

    


    # 1件ずつ、order_idをキーに突合し、抜けているデータを保存する



    





    logger.info("=== aggregate_batch finish ===")


