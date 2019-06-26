import os
import sys
from datetime import datetime
from sqlalchemy import Column, BIGINT, DECIMAL, DATETIME 

# 親ディレクトリの設定
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# パス / 設定系の読み込み
sys.path.append(os.path.join(app_home, "setting"))
from db_setting import ENGINE, Base

class CoincheckTicker(Base):
    
    """
    CoincheckTickerModel
    """
    __tablename__ = "coincheck_ticker"
 
    id = Column(BIGINT, primary_key = True, nullable = True)
    request_nonce = Column(BIGINT, nullable = True)
    last = Column(DECIMAL, nullable = True)
    bid = Column(DECIMAL, nullable = True)
    ask = Column(DECIMAL, nullable = True)
    high = Column(DECIMAL, nullable = True)
    low = Column(DECIMAL, nullable = True)
    volume = Column(DECIMAL, nullable = True)
    timestamp = Column(BIGINT, nullable = True)
    server_nonce = Column(BIGINT, nullable = True)
    index_price = Column(DECIMAL, nullable = True)
    created_at = Column(DATETIME, nullable = True)

    ##### insert
    def insert(session, request_nonce, ticker_info, index_price):
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

def main(args):
    Base.metadata.create_all(bind = ENGINE)

if __name__ == "__main__":
    main(sys.argv)

