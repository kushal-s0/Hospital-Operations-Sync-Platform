import React, { useState, useEffect } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import { opdAPI } from '../../services/api';
import './OPDQueue.css';

const OPDQueue = () => {
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchQueue = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await opdAPI.getCurrentQueue();
      // Handle paginated response - data may be in .results or directly in .data
      const responseData = response.data;
      const queueData = Array.isArray(responseData) 
        ? responseData 
        : (responseData.results || []);
      setQueue(queueData);
    } catch (err) {
      console.error('Failed to fetch OPD queue:', err);
      setError('Failed to load OPD queue data. Please try again.');
      setQueue([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQueue();
    
    // Refresh queue every 15 seconds
    const interval = setInterval(fetchQueue, 15000);
    return () => clearInterval(interval);
  }, []);

  const handleStartConsultation = async (id) => {
    try {
      await opdAPI.startConsultation(id);
      fetchQueue();
    } catch (err) {
      console.error('Failed to start consultation:', err);
      alert('Failed to start consultation. Please try again.');
    }
  };

  const handleEndConsultation = async (id) => {
    try {
      await opdAPI.endConsultation(id);
      fetchQueue();
    } catch (err) {
      console.error('Failed to end consultation:', err);
      alert('Failed to end consultation. Please try again.');
    }
  };

  const columns = [
    { key: 'token_number', label: 'Token #' },
    { key: 'patient_name', label: 'Patient Name' },
    { key: 'department', label: 'Department' },
    { key: 'doctor_name', label: 'Doctor' },
    { 
      key: 'priority', 
      label: 'Priority',
      render: (row) => <StatusBadge status={row.priority || 'normal'} />
    },
    { 
      key: 'status', 
      label: 'Status',
      render: (row) => <StatusBadge status={row.status} />
    },
    { 
      key: 'check_in_time', 
      label: 'Check-in Time',
      render: (row) => row.check_in_time ? new Date(row.check_in_time).toLocaleTimeString() : '-'
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (row) => (
        <div className="action-buttons">
          {row.status === 'waiting' && (
            <button 
              className="btn btn-primary btn-sm"
              onClick={() => handleStartConsultation(row.id)}
            >
              Start
            </button>
          )}
          {row.status === 'in_consultation' && (
            <button 
              className="btn btn-success btn-sm"
              onClick={() => handleEndConsultation(row.id)}
            >
              Complete
            </button>
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
          <p>Dynamic queue management with real-time updates</p>
        </div>
        <button className="btn btn-primary">+ Add Patient</button>
      </div>

      {loading && <div className="loading">Loading OPD queue...</div>}
      {error && <div className="error-message">{error}</div>}

      {!loading && !error && (
        <>
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
              <span className="stat-number">{queue.length}</span>
              <span className="stat-text">Total Today</span>
            </div>
          </div>

          {queue.length === 0 ? (
            <p className="no-data">No patients in queue</p>
          ) : (
            <Table columns={columns} data={queue} />
          )}
        </>
      )}
    </div>
  );
};

export default OPDQueue;
