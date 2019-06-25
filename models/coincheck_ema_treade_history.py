import os
import sys
from datetime import datetime
from sqlalchemy import Column, BIGINT, DECIMAL, DATETIME, VARCHAR

# 親ディレクトリの設定
app_home = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".." ))

# パス / 設定系の読み込み
sys.path.append(os.path.join(app_home, "setting"))
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


    ### select
    def get_record_filter_status(session, status):
        return session.query(CoincheckEmaTreadeHistory).filter_by(status = status).all()



    ### insert
    def first_insert(session, request_nonce, amount, order_id):
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

        return tread_history


def main(args):
    Base.metadata.create_all(bind = ENGINE)

if __name__ == "__main__":
    main(sys.argv)

