"""
Contains the controller for the database
"""
from api.models import Base
from flask import current_app
from api.models.user import User
from api.models.order import Order
from api.models.shipping import Shipping
from api.models.payment import Payment
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """Class for interacting with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'.format(current_app.config['DB_USERNAME'],
                                                                              current_app.config['DB_PASSWORD'],
                                                                              current_app.config['DB_HOSTNAME'],
                                                                              current_app.config['DB_PORT'],
                                                                              current_app.config['DB_NAME']))

        if current_app.config['DB_ENV'] == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls):
        """queries for all objects of entity"""
        new_dict = {}

        if not cls:
            return new_dict

        objs = self.__session.query(cls).all()

        for obj in objs:
            key = obj.__class__.__name__ + '.' + obj.id
            new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def get(self, cls, id):
        """
        Returns the object based on the class and its ID, or
        None if not found
        """
        obj = self.__session.query(cls).get(id)
        if obj:
            return obj

        return None

    def get_by_attr(self, cls, attr, value):
        """
        Returns the object based on the class and its ID, or
        None if not found
        """
        obj = self.__session.query(cls).filter(
            getattr(cls, attr, None) == value
        ).first()
        if obj:
            return obj

        return None

    def close(self):
        """Closes connection to database"""
        self.__session.remove()

    def reload(self):
        """Reloads entities from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
