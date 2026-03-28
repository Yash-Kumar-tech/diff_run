import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Activity } from 'lucide-react';
import RunList from './pages/RunList';
import RunDetail from './pages/RunDetail';

function App() {
  return (
    <BrowserRouter>
      <div className="layout">
        <header className="navbar">
          <Link to="/" className="navbar-brand">
            <Activity color="#818cf8" size={28} />
            <span>diff_run MVP</span>
          </Link>
          <div className="nav-actions">
            <a href="https://github.com" target="_blank" rel="noreferrer" className="btn btn-secondary">
              GitHub
            </a>
          </div>
        </header>
        
        <main>
          <Routes>
            <Route path="/" element={<RunList />} />
            <Route path="/run/:id" element={<RunDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
