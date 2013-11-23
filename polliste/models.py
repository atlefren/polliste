from sqlalchemy import Column, Integer, String

from database import Base

class Pol(Base):
    __tablename__ = 'pol'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        assert len(name) > 0
        self.name = name

class Brewery(Base):
    __tablename__ = 'brewery'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        assert len(name) > 0
        self.name = name