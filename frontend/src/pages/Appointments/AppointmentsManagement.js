import React, { useState, useEffect } from 'react';
import './AppointmentsManagement.css';

const AppointmentsManagement = () => {
  const [appointments, setAppointments] = useState([]);
  const [stats, setStats] = useState({ total_pending: 0, today_appointments: 0, upcoming_appointments: 0 });
  const [loading, setLoading] = useState(true);
  const [selectedTab, setSelectedTab] = useState('pending'); // pending, today, upcoming, all
  const [selectedAppointment, setSelectedAppointment] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);
  const [editingAppointment, setEditingAppointment] = useState(null);
  const [editFormData, setEditFormData] = useState({});

  useEffect(() => {
    fetchStats();
    fetchAppointments();
  }, [selectedTab]);

  const fetchStats = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/appointments/appointments/stats/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchAppointments = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      let url = 'http://localhost:8000/api/appointments/appointments/';
      
      if (selectedTab === 'pending') {
        url += '?status=Scheduled';
      } else if (selectedTab === 'today') {
        const today = new Date().toISOString().split('T')[0];
        url += `?date=${today}`;
      } else if (selectedTab === 'upcoming') {
        url += '?status=Scheduled';
      } else if (selectedTab === 'all') {
        url += '?all=true';
      }

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        console.error('Response not OK:', response.status, response.statusText);
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Fetched appointments:', data);
      console.log('Data type:', typeof data, 'Is array:', Array.isArray(data));
      console.log('Data length:', data?.length);
      
      // Ensure data is an array
      const appointmentsData = Array.isArray(data) ? data : [];
      setAppointments(appointmentsData);
    } catch (error) {
      console.error('Error fetching appointments:', error);
      setAppointments([]); // Set empty array on error
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (appointmentId) => {
    if (!window.confirm('Approve this appointment and add to OPD queue?')) return;

    setActionLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(
        `http://localhost:8000/api/appointments/appointments/${appointmentId}/approve/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.ok) {
        const data = await response.json();
        alert(data.message);
        
        // Update the appointment status locally to remove buttons immediately
        setAppointments(prevAppointments => 
          prevAppointments.map(apt => 
            apt.appointment_id === appointmentId 
              ? { ...apt, status: 'Completed' }
              : apt
          )
        );
        
        fetchStats();
        setSelectedAppointment(null);
      } else {
        const error = await response.json();
        alert(`Error: ${error.error || 'Failed to approve appointment'}`);
      }
    } catch (error) {
      alert('Network error. Please try again.');
      console.error('Error approving appointment:', error);
    } finally {
      setActionLoading(false);
    }
  };

  const handleCancel = async (appointmentId) => {
    if (!window.confirm('Are you sure you want to cancel this appointment?')) return;

    setActionLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(
        `http://localhost:8000/api/appointments/appointments/${appointmentId}/cancel/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.ok) {
        alert('Appointment cancelled successfully');
        
        // Update the appointment status locally to remove buttons immediately
        setAppointments(prevAppointments => 
          prevAppointments.map(apt => 
            apt.appointment_id === appointmentId 
              ? { ...apt, status: 'Cancelled' }
              : apt
          )
        );
        
        fetchStats();
        setSelectedAppointment(null);
      } else {
        alert('Failed to cancel appointment');
      }
    } catch (error) {
      alert('Network error. Please try again.');
      console.error('Error cancelling appointment:', error);
    } finally {
      setActionLoading(false);
    }
  };

  const handleEdit = (appointment) => {
    setEditingAppointment(appointment);
    setEditFormData({
      appointment_date: appointment.appointment_date,
      appointment_time: appointment.appointment_time,
      reason_for_visit: appointment.reason_for_visit,
      status: appointment.status
    });
  };

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSaveEdit = async () => {
    if (!editingAppointment) return;

    setActionLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(
        `http://localhost:8000/api/appointments/appointments/${editingAppointment.appointment_id}/`,
        {
          method: 'PATCH',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(editFormData)
        }
      );

      if (response.ok) {
        alert('Appointment updated successfully');
        fetchAppointments();
        fetchStats();
        setEditingAppointment(null);
        setEditFormData({});
      } else {
        const error = await response.json();
        alert(`Failed to update appointment: ${error.detail || 'Unknown error'}`);
      }
    } catch (error) {
      alert('Network error. Please try again.');
      console.error('Error updating appointment:', error);
    } finally {
      setActionLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });
  };

  const formatTime = (timeString) => {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
  };

  const getStatusBadge = (status) => {
    const statusColors = {
      'Scheduled': 'status-pending',
      'Completed': 'status-completed',
      'Cancelled': 'status-cancelled',
      'Approved': 'status-approved'
    };
    return statusColors[status] || 'status-pending';
  };

  return (
    <div className="appointments-management">
      <div className="appointments-header">
        <div>
          <h1>📅 Appointments Management</h1>
          <p>Manage and approve patient appointments</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="appointments-stats">
        <div className="stat-card stat-pending">
          <div className="stat-icon">⏳</div>
          <div className="stat-details">
            <span className="stat-label">Pending Approval</span>
            <span className="stat-value">{stats.total_pending}</span>
          </div>
        </div>
        <div className="stat-card stat-today">
          <div className="stat-icon">📆</div>
          <div className="stat-details">
            <span className="stat-label">Today's Appointments</span>
            <span className="stat-value">{stats.today_appointments}</span>
          </div>
        </div>
        <div className="stat-card stat-upcoming">
          <div className="stat-icon">📅</div>
          <div className="stat-details">
            <span className="stat-label">Upcoming (7 days)</span>
            <span className="stat-value">{stats.upcoming_appointments}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="appointments-tabs">
        <button
          className={`tab-button ${selectedTab === 'pending' ? 'active' : ''}`}
          onClick={() => setSelectedTab('pending')}
        >
          Pending ({stats.total_pending})
        </button>
        <button
          className={`tab-button ${selectedTab === 'today' ? 'active' : ''}`}
          onClick={() => setSelectedTab('today')}
        >
          Today ({stats.today_appointments})
        </button>
        <button
          className={`tab-button ${selectedTab === 'upcoming' ? 'active' : ''}`}
          onClick={() => setSelectedTab('upcoming')}
        >
          Upcoming
        </button>
        <button
          className={`tab-button ${selectedTab === 'all' ? 'active' : ''}`}
          onClick={() => setSelectedTab('all')}
        >
          All Appointments
        </button>
      </div>

      {/* Appointments List */}
      <div className="appointments-content">
        {loading ? (
          <div className="appointments-loading">
            <div className="spinner"></div>
            <p>Loading appointments...</p>
          </div>
        ) : !Array.isArray(appointments) ? (
          <div className="appointments-empty">
            <span className="empty-icon">⚠️</span>
            <h3>Invalid data format</h3>
            <p>Expected array but got: {typeof appointments}</p>
          </div>
        ) : appointments.length === 0 ? (
          <div className="appointments-empty">
            <span className="empty-icon">📋</span>
            <h3>No appointments found</h3>
            <p>There are no appointments in this category</p>
          </div>
        ) : (
          <div className="appointments-grid">
            {appointments.map((appointment) => (
              <div key={appointment.appointment_id} className="appointment-card">
                <div className="appointment-card-header">
                  <div className="patient-info">
                    <h3>{appointment.patient_name}</h3>
                    <span className="patient-contact">📞 {appointment.patient_contact}</span>
                    <span className="patient-email">📧 {appointment.patient_email}</span>
                  </div>
                  <span className={`status-badge ${getStatusBadge(appointment.status)}`}>
                    {appointment.status}
                  </span>
                </div>

                <div className="appointment-details">
                  <div className="detail-row">
                    <span className="detail-label">📅 Date:</span>
                    <span className="detail-value">{formatDate(appointment.appointment_date)}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">🕐 Time:</span>
                    <span className="detail-value">{formatTime(appointment.appointment_time)}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">👨‍⚕️ Doctor:</span>
                    <span className="detail-value">{appointment.doctor_name || 'Not Assigned'}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">🏥 Department:</span>
                    <span className="detail-value">{appointment.department_name || 'N/A'}</span>
                  </div>
                  <div className="detail-row">
                    <span className="detail-label">📝 Reason:</span>
                    <span className="detail-value">{appointment.reason_for_visit}</span>
                  </div>
                </div>

                <div className="appointment-actions">
                  {appointment.status === 'Scheduled' && (
                    <>
                      <button
                        className="btn-edit"
                        onClick={() => handleEdit(appointment)}
                        disabled={actionLoading}
                      >
                        ✎ Edit
                      </button>
                      <button
                        className="btn-approve"
                        onClick={() => handleApprove(appointment.appointment_id)}
                        disabled={actionLoading}
                      >
                        ✓ Approve
                      </button>
                      <button
                        className="btn-cancel"
                        onClick={() => handleCancel(appointment.appointment_id)}
                        disabled={actionLoading}
                      >
                        ✗ Cancel
                      </button>
                    </>
                  )}
                  {appointment.status === 'Completed' && (
                    <button className="btn-view" disabled>
                      Completed
                    </button>
                  )}
                  {appointment.status === 'Cancelled' && (
                    <button className="btn-view" disabled>
                      Cancelled
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Edit Modal */}
      {editingAppointment && (
        <div className="edit-modal-overlay" onClick={() => setEditingAppointment(null)}>
          <div className="edit-modal" onClick={(e) => e.stopPropagation()}>
            <div className="edit-modal-header">
              <h2>✎ Edit Appointment</h2>
              <button className="modal-close-btn" onClick={() => setEditingAppointment(null)}>
                &times;
              </button>
            </div>
            
            <div className="edit-modal-body">
              <div className="edit-form-group">
                <label>Patient</label>
                <input type="text" value={editingAppointment.patient_name} disabled />
              </div>

              <div className="edit-form-row">
                <div className="edit-form-group">
                  <label>Appointment Date *</label>
                  <input
                    type="date"
                    name="appointment_date"
                    value={editFormData.appointment_date}
                    onChange={handleEditChange}
                    min={new Date().toISOString().split('T')[0]}
                  />
                </div>
                <div className="edit-form-group">
                  <label>Appointment Time *</label>
                  <input
                    type="time"
                    name="appointment_time"
                    value={editFormData.appointment_time}
                    onChange={handleEditChange}
                  />
                </div>
              </div>

              <div className="edit-form-group">
                <label>Reason for Visit *</label>
                <textarea
                  name="reason_for_visit"
                  value={editFormData.reason_for_visit}
                  onChange={handleEditChange}
                  rows="3"
                />
              </div>

              <div className="edit-form-group">
                <label>Status</label>
                <select
                  name="status"
                  value={editFormData.status}
                  onChange={handleEditChange}
                >
                  <option value="Scheduled">Scheduled (Pending)</option>
                  <option value="Cancelled">Cancelled</option>
                </select>
              </div>
            </div>

            <div className="edit-modal-actions">
              <button
                className="btn-modal-cancel"
                onClick={() => setEditingAppointment(null)}
              >
                Cancel
              </button>
              <button
                className="btn-modal-save"
                onClick={handleSaveEdit}
                disabled={actionLoading}
              >
                {actionLoading ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AppointmentsManagement;
