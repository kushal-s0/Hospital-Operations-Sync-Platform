import React, { useState, useEffect } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import { admissionsAPI } from '../../services/api';
import './Admissions.css';

const Admissions = () => {
  const [admissions, setAdmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const fetchAdmissions = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await admissionsAPI.getCurrent();
      // Handle paginated response - data may be in .results or directly in .data
      const responseData = response.data;
      const admissionsData = Array.isArray(responseData) 
        ? responseData 
        : (responseData.results || []);
      setAdmissions(admissionsData);
    } catch (err) {
      console.error('Failed to fetch admissions:', err);
      setError('Failed to load admissions data. Please try again.');
      setAdmissions([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdmissions();
  }, []);

  const handleDischarge = async (admissionId) => {
    try {
      await admissionsAPI.discharge(admissionId);
      // Refresh the list after discharge
      fetchAdmissions();
    } catch (err) {
      console.error('Failed to discharge patient:', err);
      alert('Failed to discharge patient. Please try again.');
    }
  };

  const columns = [
    { key: 'admission_id', label: 'Admission #' },
    { key: 'patient_name', label: 'Patient Name' },
    { key: 'bed_info', label: 'Bed' },
    { 
      key: 'condition_level', 
      label: 'Condition',
      render: (row) => <StatusBadge status={row.condition_level || 'stable'} />
    },
    { 
      key: 'admission_time', 
      label: 'Admission Date',
      render: (row) => row.admission_time ? new Date(row.admission_time).toLocaleDateString() : '-'
    },
    { 
      key: 'status', 
      label: 'Status',
      render: (row) => <StatusBadge status={row.status?.toLowerCase() || 'active'} />
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (row) => (
        <div className="action-buttons">
          <button className="btn btn-secondary btn-sm">View</button>
          {row.status === 'Active' && (
            <button 
              className="btn btn-success btn-sm"
              onClick={() => handleDischarge(row.admission_id)}
            >
              Discharge
            </button>
          )}
        </div>
      )
    }
  ];

  return (
    <div className="admissions">
      <div className="page-header">
        <div>
          <h1>Admissions Management</h1>
          <p>Rule-based admission workflow and patient management</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          + New Admission
        </button>
      </div>

      {showForm && (
        <div className="admission-form-card">
          <h3>New Admission Form</h3>
          <form className="admission-form">
            <div className="form-row">
              <div className="form-group">
                <label>Patient Name</label>
                <input type="text" placeholder="Enter patient name" />
              </div>
              <div className="form-group">
                <label>Condition Level</label>
                <select>
                  <option value="stable">Stable</option>
                  <option value="critical">Critical</option>
                  <option value="serious">Serious</option>
                </select>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Preferred Bed Type</label>
                <select>
                  <option value="General">General</option>
                  <option value="ICU">ICU</option>
                  <option value="Private">Private</option>
                  <option value="Semi-Private">Semi-Private</option>
                </select>
              </div>
              <div className="form-group">
                <label>Department</label>
                <select>
                  <option value="">Select Department</option>
                  <option value="general_medicine">General Medicine</option>
                  <option value="cardiology">Cardiology</option>
                  <option value="surgery">Surgery</option>
                  <option value="pediatrics">Pediatrics</option>
                </select>
              </div>
            </div>
            <div className="form-actions">
              <button type="button" className="btn btn-primary">Find Matching Bed</button>
              <button type="submit" className="btn btn-success">Confirm Admission</button>
              <button type="button" className="btn btn-secondary" onClick={() => setShowForm(false)}>Cancel</button>
            </div>
          </form>
        </div>
      )}

      {loading && <div className="loading">Loading admissions...</div>}
      {error && <div className="error-message">{error}</div>}

      {!loading && !error && (
        <>
          <div className="admission-stats">
            <div className="stat-item">
              <span className="stat-number">{admissions.length}</span>
              <span className="stat-text">Current Admissions</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">
                {admissions.filter(a => a.condition_level === 'critical').length}
              </span>
              <span className="stat-text">Critical Cases</span>
            </div>
          </div>

          {admissions.length === 0 ? (
            <p className="no-data">No current admissions</p>
          ) : (
            <Table columns={columns} data={admissions} />
          )}
        </>
      )}
    </div>
  );
};

export default Admissions;
