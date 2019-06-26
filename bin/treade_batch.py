# -*- coding: utf-8 -*-
import sys
import os
from time import sleep
from pathlib import Path
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
from coincheck_ema_treade_history import CoincheckEmaTreadeHistory
from db_setting import session
from logger import logger
from coincheck_ccxt import coincheck

def get_signal(session):
    signal = {}
    index_desc = Coincheck6tema16dema.get_limit_record_order_desc(session, 1)
        
    for index in index_desc:
        signal["gcross"] = index.gcross
        signal["dcross"] = index.dcross

    return signal

def get_position(session):
    position = CoincheckEmaTreadeHistory.get_record_filter_status(session, "open")

    ### ポジションが1つ以上存在する
    if len(position) > 1:
        raise Exception("Hold multiple position")

    return position

def get_tciker_info(coincheck):
    ticker = coincheck.fetch_ticker("BTC/JPY")
    return ticker["info"]

def create_order(coincheck, side, amount, price):
    res = coincheck.create_order(symbol = "BTC/JPY", type = "limit", side = side, amount = amount, price = price)
    
    if res["id"] is None:
        raise Exception("Can not order")

    return res

def get_open_orders(coincheck):
    open_orders = coincheck.fetch_open_orders()

    if len(open_orders) > 1:
        raise Exception("Hold multiple position")

    return open_orders

def cancel_order(coincheck, order_id):
    coincheck.cancel_order(order_id)

def update_open_data(coincheck, session, tread_history):
    orders = coincheck.fetch_my_trades()

    for order in orders:
        if order["order_id"] == order_id:
            open_time = order["created_at"]
            open_rate = order["rate"]

    tread_history.open_time(open_time)
    tread_history.open_rate(open_rate)
    tread_history.status("open")
    tread_history.updated_at(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    session.commit()

def update_close_data(coincheck, session, tread_history):
    orders = coincheck.fetch_my_trades()

    for order in orders:
        if order["order_id"] == order_id:
            open_time = order["created_at"]
            open_rate = order["rate"]

    tread_history.close_time(close_time)
    tread_history.close_rate(close_rate)
    tread_history.status("close")
    tread_history.updated_at(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    session.commit()

def finish_logger(logger, message):
    logger.info("{0}".format(message))
    logger.info("=== trade_batch finish ===")

if __name__ == "__main__" :

    #TODO いつか変数化する
    tread_amount = 0.01

    logger.info("=== trade_batch start ===")
    
    ### プロセスがないか確認する
    if (os.path.exists("treade_process.txt")):
        finish_logger(logger, "Exist process")
        sys.exit(1)

    ### プロセス起動中ファイルを作成
    Path("treade_process.txt").touch()

    try:
        ### 最新のシグナルを取得
        signal = get_signal(session)
    
        ### ポジションを持っているか？
        position = get_position(session)
    
        ### ポジションを持っていない & Gクロスしていた場合
        if (len(position) == 0) & signal["gcross"]:
        
            logger.info("Gcross & buy order")
            
            # bidの値を取得
            ticker_info = get_tciker_info(coincheck)
            ticker_bid = ticker_info["bid"]

            # 注文
            request_nonce = datetime.now().strftime("%Y%m%d%H%M%S")
            res = create_order(coincheck, side = "buy", amount = tread_amount, price = ticker_bid)

            order_id = res["id"]
            tread_history = CoincheckEmaTreadeHistory.first_insert(session, request_nonce, amount, order_id)

            sleep(1)

            # 未決済のポジションを全て取得 
            open_orders = get_open_orders(coincheck)

            # takeされなかったのでキャンセル & data更新
            if len(open_orders) == 1:
                cancel_order(coincheck, order_id)
                
                tread_history.status("not_position")
                tread_history.updated_at(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                session.commit()
            
                finish_logger(logger, "Not Position")
                sys.exit(1)
            
            # takeされた場合
            else:
                update_open_data(coincheck, session, tread_history)
                finish_logger(logger, "Open position")
                sys.exit(1)
    
        ### ポジションを持っている & Dクロスしていた場合
        if (len(position) == 1) & signal["dcross"]:

            logger.info("Dcross & sell order")
            
            # 変数をセット
            for p in position:
                tread_history = p
            
            # ポジションを解消したいので、orderを出し続けるためのflg
            order_flg = True
            
            while(order_flg):
                # askの値を取得
                ticker_info = get_tciker_info(coincheck)
                ticker_ask = ticker_info["ask"]

                res = create_order(coincheck, side = "sell", amount = tread_amount, price = ticker_ask)
                order_id = res["id"]

                sleep(1)

                # 未決済のポジションを全て取得
                open_orders = get_open_orders(coincheck)

                # takeされなかったのでキャンセル
                if len(open_orders) == 1:
                    cancel_order(coincheck, order_id)
                    logger.info("Can not sell order")
                
                # takeされた場合
                else:
                    update_close_data(coincheck, session, tread_history)
                    order_flg = False
                    finish_logger(logger, "Close  position")
                    sys.exit(1)

    # キャッチして例外をログに記録
    except Exception as e:
        logger.exception(e)
        sys.exit(1)

    ### プロセス終了のため、ファイルを削除
    os.remove("treade_process.txt")
    logger.info("=== trade_batch finish ===")



