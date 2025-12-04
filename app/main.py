from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
import models
from models import (
    QuizAnswerSubmit,
    QuizAnswerResponse,
    HintRequest,
    HintResponse,
)
from database import engine, SessionLocal
from typing import Annotated, Dict, List, Tuple
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import helper_sql
import helper_rag
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

@app.post(
    "/quiz/submit",
    response_model=QuizAnswerResponse,
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Quiz item not found"}
    },
)
def submit_quiz(answer: QuizAnswerSubmit, db: db_dependency):
    result = helper_sql.quiz_answer(
        answer.item_id,
        answer.user_answer,
        answer.group_id,
        answer.user_id,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz item not found",
        )

    return QuizAnswerResponse(**result)

@app.post(
    "/quiz/hint",
    response_model=HintResponse,
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Quiz item not found"},
        500: {"description": "Hint generation failed"},
    },
)
def get_quiz_hint(request: HintRequest, db: db_dependency):
    word_context = helper_sql.get_word_details(request.item_id)
    #test only
    # word_context = {
    #     "spelling": "apple",
    #     "summary_meaning": "fruit",
    #     "full_definition": "a round fruit with a smooth skin and a crisp texture",
    #     "example_sentence": "I like to eat apples",
    #     "example_translation": "나는 사과를 좋아해요",
    #     "mnemonic_tip": "apple is a fruit",
    # }
    if not word_context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz item not found",
        )

    try:
        hint = helper_rag.generate_hint(word_context)
    except helper_rag.HintGenerationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return HintResponse(item_id=request.item_id, hint=hint)