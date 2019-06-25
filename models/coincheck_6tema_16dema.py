import os
import sys
from datetime import datetime
from sqlalchemy import Column, BIGINT, DECIMAL, DATETIME, BOOLEAN 

# 親ディレクトリの設定
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# パス / 設定系の読み込み
sys.path.append(os.path.join(app_home, "setting"))
from db_setting import ENGINE, Base

class Coincheck6tema16dema(Base):
    
    """
    Coincheck6tema16demaModel
    """
    __tablename__ = "coincheck_6tema_16dema"
 
    id = Column(BIGINT, primary_key = True, nullable = True)
    server_nonce = Column(BIGINT, nullable = True)
    index_price = Column(DECIMAL, nullable = True)
    short_ema = Column(DECIMAL)
    long_ema = Column(DECIMAL)
    gcross = Column(BOOLEAN, nullable = True)
    dcross = Column(BOOLEAN, nullable = True)
    created_at = Column(DATETIME, nullable = True)

    ##### select
    def get_limit_record_order_desc(session, limit_num):
        return session.query(Coincheck6tema16dema).order_by(desc(Coincheck6tema16dema.id)).limit(limit_num).all()

    ##### insert
    def insert(session, ticker_timestamp, index_price, short_ema, long_ema, gcross, dcross)
        session.add(
            Coincheck6tema16dema(
                server_nonce = datetime.fromtimestamp(ticker_timestamp).strftime("%Y%m%d%H%M%S"),
                index_price = index_price,
                short_ema = short_ema,
                long_ema = long_ema,
                gcross = gcross,
                dcross = dcross,
                created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        session.commit()


def main(args):
    Base.metadata.create_all(bind = ENGINE)

if __name__ == "__main__":
    main(sys.argv)

