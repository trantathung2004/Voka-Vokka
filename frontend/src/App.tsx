import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Vocabulary from './pages/Vocabulary';
import GroupDetail from './pages/GroupDetail';
import Quiz from './pages/Quiz';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/vocabulary" element={<Vocabulary />} />
        <Route path="/vocabulary/:groupId" element={<GroupDetail />} />
        <Route path="/quiz" element={<Quiz />} />
      </Routes>
    </Router>
  );
}

export default App;
