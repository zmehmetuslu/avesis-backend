from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse 
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import engine, SessionLocal
import os

# --- 1. AYARLAR ---
# Dosyaları 'main.py' ile aynı yerde ara
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# İzinler
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 2. VERİTABANI BAĞLANTISI
# ---------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# 3. HTML SAYFALARI (DÜZELTİLDİ: Ana Dizinden Okuma)
# ---------------------------------------------------------

# Sadece CSS ve Resimler için 'static' klasörünü bağla
static_path = os.path.join(BASE_DIR, "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

# HTML dosyalarını ana dizinden (BASE_DIR) bulup getiren fonksiyon
def serve_page(filename):
    file_path = os.path.join(BASE_DIR, filename)
    return FileResponse(file_path)

@app.get("/")
def read_root(): return serve_page('index.html')

@app.get("/index.html")
def read_index(): return serve_page('index.html')

@app.get("/arastirmacilar.html")
def read_arastirmacilar(): return serve_page('arastirmacilar.html')

@app.get("/yayinlar.html")
def read_yayinlar(): return serve_page('yayinlar.html')

@app.get("/projeler.html")
def read_projeler(): return serve_page('projeler.html')

@app.get("/tezler.html")
def read_tezler(): return serve_page('tezler.html')

@app.get("/login.html")
def read_login(): return serve_page('login.html')

@app.get("/register.html")
def read_register(): return serve_page('register.html')

@app.get("/panel.html")
def read_panel(): return serve_page('panel.html')

@app.get("/kesfet.html")
def read_kesfet(): return serve_page('kesfet.html')

# ---------------------------------------------------------
# 4. API ENDPOINTLERİ
# ---------------------------------------------------------

@app.post("/register")
def register(user: schemas.RegisterRequest, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı!")
    
    new_user = models.User(name=user.name, email=user.email, password=user.password, role=user.role)
    db.add(new_user)
    
    if user.role == "researcher":
        new_researcher = models.Researcher(name=user.name, email=user.email, field="Genel", profile="#")
        db.add(new_researcher)
    
    db.commit()
    return {"message": "Kayıt Başarılı"}

@app.post("/login")
def login(creds: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == creds.email, models.User.password == creds.password).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Hatalı e-posta veya şifre")
    
    # "undefined" HATASI BURADA ÇÖZÜLDÜ:
    # Frontend 'user_name' bekliyordu, artık onu gönderiyoruz.
    return {"status": "success", "user_name": user.name, "role": user.role}

@app.get("/publications", response_model=List[schemas.PublicationOut])
def get_publications(db: Session = Depends(get_db)):
    pubs = db.query(models.Publication).all()
    return [{"id": p.id, "title": p.title, "type": p.type, "year": p.year, "researcher": p.researcher.name if p.researcher else "Bilinmiyor"} for p in pubs]

@app.post("/publications")
def create_publication(item: schemas.PublicationCreate, db: Session = Depends(get_db)):
    new_pub = models.Publication(title=item.title, type=item.type, year=item.year, researcher_id=item.researcher_id)
    db.add(new_pub); db.commit()
    return {"message": "Yayın başarıyla eklendi"}

@app.get("/researchers", response_model=List[schemas.ResearcherOut])
def get_researchers(db: Session = Depends(get_db)):
    return db.query(models.Researcher).all()

@app.get("/projects", response_model=List[schemas.ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    return [{"id": p.id, "title": p.title, "status": p.status, "year": p.year, "researcher": p.researcher.name if p.researcher else "Bilinmiyor"} for p in projects]

@app.post("/projects")
def create_project(item: schemas.ProjectCreate, db: Session = Depends(get_db)):
    new_project = models.Project(title=item.title, status=item.status, year=item.year, researcher_id=item.researcher_id)
    db.add(new_project); db.commit()
    return {"message": "Proje eklendi"}

@app.get("/theses", response_model=List[schemas.ThesisOut])
def get_theses(db: Session = Depends(get_db)):
    theses = db.query(models.Thesis).all()
    return [{"id": t.id, "title": t.title, "student": t.student, "type": t.type, "year": t.year, "advisor_name": t.advisor.name if t.advisor else "Bilinmiyor"} for t in theses]

@app.post("/theses")
def create_thesis(item: schemas.ThesisCreate, db: Session = Depends(get_db)):
    new_thesis = models.Thesis(title=item.title, student=item.student, type=item.type, year=item.year, advisor_id=item.advisor_id)
    db.add(new_thesis); db.commit()
    return {"message": "Tez eklendi"}

# ---------------------------------------------------------
# 5. BAŞLANGIÇ VERİLERİ
# ---------------------------------------------------------
@app.on_event("startup")
def startup_data():
    db = SessionLocal()
    if not db.query(models.Researcher).first():
        r1 = models.Researcher(name="Dr. Ali Yılmaz", field="Yapay Zeka", email="ali@uni.edu", profile="#")
        db.add(r1); db.commit(); db.refresh(r1)
        
        if not db.query(models.User).filter(models.User.email == "admin@ACADEX.com").first():
            admin = models.User(name="Yönetici", email="admin@ACADEX.com", password="123", role="admin")
            db.add(admin)
            
        p1 = models.Project(title="Akıllı Şehirler", status="Aktif", year=2025, researcher_id=r1.id)
        db.add(p1); db.commit()
    db.close()