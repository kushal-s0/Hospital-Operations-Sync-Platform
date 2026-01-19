import React, { useState, useEffect } from 'react';
import { Card } from '../../components/Common';
import './Dashboard.css';

const Dashboard = () => {
  // Mock data - will be replaced with API calls
  const [summary, setSummary] = useState({
    total_beds: 250,
    available_beds: 45,
    occupied_beds: 180,
    occupancy_rate: 72,
    total_opd_patients_today: 156,
    waiting_patients: 23,
    current_admissions: 180,
    low_stock_items: 8,
  });

  const [departmentData, setDepartmentData] = useState([
    { department: 'General Medicine', total_beds: 50, available: 12, occupied: 35, occupancy_rate: 70 },
    { department: 'ICU', total_beds: 20, available: 3, occupied: 17, occupancy_rate: 85 },
    { department: 'Pediatrics', total_beds: 30, available: 8, occupied: 20, occupancy_rate: 66.7 },
    { department: 'Surgery', total_beds: 40, available: 10, occupied: 28, occupancy_rate: 70 },
    { department: 'Maternity', total_beds: 25, available: 7, occupied: 16, occupancy_rate: 64 },
  ]);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Operational Command View</h1>
        <p>Real-time hospital operations dashboard</p>
      </div>

      <div className="stats-grid">
        <Card
          title="Total Beds"
          value={summary.total_beds}
          icon="🛏️"
          color="blue"
        />
        <Card
          title="Available Beds"
          value={summary.available_beds}
          icon="✅"
          color="green"
          subtitle={`${summary.occupancy_rate}% occupancy`}
        />
        <Card
          title="OPD Patients Today"
          value={summary.total_opd_patients_today}
          icon="🎫"
          color="orange"
          subtitle={`${summary.waiting_patients} waiting`}
        />
        <Card
          title="Current Admissions"
          value={summary.current_admissions}
          icon="📋"
          color="blue"
        />
        <Card
          title="Low Stock Items"
          value={summary.low_stock_items}
          icon="⚠️"
          color="red"
          subtitle="Needs attention"
        />
      </div>

      <div className="dashboard-section">
        <h2>Department-wise Bed Occupancy</h2>
        <div className="department-grid">
          {departmentData.map((dept) => (
            <div key={dept.department} className="department-card">
              <h3>{dept.department}</h3>
              <div className="department-stats">
                <div className="stat">
                  <span className="stat-value">{dept.total_beds}</span>
                  <span className="stat-label">Total</span>
                </div>
                <div className="stat">
                  <span className="stat-value available">{dept.available}</span>
                  <span className="stat-label">Available</span>
                </div>
                <div className="stat">
                  <span className="stat-value occupied">{dept.occupied}</span>
                  <span className="stat-label">Occupied</span>
                </div>
              </div>
              <div className="occupancy-bar">
                <div
                  className="occupancy-fill"
                  style={{ width: `${dept.occupancy_rate}%` }}
                ></div>
              </div>
              <span className="occupancy-text">{dept.occupancy_rate}% Occupancy</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
