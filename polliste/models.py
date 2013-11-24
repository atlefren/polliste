from sqlalchemy import Column, Integer, String, Float, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship, backref

from database import Base

class Pol(Base):
    __tablename__ = 'pol'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    address = Column(String(50))

    def __init__(self, name, **kwargs):
        assert len(name) > 0
        self.name = name
        self.address = kwargs.get("address", None)

class Beer(Base):
    __tablename__ = 'Beer'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    brewery_id = Column(Integer, ForeignKey('brewery.id'))
    style = Column(String(50))
    abv  = Column(Float)
    size = Column(Float)

    def __init__(self, name, brewery, **kwargs):
        assert len(name) > 0
        assert brewery
        self.name = name
        self.brewery =  brewery
        self.style = kwargs.get("style", None)
        self.abv = kwargs.get("abv", None)
        self.size = kwargs.get("size", None)

class Brewery(Base):
    __tablename__ = 'brewery'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    beers = relationship(Beer, backref="brewery")
    def __init__(self, name):
        assert len(name) > 0
        self.name = name

ROLE_USER = 0
ROLE_ADMIN = 1

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    username = Column(String(64), index = True, unique = True)
    email = Column(String(120), index = True, unique = True)
    role = Column(SmallInteger, default = ROLE_USER)
    name = Column(String(120), index = True, unique = True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    def __repr__(self):
        return '<User %r>' % (self.username)
