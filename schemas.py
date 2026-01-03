from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str

class ResearcherOut(BaseModel):
    id: int
    name: str
    title: str
    department: str
    email: str
    profile: str
    class Config:
        orm_mode = True

class PublicationCreate(BaseModel):
    title: str
    type: str
    year: int
    researcher_id: int

class PublicationOut(BaseModel):
    id: int
    title: str
    type: str
    year: int
    researcher: str 

class ProjectCreate(BaseModel):
    title: str
    status: str
    year: int
    researcher_id: int

class ProjectOut(BaseModel):
    id: int
    title: str
    status: str
    year: int
    researcher: str

class ThesisCreate(BaseModel):
    title: str
    student: str
    type: str
    year: int
    advisor_id: int

class ThesisOut(BaseModel):
    id: int
    title: str
    student: str
    type: str
    year: int
    advisor_name: str