import sys
import os
from sqlalchemy import text

# Ensure we can import from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine

def insert_test_data():
    print("Connecting to database...")
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            # 1. Insert Group
            print("Inserting Group 'Basic Emotions'...")
            connection.execute(text("""
                INSERT INTO group_list (group_number, title_kr, footer_phrase_en, footer_phrase_kr)
                VALUES (1, '기본 감정', 'Emotions make us human', '감정은 우리를 인간답게 만든다');
            """))
            
            # Get the group_id
            result = connection.execute(text("SELECT LAST_INSERT_ID()"))
            group_id = result.scalar()
            print(f"Created Group ID: {group_id}")

            words_data = [
                {
                    "spelling": "Happy",
                    "summary": "행복한",
                    "letter": "H",
                    "def": "Feeling or showing pleasure or contentment.",
                    "ex": "I am so happy today.",
                    "ex_tr": "나는 오늘 너무 행복해.",
                    "tip": "Think of a smiling face."
                },
                {
                    "spelling": "Sad",
                    "summary": "슬픈",
                    "letter": "S",
                    "def": "Feeling or showing sorrow; unhappy.",
                    "ex": "The movie was very sad.",
                    "ex_tr": "그 영화는 매우 슬펐어.",
                    "tip": "Think of tears."
                },
                {
                    "spelling": "Angry",
                    "summary": "화난",
                    "letter": "A",
                    "def": "Having a strong feeling of or showing annoyance, displeasure, or hostility.",
                    "ex": "He was angry about the mistake.",
                    "ex_tr": "그는 그 실수에 대해 화가 났다.",
                    "tip": "Red face."
                },
                {
                    "spelling": "Excited",
                    "summary": "신난",
                    "letter": "E",
                    "def": "Very enthusiastic and eager.",
                    "ex": "She is excited about the trip.",
                    "ex_tr": "그녀는 여행에 대해 들떠 있다.",
                    "tip": "Jumping up and down."
                },
                {
                    "spelling": "Nervous",
                    "summary": "긴장한",
                    "letter": "N",
                    "def": "Easily agitated or alarmed; tending to be anxious; highly strung.",
                    "ex": "I get nervous before exams.",
                    "ex_tr": "나는 시험 전에 긴장해.",
                    "tip": "Shaking hands."
                }
            ]

            for i, w in enumerate(words_data, 1):
                print(f"Inserting Word: {w['spelling']}")
                # Insert Word
                connection.execute(text("INSERT INTO words (spelling) VALUES (:spelling)"), {"spelling": w['spelling']})
                
                result = connection.execute(text("SELECT LAST_INSERT_ID()"))
                word_id = result.scalar()

                # Insert Group Item
                connection.execute(text("""
                    INSERT INTO group_items (group_id, word_id, display_order, summary_meaning, display_letter)
                    VALUES (:group_id, :word_id, :order, :summary, :letter)
                """), {
                    "group_id": group_id,
                    "word_id": word_id,
                    "order": i,
                    "summary": w['summary'],
                    "letter": w['letter']
                })

                # Insert Word Details
                connection.execute(text("""
                    INSERT INTO word_details (word_id, full_definition, example_sentence, example_translation, mnemonic_tip)
                    VALUES (:word_id, :def, :ex, :ex_tr, :tip)
                """), {
                    "word_id": word_id,
                    "def": w['def'],
                    "ex": w['ex'],
                    "ex_tr": w['ex_tr'],
                    "tip": w['tip']
                })

            trans.commit()
            print("Test data inserted successfully!")
        except Exception as e:
            trans.rollback()
            print(f"Error occurred: {e}")
            print("Rolled back changes.")
            raise

if __name__ == "__main__":
    insert_test_data()
