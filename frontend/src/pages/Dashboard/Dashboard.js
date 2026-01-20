import React, { useState, useEffect } from 'react';
import { Card } from '../../components/Common';
import { BedIcon, PatientIcon, QueueIcon, AdmissionIcon, AlertIcon, CheckCircleIcon, ActivityIcon } from '../../components/Common/Icons';
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
      <div className="page-header">
        <div>
          <h1 className="page-title">Hospital Operations Dashboard</h1>
          <p className="page-subtitle">Real-time overview of hospital operations and key metrics</p>
        </div>
        <div className="header-actions">
          <span className="last-updated">Last updated: {new Date().toLocaleTimeString()}</span>
        </div>
      </div>

      {loading && (
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading dashboard data...</p>
        </div>
      )}
      
      {error && (
        <div className="error-alert">
          <AlertIcon />
          <span>{error}</span>
        </div>
      )}

      {!loading && !error && (
        <>
          <div className="stats-grid">
            <Card
              title="Total Beds"
              value={summary.total_beds}
              icon={<BedIcon />}
              color="blue"
            />
            <Card
              title="Available Beds"
              value={summary.available_beds}
              icon={<CheckCircleIcon />}
              color="green"
              subtitle={`${summary.occupancy_rate}% occupancy rate`}
              trend={{ direction: 'up', value: '+5%' }}
            />
            <Card
              title="OPD Patients Today"
              value={summary.total_opd_patients_today}
              icon={<PatientIcon />}
              color="teal"
              subtitle={`${summary.waiting_patients} currently waiting`}
            />
            <Card
              title="Active Admissions"
              value={summary.current_admissions}
              icon={<AdmissionIcon />}
              color="blue"
            />
            <Card
              title="Low Stock Alerts"
              value={summary.low_stock_items}
              icon={<AlertIcon />}
              color="red"
              subtitle={summary.low_stock_items > 0 ? "Immediate attention required" : "All items stocked"}
            />
            <Card
              title="Queue Status"
              value={summary.waiting_patients}
              icon={<ActivityIcon />}
              color="purple"
              subtitle="Patients in queue"
            />
          </div>

          <div className="dashboard-section">
            <div className="section-header">
              <h2 className="section-title">Department-wise Bed Occupancy</h2>
              <p className="section-subtitle">Real-time bed availability across all departments</p>
            </div>
            
            {departmentData.length === 0 ? (
              <div className="empty-state">
                <QueueIcon />
                <p className="empty-state-title">No department data available</p>
                <p className="empty-state-text">Department statistics will appear here once data is available</p>
              </div>
            ) : (
              <div className="department-grid">
                {departmentData.map((dept) => (
                  <div key={dept.department_id || dept.department} className="department-card">
                    <div className="department-header">
                      <h3 className="department-name">{dept.department}</h3>
                      <span className={`occupancy-badge ${dept.occupancy_rate > 80 ? 'high' : dept.occupancy_rate > 50 ? 'medium' : 'low'}`}>
                        {dept.occupancy_rate}%
                      </span>
                    </div>
                    
                    <div className="department-stats">
                      <div className="stat-item">
                        <span className="stat-value">{dept.total_beds}</span>
                        <span className="stat-label">Total Beds</span>
                      </div>
                      <div className="stat-item stat-available">
                        <span className="stat-value">{dept.available}</span>
                        <span className="stat-label">Available</span>
                      </div>
                      <div className="stat-item stat-occupied">
                        <span className="stat-value">{dept.occupied}</span>
                        <span className="stat-label">Occupied</span>
                      </div>
                    </div>
                    
                    <div className="occupancy-bar-container">
                      <div className="occupancy-bar">
                        <div
                          className={`occupancy-fill ${dept.occupancy_rate > 80 ? 'high' : dept.occupancy_rate > 50 ? 'medium' : 'low'}`}
                          style={{ width: `${dept.occupancy_rate}%` }}
                        ></div>
                      </div>
                    </div>
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
