from pydantic import BaseModel
from typing import Optional

# --- 1. GİRİŞ VE KAYIT ŞABLONLARI ---

class LoginRequest(BaseModel):
    email: str
    password: str

# HATANIN OLDUĞU YER BURASIYDI (RegisterRequest)
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "student"

# --- 2. VERİ EKLEME ŞABLONLARI (CREATE) ---

class ProjectCreate(BaseModel):
    title: str
    status: str
    year: int
    researcher_id: int

class ThesisCreate(BaseModel):
    title: str
    student: str
    type: str
    year: int
    advisor_id: int

class PublicationCreate(BaseModel):
    title: str
    type: str   # Makale, Bildiri vb.
    year: int
    researcher_id: int

    
# --- 3. VERİ GÖSTERME ŞABLONLARI (OUT) ---

class ResearcherOut(BaseModel):
    id: int
    name: str
    field: str
    email: str
    profile: str
    class Config:
        from_attributes = True 

class ProjectOut(BaseModel):
    id: int
    title: str
    status: str
    year: int
    researcher: str
    class Config:
        from_attributes = True

class ThesisOut(BaseModel):
    id: int
    title: str
    student: str
    type: str
    year: int
    advisor_name: str
    class Config:
        from_attributes = True

class PublicationOut(BaseModel):
    id: int
    title: str
    type: str
    year: int
    researcher: str
    class Config:
        from_attributes = True