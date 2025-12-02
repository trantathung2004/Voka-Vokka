-- CREATE DATABASE voka;

use voka;

-- CREATE TABLE users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     username VARCHAR(150) UNIQUE NOT NULL,
--     hashed_password VARCHAR(255) NOT NULL
-- );

-- 1. GROUPS TABLE
-- Stores the list shown on the main tab (Image 1) and the footer phrase (Image 2)
drop table if exists group_list;

CREATE TABLE group_list (
    group_id INTEGER PRIMARY KEY AUTO_INCREMENT, -- Unique ID
    group_number INTEGER NOT NULL, -- The display number (e.g., 2)
    title_kr VARCHAR(100) NOT NULL, -- e.g., "탐욕 / 굶주림"
    footer_phrase_en TEXT, -- e.g., "Bite off more than one can chew"
    footer_phrase_kr TEXT -- e.g., "감당할 수 없이 과욕을 부리다"
);

-- 2. WORDS TABLE
-- The master dictionary of English words.
-- Normalized so if 'Voracious' appears in multiple groups, we don't duplicate spelling.
drop table if exists words;

CREATE TABLE words (
    word_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    spelling VARCHAR(100) NOT NULL
    -- phonetic VARCHAR(100)                 -- Optional: e.g., "/vəˈrāSHəs/"
);

-- 3. GROUP_ITEMS TABLE (The Grid View)
-- Links Groups and Words. This controls the specific 'Card' view in Image 2.
-- It stores the 'Summary Meaning' which is distinct from the detailed definition.
drop table if exists group_items;

CREATE TABLE group_items (
    item_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    group_id INTEGER,
    word_id INTEGER,
    display_order INTEGER, -- Controls the grid order (1, 2, 3...)
    summary_meaning VARCHAR(100), -- Short meaning shown on the card (e.g., "탐욕스러운")
    display_letter CHAR(1), -- The big letter shown above meaning (e.g., "V")
    FOREIGN KEY (group_id) REFERENCES group_list (group_id),
    FOREIGN KEY (word_id) REFERENCES words (word_id)
);

-- 4. WORD_DETAILS TABLE (The Popup)
-- Stores the content shown ONLY when a user taps a word.
drop table if exists word_details;

CREATE TABLE word_details (
    detail_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    word_id INTEGER,
    full_definition TEXT, -- Detailed Korean definition
    example_sentence TEXT, -- English example
    example_translation TEXT, -- Korean translation of example
    mnemonic_tip TEXT, -- The memory aid/tip
    FOREIGN KEY (word_id) REFERENCES words (word_id)
);