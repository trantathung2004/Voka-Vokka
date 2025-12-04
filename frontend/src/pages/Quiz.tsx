import { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getGroupItems, submitQuizAnswer, getQuizHint, type VocabularyItem } from '../api/client';
import Modal from '../components/Modal';
import './GroupDetail.css'; // Reuse basic layout styles
import './Quiz.css'; // Specific quiz styles

interface QuizItemState {
    itemId: number;
    userAnswer: string;
    isCorrect: boolean | null; // null = not submitted, true = correct, false = incorrect
    feedback: string | null;
    hint: string | null;
}

const Quiz = () => {
    const { groupId } = useParams<{ groupId: string }>();
    const [items, setItems] = useState<VocabularyItem[]>([]);
    const [quizState, setQuizState] = useState<Record<number, QuizItemState>>({});
    const [loading, setLoading] = useState(true);
    const [startTime] = useState(Date.now());
    const [elapsedTime, setElapsedTime] = useState(0);
    const [progress, setProgress] = useState(0);
    const [isHintModalOpen, setIsHintModalOpen] = useState(false);
    const [selectedHintItem, setSelectedHintItem] = useState<number | null>(null);
    const [loadingHint, setLoadingHint] = useState(false);

    const navigate = useNavigate();
    const timerRef = useRef<number | undefined>(undefined);

    useEffect(() => {
        const fetchItems = async () => {
            if (!groupId) return;
            try {
                const data = await getGroupItems(parseInt(groupId));
                setItems(data);
                // Initialize quiz state
                const initial: Record<number, QuizItemState> = {};
                data.forEach(item => {
                    initial[item.item_id] = {
                        itemId: item.item_id,
                        userAnswer: '',
                        isCorrect: null,
                        feedback: null,
                        hint: null
                    };
                });
                setQuizState(initial);
            } catch (error) {
                console.error('Failed to fetch items:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchItems();

        timerRef.current = setInterval(() => {
            setElapsedTime(Math.floor((Date.now() - startTime) / 1000));
        }, 1000);

        return () => clearInterval(timerRef.current);
    }, [groupId, startTime]);

    useEffect(() => {
        if (items.length === 0) return;
        const correctCount = Object.values(quizState).filter(s => s.isCorrect).length;
        setProgress(Math.round((correctCount / items.length) * 100));
    }, [quizState, items.length]);

    const handleInputChange = (itemId: number, value: string) => {
        setQuizState(prev => ({
            ...prev,
            [itemId]: { ...prev[itemId], userAnswer: value }
        }));
    };

    const handleKeyDown = async (e: React.KeyboardEvent, itemId: number) => {
        if (e.key === 'Enter') {
            await handleSubmit(itemId);
        }
    };

    const handleSubmit = async (itemId: number) => {
        const state = quizState[itemId];
        if (!state.userAnswer.trim()) return;

        try {
            const result = await submitQuizAnswer(itemId, state.userAnswer, parseInt(groupId!), 1);
            setQuizState(prev => ({
                ...prev,
                [itemId]: {
                    ...prev[itemId],
                    isCorrect: result.is_correct,
                    feedback: result.feedback
                }
            }));
        } catch (error) {
            console.error('Failed to submit answer:', error);
        }
    };

    const handleKoreanClick = (itemId: number) => {
        setSelectedHintItem(itemId);
        setIsHintModalOpen(true);
    };

    const handleAskAITutor = async () => {
        if (!selectedHintItem) return;
        setLoadingHint(true);
        try {
            const result = await getQuizHint(selectedHintItem);
            setQuizState(prev => ({
                ...prev,
                [selectedHintItem]: { ...prev[selectedHintItem], hint: result.hint }
            }));
        } catch (error) {
            console.error('Failed to get hint:', error);
        } finally {
            setLoadingHint(false);
        }
    };

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div className="detail-container">
            <header className="detail-header quiz-header">
                <button className="back-btn" onClick={() => navigate('/quiz')}>Exit Quiz</button>
                <div className="quiz-stats">
                    <div className="stat-box">
                        <span className="label">Time</span>
                        <span className="value">{formatTime(elapsedTime)}</span>
                    </div>
                    <div className="stat-box">
                        <span className="label">Progress</span>
                        <span className="value">{progress}%</span>
                    </div>
                </div>
            </header>

            {loading ? (
                <div className="loading">Loading Quiz...</div>
            ) : (
                <div className="vocab-grid">
                    {items.map((item) => {
                        const state = quizState[item.item_id];
                        const isCorrect = state?.isCorrect === true;
                        const isWrong = state?.isCorrect === false;

                        return (
                            <div key={item.item_id} className="grid-row quiz-row">
                                <div className={`grid-cell english input-cell ${isCorrect ? 'correct' : ''} ${isWrong ? 'wrong' : ''}`}>
                                    {isCorrect ? (
                                        <span className="correct-answer">{state.userAnswer}</span>
                                    ) : (
                                        <input
                                            type="text"
                                            value={state?.userAnswer || ''}
                                            onChange={(e) => handleInputChange(item.item_id, e.target.value)}
                                            onKeyDown={(e) => handleKeyDown(e, item.item_id)}
                                            placeholder="Type English word..."
                                            className="quiz-input"
                                            autoFocus={items[0].item_id === item.item_id}
                                        />
                                    )}
                                    {isCorrect && <span className="checkmark">✓</span>}
                                </div>

                                <div
                                    className="grid-cell korean clickable"
                                    onClick={() => handleKoreanClick(item.item_id)}
                                >
                                    <span className="korean-word">{item.summary_meaning}</span>
                                    {/* Hint letter hidden in quiz? Or maybe shown? User said "all English words are hidden". 
                      Usually hint letter is part of the "Korean grid" in the design description. 
                      Let's keep it but maybe obscure it? Or keep it as a small hint. 
                      "Korean grid contains the Korean word and the first letter of the English word."
                      So we keep it.
                  */}
                                    <span className="hint-letter">{item.display_letter}</span>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            <Modal
                isOpen={isHintModalOpen}
                onClose={() => setIsHintModalOpen(false)}
                title="Need a Hint?"
            >
                <div className="hint-modal-content">
                    <p>Stuck on this word?</p>

                    {selectedHintItem && quizState[selectedHintItem]?.hint ? (
                        <div className="ai-hint">
                            <h4>AI Tutor Hint:</h4>
                            <p>{quizState[selectedHintItem].hint}</p>
                        </div>
                    ) : (
                        <button
                            className="ai-tutor-btn"
                            onClick={handleAskAITutor}
                            disabled={loadingHint}
                        >
                            {loadingHint ? 'Asking AI...' : 'Ask AI Tutor'}
                        </button>
                    )}
                </div>
            </Modal>
        </div>
    );
};

export default Quiz;
