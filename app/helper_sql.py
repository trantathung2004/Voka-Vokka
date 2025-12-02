from database import SessionLocal
from sqlalchemy import text
from decimal import Decimal
from typing import Dict, List, Tuple, Any

def get_group_list():
    db = SessionLocal()
    try:
        query = text("""
        Select 
            group_id, 
            group_number, 
            title_kr 
        From group_list
        """)
        result = db.execute(query).fetchall()
        return [dict(row._mapping) for row in result]
    finally:
        db.close()

def get_group_items(group_id: int):
    db = SessionLocal()
    try:
        query = text("""
        Select 
            g.item_id, 
            g.display_order, 
            g.summary_meaning, 
            g.display_letter, 
            w.spelling
        From group_items g
        Join words w On g.word_id = w.word_id
        Where g.group_id = :group_id
        """)
        result = db.execute(query, {"group_id": group_id}).fetchall()
        return [dict(row._mapping) for row in result]
    finally:
        db.close() 

def get_group_footer(group_id: int):
    db = SessionLocal()
    try:
        query = text("""
        Select 
            footer_phrase_en, 
            footer_phrase_kr 
        From group_list
        Where group_id = :group_id
        """)
        result = db.execute(query, {"group_id": group_id}).fetchone()
        return dict(result._mapping) if result else None
    finally:
        db.close()

def get_word_details(item_id: int):
    db = SessionLocal()
    try:
        query = text("""
        Select 
            w.word_id, 
            w.spelling, 
            wd.full_definition, 
            wd.example_sentence, 
            wd.example_translation, 
            wd.mnemonic_tip 
        From words w
        Join word_details wd On w.word_id = wd.word_id
        Where g.item_id = :item_id
        """)
        result = db.execute(query, {"item_id": item_id}).fetchone()
        return dict(result._mapping) if result else None
    finally:
        db.close()