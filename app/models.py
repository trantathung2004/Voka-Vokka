from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from typing import Optional, List
from pydantic import BaseModel

class Users(Base):
    __tablename__ = "users"

    ID = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True)
    hashed_password = Column(String(255))
    
class Groups(Base):
    __tablename__ = "group_list"

    group_id = Column(Integer, primary_key=True, index=True)
    group_number = Column(Integer, nullable=False)
    title_kr = Column(String(100), nullable=False)
    footer_phrase_en = Column(String(255))
    footer_phrase_kr = Column(String(255))

class Words(Base):
    __tablename__ = "words"

    word_id = Column(Integer, primary_key=True, index=True)
    spelling = Column(String(100), nullable=False)
    # phonetic = Column(String(100))

class GroupItems(Base):
    __tablename__ = "group_items"

    item_id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    word_id = Column(Integer, ForeignKey("words.word_id"))
    display_order = Column(Integer, nullable=False)
    summary_meaning = Column(String(100))
    display_letter = Column(String(1))

class WordDetails(Base):
    __tablename__ = "word_details"

    detail_id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.word_id"))
    full_definition = Column(String(255))
    example_sentence = Column(String(255))
    example_translation = Column(String(255))
    mnemonic_tip = Column(String(255))

class QuizAnswerSubmit(BaseModel):
    item_id: int
    user_answer: str
    group_id: int
    user_id: int

class QuizAnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    user_answer: str
    feedback: str

class HintRequest(BaseModel):
    item_id: int
    # hint_level: int  # 1, 2, or 3
    user_id: int

class HintResponse(BaseModel):
    item_id: int
    hint: str

class GroupItem(BaseModel):
    item_id: int
    spelling: str
    summary_meaning: str
    display_letter: str
    display_order: int

class WordDetail(BaseModel):
    word_id: int
    spelling: str
    full_definition: str
    example_sentence: str
    example_translation: str
    mnemonic_tip: str