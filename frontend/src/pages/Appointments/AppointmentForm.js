import React, { useState, useEffect } from 'react';
import './AppointmentForm.css';

const AppointmentForm = ({ onSubmit, onCancel, appointment = null, publicMode = false }) => {
  const [formData, setFormData] = useState({
    patient_id: '',
    patient_first_name: '',
    patient_last_name: '',
    contact_number: '',
    age: '',
    doctor_id: '',
    doctor_name: '',
    appointment_date: '',
    appointment_time: '',
    time_slot: '',
    reason_for_visit: '',
  });

  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Get current user from localStorage (only if not in public mode)
  const currentUser = publicMode ? {} : JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    fetchDoctors();
    if (appointment) {
      // Populate form with appointment data if editing
      setFormData({
        patient_id: appointment.patient || '',
        patient_first_name: appointment.patient_name?.split(' ')[0] || '',
        patient_last_name: appointment.patient_name?.split(' ')[1] || '',
        age: appointment.age || '',
        doctor_id: appointment.doctor || '',
        doctor_name: appointment.doctor_name || '',
        appointment_date: appointment.appointment_date || '',
        appointment_time: appointment.appointment_time || '',
        time_slot: appointment.time_slot || '',
        reason_for_visit: appointment.reason_for_visit || '',
      });
    }
  }, [appointment]);

  const fetchDoctors = async () => {
    try {
      // Use public endpoint if in public mode, otherwise use authenticated endpoint
      const endpoint = publicMode 
        ? 'http://localhost:8000/api/auth/public/doctors/'
        : 'http://localhost:8000/api/auth/staff/';
      
      const headers = publicMode 
        ? { 'Content-Type': 'application/json' }
        : {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          };

      const response = await fetch(endpoint, { headers });

      if (response.ok) {
        const data = await response.json();
        // In public mode, data is already doctors list; in auth mode, need to filter
        const doctorsList = publicMode 
          ? data
          : (Array.isArray(data)
              ? data.filter(staff => staff.role === 'Doctor')
              : (data.results || []).filter(staff => staff.role === 'Doctor'));
        setDoctors(doctorsList);
      }
    } catch (err) {
      console.error('Error fetching doctors:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleDoctorChange = (e) => {
    const selectedId = e.target.value;
    const doctor = doctors.find(d => d.staff_id === parseInt(selectedId));
    
    setFormData(prev => ({
      ...prev,
      doctor_id: selectedId,
      doctor_name: doctor ? `${doctor.first_name} ${doctor.last_name}` : ''
    }));
  };

  const generateTimeSlot = () => {
    // Auto-generate time slot based on appointment time
    if (formData.appointment_time) {
      const [hours, minutes] = formData.appointment_time.split(':');
      const startTime = formData.appointment_time;
      
      // Add 30 minutes for slot duration
      let endHours = parseInt(hours);
      let endMinutes = parseInt(minutes) + 30;
      
      // Handle minute overflow
      if (endMinutes >= 60) {
        endMinutes -= 60;
        endHours += 1;
      }
      
      // Handle hour overflow (24-hour format)
      if (endHours >= 24) {
        endHours = 0;
      }
      
      const endTime = `${String(endHours).padStart(2, '0')}:${String(endMinutes).padStart(2, '0')}`;
      
      const slot = `${startTime}-${endTime}`;
      setFormData(prev => ({
        ...prev,
        time_slot: slot
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validation
    if (!formData.patient_first_name || !formData.patient_last_name) {
      setError('Patient name is required');
      return;
    }
    if (!formData.age) {
      setError('Age is required');
      return;
    }
    if (!formData.doctor_id) {
      setError('Doctor selection is required');
      return;
    }
    if (!formData.appointment_date) {
      setError('Appointment date is required');
      return;
    }
    if (!formData.appointment_time) {
      setError('Appointment time is required');
      return;
    }

    setLoading(true);

    try {
      const appointmentData = {
        patient_first_name: formData.patient_first_name,
        patient_last_name: formData.patient_last_name,
        contact_number_input: formData.contact_number,
        age: parseInt(formData.age),
        doctor_id: parseInt(formData.doctor_id),
        appointment_date: formData.appointment_date,
        appointment_time: formData.appointment_time,
        time_slot: formData.time_slot || `${formData.appointment_time}-${formData.appointment_time}`,
        reason_for_visit: formData.reason_for_visit,
      };

      // Add status only for authenticated mode
      if (!publicMode) {
        appointmentData.status = 'Scheduled';
      }

      // Use different endpoints based on mode
      let url, method, headers;
      
      if (publicMode) {
        // Public mode - always create new appointment
        url = 'http://localhost:8000/api/opd/public/book-appointment/';
        method = 'POST';
        headers = { 'Content-Type': 'application/json' };
      } else {
        // Authenticated mode - can create or update
        url = appointment
          ? `http://localhost:8000/api/opd/appointments/${appointment.appointment_id}/`
          : 'http://localhost:8000/api/opd/appointments/';
        method = appointment ? 'PUT' : 'POST';
        headers = {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          'Content-Type': 'application/json'
        };
      }

      const response = await fetch(url, {
        method,
        headers,
        body: JSON.stringify(appointmentData)
      });

      if (response.ok) {
        const result = await response.json();
        const message = publicMode 
          ? 'Appointment booked successfully! We will contact you shortly.'
          : `Appointment ${appointment ? 'updated' : 'created'} successfully!`;
        setSuccess(message);
        
        // In public mode, reset form after success
        if (publicMode) {
          setTimeout(() => {
            setFormData({
              patient_first_name: '',
              patient_last_name: '',
              contact_number: '',
              age: '',
              doctor_id: '',
              appointment_date: '',
              appointment_time: '',
              time_slot: '',
              reason_for_visit: '',
            });
            if (onSubmit) {
              onSubmit(result);
            }
          }, 2000);
        } else {
          setTimeout(() => {
            onSubmit(result);
          }, 1000);
        }
      } else {
        const errorData = await response.json();
        setError(errorData.detail || `Failed to ${appointment ? 'update' : 'create'} appointment`);
      }
    } catch (err) {
      console.error('Error:', err);
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="appointment-form-container">
      <h2>{publicMode ? 'Book an Appointment' : (appointment ? 'Edit Appointment' : 'Book New Appointment')}</h2>
      {publicMode && <p className="form-subtitle">Fill out the form below and we'll get back to you shortly</p>}
      
      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <form onSubmit={handleSubmit} className="appointment-form">
        <div className="form-section">
          <h3>Patient Information</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="patient_first_name">First Name *</label>
              <input
                type="text"
                id="patient_first_name"
                name="patient_first_name"
                value={formData.patient_first_name}
                onChange={handleChange}
                placeholder="Patient's first name"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="patient_last_name">Last Name *</label>
              <input
                type="text"
                id="patient_last_name"
                name="patient_last_name"
                value={formData.patient_last_name}
                onChange={handleChange}
                placeholder="Patient's last name"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="age">Age *</label>
              <input
                type="number"
                id="age"
                name="age"
                value={formData.age}
                onChange={handleChange}
                placeholder="Patient's age"
                min="1"
                max="150"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="contact_number">Contact Number {publicMode && '*'}</label>
              <input
                type="tel"
                id="contact_number"
                name="contact_number"
                value={formData.contact_number}
                onChange={handleChange}
                placeholder={publicMode ? "Your phone number" : "Patient's contact number"}
                required={publicMode}
              />
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>Appointment Details</h3>

          <div className="form-group">
            <label htmlFor="doctor_id">{publicMode ? 'Select Doctor *' : 'Doctor *'}</label>
            <select
              id="doctor_id"
              name="doctor_id"
              value={formData.doctor_id}
              onChange={handleDoctorChange}
              required
            >
              <option value="">{publicMode ? 'Choose a Doctor' : 'Select a Doctor'}</option>
              {doctors.map(doctor => (
                <option key={doctor.staff_id} value={doctor.staff_id}>
                  Dr. {doctor.first_name} {doctor.last_name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="appointment_date">{publicMode ? 'Preferred Date *' : 'Appointment Date *'}</label>
              <input
                type="date"
                id="appointment_date"
                name="appointment_date"
                value={formData.appointment_date}
                onChange={handleChange}
                min={publicMode ? new Date().toISOString().split('T')[0] : undefined}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="appointment_time">{publicMode ? 'Preferred Time *' : 'Appointment Time *'}</label>
              <input
                type="time"
                id="appointment_time"
                name="appointment_time"
                value={formData.appointment_time}
                onChange={(e) => {
                  handleChange(e);
                  // Auto-generate time slot when time changes
                  setTimeout(generateTimeSlot, 0);
                }}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="time_slot">Time Slot</label>
            <input
              type="text"
              id="time_slot"
              name="time_slot"
              value={formData.time_slot}
              onChange={handleChange}
              placeholder="e.g., 09:00-09:30"
              disabled
              className="input-disabled"
            />
            <small>Time slot is auto-generated (30-minute duration)</small>
          </div>

          <div className="form-group full-width">
            <label htmlFor="reason_for_visit">Reason for Visit {publicMode && '(Optional)'}</label>
            <textarea
              id="reason_for_visit"
              name="reason_for_visit"
              value={formData.reason_for_visit}
              onChange={handleChange}
              placeholder="Describe your symptoms or reason for visit"
              rows="4"
            />
          </div>
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading 
              ? (publicMode ? 'Booking...' : 'Processing...') 
              : (publicMode ? 'Book Appointment' : (appointment ? 'Update Appointment' : 'Book Appointment'))}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
            disabled={loading}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default AppointmentForm;
