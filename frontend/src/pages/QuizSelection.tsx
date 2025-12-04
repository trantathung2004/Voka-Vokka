import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getGroups, type Group } from '../api/client';
import './Vocabulary.css'; // Reuse vocabulary styles

const QuizSelection = () => {
    const [groups, setGroups] = useState<Group[]>([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchGroups = async () => {
            try {
                const data = await getGroups();
                setGroups(data);
            } catch (error) {
                console.error('Failed to fetch groups:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchGroups();
    }, []);

    return (
        <div className="vocab-container">
            <header className="vocab-header">
                <button className="back-btn" onClick={() => navigate('/')}>← Back</button>
                <h1>Select a Quiz Group</h1>
            </header>

            {loading ? (
                <div className="loading">Loading...</div>
            ) : (
                <div className="groups-grid">
                    {groups.map((group) => (
                        <div
                            key={group.group_id}
                            className="group-card"
                            onClick={() => navigate(`/quiz/${group.group_id}`)}
                        >
                            <h2>{group.title_kr}</h2>
                            <p>Group {group.group_number}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default QuizSelection;
