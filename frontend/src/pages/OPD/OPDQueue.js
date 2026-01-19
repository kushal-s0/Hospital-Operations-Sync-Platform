import React, { useState, useEffect } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import { opdAPI } from '../../services/api';
import './OPDQueue.css';

const OPDQueue = () => {
  const [queue, setQueue] = useState([
    { id: 1, token_number: 101, patient_name: 'John Doe', department: 'General Medicine', doctor_name: 'Dr. Smith', status: 'waiting', priority: 'normal', check_in_time: '09:15 AM', estimated_wait_time: 15 },
    { id: 2, token_number: 102, patient_name: 'Jane Smith', department: 'Cardiology', doctor_name: 'Dr. Johnson', status: 'in_consultation', priority: 'urgent', check_in_time: '09:20 AM', estimated_wait_time: 0 },
    { id: 3, token_number: 103, patient_name: 'Mike Wilson', department: 'Orthopedics', doctor_name: 'Dr. Brown', status: 'waiting', priority: 'normal', check_in_time: '09:30 AM', estimated_wait_time: 25 },
    { id: 4, token_number: 104, patient_name: 'Sarah Davis', department: 'General Medicine', doctor_name: 'Dr. Smith', status: 'waiting', priority: 'emergency', check_in_time: '09:35 AM', estimated_wait_time: 5 },
  ]);
  
  const [waitTimePrediction, setWaitTimePrediction] = useState(null);
  const [showPredictionPanel, setShowPredictionPanel] = useState(false);
  const [predictionLoading, setPredictionLoading] = useState(false);

  // Fetch wait time prediction on mount
  useEffect(() => {
    fetchWaitTimePrediction();
  }, []);

  const fetchWaitTimePrediction = async (urgency = 'normal') => {
    setPredictionLoading(true);
    try {
      const response = await opdAPI.predictWaitTime({ urgency_level: urgency });
      setWaitTimePrediction(response.data);
    } catch (error) {
      console.error('Error fetching wait time prediction:', error);
    }
    setPredictionLoading(false);
  };

  const columns = [
    { key: 'token_number', label: 'Token #' },
    { key: 'patient_name', label: 'Patient Name' },
    { key: 'department', label: 'Department' },
    { key: 'doctor_name', label: 'Doctor' },
    { 
      key: 'priority', 
      label: 'Priority',
      render: (row) => <StatusBadge status={row.priority} />
    },
    { 
      key: 'status', 
      label: 'Status',
      render: (row) => <StatusBadge status={row.status} />
    },
    { key: 'check_in_time', label: 'Check-in Time' },
    { 
      key: 'estimated_wait_time', 
      label: 'Est. Wait',
      render: (row) => row.status === 'waiting' ? `${row.estimated_wait_time} min` : '-'
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (row) => (
        <div className="action-buttons">
          {row.status === 'waiting' && (
            <button className="btn btn-primary btn-sm">Start</button>
          )}
          {row.status === 'in_consultation' && (
            <button className="btn btn-success btn-sm">Complete</button>
          )}
        </div>
      )
    }
  ];

  return (
    <div className="opd-queue">
      <div className="page-header">
        <div>
          <h1>OPD Queue Management</h1>
          <p>Dynamic queue management with ML-powered wait time predictions</p>
        </div>
        <div className="header-actions">
          <button 
            className="btn btn-secondary"
            onClick={() => setShowPredictionPanel(!showPredictionPanel)}
          >
            🤖 {showPredictionPanel ? 'Hide' : 'Show'} Wait Time Predictor
          </button>
          <button className="btn btn-primary">+ Add Patient</button>
        </div>
      </div>

      {/* ML Wait Time Prediction Panel */}
      {showPredictionPanel && (
        <div className="wait-time-predictor">
          <h2>⏱️ ML Wait Time Prediction</h2>
          
          <div className="prediction-controls">
            <label>Check prediction for urgency level:</label>
            <div className="urgency-buttons">
              <button 
                className="urgency-btn normal"
                onClick={() => fetchWaitTimePrediction('normal')}
              >
                Normal
              </button>
              <button 
                className="urgency-btn urgent"
                onClick={() => fetchWaitTimePrediction('urgent')}
              >
                Urgent
              </button>
              <button 
                className="urgency-btn emergency"
                onClick={() => fetchWaitTimePrediction('emergency')}
              >
                Emergency
              </button>
            </div>
          </div>

          {predictionLoading && (
            <div className="prediction-loading">
              <span>🔄 Calculating wait time...</span>
            </div>
          )}

          {waitTimePrediction && !predictionLoading && (
            <div className="prediction-result">
              <div className="main-prediction">
                <div className="wait-time-display">
                  <span className="time-value">{waitTimePrediction.predicted_wait_time_minutes}</span>
                  <span className="time-unit">minutes</span>
                </div>
                <div className={`confidence-badge ${waitTimePrediction.confidence}`}>
                  Confidence: {waitTimePrediction.confidence}
                </div>
              </div>

              <div className="prediction-details">
                <div className="detail-section">
                  <h4>📊 Current Queue Status</h4>
                  <div className="detail-grid">
                    <div className="detail-item">
                      <span className="detail-label">Patients Waiting</span>
                      <span className="detail-value">{waitTimePrediction.current_queue_status?.patients_waiting}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">In Consultation</span>
                      <span className="detail-value">{waitTimePrediction.current_queue_status?.patients_in_consultation}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Avg Consultation</span>
                      <span className="detail-value">{waitTimePrediction.current_queue_status?.avg_consultation_time} min</span>
                    </div>
                  </div>
                </div>

                <div className="detail-section">
                  <h4>🎯 Factors Considered</h4>
                  <div className="factors-list">
                    <span className="factor-chip">
                      Urgency: {waitTimePrediction.factors_considered?.urgency_level}
                    </span>
                    <span className="factor-chip">
                      Time: {waitTimePrediction.factors_considered?.time_of_day}
                    </span>
                    <span className="factor-chip">
                      {waitTimePrediction.factors_considered?.is_weekend ? '📅 Weekend' : '📅 Weekday'}
                    </span>
                  </div>
                </div>

                <div className="recommendation-box">
                  <span className="recommendation-icon">💡</span>
                  <p>{waitTimePrediction.recommendation}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      <div className="queue-stats">
        <div className="stat-item">
          <span className="stat-number">{queue.filter(q => q.status === 'waiting').length}</span>
          <span className="stat-text">Waiting</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">{queue.filter(q => q.status === 'in_consultation').length}</span>
          <span className="stat-text">In Consultation</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">~{waitTimePrediction?.predicted_wait_time_minutes || 18}</span>
          <span className="stat-text">🤖 ML Predicted Wait (min)</span>
        </div>
      </div>

      <Table columns={columns} data={queue} />
    </div>
  );
};

export default OPDQueue;
