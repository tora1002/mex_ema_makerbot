# -*- coding: utf-8 -*-
import sys
import os
from time import sleep
from pathlib import Path
import pymysql.cursors
from sqlalchemy import desc

# set home directory
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# set models path
sys.path.append(os.path.join(app_home, "models"))

# road self models
from coincheck_ticker import CoincheckTicker
from coincheck_6tema_16dema import Coincheck6tema16dema
from coincheck_ema_treade_history import CoincheckEmaTreadeHistory

# set setting path
sys.path.append(os.path.join(app_home, "setting"))

# road self settings
#TODO try-exception at settings file
from db_setting import session
from logger import logger
from coincheck_ccxt import coincheck

#TODO variable
tread_amount = 0.01

### exsit process?
if (os.path.exists("treade_process.txt")):
    # logger & exit batch
    #TODO logger
    sys.exit()

### make file
#Path("treade_process.txt").touch()

### have a position?
position = session.query(CoincheckEmaTreadeHistory).filter_by(status = "open").all()
if len(position) > 1:
    #TODO exception
    sys.exit()
else:
    index_obj = session.query(Coincheck6tema16dema).order_by(desc(Coincheck6tema16dema.id)).limit(1).all()

    for index in index_obj:
        gcross = index.gcross
        dcross = index.dcross
    
    ### if not have a position
    if len(position) == 0:

        ### if Gcross, order bid
        if gcross:
            # get bid price
            ticker = coincheck.fetch_ticker("BTC/JPY")
            ticker_bid = ticker["info"]["bid"]

            # order bid
            request_nonce = datetime.now().strftime("%Y%m%d%H%M%S")
            res = coincheck.create_order(symbol = "BTC/JPY", type = "limit", side = "buy", amount = tread_amount, price = ticker_bid)

            if res["id"] is None:
                #TODO exception

            order_id = res["id"]
            tread_history = session.add(
                Coincheck6tema16dema(
                    order_request_nonce = request_nonce,
                    amount = tread_amount,
                    order_id = order_id,
                    status = "request",
                    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
            )

            session.commit()

            sleep(1)

            # get open orders
            open_orders = coincheck.fetch_open_orders()

            if len(open_orders) > 1:
                #TODO exception
            elif len(open_orders) == 1:
                # cancel order
                coincheck.cancel_order(order_id)
                
                # update database
                tread_history.status("not_position")
                tread_history.updated_at(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                session.commit()
                sys.exit()

            else:
                # get order info
                orders = fetch_my_trades()

                for order in orders:
                    if order["order_id"] == order_id:
                        open_time = order["created_at"]
                        open_rate = order["rate"]

                # uodate database
                tread_history.open_time(open_time)
                tread_history.open_rate(open_rate)
                tread_history.status("open")
                tread_history.updated_at(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                session.commit()
                sys.exit()

    ### if have a position
    else:
        ### if Dcross, order ask
        if dcross:
            order_flg = True
            
            while(order_flg):
                # get ask price
                ticker = coincheck.fetch_ticker("BTC/JPY")
                ticker_bid = ticker["info"]["ask"]

                res = coincheck.create_order(symbol = "BTC/JPY", type = "limit", side = "sell", amount = tread_amount, price = ticker_bid)
                
                if res["id"] is None:
                    #TODO exception

                order_id = res["id"]

                sleep(1)

                # get open orders
                open_orders = coincheck.fetch_open_orders()
            
                if len(open_orders) > 1:
                    #TODO exception
                elif len(open_orders) == 1:
                    # cancel order
                    coincheck.cancel_order(order_id)
                else:
                    order_flg = False

            
            # get order info
            orders = fetch_my_trades()

            for order in orders:
                if order["order_id"] == order_id:
                    close_time = order["created_at"]
                    close_rate = order["rate"]

            # uodate database
            tread_history.close_time(close_time)
            tread_history.close_rate(close_rate)
            tread_history.status("close")
            tread_history.updated_at(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            session.commit()
            sys.exit()

### delete file
#os.remove("treade_process.txt")

