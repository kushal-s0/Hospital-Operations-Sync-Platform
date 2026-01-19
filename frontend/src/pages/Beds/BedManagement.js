import React, { useState } from 'react';
import { StatusBadge } from '../../components/Common';
import './BedManagement.css';

const BedManagement = () => {
  const [selectedDepartment, setSelectedDepartment] = useState('all');
  
  const departments = [
    { id: 'all', name: 'All Departments' },
    { id: 'general', name: 'General Medicine' },
    { id: 'icu', name: 'ICU' },
    { id: 'surgery', name: 'Surgery' },
    { id: 'pediatrics', name: 'Pediatrics' },
    { id: 'maternity', name: 'Maternity' },
  ];

  const beds = [
    { id: 1, bed_number: 'GM-101', department: 'General Medicine', bed_type: 'general', status: 'available', room_number: 'R101', floor: 1 },
    { id: 2, bed_number: 'GM-102', department: 'General Medicine', bed_type: 'general', status: 'occupied', room_number: 'R101', floor: 1, patient_name: 'John Doe' },
    { id: 3, bed_number: 'ICU-001', department: 'ICU', bed_type: 'icu', status: 'occupied', room_number: 'ICU-1', floor: 2, patient_name: 'Jane Smith' },
    { id: 4, bed_number: 'ICU-002', department: 'ICU', bed_type: 'icu', status: 'available', room_number: 'ICU-1', floor: 2 },
    { id: 5, bed_number: 'SRG-101', department: 'Surgery', bed_type: 'private', status: 'maintenance', room_number: 'S101', floor: 3 },
    { id: 6, bed_number: 'PED-101', department: 'Pediatrics', bed_type: 'pediatric', status: 'reserved', room_number: 'P101', floor: 1 },
    { id: 7, bed_number: 'MAT-101', department: 'Maternity', bed_type: 'maternity', status: 'available', room_number: 'M101', floor: 1 },
    { id: 8, bed_number: 'GM-103', department: 'General Medicine', bed_type: 'semi_private', status: 'occupied', room_number: 'R102', floor: 1, patient_name: 'Mike Wilson' },
  ];

  const filteredBeds = selectedDepartment === 'all' 
    ? beds 
    : beds.filter(bed => bed.department.toLowerCase().includes(selectedDepartment));

  const stats = {
    total: beds.length,
    available: beds.filter(b => b.status === 'available').length,
    occupied: beds.filter(b => b.status === 'occupied').length,
    maintenance: beds.filter(b => b.status === 'maintenance').length,
  };

  return (
    <div className="bed-management">
      <div className="page-header">
        <div>
          <h1>Live Bed Availability Dashboard</h1>
          <p>Real-time bed occupancy and availability status</p>
        </div>
      </div>

      <div className="bed-stats">
        <div className="stat-card total">
          <span className="stat-value">{stats.total}</span>
          <span className="stat-label">Total Beds</span>
        </div>
        <div className="stat-card available">
          <span className="stat-value">{stats.available}</span>
          <span className="stat-label">Available</span>
        </div>
        <div className="stat-card occupied">
          <span className="stat-value">{stats.occupied}</span>
          <span className="stat-label">Occupied</span>
        </div>
        <div className="stat-card maintenance">
          <span className="stat-value">{stats.maintenance}</span>
          <span className="stat-label">Maintenance</span>
        </div>
      </div>

      <div className="filter-section">
        <label>Filter by Department:</label>
        <select 
          value={selectedDepartment} 
          onChange={(e) => setSelectedDepartment(e.target.value)}
        >
          {departments.map(dept => (
            <option key={dept.id} value={dept.id}>{dept.name}</option>
          ))}
        </select>
      </div>

      <div className="beds-grid">
        {filteredBeds.map(bed => (
          <div key={bed.id} className={`bed-card bed-${bed.status}`}>
            <div className="bed-header">
              <span className="bed-number">{bed.bed_number}</span>
              <StatusBadge status={bed.status} />
            </div>
            <div className="bed-info">
              <p><strong>Department:</strong> {bed.department}</p>
              <p><strong>Type:</strong> {bed.bed_type.replace('_', ' ')}</p>
              <p><strong>Room:</strong> {bed.room_number}</p>
              <p><strong>Floor:</strong> {bed.floor}</p>
              {bed.patient_name && (
                <p><strong>Patient:</strong> {bed.patient_name}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BedManagement;
