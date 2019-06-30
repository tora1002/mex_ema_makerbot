import os
import sys
from datetime import datetime
from sqlalchemy import Column, BIGINT, DECIMAL, DATETIME, VARCHAR

# 親ディレクトリの設定
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# パス / 設定系の読み込み
sys.path.append(os.path.join(app_home, "setting"))
from db_setting import ENGINE, Base

class CoincheckEmaTradeHistory(Base):

    """
    CoincheckEmaTradeHistory
    """
    __tablename__ = "coincheck_ema_trade_history"
 
    id = Column(BIGINT, primary_key = True, nullable = True)
    order_request_nonce = Column(BIGINT, nullable = True)
    amount = Column(DECIMAL, nullable = True)
    status = Column(VARCHAR(20), nullable = True)
    open_order_id = Column(BIGINT, nullable = True)
    open_time = Column(DATETIME)
    open_rate = Column(DECIMAL)
    close_order_id = Column(BIGINT)
    close_time = Column(DATETIME)
    close_rate = Column(DECIMAL)
    profit = Column(BIGINT)
    created_at = Column(DATETIME, nullable = True)
    updated_at = Column(DATETIME, nullable = True)

    ### select
    def get_record_filter_status(session, postion_status):
        return session.query(CoincheckEmaTradeHistory).filter_by(status = postion_status).all()

def main(args):
    Base.metadata.create_all(bind = ENGINE)

if __name__ == "__main__":
    main(sys.argv)

