import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getGroupItems, getWordDetails, type VocabularyItem, type WordDetail } from '../api/client';
import Modal from '../components/Modal';
import './GroupDetail.css';

const GroupDetail = () => {
    const { groupId } = useParams<{ groupId: string }>();
    const [items, setItems] = useState<VocabularyItem[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedWord, setSelectedWord] = useState<WordDetail | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [loadingDetails, setLoadingDetails] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchItems = async () => {
            if (!groupId) return;
            try {
                const data = await getGroupItems(parseInt(groupId));
                setItems(data);
            } catch (error) {
                console.error('Failed to fetch items:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchItems();
    }, [groupId]);

    const handleWordClick = async (itemId: number) => {
        setLoadingDetails(true);
        try {
            const details = await getWordDetails(itemId);
            setSelectedWord(details);
            setIsModalOpen(true);
        } catch (error) {
            console.error('Failed to fetch word details:', error);
        } finally {
            setLoadingDetails(false);
        }
    };

    return (
        <div className="detail-container">
            <header className="detail-header">
                <button className="back-btn" onClick={() => navigate('/vocabulary')}>← Back</button>
                <h1>Group {groupId} Vocabulary</h1>
            </header>

            {loading ? (
                <div className="loading">Loading...</div>
            ) : (
                <div className="vocab-grid">
                    <div className="grid-header">English</div>
                    <div className="grid-header">Korean / Hint</div>

                    {items.map((item) => (
                        <div
                            key={item.item_id}
                            className="grid-row"
                            onClick={() => handleWordClick(item.item_id)}
                        >
                            <div className="grid-cell english">
                                {item.spelling}
                            </div>
                            <div className="grid-cell korean">
                                <span className="korean-word">{item.summary_meaning}</span>
                                <span className="hint-letter">{item.display_letter}</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={selectedWord?.spelling}
            >
                {loadingDetails ? (
                    <div className="loading-details">Loading details...</div>
                ) : selectedWord ? (
                    <div className="word-details">
                        <div className="detail-section">
                            <h3>Definition</h3>
                            <p>{selectedWord.full_definition}</p>
                        </div>

                        <div className="detail-section">
                            <h3>Example</h3>
                            <p className="example-en">{selectedWord.example_sentence}</p>
                            <p className="example-kr">{selectedWord.example_translation}</p>
                        </div>

                        <div className="detail-section">
                            <h3>Mnemonic Tip</h3>
                            <p className="mnemonic">{selectedWord.mnemonic_tip}</p>
                        </div>
                    </div>
                ) : null}
            </Modal>
        </div>
    );
};

export default GroupDetail;
