from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# fixed variable
dialect = "mysql"
driver = "pymysql"
username = "root"
password = "rootroot"
host = "localhost"
database = "crypto_databases"
charset_type = "utf8"
db_url = f"{dialect}+{driver}://{username}:{password}@{host}/{database}?charset={charset_type}"

# engine instance for db
#ENGINE = create_engine(db_url, echo=True)
ENGINE = create_engine(db_url, echo=False)

# make session
Session = sessionmaker(bind = ENGINE)
session = Session()

# make base model
Base = declarative_base()

