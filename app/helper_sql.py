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
            gi.item_id,
            gi.summary_meaning,
            gi.display_letter,
            g.group_number,
            w.word_id, 
            w.spelling, 
            wd.full_definition, 
            wd.example_sentence, 
            wd.example_translation, 
            wd.mnemonic_tip 
        From group_items gi
        Join group_list g On gi.group_id = g.group_id
        Join words w On gi.word_id = w.word_id
        Join word_details wd On w.word_id = wd.word_id
        Where gi.item_id = :item_id
        """)
        result = db.execute(query, {"item_id": item_id}).fetchone()
        return dict(result._mapping) if result else None
    finally:
        db.close()

def quiz_answer(item_id: int, user_answer: str, group_id: int, user_id: int):
    """
    Evaluate the user's quiz submission against the stored spelling.
    Currently we only compare the spelling and return a lightweight feedback
    object; future iterations can log attempts keyed by user_id/group_id.
    """
    db = SessionLocal()
    try:
        query = text("""
        Select 
            gi.item_id,
            gi.group_id,
            gi.summary_meaning,
            gi.display_letter,
            w.spelling
        From group_items gi
        Join words w On gi.word_id = w.word_id
        Where gi.item_id = :item_id
          And gi.group_id = :group_id
        """)

        result = db.execute(
            query,
            {"item_id": item_id, "group_id": group_id}
        ).fetchone()

        if not result:
            return None

        row = dict(result._mapping)
        normalized_correct = row["spelling"].strip().lower()
        normalized_user = user_answer.strip().lower()
        is_correct = normalized_correct == normalized_user

        feedback = "Great job! That's correct." if is_correct else "Incorrect, please try again."

        return {
            "is_correct": is_correct,
            "correct_answer": row["spelling"],
            "user_answer": user_answer,
            "feedback": feedback,
        }
    finally:
        db.close()