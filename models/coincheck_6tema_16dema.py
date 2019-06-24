import os
import sys
from datetime import datetime
from sqlalchemy import Column, BIGINT, DECIMAL, DATETIME, BOOLEAN 

# set home directory
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# set models path
sys.path.append(os.path.join(app_home, "setting"))

# road settings
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
 
def main(args):
    Base.metadata.create_all(bind = ENGINE)

if __name__ == "__main__":
    main(sys.argv)

