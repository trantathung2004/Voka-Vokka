USE voka;

-- 1. Insert Group
INSERT INTO
    group_list (
        group_number,
        title_kr,
        footer_phrase_en,
        footer_phrase_kr
    )
VALUES (
        1,
        '기본 감정',
        'Emotions make us human',
        '감정은 우리를 인간답게 만든다'
    );

-- Store the group_id
SET @group_id = LAST_INSERT_ID();

-- 2. Insert Words and Details
-- Word 1: Happy
INSERT INTO words (spelling) VALUES ('Happy');

SET @word_id_1 = LAST_INSERT_ID();

INSERT INTO
    group_items (
        group_id,
        word_id,
        display_order,
        summary_meaning,
        display_letter
    )
VALUES (
        @group_id,
        @word_id_1,
        1,
        '행복한',
        'H'
    );

INSERT INTO
    word_details (
        word_id,
        full_definition,
        example_sentence,
        example_translation,
        mnemonic_tip
    )
VALUES (
        @word_id_1,
        'Feeling or showing pleasure or contentment.',
        'I am so happy today.',
        '나는 오늘 너무 행복해.',
        'Think of a smiling face.'
    );

-- Word 2: Sad
INSERT INTO words (spelling) VALUES ('Sad');

SET @word_id_2 = LAST_INSERT_ID();

INSERT INTO
    group_items (
        group_id,
        word_id,
        display_order,
        summary_meaning,
        display_letter
    )
VALUES (
        @group_id,
        @word_id_2,
        2,
        '슬픈',
        'S'
    );

INSERT INTO
    word_details (
        word_id,
        full_definition,
        example_sentence,
        example_translation,
        mnemonic_tip
    )
VALUES (
        @word_id_2,
        'Feeling or showing sorrow; unhappy.',
        'The movie was very sad.',
        '그 영화는 매우 슬펐어.',
        'Think of tears.'
    );

-- Word 3: Angry
INSERT INTO words (spelling) VALUES ('Angry');

SET @word_id_3 = LAST_INSERT_ID();

INSERT INTO
    group_items (
        group_id,
        word_id,
        display_order,
        summary_meaning,
        display_letter
    )
VALUES (
        @group_id,
        @word_id_3,
        3,
        '화난',
        'A'
    );

INSERT INTO
    word_details (
        word_id,
        full_definition,
        example_sentence,
        example_translation,
        mnemonic_tip
    )
VALUES (
        @word_id_3,
        'Having a strong feeling of or showing annoyance, displeasure, or hostility.',
        'He was angry about the mistake.',
        '그는 그 실수에 대해 화가 났다.',
        'Red face.'
    );

-- Word 4: Excited
INSERT INTO words (spelling) VALUES ('Excited');

SET @word_id_4 = LAST_INSERT_ID();

INSERT INTO
    group_items (
        group_id,
        word_id,
        display_order,
        summary_meaning,
        display_letter
    )
VALUES (
        @group_id,
        @word_id_4,
        4,
        '신난',
        'E'
    );

INSERT INTO
    word_details (
        word_id,
        full_definition,
        example_sentence,
        example_translation,
        mnemonic_tip
    )
VALUES (
        @word_id_4,
        'Very enthusiastic and eager.',
        'She is excited about the trip.',
        '그녀는 여행에 대해 들떠 있다.',
        'Jumping up and down.'
    );

-- Word 5: Nervous
INSERT INTO words (spelling) VALUES ('Nervous');

SET @word_id_5 = LAST_INSERT_ID();

INSERT INTO
    group_items (
        group_id,
        word_id,
        display_order,
        summary_meaning,
        display_letter
    )
VALUES (
        @group_id,
        @word_id_5,
        5,
        '긴장한',
        'N'
    );

INSERT INTO
    word_details (
        word_id,
        full_definition,
        example_sentence,
        example_translation,
        mnemonic_tip
    )
VALUES (
        @word_id_5,
        'Easily agitated or alarmed; tending to be anxious; highly strung.',
        'I get nervous before exams.',
        '나는 시험 전에 긴장해.',
        'Shaking hands.'
    );