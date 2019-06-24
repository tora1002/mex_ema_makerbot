import os
import sys
from datetime import datetime
from sqlalchemy import Column, BIGINT, DECIMAL, DATETIME 

# set home directory
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# set models path
sys.path.append(os.path.join(app_home, "setting"))

# road settings
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
 
def main(args):
    Base.metadata.create_all(bind = ENGINE)

if __name__ == "__main__":
    main(sys.argv)

