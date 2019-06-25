import os
import sys
from datetime import datetime
from sqlalchemy import Column, BIGINT, DECIMAL, DATETIME, VARCHAR

# set home directory
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# set models path
sys.path.append(os.path.join(app_home, "setting"))

# road settings
from db_setting import ENGINE, Base

class CoincheckEmaTreadeHistory(Base):

    """
    CoincheckEmaTreadeHistory
    """
    __tablename__ = "coincheck_ema_treade_history"
 
    id = Column(BIGINT, primary_key = True, nullable = True)
    order_request_nonce = Column(BIGINT, nullable = True)
    amount = Column(DECIMAL, nullable = True)
    order_id = Column(BIGINT, nullable = True)
    open_time = Column(DATETIME)
    open_rate = Column(DECIMAL)
    close_time = Column(DATETIME)
    close_rate = Column(DECIMAL)
    status = Column(VARCHAR(20), nullable = True)
    created_at = Column(DATETIME, nullable = True)
 
def main(args):
    Base.metadata.create_all(bind = ENGINE)

if __name__ == "__main__":
    main(sys.argv)

