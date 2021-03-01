"""
@project: tinigine
@author: kang
@github: https://github.com/fsksf 
@since: 2021/2/1 10:22 PM
"""
import sqlalchemy.exc as sqlexc
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy import create_engine, desc, and_
from sqlalchemy.orm import sessionmaker


from tinigine.config import conf
SQLALCHEMY_DATABASE_URI = conf.get_config()['db']['main']


db = create_engine(SQLALCHEMY_DATABASE_URI)
DBSession = sessionmaker(bind=db)


class ModelMixin:

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base = declarative_base()


class DBConnect:

    def __init__(self):
        self._s = DBSession()

    def __enter__(self):
        return self._s

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._s.close()


class DBUtil:

    @staticmethod
    def select(query_list: list, filter_list: list, obj_type='dict'):
        with DBConnect() as s:
            data = s.query(*query_list).filter(*filter_list).all()
            if obj_type == 'dict':
                if data and isinstance(data[0], Base):
                    data = [d.to_dict() for d in data]
                elif data:
                    fields = [qf.name for qf in query_list]
                    data = [dict(tuple(zip(fields, d))) for d in data]
            elif obj_type == 'tuple':
                if data and isinstance(data[0], Base):
                    data = [tuple(d.to_dict().values) for d in data]
            return data

    @staticmethod
    def insert(model_obj, field_dict_list):
        with DBConnect() as s:
            data = s.add_all([model_obj(**d) for d in field_dict_list])
            s.commit()

    @staticmethod
    def upsert(model_obj, field_dict_list, unique):
        with DBConnect() as s:
            for d in field_dict_list:
                try:
                    s.add(model_obj(**d))
                    s.commit()
                except sqlexc.IntegrityError:
                    filter_list = []
                    s.rollback()
                    for filter_obj in unique:
                        filter_value = d.pop(filter_obj.name)
                        if isinstance(filter_value, (tuple, list)):
                            filter_list.append(filter_obj.in_(filter_value))
                        else:
                            filter_list.append(filter_obj == filter_value)
                    s.query(model_obj).filter(*filter_list).update(d)
                    s.commit()

    @staticmethod
    def update(model_obj, field_dict_list, unique):
        with DBConnect() as s:
            for d in field_dict_list:
                filter_list = []
                for filter_obj in unique:
                    filter_value = d.pop(filter_obj.name)
                    if isinstance(filter_value, (tuple, list)):
                        filter_list.append(filter_obj.in_(filter_value))
                    else:
                        filter_list.append(filter_obj == filter_value)
                s.query(model_obj).filter(*filter_list).update(d)
                s.commit()
