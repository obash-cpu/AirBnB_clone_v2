#!/usr/bin/python3
"""DBStorage class for AirBnB"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session, relationship
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage():
    """DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initial method"""
        mysql_user = getenv('HBNB_MYSQL_USER')
        mysql_pwd = getenv('HBNB_MYSQL_PWD')
        mysql_host = getenv('HBNB_MYSQL_HOST')
        mysql_db = getenv('HBNB_MYSQL_DB')
        mysql_env = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            mysql_user, mysql_pwd, mysql_host, mysql_db), pool_pre_ping=True)

        """DROP ALL TABLES"""
        if mysql_env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """show all data
        """
        if cls:
            objs = self.__session.query(cls).all()

        else:
            classes = [State, City, User, Place, Review, Amenity]
            objs = []
            for _class in classes:
                objs += self.__session.query(_class)

        """create and save data"""
        new_dict = {}

        for obj in objs:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """Add the object in the databse"""
        if obj:
            self.__session.add(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)

        self.__session = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)

        Session = scoped_session(self.__session)
        self.__session = Session()

    def save(self):
        """Commit all changes of the current
        database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database"""
        if obj:
            self.__session.delete(obj)

    def close(self):
        """
        Closes Session
        """
        self.__session.close()
