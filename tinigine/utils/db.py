"""
@project: tinigine
@author: kang
@github: https://github.com/fsksf 
@since: 2021/2/1 10:22 PM
"""
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy import create_engine

from tinigine.config import conf
SQLALCHEMY_DATABASE_URI = conf.get_config()['db']['main']


engine = create_engine(SQLALCHEMY_DATABASE_URI)

Base = declarative_base()
