import React, { useState, useEffect } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import { admissionsAPI } from '../../services/api';
import './Admissions.css';

const Admissions = () => {
  const [admissions, setAdmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [selectedAdmission, setSelectedAdmission] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  
  // Search and filter state
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCondition, setFilterCondition] = useState('all');

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
    // Ask for confirmation before discharging
    const confirmed = window.confirm(
      'Are you sure you want to discharge this patient? The bed will be set to maintenance status.'
    );
    
    if (!confirmed) {
      return; // User cancelled the discharge
    }

    try {
      await admissionsAPI.discharge(admissionId);
      // Refresh the list after discharge
      fetchAdmissions();
      alert('Patient discharged successfully. Bed status set to maintenance.');
    } catch (err) {
      console.error('Failed to discharge patient:', err);
      alert('Failed to discharge patient. Please try again.');
    }
  };

  const handleViewDetails = (admission) => {
    setSelectedAdmission(admission);
    setShowDetails(true);
  };

  const handleCloseDetails = () => {
    setShowDetails(false);
    setSelectedAdmission(null);
  };

  // Filter and search admissions data
  const filteredAdmissions = admissions.filter(item => {
    // Search by patient name, admission ID, or bed info
    const searchLower = searchTerm.toLowerCase();
    const matchesSearch = searchTerm === '' ||
      (item.patient_name || '').toLowerCase().includes(searchLower) ||
      String(item.admission_id).includes(searchLower) ||
      (item.bed_info || '').toLowerCase().includes(searchLower);
    
    // Filter by condition level
    const matchesCondition = filterCondition === 'all' || 
      (item.condition_level || '').toLowerCase() === filterCondition.toLowerCase();
    
    return matchesSearch && matchesCondition;
  });

  const columns = [
    { key: 'admission_id', label: 'Admission #' },
    { key: 'patient_name', label: 'Patient Name' },
    { key: 'bed_info', label: 'Bed' },
    { 
      key: 'condition_level', 
      label: 'Condition',
      render: function(row) {
        return React.createElement(StatusBadge, { status: row.condition_level || 'stable' });
      }
    },
    { 
      key: 'admission_time', 
      label: 'Admission Date',
      render: function(row) {
        return row.admission_time ? new Date(row.admission_time).toLocaleDateString() : '-';
      }
    },
    { 
      key: 'status', 
      label: 'Status',
      render: function(row) {
        return React.createElement(StatusBadge, { status: row.status?.toLowerCase() || 'active' });
      }
    },
    {
      key: 'actions',
      label: 'Actions',
      render: function(row) {
        return React.createElement('div', { className: 'action-buttons' },
          React.createElement('button', {
            className: 'btn btn-secondary btn-sm',
            onClick: function() { handleViewDetails(row); }
          }, 'View'),
          row.status === 'Active' && React.createElement('button', {
            className: 'btn btn-success btn-sm',
            onClick: function() { handleDischarge(row.admission_id); }
          }, 'Discharge')
        );
      }
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

      {/* Search and Filters */}
      <div className="search-filter-section">
        <div className="search-bar">
          <input
            type="text"
            placeholder="🔍 Search by patient name, admission ID, or bed number."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          {searchTerm && (
            <button 
              className="clear-search"
              onClick={() => setSearchTerm('')}
              title="Clear search"
            >
              ✕
            </button>
          )}
        </div>
        
        <div className="filters">
          <div className="filter-group">
            <label>Condition:</label>
            <select 
              value={filterCondition} 
              onChange={(e) => setFilterCondition(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Conditions</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>
          
          {(searchTerm || filterCondition !== 'all') && (
            <button 
              className="btn btn-secondary btn-sm"
              onClick={() => {
                setSearchTerm('');
                setFilterCondition('all');
              }}
            >
              Clear All Filters
            </button>
          )}
        </div>
      </div>

      {/*     <div className="form-group">
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

      {/* Patient Details Modal */}
      {showDetails && selectedAdmission && (
        <div className="modal-overlay" onClick={handleCloseDetails}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Admission Details</h2>
              <button className="close-btn" onClick={handleCloseDetails}>×</button>
            </div>
            
            <div className="admission-details">
              <div className="details-section">
                <h3>Patient Information</h3>
                <div className="details-grid">
                  <div className="detail-item">
                    <span className="label">Admission ID:</span>
                    <span className="value">{selectedAdmission.admission_id}</span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Patient Name:</span>
                    <span className="value">{selectedAdmission.patient_name || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Patient ID:</span>
                    <span className="value">{selectedAdmission.patient_id || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Status:</span>
                    <span className="value">
                      <StatusBadge status={selectedAdmission.status?.toLowerCase() || 'active'} />
                    </span>
                  </div>
                </div>
              </div>

              <div className="details-section">
                <h3>Admission Details</h3>
                <div className="details-grid">
                  <div className="detail-item">
                    <span className="label">Admission Date:</span>
                    <span className="value">
                      {selectedAdmission.admission_time 
                        ? new Date(selectedAdmission.admission_time).toLocaleString()
                        : 'N/A'}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Discharge Date:</span>
                    <span className="value">
                      {selectedAdmission.discharge_time 
                        ? new Date(selectedAdmission.discharge_time).toLocaleString()
                        : 'Not Discharged'}
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Condition Level:</span>
                    <span className="value">
                      <StatusBadge status={selectedAdmission.condition_level || 'stable'} />
                    </span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Bed Information:</span>
                    <span className="value">{selectedAdmission.bed_info || 'N/A'}</span>
                  </div>
                </div>
              </div>

              <div className="details-section">
                <h3>Medical Information</h3>
                <div className="details-grid">
                  <div className="detail-item">
                    <span className="label">Primary Diagnosis:</span>
                    <span className="value">{selectedAdmission.primary_diagnosis || 'N/A'}</span>
                  </div>
                  <div className="detail-item">
                    <span className="label">Treatment Plan:</span>
                    <span className="value">{selectedAdmission.treatment_plan || 'N/A'}</span>
                  </div>
                  <div className="detail-item full-width">
                    <span className="label">Notes:</span>
                    <span className="value">{selectedAdmission.notes || 'No notes available'}</span>
                  </div>
                </div>
              </div>

              {selectedAdmission.discharge_summary && (
                <div className="details-section">
                  <h3>Discharge Summary</h3>
                  <p>{selectedAdmission.discharge_summary}</p>
                </div>
              )}
            </div>

            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={handleCloseDetails}>
                Close
              </button>
              {selectedAdmission.status === 'Active' && (
                <button 
                  className="btn btn-success"
                  onClick={() => {
                    handleDischarge(selectedAdmission.admission_id);
                    handleCloseDetails();
                  }}
                >
                  Discharge Patient
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {loading && <div className="loading">Loading admissions...</div>}
      {error && <div className="error-message">{error}</div>}

      {!loading && !error && (
        <>
          <div className="admission-stats">
            <div className="stat-item">
              <span className="stat-number">{filteredAdmissions.length}</span>
              <span className="stat-text">Showing Admissions</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{admissions.length}</span>
              <span className="stat-text">Total Admissions</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">
                {filteredAdmissions.filter(a => a.condition_level?.toLowerCase() === 'critical').length}
              </span>
              <span className="stat-text">Critical Cases</span>
            </div>
          </div>

          {filteredAdmissions.length === 0 && admissions.length > 0 ? (
            <div className="no-results">
              <p>No admissions found matching your search criteria.</p>
              <button 
                className="btn btn-secondary"
                onClick={() => {
                  setSearchTerm('');
                  setFilterCondition('all');
                }}
              >
                Clear Filters
              </button>
            </div>
          ) : filteredAdmissions.length === 0 ? (
            <p className="no-data">No current admissions</p>
          ) : (
            <Table columns={columns} data={filteredAdmissions} />
          )}
        </>
      )}
    </div>
  );
};

export default Admissions;
