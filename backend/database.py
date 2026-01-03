from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os # YENİ: Bilgisayarın/Sunucunun ayarlarına bakmak için

# 1. AKILLI ADRES SEÇİMİ
# Render'da "DATABASE_URL" diye bir ayar arar. Bulamazsa (senin bilgisayarında) SQLite kullanır.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ACADEX.db")

# Render bazen adresi "postgres://" diye verir ama SQLAlchemy "postgresql://" ister.
# Bu kod o ufak harf hatasını otomatik düzeltir.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. MOTOR AYARLARI
# SQLite için "check_same_thread" lazımdır ama PostgreSQL bunu sevmez, hata verir.
# O yüzden bu ayarı sadece SQLite ise ekliyoruz.
connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

# 3. OTURUM FABRİKASI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. TABAN
Base = declarative_base()