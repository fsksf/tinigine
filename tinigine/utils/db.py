"""
@project: tinigine
@author: kang
@github: https://github.com/fsksf 
@since: 2021/2/1 10:22 PM
"""
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

from tinigine.config import conf
SQLALCHEMY_DATABASE_URI = conf.get_config()['db']['main']


db = create_engine(SQLALCHEMY_DATABASE_URI)
DBSession = sessionmaker(bind=db)
Base = declarative_base()


class DBConnect:

    def __init__(self):
        self._s = DBSession()

    def __enter__(self):
        return self._s

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._s.close()