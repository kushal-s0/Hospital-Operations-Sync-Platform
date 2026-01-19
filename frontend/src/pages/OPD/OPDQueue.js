import React, { useState, useEffect } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import { opdAPI } from '../../services/api';
import './OPDQueue.css';

const OPDQueue = () => {
  const [queue, setQueue] = useState([]);
  const [waitTimePrediction, setWaitTimePrediction] = useState(null);
  const [showPredictionPanel, setShowPredictionPanel] = useState(false);
  const [predictionLoading, setPredictionLoading] = useState(false);
  const [showAddPatientForm, setShowAddPatientForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Get current user from localStorage
  const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
  const isNurse = currentUser.role === 'Nurse';
  
  // Form state for adding patient
  const [patientForm, setPatientForm] = useState({
    patient_first_name: '',
    patient_last_name: '',
    contact_number: '',
    department: 'General Medicine',
    doctor_name: '',
    priority: 'normal',
    notes: ''
  });

  // Fetch wait time prediction on mount
  useEffect(() => {
    fetchQueue();
    fetchWaitTimePrediction();
  }, []);

  // Fetch current queue from API
  const fetchQueue = async () => {
    try {
      const response = await opdAPI.getAll();
      // Handle both array and paginated response formats
      const queueData = Array.isArray(response.data) 
        ? response.data 
        : (response.data.results || []);
      setQueue(queueData);
    } catch (error) {
      console.error('Error fetching queue:', error);
      setQueue([]); // Set empty array on error
    }
  };

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

  // Handle form input changes
  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setPatientForm(prev => ({ ...prev, [name]: value }));
  };

  // Handle adding new patient to queue
  const handleAddPatient = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      // Create the patient and queue entry
      const queueData = {
        patient_first_name: patientForm.patient_first_name,
        patient_last_name: patientForm.patient_last_name,
        contact_number: patientForm.contact_number,
        department_name_input: patientForm.department,
        doctor_name_input: patientForm.doctor_name,
        priority: patientForm.priority,
        status: 'waiting',
        notes: patientForm.notes
      };

      await opdAPI.create(queueData);
      setSuccess('Patient added to queue successfully!');
      
      // Reset form
      setPatientForm({
        patient_first_name: '',
        patient_last_name: '',
        contact_number: '',
        department: 'General Medicine',
        doctor_name: '',
        priority: 'normal',
        notes: ''
      });
      
      // Refresh queue and close form
      fetchQueue();
      setTimeout(() => {
        setShowAddPatientForm(false);
        setSuccess('');
      }, 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add patient to queue');
    } finally {
      setLoading(false);
    }
  };

  // Handle starting consultation
  const handleStartConsultation = async (queueItem) => {
    try {
      await opdAPI.startConsultation(queueItem.id);
      setSuccess(`Started consultation for Token #${queueItem.token_number}`);
      fetchQueue();
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      setError('Failed to start consultation');
      setTimeout(() => setError(''), 3000);
    }
  };

  // Handle completing consultation
  const handleCompleteConsultation = async (queueItem) => {
    try {
      await opdAPI.endConsultation(queueItem.id);
      setSuccess(`Completed consultation for Token #${queueItem.token_number}`);
      fetchQueue();
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      setError('Failed to complete consultation');
      setTimeout(() => setError(''), 3000);
    }
  };

  const columns = [
    { key: 'token_number', label: 'Token #' },
    { 
      key: 'patient_name', 
      label: 'Patient Name',
      render: (row) => {
        // Use the serialized patient_name or construct from patient object
        if (row.patient_name) {
          return row.patient_name;
        }
        const patient = row.patient;
        if (patient) {
          return `${patient.first_name} ${patient.last_name}`;
        }
        return 'N/A';
      }
    },
    { 
      key: 'department_name', 
      label: 'Department',
      render: (row) => row.department_name || row.department || 'N/A'
    },
    { 
      key: 'doctor_name', 
      label: 'Doctor',
      render: (row) => row.doctor_name || 'N/A'
    },
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
    { 
      key: 'check_in_time', 
      label: 'Check-in Time',
      render: (row) => row.check_in_time ? new Date(row.check_in_time).toLocaleTimeString() : 'N/A'
    },
    { 
      key: 'estimated_wait_time', 
      label: 'Est. Wait',
      render: (row) => row.status === 'waiting' && row.estimated_wait_time 
        ? `${row.estimated_wait_time} min` 
        : '-'
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (row) => (
        <div className="action-buttons">
          {row.status === 'waiting' && (
            <button 
              className="btn btn-primary btn-sm"
              onClick={() => handleStartConsultation(row)}
            >
              Start
            </button>
          )}
          {row.status === 'in_consultation' && (
            <button 
              className="btn btn-success btn-sm"
              onClick={() => handleCompleteConsultation(row)}
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
          <p>Dynamic queue management with ML-powered wait time predictions</p>
        </div>
        <div className="header-actions">
          <button 
            className="btn btn-secondary"
            onClick={() => setShowPredictionPanel(!showPredictionPanel)}
          >
            🤖 {showPredictionPanel ? 'Hide' : 'Show'} Wait Time Predictor
          </button>
          {isNurse && (
            <button 
              className="btn btn-primary"
              onClick={() => setShowAddPatientForm(true)}
            >
              + Add Patient
            </button>
          )}
        </div>
      </div>

      {/* Success/Error Messages */}
      {success && (
        <div className="alert alert-success">
          ✅ {success}
        </div>
      )}
      {error && (
        <div className="alert alert-error">
          ❌ {error}
        </div>
      )}

      {/* Add Patient Form Modal */}
      {showAddPatientForm && isNurse && (
        <div className="modal-overlay" onClick={() => setShowAddPatientForm(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Add Patient to OPD Queue</h2>
              <button 
                className="close-btn"
                onClick={() => setShowAddPatientForm(false)}
              >
                ×
              </button>
            </div>
            
            <form onSubmit={handleAddPatient} className="patient-form">
              <div className="form-section">
                <h3>Basic Information</h3>
                
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="patient_first_name">First Name *</label>
                    <input
                      type="text"
                      id="patient_first_name"
                      name="patient_first_name"
                      value={patientForm.patient_first_name}
                      onChange={handleFormChange}
                      required
                      placeholder="Enter first name"
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="patient_last_name">Last Name *</label>
                    <input
                      type="text"
                      id="patient_last_name"
                      name="patient_last_name"
                      value={patientForm.patient_last_name}
                      onChange={handleFormChange}
                      required
                      placeholder="Enter last name"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="contact_number">Contact Number *</label>
                    <input
                      type="tel"
                      id="contact_number"
                      name="contact_number"
                      value={patientForm.contact_number}
                      onChange={handleFormChange}
                      required
                      placeholder="Enter contact number"
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="department">Department *</label>
                    <select
                      id="department"
                      name="department"
                      value={patientForm.department}
                      onChange={handleFormChange}
                      required
                    >
                      <option value="General Medicine">General Medicine</option>
                      <option value="Cardiology">Cardiology</option>
                      <option value="Orthopedics">Orthopedics</option>
                      <option value="Pediatrics">Pediatrics</option>
                      <option value="Emergency">Emergency</option>
                    </select>
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="doctor_name">Doctor Name *</label>
                    <input
                      type="text"
                      id="doctor_name"
                      name="doctor_name"
                      value={patientForm.doctor_name}
                      onChange={handleFormChange}
                      required
                      placeholder="Enter doctor name"
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="priority">Priority *</label>
                    <select
                      id="priority"
                      name="priority"
                      value={patientForm.priority}
                      onChange={handleFormChange}
                      required
                    >
                      <option value="normal">Normal</option>
                      <option value="urgent">Urgent</option>
                      <option value="emergency">Emergency</option>
                    </select>
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="notes">Notes (Optional)</label>
                  <textarea
                    id="notes"
                    name="notes"
                    value={patientForm.notes}
                    onChange={handleFormChange}
                    rows="3"
                    placeholder="Any additional notes..."
                  />
                </div>
              </div>

              <div className="form-actions">
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={() => setShowAddPatientForm(false)}
                  disabled={loading}
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="btn btn-primary"
                  disabled={loading}
                >
                  {loading ? 'Adding...' : 'Add to Queue'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

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
