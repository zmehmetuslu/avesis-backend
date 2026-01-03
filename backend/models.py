from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)

class Researcher(Base):
    __tablename__ = "researchers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    title = Column(String, default="Dr.")
    department = Column(String, default="Bilgisayar Müh.")
    email = Column(String)
    field = Column(String)
    profile = Column(String)
    
    publications = relationship("Publication", back_populates="researcher")
    projects = relationship("Project", back_populates="researcher")

class Publication(Base):
    __tablename__ = "publications"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(String)
    year = Column(Integer)
    researcher_id = Column(Integer, ForeignKey("researchers.id"))
    
    researcher = relationship("Researcher", back_populates="publications")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(String)
    year = Column(Integer)
    description = Column(String, default="")
    researcher_id = Column(Integer, ForeignKey("researchers.id"))
    
    researcher = relationship("Researcher", back_populates="projects")

class Thesis(Base):
    __tablename__ = "theses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    student = Column(String)
    type = Column(String)
    year = Column(Integer)
    advisor_id = Column(Integer, ForeignKey("researchers.id"))
    
    advisor = relationship("Researcher")