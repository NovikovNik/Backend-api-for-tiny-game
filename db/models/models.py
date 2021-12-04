from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, UniqueConstraint, SMALLINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(VARCHAR(50), nullable=True)
    password = Column(VARCHAR(300),nullable=False)
    email = Column(VARCHAR(70))
    
    UniqueConstraint(username, name='username')
    UniqueConstraint(email, name='email')

   
class Hero(Base):
    __tablename__ = 'heroes'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey(f'{User.__tablename__}.{User.id.name}'), nullable=False)
    hero_name = Column(VARCHAR(60), nullable=True)
    user = relationship('User', backref='heroes')