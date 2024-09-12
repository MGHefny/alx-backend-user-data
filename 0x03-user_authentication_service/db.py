#!/usr/bin/env python3
""" Database for ORM """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ add new u_rec
        """
        n_user = User(email=email, hashed_password=hashed_password)
        self._session.add(n_user)
        self._session.commit()
        return n_user

    def find_user_by(self, **kwargs) -> User:
        """ serch user
        """
        record = self._session.query(User)
        for x, y in kwargs.items():
            if x not in User.__dict__:
                raise InvalidRequestError
            for z in record:
                if getattr(z, x) == y:
                    return z
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """ edit user
        """
        f_user = self.find_user_by(id=user_id)

        record = User.__table__.columns.keys()
        for x in kwargs.keys():
            if x not in record:
                raise ValueError

        for x, y in kwargs.items():
            setattr(f_user, x, y)

        self._session.commit()
