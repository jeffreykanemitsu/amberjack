#!/usr/bin/python3
"""
Database storage engine using SQLAlchemy with mysql+mysqldb database connection
"""

import os
from models.base_model import Base
from models.website import Website
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {"Website": Website}


class DBStorage:
    """Database Storage"""

    def __init__(self):
        """Initializes the database object"""
        user = os.getenv('URL_MYSQL_USER')
        passwd = os.getenv('URL_MYSQL_PWD')
        host = os.getenv('URL_MYSQL_HOST')
        database = os.getenv('URL_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, database))

    def all(self, cls=None):
        """returns a dictionary of all the objects present"""
        if not self.__session:
            self.reload()
        objects = {}
        if type(cls) == str:
            cls = classes.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in classes.values():
                for obj in self.__session.query(cls):
                    objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return objects

    def reload(self):
        """reloads objects from the database"""
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """creates a new object"""
        self.__session.add(obj)

    def save(self):
        """saves the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object"""
        if cls is "Website" and id is not None and type(id) is str:
            return self.__session.query(Website).filter(Website.
                                                        short_url == id).first()
        elif cls is not None and type(cls) is str and id is not None and\
           type(id) is str and cls in classes:
            cls = classes[cls]
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
            return None

    def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if type(cls) == str and cls in classes:
            cls = classes[cls]
            total = self.__session.query(cls).count()
        elif cls is None:
            for cls in classes.values():
                total += self.__session.query(cls).count()
        return total

    def get_short(self, cls, long):
        """retrieve a short_url from a website name"""
        if cls == "Website":
            result = self.__session.query(Website).filter(Website.name == long).first()
            return result
