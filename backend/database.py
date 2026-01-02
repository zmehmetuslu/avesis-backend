from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base

#1. depo adresi,veri tabani olusturma
DATABASE_URL="sqlite:///./avesis.db"

#2. motoru calistir,phytonun veri tabanina ulasmasi icin
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False})

#3. oturum fabrikasi
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#4. taban (zemin),Benden türeyen her sınıf veritabanında bir tablo olacak”
Base = declarative_base()


#bu kodlar phytonun bir veri tabani dosyasiyla
#duzgun ve guvenli calismasini saglar