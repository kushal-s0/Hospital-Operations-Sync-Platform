import React, { useState, useEffect } from 'react';
import './AppointmentsList.css';

const AppointmentsList = ({ appointments = [], onAddToQueue, onEdit, onCancel, loading = false }) => {
  const [filteredAppointments, setFilteredAppointments] = useState([]);
  const [filterStatus, setFilterStatus] = useState('Scheduled');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('date');

  const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
  const isStaff = currentUser.role === 'Nurse' || currentUser.role === 'Doctor' || currentUser.role === 'Admin';

  useEffect(() => {
    let filtered = appointments;

    // Filter by status
    if (filterStatus !== 'All') {
      filtered = filtered.filter(apt => apt.status === filterStatus);
    }

    // Filter by search term (patient name or doctor name)
    if (searchTerm) {
      filtered = filtered.filter(apt =>
        (apt.patient_name && apt.patient_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (apt.doctor_name && apt.doctor_name.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Sort
    if (sortBy === 'date') {
      filtered.sort((a, b) => new Date(a.appointment_date) - new Date(b.appointment_date));
    } else if (sortBy === 'doctor') {
      filtered.sort((a, b) => (a.doctor_name || '').localeCompare(b.doctor_name || ''));
    }

    setFilteredAppointments(filtered);
  }, [appointments, filterStatus, searchTerm, sortBy]);

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  };

  const formatTime = (timeString) => {
    if (!timeString) return 'N/A';
    const [hours, minutes] = timeString.split(':');
    return `${hours}:${minutes}`;
  };

  const handleAddToQueue = (appointment) => {
    if (onAddToQueue) {
      onAddToQueue(appointment);
    }
  };

  const handleEdit = (appointment) => {
    if (onEdit) {
      onEdit(appointment);
    }
  };

  const handleCancel = (appointment) => {
    if (onCancel) {
      if (window.confirm(`Are you sure you want to cancel this appointment?`)) {
        onCancel(appointment);
      }
    }
  };

  if (!appointments || appointments.length === 0) {
    return (
      <div className="appointments-empty">
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <h3>No Appointments Found</h3>
          <p>There are no scheduled appointments yet.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="appointments-container">
      <div className="appointments-header">
        <h2>Appointment Management</h2>
        <div className="appointments-stats">
          <span className="stat-badge">
            Total: <strong>{appointments.length}</strong>
          </span>
          <span className="stat-badge">
            Scheduled: <strong>{appointments.filter(a => a.status === 'Scheduled').length}</strong>
          </span>
        </div>
      </div>

      <div className="appointments-filters">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search by patient or doctor name..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filter-controls">
          <div className="filter-group">
            <label>Status:</label>
            <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)} className="filter-select">
              <option value="All">All</option>
              <option value="Scheduled">Scheduled</option>
              <option value="Completed">Completed</option>
              <option value="Cancelled">Cancelled</option>
            </select>
          </div>
        </div>
      </div>

      {filteredAppointments.length === 0 ? (
        <div className="no-results">
          <p>No appointments match your search criteria.</p>
        </div>
      ) : (
        <div className="appointments-list">
          {filteredAppointments.map((appointment) => (
            <div key={appointment.appointment_id} className="appointment-card">
              <div className="appointment-header">
                <div className="appointment-patient">
                  <h3>{appointment.patient_name || `Patient ID: ${appointment.patient || 'N/A'}`}</h3>
                  <span className="patient-age">Age: {appointment.age || 'N/A'}</span>
                </div>
                <div className="appointment-status">
                  <span className={`status-badge status-${appointment.status.toLowerCase()}`}>
                    {appointment.status}
                  </span>
                </div>
              </div>

              <div className="appointment-details">
                <div className="detail-row">
                  <span className="detail-label">Date & Time:</span>
                  <span className="detail-value">
                    {formatDate(appointment.appointment_date)} at {formatTime(appointment.appointment_time)}
                  </span>
                </div>

                <div className="detail-row">
                  <span className="detail-label">Contact:</span>
                  <span className="detail-value">{appointment.contact_number || 'N/A'}</span>
                </div>

                <div className="detail-row">
                  <span className="detail-label">Doctor:</span>
                  <span className="detail-value">{appointment.doctor_name || 'Not Assigned'}</span>
                </div>

                <div className="detail-row">
                  <span className="detail-label">Reason:</span>
                  <span className="detail-value">{appointment.reason_for_visit || 'Not specified'}</span>
                </div>
              </div>

              <div className="appointment-actions">
                {isStaff && appointment.status === 'Scheduled' && (
                  <button
                    className="btn btn-add-queue"
                    onClick={() => handleAddToQueue(appointment)}
                    disabled={loading}
                    title="Add patient to OPD queue when they check in"
                  >
                    ➕ Add to Queue
                  </button>
                )}
                
                {appointment.status === 'Scheduled' && (
                  <>
                    <button
                      className="btn btn-edit"
                      onClick={() => handleEdit(appointment)}
                      disabled={loading}
                    >
                      ✏️ Edit
                    </button>
                    <button
                      className="btn btn-cancel"
                      onClick={() => handleCancel(appointment)}
                      disabled={loading}
                    >
                      ✗ Cancel
                    </button>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AppointmentsList;
