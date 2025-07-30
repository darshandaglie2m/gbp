from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database, google

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="GBP Manager")

# Dependency

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users/', response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@app.post('/users/{user_id}/projects/', response_model=schemas.Project)
def create_project_for_user(user_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project, user_id)
@app.get('/projects/{project_id}', response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project
@app.get('/users/{user_id}/projects/', response_model=list[schemas.Project])
def list_projects(user_id: int, db: Session = Depends(get_db)):
    return crud.get_projects(db, user_id)

@app.post('/projects/{project_id}/audit')
async def audit_project(project_id: int, db: Session = Depends(get_db)):
  
    project = crud.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    details = {}
    reviews = []
    if project.gbp_location_id:
        try:
            details = google.fetch_gbp_details(project.gbp_location_id)
            reviews = google.fetch_reviews(project.gbp_location_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    recommendations = await google.analyze_gbp(details, [r.get('comment', '') for r in reviews])
    return {"details": details, "reviews": reviews, "recommendations": recommendations}
    # Stub: pull details from google business APIs
    details = {"project_id": project_id, "info": "dummy"}
    reviews = []
    recommendations = await google.analyze_gbp(details, reviews)
    return {"recommendations": recommendations}
