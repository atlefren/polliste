from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base

class Pol(Base):
    __tablename__ = 'pol'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        assert len(name) > 0
        self.name = name

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

