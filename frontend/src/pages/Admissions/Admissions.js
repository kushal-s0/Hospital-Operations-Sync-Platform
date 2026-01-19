import React, { useState } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import './Admissions.css';

const Admissions = () => {
  const [admissions, setAdmissions] = useState([
    { id: 1, patient_name: 'John Doe', bed_number: 'GM-102', admission_type: 'planned', status: 'admitted', diagnosis: 'Pneumonia', treating_doctor: 'Dr. Smith', admission_date: '2026-01-18' },
    { id: 2, patient_name: 'Jane Smith', bed_number: 'ICU-001', admission_type: 'emergency', status: 'admitted', diagnosis: 'Cardiac Arrest', treating_doctor: 'Dr. Johnson', admission_date: '2026-01-17' },
    { id: 3, patient_name: 'Mike Wilson', bed_number: 'GM-103', admission_type: 'transfer', status: 'admitted', diagnosis: 'Post Surgery Care', treating_doctor: 'Dr. Brown', admission_date: '2026-01-15' },
  ]);

  const [showForm, setShowForm] = useState(false);

  const columns = [
    { key: 'id', label: 'Admission #' },
    { key: 'patient_name', label: 'Patient Name' },
    { key: 'bed_number', label: 'Bed' },
    { 
      key: 'admission_type', 
      label: 'Type',
      render: (row) => <StatusBadge status={row.admission_type} />
    },
    { key: 'diagnosis', label: 'Diagnosis' },
    { key: 'treating_doctor', label: 'Doctor' },
    { key: 'admission_date', label: 'Admission Date' },
    { 
      key: 'status', 
      label: 'Status',
      render: (row) => <StatusBadge status={row.status} />
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (row) => (
        <div className="action-buttons">
          <button className="btn btn-secondary btn-sm">View</button>
          <button className="btn btn-success btn-sm">Discharge</button>
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
                <label>Admission Type</label>
                <select>
                  <option value="planned">Planned</option>
                  <option value="emergency">Emergency</option>
                  <option value="transfer">Transfer</option>
                </select>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Diagnosis</label>
                <input type="text" placeholder="Enter diagnosis" />
              </div>
              <div className="form-group">
                <label>Treating Doctor</label>
                <input type="text" placeholder="Enter doctor name" />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Preferred Bed Type</label>
                <select>
                  <option value="general">General</option>
                  <option value="icu">ICU</option>
                  <option value="private">Private</option>
                  <option value="semi_private">Semi-Private</option>
                </select>
              </div>
              <div className="form-group">
                <label>Department</label>
                <select>
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

      <div className="admission-stats">
        <div className="stat-item">
          <span className="stat-number">{admissions.length}</span>
          <span className="stat-text">Current Admissions</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">{admissions.filter(a => a.admission_type === 'emergency').length}</span>
          <span className="stat-text">Emergency Cases</span>
        </div>
        <div className="stat-item">
          <span className="stat-number">3</span>
          <span className="stat-text">Discharges Today</span>
        </div>
      </div>

      <Table columns={columns} data={admissions} />
    </div>
  );
};

export default Admissions;
