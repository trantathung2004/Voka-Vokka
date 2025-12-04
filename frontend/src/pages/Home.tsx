import { useNavigate } from 'react-router-dom';
import './Home.css';

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1 className="title">Voka Vokka</h1>
            <div className="button-group">
                <button className="main-btn" onClick={() => navigate('/vocabulary')}>
                    Vocabulary
                </button>
                <button className="main-btn secondary" onClick={() => navigate('/quiz')}>
                    Quiz
                </button>
            </div>
        </div>
    );
};

export default Home;
