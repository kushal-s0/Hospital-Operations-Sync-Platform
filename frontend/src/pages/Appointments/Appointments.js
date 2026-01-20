import React, { useState, useEffect } from 'react';
import './Appointments.css';

const Appointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userRole, setUserRole] = useState(null);
  const [filter, setFilter] = useState('all');
  const [editingPriority, setEditingPriority] = useState(null);

  useEffect(() => {
    // Get user role from localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      const user = JSON.parse(userData);
      setUserRole(user.role);
      
      // Only allow Admin and Nurse to see this page
      if (user.role !== 'Admin' && user.role !== 'Nurse') {
        setError('Unauthorized: Only Admin and Nurse can view appointments');
        setLoading(false);
        return;
      }
    }
    
    fetchAppointments();
    
    // Refresh appointments every 30 seconds
    const interval = setInterval(fetchAppointments, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchAppointments = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const token = localStorage.getItem('access_token');
      const response = await fetch('http://localhost:8000/api/receptionist/appointments/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch appointments');
      }

      const data = await response.json();
      setAppointments(Array.isArray(data) ? data : data.results || []);
    } catch (err) {
      console.error('Error fetching appointments:', err);
      setError('Failed to load appointments. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getFilteredAppointments = () => {
    if (filter === 'all') return appointments;
    if (filter === 'scheduled') return appointments.filter(a => a.status === 'Scheduled');
    if (filter === 'completed') return appointments.filter(a => a.status === 'Completed');
    if (filter === 'cancelled') return appointments.filter(a => a.status === 'Cancelled');
    return appointments;
  };

  const handleStatusChange = async (appointmentId, newStatus) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/receptionist/appointments/${appointmentId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ status: newStatus })
      });

      if (!response.ok) {
        throw new Error('Failed to update appointment status');
      }

      // Refresh appointments after status change
      fetchAppointments();
    } catch (err) {
      console.error('Error updating appointment status:', err);
      alert('Failed to update appointment status');
    }
  };

  const handleAcceptToOPD = async (appointmentId) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/receptionist/appointments/${appointmentId}/accept_to_opd/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to accept appointment to OPD queue');
      }

      const data = await response.json();
      alert(`✓ Appointment accepted!\nToken #${data.token_number}\nDoctor: ${data.doctor}\nDepartment: ${data.department}`);
      
      // Refresh appointments after accepting to OPD
      fetchAppointments();
    } catch (err) {
      console.error('Error accepting appointment to OPD:', err);
      alert(`Error: ${err.message}`);
    }
  };

  const handlePriorityChange = async (appointmentId, newPriority) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`http://localhost:8000/api/receptionist/appointments/${appointmentId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ priority: newPriority })
      });

      if (!response.ok) {
        throw new Error('Failed to update appointment priority');
      }

      setEditingPriority(null);
      fetchAppointments();
    } catch (err) {
      console.error('Error updating appointment priority:', err);
      alert('Failed to update appointment priority');
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const formatTime = (timeString) => {
    if (!timeString) return 'N/A';
    return timeString.substring(0, 5); // HH:MM format
  };

  const filteredAppointments = getFilteredAppointments();

  return (
    <div className="appointments-container">
      <div className="appointments-header">
        <h1>Appointments Management</h1>
        <p>View and manage all patient appointments</p>
      </div>

      {error && (
        <div className="error-message">
          <span>⚠️</span> {error}
        </div>
      )}

      {!error && (
        <>
          <div className="filter-section">
            <button 
              className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => setFilter('all')}
            >
              All ({appointments.length})
            </button>
            <button 
              className={`filter-btn ${filter === 'scheduled' ? 'active' : ''}`}
              onClick={() => setFilter('scheduled')}
            >
              Scheduled ({appointments.filter(a => a.status === 'Scheduled').length})
            </button>
            <button 
              className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
              onClick={() => setFilter('completed')}
            >
              Completed ({appointments.filter(a => a.status === 'Completed').length})
            </button>
            <button 
              className={`filter-btn ${filter === 'cancelled' ? 'active' : ''}`}
              onClick={() => setFilter('cancelled')}
            >
              Cancelled ({appointments.filter(a => a.status === 'Cancelled').length})
            </button>
          </div>

          {loading ? (
            <div className="loading">Loading appointments...</div>
          ) : filteredAppointments.length === 0 ? (
            <div className="no-data">
              <span className="no-data-icon">📭</span>
              <p>No appointments found in this category</p>
            </div>
          ) : (
            <div className="appointments-table-wrapper">
              <table className="appointments-table">
                <thead>
                  <tr>
                    <th>Appointment ID</th>
                    <th>Patient Name</th>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Reason for Visit</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredAppointments.map((appointment) => (
                    <tr key={appointment.appointment_id} className={`status-${appointment.status.toLowerCase()}`}>
                      <td className="appointment-id">#{appointment.appointment_id}</td>
                      <td className="patient-name">{appointment.patient_name || 'N/A'}</td>
                      <td>{formatDate(appointment.appointment_date)}</td>
                      <td>{formatTime(appointment.appointment_time)}</td>
                      <td className="reason">
                        <span title={appointment.reason_for_visit}>
                          {appointment.reason_for_visit || 'General Checkup'}
                        </span>
                      </td>
                      <td>
                        {userRole === 'Admin' ? (
                          editingPriority === appointment.appointment_id ? (
                            <select 
                              className="priority-select"
                              defaultValue={appointment.priority || 'normal'}
                              onChange={(e) => handlePriorityChange(appointment.appointment_id, e.target.value)}
                              onBlur={() => setEditingPriority(null)}
                              autoFocus
                            >
                              <option value="normal">Normal</option>
                              <option value="urgent">Urgent</option>
                              <option value="emergency">Emergency</option>
                            </select>
                          ) : (
                            <span 
                              className={`priority-badge priority-${(appointment.priority || 'normal').toLowerCase()}`}
                              onClick={() => setEditingPriority(appointment.appointment_id)}
                              title="Click to edit"
                            >
                              {appointment.priority ? appointment.priority.charAt(0).toUpperCase() + appointment.priority.slice(1) : 'Normal'}
                            </span>
                          )
                        ) : (
                          <span className={`priority-badge priority-${(appointment.priority || 'normal').toLowerCase()}`}>
                            {appointment.priority ? appointment.priority.charAt(0).toUpperCase() + appointment.priority.slice(1) : 'Normal'}
                          </span>
                        )}
                      </td>
                      <td>
                        <span className={`status-badge status-${appointment.status.toLowerCase()}`}>
                          {appointment.status}
                        </span>
                      </td>
                      <td className="actions">
                        {appointment.status === 'Scheduled' && (
                          <>
                            <button 
                              className="action-btn completed-btn"
                              onClick={() => handleAcceptToOPD(appointment.appointment_id)}
                              title="Add to OPD Queue"
                            >
                              ✓
                            </button>
                            <button 
                              className="action-btn cancel-btn"
                              onClick={() => handleStatusChange(appointment.appointment_id, 'Cancelled')}
                              title="Cancel"
                            >
                              ✕
                            </button>
                          </>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Appointments;
