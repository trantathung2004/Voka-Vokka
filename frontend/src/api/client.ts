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
