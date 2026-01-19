import React, { useState, useEffect } from 'react';
import { Card } from '../../components/Common';
import { dashboardAPI } from '../../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [summary, setSummary] = useState({
    total_beds: 0,
    available_beds: 0,
    occupied_beds: 0,
    occupancy_rate: 0,
    total_opd_patients_today: 0,
    waiting_patients: 0,
    current_admissions: 0,
    low_stock_items: 0,
  });

  const [departmentData, setDepartmentData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch summary and department data in parallel
        const [summaryResponse, departmentResponse] = await Promise.all([
          dashboardAPI.getSummary(),
          dashboardAPI.getDepartmentSummary()
        ]);
        
        setSummary(summaryResponse.data);
        setDepartmentData(departmentResponse.data);
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to load dashboard data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Operational Command View</h1>
        <p>Real-time hospital operations dashboard</p>
      </div>

      {loading && <div className="loading">Loading dashboard data...</div>}
      {error && <div className="error-message">{error}</div>}

      {!loading && !error && (
        <>
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
            {departmentData.length === 0 ? (
              <p className="no-data">No department data available</p>
            ) : (
              <div className="department-grid">
                {departmentData.map((dept) => (
                  <div key={dept.department_id || dept.department} className="department-card">
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
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
