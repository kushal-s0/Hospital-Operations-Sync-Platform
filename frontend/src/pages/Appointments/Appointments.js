import React, { useState, useEffect } from 'react';
import AppointmentForm from './AppointmentForm';
import AppointmentsList from './AppointmentsList';
import './Appointments.css';

const Appointments = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingAppointment, setEditingAppointment] = useState(null);
  const [addingToQueue, setAddingToQueue] = useState(null);
  const [showQueueDialog, setShowQueueDialog] = useState(false);
  const [queuePriority, setQueuePriority] = useState('normal');
  const [queueLoading, setQueueLoading] = useState(false);

  const currentUser = JSON.parse(localStorage.getItem('user') || '{}');
  const isStaff = currentUser.role === 'Nurse' || currentUser.role === 'Doctor' || currentUser.role === 'Admin';

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      
      if (!token) {
        setError('Please login to view appointments');
        setLoading(false);
        return;
      }
      
      const response = await fetch('http://localhost:8000/api/opd/appointments/', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        const appointmentsList = Array.isArray(data) ? data : (data.results || []);
        setAppointments(appointmentsList);
      } else if (response.status === 401) {
        setError('Session expired. Please login again.');
        // Optionally redirect to login
        setTimeout(() => {
          window.location.href = '/login';
        }, 2000);
      } else {
        setError('Failed to fetch appointments');
      }
    } catch (err) {
      console.error('Error fetching appointments:', err);
      setError('Error fetching appointments');
    } finally {
      setLoading(false);
    }
  };

  const handleFormSubmit = (newAppointment) => {
    if (editingAppointment) {
      // Update existing
      setAppointments(appointments.map(apt =>
        apt.appointment_id === newAppointment.appointment_id ? newAppointment : apt
      ));
      setEditingAppointment(null);
    } else {
      // Add new
      setAppointments([...appointments, newAppointment]);
    }
    setShowForm(false);
    setSuccess(`Appointment ${editingAppointment ? 'updated' : 'created'} successfully!`);
    setTimeout(() => setSuccess(''), 3000);
    fetchAppointments(); // Refresh list
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingAppointment(null);
  };

  const handleEdit = (appointment) => {
    setEditingAppointment(appointment);
    setShowForm(true);
  };

  const handleCancelAppointment = async (appointment) => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(
        `http://localhost:8000/api/opd/appointments/${appointment.appointment_id}/cancel/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.ok) {
        setSuccess('Appointment cancelled successfully');
        fetchAppointments();
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError('Failed to cancel appointment');
      }
    } catch (err) {
      console.error('Error:', err);
      setError('Error cancelling appointment');
    }
  };

  const handleAddToQueue = (appointment) => {
    setAddingToQueue(appointment);
    setShowQueueDialog(true);
  };

  const confirmAddToQueue = async () => {
    if (!addingToQueue) return;

    setQueueLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(
        `http://localhost:8000/api/opd/appointments/${addingToQueue.appointment_id}/add_to_queue/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            priority: queuePriority,
            notes: `From appointment for ${addingToQueue.patient_name}`
          })
        }
      );

      if (response.ok) {
        const result = await response.json();
        setSuccess('Patient added to OPD queue successfully! Token: #' + result.queue_entry.token_number);
        fetchAppointments();
        setShowQueueDialog(false);
        setAddingToQueue(null);
        setQueuePriority('normal');
        setTimeout(() => setSuccess(''), 5000);
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to add to queue');
      }
    } catch (err) {
      console.error('Error:', err);
      setError('Error adding to queue');
    } finally {
      setQueueLoading(false);
    }
  };

  return (
    <div className="appointments-page">
      {error && (
        <div className="alert alert-error">
          {error}
          <button className="alert-close" onClick={() => setError('')}>×</button>
        </div>
      )}

      {success && (
        <div className="alert alert-success">
          {success}
          <button className="alert-close" onClick={() => setSuccess('')}>×</button>
        </div>
      )}

      <div className="appointments-main">
        {!showForm ? (
          <>
            <div className="appointments-toolbar">
              {isStaff && (
                <button className="btn-create" onClick={() => {
                  setEditingAppointment(null);
                  setShowForm(true);
                }}>
                  + Create Appointment
                </button>
              )}
            </div>

            <AppointmentsList
              appointments={appointments}
              onAddToQueue={handleAddToQueue}
              onEdit={handleEdit}
              onCancel={handleCancelAppointment}
              loading={loading}
            />
          </>
        ) : (
          <AppointmentForm
            appointment={editingAppointment}
            onSubmit={handleFormSubmit}
            onCancel={handleFormCancel}
          />
        )}
      </div>

      {/* Add to Queue Dialog */}
      {showQueueDialog && addingToQueue && (
        <div className="dialog-overlay" onClick={() => !queueLoading && setShowQueueDialog(false)}>
          <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
            <h2>Add Patient to OPD Queue</h2>
            <div className="dialog-body">
              <p><strong>Patient:</strong> {addingToQueue.patient_name}</p>
              <p><strong>Age:</strong> {addingToQueue.age} years</p>
              <p><strong>Doctor:</strong> {addingToQueue.doctor_name || 'Not Assigned'}</p>
              <p><strong>Appointment:</strong> {addingToQueue.appointment_date} at {addingToQueue.appointment_time}</p>

              <div className="form-group">
                <label htmlFor="priority">Priority Level:</label>
                <select
                  id="priority"
                  value={queuePriority}
                  onChange={(e) => setQueuePriority(e.target.value)}
                  disabled={queueLoading}
                >
                  <option value="normal">Normal</option>
                  <option value="urgent">Urgent</option>
                  <option value="emergency">Emergency</option>
                </select>
              </div>
            </div>

            <div className="dialog-actions">
              <button
                className="btn btn-primary"
                onClick={confirmAddToQueue}
                disabled={queueLoading}
              >
                {queueLoading ? 'Processing...' : 'Add to Queue'}
              </button>
              <button
                className="btn btn-secondary"
                onClick={() => setShowQueueDialog(false)}
                disabled={queueLoading}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Appointments;
