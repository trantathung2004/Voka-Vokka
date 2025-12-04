import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getGroupItems, getWordDetails, getGroupFooter, type VocabularyItem, type WordDetail, type GroupFooter } from '../api/client';
import Modal from '../components/Modal';
import './GroupDetail.css';

const GroupDetail = () => {
    const { groupId } = useParams<{ groupId: string }>();
    const [items, setItems] = useState<VocabularyItem[]>([]);
    const [footer, setFooter] = useState<GroupFooter | null>(null);
    const [loading, setLoading] = useState(true);
    const [selectedWord, setSelectedWord] = useState<WordDetail | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [loadingDetails, setLoadingDetails] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            if (!groupId) return;
            try {
                const [itemsData, footerData] = await Promise.all([
                    getGroupItems(parseInt(groupId)),
                    getGroupFooter(parseInt(groupId))
                ]);
                setItems(itemsData);
                setFooter(footerData);
            } catch (error) {
                console.error('Failed to fetch group data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
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
                <>
                    <div className="vocab-grid">
                        {/* Headers removed for bubble design */}

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

                    {footer && (
                        <div className="group-footer">
                            <p className="footer-en">"{footer.footer_phrase_en}"</p>
                            <p className="footer-kr">{footer.footer_phrase_kr}</p>
                        </div>
                    )}
                </>
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
