from fastapi import FastAPI
from app.db.session import Base, engine
from app.db.session import SessionLocal
from app.models import candidates

app = FastAPI(title="RecruitAI")

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "RecruitAI Running"}


@app.get("/version")
def version():
    return {"version":"0.1"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/db-check")
def db_check():
    return {"database": "connected"}