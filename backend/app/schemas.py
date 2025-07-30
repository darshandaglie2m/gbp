from pydantic import BaseModel, EmailStr

class ProjectBase(BaseModel):
    name: str
    company_details: str | None = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    projects: list[Project] = []
    class Config:
        orm_mode = True
