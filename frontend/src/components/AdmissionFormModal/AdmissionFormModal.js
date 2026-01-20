import React, { useState, useEffect } from 'react';
import './AdmissionFormModal.css';

const AdmissionFormModal = ({ opdEntry, onClose, onSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [availableBeds, setAvailableBeds] = useState([]);
  const [formData, setFormData] = useState({
    opd_queue_id: opdEntry?.id || '',
    bed_id: '',
    condition_level: 'Medium',
    admission_notes: ''
  });

  useEffect(() => {
    fetchAvailableBeds();
  }, []);

  const fetchAvailableBeds = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/beds/available/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setAvailableBeds(data);
      }
    } catch (error) {
      console.error('Error fetching available beds:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.bed_id) {
      alert('Please select a bed');
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/admissions/admit_from_opd/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        alert(data.message || 'Patient admitted successfully!');
        onSuccess();
        onClose();
      } else {
        const error = await response.json();
        alert(`Error: ${error.error || 'Failed to admit patient'}`);
      }
    } catch (error) {
      alert('Network error. Please try again.');
      console.error('Error admitting patient:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admission-modal-overlay" onClick={onClose}>
      <div className="admission-modal" onClick={(e) => e.stopPropagation()}>
        <div className="admission-modal-header">
          <h2>🏥 Admit Patient</h2>
          <button className="modal-close-btn" onClick={onClose}>
            &times;
          </button>
        </div>

        <div className="admission-modal-body">
          {/* Patient Information (Pre-filled from OPD) */}
          <div className="info-section">
            <h3>Patient Information</h3>
            <div className="info-grid">
              <div className="info-item">
                <label>Patient Name:</label>
                <span>{opdEntry?.patient_name || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Token Number:</label>
                <span>#{opdEntry?.token_number || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Doctor:</label>
                <span>{opdEntry?.doctor_name || 'N/A'}</span>
              </div>
              <div className="info-item">
                <label>Department:</label>
                <span>{opdEntry?.department_name || 'N/A'}</span>
              </div>
            </div>
          </div>

          {/* Admission Form */}
          <form onSubmit={handleSubmit}>
            <div className="form-section">
              <h3>Admission Details</h3>

              <div className="form-group">
                <label htmlFor="bed_id">Select Bed *</label>
                <select
                  id="bed_id"
                  name="bed_id"
                  value={formData.bed_id}
                  onChange={handleChange}
                  required
                >
                  <option value="">-- Select a bed --</option>
                  {availableBeds.map(bed => (
                    <option key={bed.bed_id} value={bed.bed_id}>
                      Bed {bed.bed_id} - {bed.bed_type} ({bed.department_name || 'Unknown Dept'})
                    </option>
                  ))}
                </select>
                {availableBeds.length === 0 && (
                  <small className="text-warning">⚠️ No beds available at the moment</small>
                )}
              </div>

              <div className="form-group">
                <label htmlFor="condition_level">Condition Level *</label>
                <select
                  id="condition_level"
                  name="condition_level"
                  value={formData.condition_level}
                  onChange={handleChange}
                  required
                >
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                  <option value="Critical">Critical</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="admission_notes">Admission Notes</label>
                <textarea
                  id="admission_notes"
                  name="admission_notes"
                  value={formData.admission_notes}
                  onChange={handleChange}
                  rows="4"
                  placeholder="Enter any additional notes for admission..."
                />
              </div>
            </div>

            <div className="admission-modal-actions">
              <button
                type="button"
                className="btn-modal-cancel"
                onClick={onClose}
                disabled={loading}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn-modal-admit"
                disabled={loading || availableBeds.length === 0}
              >
                {loading ? 'Admitting...' : '✓ Admit Patient'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AdmissionFormModal;
