import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, HardDrive, Cpu, Image as ImageIcon, Music, Settings, BarChart2 } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import axios from 'axios';
import './RunDetail.css';

interface Metric {
  step: number;
  name: string;
  value: number;
  timestamp: string;
}

interface Artifact {
  type: string;
  name: string;
  file_path: string;
}

export default function RunDetail() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`http://localhost:8000/api/runs/${id}`)
      .then(res => setData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="loading">Loading run details...</div>;
  if (!data) return <div className="empty-state">Run not found</div>;

  const { run, metrics, artifacts, config } = data;

  // Process metrics for Recharts
  const chartDataMap: Record<number, any> = {};
  const metricNames = new Set<string>();

  metrics.forEach((m: Metric) => {
    if (!chartDataMap[m.step]) {
      chartDataMap[m.step] = { step: m.step };
    }
    chartDataMap[m.step][m.name] = m.value;
    metricNames.add(m.name);
  });

  const chartData = Object.values(chartDataMap).sort((a, b) => a.step - b.step);

  const sysMetrics = Array.from(metricNames).filter(n => n.startsWith('sys_'));
  const modelMetrics = Array.from(metricNames).filter(n => !n.startsWith('sys_'));

  const images = artifacts.filter((a: Artifact) => a.type === 'image');
  const audio = artifacts.filter((a: Artifact) => a.type === 'audio');

  return (
    <div className="run-detail animate-enter">
      <div className="detail-header">
        <Link to="/" className="btn btn-secondary back-btn">
          <ArrowLeft size={16} /> Back
        </Link>
        <div className="title-area">
          <h2>{run.project}</h2>
          <span className={`badge ${run.status}`}>{run.status}</span>
          <span className="hash-id">{run.id}</span>
        </div>
      </div>

      <div className="detail-grid">
        <div className="main-column">
          
          {modelMetrics.length > 0 && (
            <div className="glass-panel section-panel">
              <div className="section-header">
                <BarChart2 size={18} />
                <h3>Model Metrics</h3>
              </div>
              <div className="chart-wrapper">
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis dataKey="step" stroke="#9aa0a6" />
                    <YAxis stroke="#9aa0a6" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#12141a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} 
                    />
                    <Legend />
                    {modelMetrics.map((name, i) => (
                      <Line 
                        key={name}
                        type="monotone" 
                        dataKey={name} 
                        stroke={`hsl(${i * 60 + 200}, 70%, 60%)`} 
                        strokeWidth={2}
                        dot={{ r: 3 }}
                        activeDot={{ r: 6 }}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {sysMetrics.length > 0 && (
            <div className="glass-panel section-panel">
              <div className="section-header">
                <Cpu size={18} />
                <h3>System Resources</h3>
              </div>
              <div className="chart-wrapper">
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                    <XAxis dataKey="step" stroke="#9aa0a6" />
                    <YAxis stroke="#9aa0a6" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#12141a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} 
                    />
                    <Legend />
                    {sysMetrics.map((name, i) => (
                      <Line 
                        key={name}
                        type="monotone" 
                        dataKey={name} 
                        stroke={i === 0 ? '#10b981' : '#f59e0b'} 
                        strokeWidth={2}
                        dot={false}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {(images.length > 0 || audio.length > 0) && (
            <div className="glass-panel section-panel artifacts-panel">
              <div className="section-header">
                <HardDrive size={18} />
                <h3>Artifacts</h3>
              </div>
              
              {images.length > 0 && (
                <div className="artifact-group">
                  <h4><ImageIcon size={14} /> Images</h4>
                  <div className="image-grid">
                    {images.map((img: Artifact, i: number) => {
                      const filename = img.file_path.split(/[\\/]/).pop();
                      return (
                        <div key={i} className="image-card">
                          <img src={`http://localhost:8000/artifacts/${id}/images/${filename}`} alt={img.name} />
                          <div className="img-cap">{img.name}</div>
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}

              {audio.length > 0 && (
                <div className="artifact-group">
                  <h4><Music size={14} /> Audio</h4>
                  <div className="audio-list">
                    {audio.map((aud: Artifact, i: number) => {
                      const filename = aud.file_path.split(/[\\/]/).pop();
                      return (
                        <div key={i} className="audio-card">
                          <span className="aud-name">{aud.name}</span>
                          <audio controls src={`http://localhost:8000/artifacts/${id}/audio/${filename}`} />
                        </div>
                      )
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

        </div>

        <div className="side-column">
          <div className="glass-panel section-panel">
            <div className="section-header">
              <Settings size={18} />
              <h3>Configuration</h3>
            </div>
            <div className="config-blob">
              <pre>{JSON.stringify(config, null, 2)}</pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
