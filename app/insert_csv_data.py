import sys
import os
import csv
from sqlalchemy import text

# Ensure we can import from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine

def insert_csv_data():
    print("Connecting to database...")
    
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    groups_file = os.path.join(data_dir, 'groups.csv')
    words_file = os.path.join(data_dir, 'words.csv')
    group_items_file = os.path.join(data_dir, 'group_items.csv')
    word_details_file = os.path.join(data_dir, 'word_details.csv')

    with engine.connect() as connection:
        trans = connection.begin()
        try:
            # 0. Clean up existing data (Optional: for testing purposes, user might want to keep it? 
            # The prompt says "add data", but usually with explicit IDs we might clash.
            # I will use INSERT IGNORE logic or assume empty/clean DB for this specific "turn the data .csv file into... proper files that can later be used to add data" request implies bootstrapping.
            # But valid SQL standard is safer. I'll just use INSERT and let it fail if dupes, or I should truncate?
            # Given previous convo about "Creating Test Data", I'll assume it's fine to clean or just insert.
            # Let's try to just INSERT. If ID conflicts, it will error, which is good feedback.
            
            # Disable FK checks to allow arbitrary order if needed, but we will go in order.
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            
            # Function to read CSV
            def read_csv(filepath):
                with open(filepath, mode='r', encoding='utf-8') as f:
                    return list(csv.DictReader(f))

            # 1. Insert Groups
            print(f"Loading {groups_file}...")
            groups = read_csv(groups_file)
            for row in groups:
                 connection.execute(text("""
                    INSERT INTO group_list (group_id, group_number, title_kr, footer_phrase_en, footer_phrase_kr)
                    VALUES (:group_id, :group_number, :title_kr, :footer_phrase_en, :footer_phrase_kr)
                    ON DUPLICATE KEY UPDATE 
                        title_kr=:title_kr, 
                        footer_phrase_en=:footer_phrase_en, 
                        footer_phrase_kr=:footer_phrase_kr
                """), row)
            print(f"Inserted/Updated {len(groups)} groups.")

            # 2. Insert Words
            print(f"Loading {words_file}...")
            words = read_csv(words_file)
            for row in words:
                connection.execute(text("""
                    INSERT INTO words (word_id, spelling)
                    VALUES (:word_id, :spelling)
                    ON DUPLICATE KEY UPDATE spelling=:spelling
                """), row)
            print(f"Inserted/Updated {len(words)} words.")

            # 3. Insert Group Items
            print(f"Loading {group_items_file}...")
            items = read_csv(group_items_file)
            for row in items:
                connection.execute(text("""
                    INSERT INTO group_items (item_id, group_id, word_id, display_order, summary_meaning, display_letter)
                    VALUES (:item_id, :group_id, :word_id, :display_order, :summary_meaning, :display_letter)
                    ON DUPLICATE KEY UPDATE 
                        group_id=:group_id, 
                        word_id=:word_id, 
                        display_order=:display_order, 
                        summary_meaning=:summary_meaning, 
                        display_letter=:display_letter
                """), row)
            print(f"Inserted/Updated {len(items)} group items.")

            # 4. Insert Word Details
            print(f"Loading {word_details_file}...")
            details = read_csv(word_details_file)
            for row in details:
                connection.execute(text("""
                    INSERT INTO word_details (detail_id, word_id, full_definition, example_sentence, example_translation, mnemonic_tip)
                    VALUES (:detail_id, :word_id, :full_definition, :example_sentence, :example_translation, :mnemonic_tip)
                    ON DUPLICATE KEY UPDATE 
                        full_definition=:full_definition, 
                        example_sentence=:example_sentence, 
                        example_translation=:example_translation, 
                        mnemonic_tip=:mnemonic_tip
                """), row)
            print(f"Inserted/Updated {len(details)} word details.")

            connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            trans.commit()
            print("CSV Data inserted successfully!")

        except Exception as e:
            trans.rollback()
            print(f"Error occurred: {e}")
            print("Rolled back changes.")
            raise

if __name__ == "__main__":
    insert_csv_data()
