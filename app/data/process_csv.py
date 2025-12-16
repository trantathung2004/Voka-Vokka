import csv
import os

def process_csv():
    # Input file
    input_file = os.path.join(os.path.dirname(__file__), 'Vocavoka_data.csv')
    
    # Output files
    output_dir = os.path.dirname(__file__)
    group_list_file = os.path.join(output_dir, 'groups.csv')
    words_file = os.path.join(output_dir, 'words.csv')
    group_items_file = os.path.join(output_dir, 'group_items.csv')
    word_details_file = os.path.join(output_dir, 'word_details.csv')

    # Data container
    # 1. Group info (Hardcoded for this single file batch as requested/inferred)
    group_info = {
        'group_id': 1,
        'group_number': 1,
        'title_kr': '탐욕 / 굶주림',
        'footer_phrase_en': 'Bite off more than one can chew',
        'footer_phrase_kr': '감당할 수 없이 과욕을 부리다'
    }

    # Tracking
    words_map = {} # spelling -> word_id
    word_id_counter = 1
    group_items = []
    word_details = []

    print(f"Reading from {input_file}...")
    
    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Check if file has data
        rows = list(reader)
        if not rows:
            print("No data found in CSV.")
            return

        for idx, row in enumerate(rows):
            spelling = row['spelling'].strip()
            
            # --- Populate Words ---
            if spelling not in words_map:
                words_map[spelling] = word_id_counter
                word_id_counter += 1
            
            current_word_id = words_map[spelling]
            
            # --- Populate Group Items ---
            # item_id will be auto-incremented in DB, but for CSV we can just match row id or omit if DB handles it.
            # However, usually for existing data import we might want to specify IDs or let DB handle it.
            # Let's include IDs for CSV to be explicit if needed, or just data. 
            # The Goal is "files that can later be used to add data". 
            # Usually COPY or INSERT assumes columns. 
            # I will include explicit IDs to ensure consistency across the 4 files for this batch.
            
            group_items.append({
                'item_id': idx + 1,
                'group_id': group_info['group_id'],
                'word_id': current_word_id,
                'display_order': idx + 1,
                'summary_meaning': row['summary_meaning'],
                'display_letter': row['display_letter']
            })
            
            # --- Populate Word Details ---
            # Assuming 1:1 for now based on this CSV structure.
            word_details.append({
                'detail_id': idx + 1,
                'word_id': current_word_id,
                'full_definition': row['full_definition'],
                'example_sentence': row['example_sentence'],
                'example_translation': row['example_translation'],
                'mnemonic_tip': row['mnemonic_tip']
            })

    # --- Write Outputs ---

    # 1. groups.csv
    print(f"Writing {group_list_file}...")
    with open(group_list_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['group_id', 'group_number', 'title_kr', 'footer_phrase_en', 'footer_phrase_kr'])
        writer.writerow([
            group_info['group_id'],
            group_info['group_number'],
            group_info['title_kr'],
            group_info['footer_phrase_en'],
            group_info['footer_phrase_kr']
        ])

    # 2. words.csv
    print(f"Writing {words_file}...")
    with open(words_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['word_id', 'spelling'])
        for spelling, w_id in words_map.items():
            writer.writerow([w_id, spelling])

    # 3. group_items.csv
    print(f"Writing {group_items_file}...")
    with open(group_items_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['item_id', 'group_id', 'word_id', 'display_order', 'summary_meaning', 'display_letter'])
        writer.writeheader()
        writer.writerows(group_items)

    # 4. word_details.csv
    print(f"Writing {word_details_file}...")
    with open(word_details_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['detail_id', 'word_id', 'full_definition', 'example_sentence', 'example_translation', 'mnemonic_tip'])
        writer.writeheader()
        writer.writerows(word_details)

    print("Success! Created 4 separate CSV files.")

if __name__ == "__main__":
    process_csv()
