from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

# 1. KULLANICILAR TABLOSU (Giriş yapanlar)
class User(Base):
    __tablename__ = "users"

    # İŞTE HATANIN OLDUĞU YER BURASIYDI 👇 (primary_key=True eksikti muhtemelen)
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="student") # student, researcher, admin

# 2. ARAŞTIRMACILAR TABLOSU (Hocalar)
class Researcher(Base):
    __tablename__ = "researchers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    field = Column(String) # Çalışma Alanı
    email = Column(String)
    profile = Column(String) # Profil resmi linki veya web sitesi

    # İlişkiler (Bir hocanın birden çok projesi olabilir)
    projects = relationship("Project", back_populates="researcher")
    publications = relationship("Publication", back_populates="researcher")
    theses = relationship("Thesis", back_populates="advisor")

# 3. PROJELER TABLOSU
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    status = Column(String) # Devam Ediyor / Tamamlandı
    year = Column(Integer)
    
    # Hangi hocaya ait?
    researcher_id = Column(Integer, ForeignKey("researchers.id"))
    researcher = relationship("Researcher", back_populates="projects")

# 4. TEZLER TABLOSU
class Thesis(Base):
    __tablename__ = "theses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    student = Column(String) # Öğrenci Adı
    type = Column(String)    # Yüksek Lisans / Doktora
    year = Column(Integer)

    # Danışman Hoca Kim?
    advisor_id = Column(Integer, ForeignKey("researchers.id"))
    advisor = relationship("Researcher", back_populates="theses")

# 5. YAYINLAR TABLOSU
class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(String) # Makale / Bildiri
    year = Column(Integer)

    researcher_id = Column(Integer, ForeignKey("researchers.id"))
    researcher = relationship("Researcher", back_populates="publications")