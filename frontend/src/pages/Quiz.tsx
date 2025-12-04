import { useNavigate } from 'react-router-dom';

const Quiz = () => {
    const navigate = useNavigate();
    return (
        <div style={{ textAlign: 'center', marginTop: '4rem' }}>
            <h1>Quiz Page</h1>
            <p>Coming Soon...</p>
            <button
                onClick={() => navigate('/')}
                style={{
                    marginTop: '2rem',
                    padding: '1rem 2rem',
                    background: 'var(--primary-color)',
                    color: 'white',
                    borderRadius: '0.5rem'
                }}
            >
                Back to Home
            </button>
        </div>
    );
};

export default Quiz;
