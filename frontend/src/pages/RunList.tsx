import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { PlayCircle, Clock, GitCommit, ChevronRight, Activity } from 'lucide-react';
import axios from 'axios';
import './RunList.css';

interface Run {
  id: string;
  project: string;
  status: string;
  start_time: string;
  git_commit: string;
  is_dirty: boolean;
}

export default function RunList() {
  const [runs, setRuns] = useState<Run[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:8000/api/runs/')
      .then(res => setRuns(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading experiments...</div>;

  return (
    <div className="run-list animate-enter">
      <div className="page-header">
        <h2>Experiment Runs</h2>
        <p>Tracking {runs.length} runs across your projects</p>
      </div>

      <div className="grid">
        {runs.map((run, i) => (
          <Link to={`/run/${run.id}`} key={run.id} className="glass-panel run-card" style={{ animationDelay: `${i * 0.05}s` }}>
            <div className="run-card-header">
              <h3>{run.project}</h3>
              <span className={`badge ${run.status}`}>
                {run.status === 'running' && <PlayCircle size={12} />}
                {run.status}
              </span>
            </div>
            
            <div className="run-card-body">
              <div className="meta-item">
                <Clock size={14} />
                <span>{new Date(run.start_time).toLocaleString()}</span>
              </div>
              <div className="meta-item">
                <GitCommit size={14} />
                <span className="mono">{run.git_commit?.substring(0, 7) || 'unknown'} {run.is_dirty ? '(dirty)' : ''}</span>
              </div>
            </div>

            <div className="run-card-footer">
              <span className="id-hash">{run.id.split('-')[0]}</span>
              <ChevronRight size={18} />
            </div>
          </Link>
        ))}
        {runs.length === 0 && (
          <div className="empty-state glass-panel">
            <Activity size={48} opacity={0.2} />
            <p>No runs tracked yet. Use the Python SDK to log an experiment!</p>
          </div>
        )}
      </div>
    </div>
  );
}
