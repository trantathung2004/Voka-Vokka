import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const client = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface Group {
    group_id: number;
    group_number: number;
    title_kr: string;
}

export interface VocabularyItem {
    item_id: number;
    display_order: number;
    summary_meaning: string;
    display_letter: string;
    spelling: string;
}

export interface WordDetail {
    item_id: number;
    summary_meaning: string;
    display_letter: string;
    group_number: number;
    word_id: number;
    spelling: string;
    full_definition: string;
    example_sentence: string;
    example_translation: string;
    mnemonic_tip: string;
}

export interface GroupFooter {
    footer_phrase_en: string;
    footer_phrase_kr: string;
}

export interface QuizSubmitResponse {
    is_correct: boolean;
    correct_answer: string;
    user_answer: string;
    feedback: string;
}

export interface HintResponse {
    item_id: number;
    hint: string;
}

export const getGroups = async (): Promise<Group[]> => {
    const response = await client.get('/groups');
    return response.data;
};

export const getGroupItems = async (groupId: number): Promise<VocabularyItem[]> => {
    const response = await client.get(`/groups/${groupId}/items`);
    return response.data;
};

export const getWordDetails = async (itemId: number): Promise<WordDetail> => {
    const response = await client.get(`/items/${itemId}/details`);
    return response.data;
};

export const getGroupFooter = async (groupId: number): Promise<GroupFooter> => {
    const response = await client.get(`/groups/${groupId}`);
    return response.data;
};

export const submitQuizAnswer = async (itemId: number, userAnswer: string, groupId: number, userId: number = 1): Promise<QuizSubmitResponse> => {
    const response = await client.post('/quiz/submit', {
        item_id: itemId,
        user_answer: userAnswer,
        group_id: groupId,
        user_id: userId,
    });
    return response.data;
};

export const getQuizHint = async (itemId: number, userId: number = 1): Promise<HintResponse> => {
    const response = await client.post('/quiz/hint', {
        item_id: itemId,
        user_id: userId,
    });
    return response.data;
};
