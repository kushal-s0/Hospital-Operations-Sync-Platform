import React, { useState } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import './OPDQueue.css';

const OPDQueue = () => {
  const [queue, setQueue] = useState([
    { id: 1, token_number: 101, patient_name: 'John Doe', department: 'General Medicine', doctor_name: 'Dr. Smith', status: 'waiting', priority: 'normal', check_in_time: '09:15 AM', estimated_wait_time: 15 },
    { id: 2, token_number: 102, patient_name: 'Jane Smith', department: 'Cardiology', doctor_name: 'Dr. Johnson', status: 'in_consultation', priority: 'urgent', check_in_time: '09:20 AM', estimated_wait_time: 0 },
    { id: 3, token_number: 103, patient_name: 'Mike Wilson', department: 'Orthopedics', doctor_name: 'Dr. Brown', status: 'waiting', priority: 'normal', check_in_time: '09:30 AM', estimated_wait_time: 25 },
    { id: 4, token_number: 104, patient_name: 'Sarah Davis', department: 'General Medicine', doctor_name: 'Dr. Smith', status: 'waiting', priority: 'emergency', check_in_time: '09:35 AM', estimated_wait_time: 5 },
  ]);

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
          <p>Dynamic queue management with real-time updates</p>
        </div>
        <button className="btn btn-primary">+ Add Patient</button>
      </div>

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
          <span className="stat-number">~18</span>
          <span className="stat-text">Avg Wait Time (min)</span>
        </div>
      </div>

      <Table columns={columns} data={queue} />
    </div>
  );
};

export default OPDQueue;
