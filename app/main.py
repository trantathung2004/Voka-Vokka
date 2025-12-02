from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal
from typing import Annotated, Dict, List, Tuple
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import helper_sql
# import auth
# from charts import get_chart_data

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/groups",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Groups not found"}
    })
def get_groups(db: db_dependency):
    results = helper_sql.get_group_list()
    
    if not results:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Groups not found"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=results
        )

@app.get("/groups/{group_id}/items",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Group items not found"}
    })
def get_group_items(group_id: int, db: db_dependency):
    results = helper_sql.get_group_items(group_id)
    
    if not results:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Group items not found"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=results
        )

@app.get("/groups/{group_id}",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Group footer not found"}
    })
def get_group_footer(group_id: int, db: db_dependency):
    results = helper_sql.get_group_footer(group_id)
    
    if not results:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Group footer not found"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=results
        )

@app.get("/items/{item_id}/details",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Word details not found"}
    })
def get_word_details(item_id: int, db: db_dependency):
    results = helper_sql.get_word_details(item_id)
    
    if not results:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Word details not found"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=results
        )

@app.get("/groups/{group_id}/quiz",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Group items not found"}
    })
def get_group_quiz(group_id: int, db: db_dependency):
    pass 

@app.post("/quiz/submit",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Group items not found"}
    })
def submit_quiz(answer: QuizAnswerSubmit, db: db_dependency):
    pass

@app.post("/quiz/hint",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Group items not found"}
    })
def get_quiz_hint(answer: QuizAnswerSubmit, db: db_dependency):
    pass