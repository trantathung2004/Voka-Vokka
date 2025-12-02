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
    __tablename__ = "groups"

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

