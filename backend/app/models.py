from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    projects = relationship('Project', back_populates='owner')

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company_details = Column(Text)
    
gbp_location_id = Column(String, index=True)
ga_property_id = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='projects')
