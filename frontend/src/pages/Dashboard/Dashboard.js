import React, { useState, useEffect, useCallback } from 'react';
import { Card, AnimatedNumber } from '../../components/Common';
import { BedIcon, PatientIcon, QueueIcon, AdmissionIcon, AlertIcon, CheckCircleIcon, ActivityIcon } from '../../components/Common/Icons';
import { dashboardAPI } from '../../services/api';
import './Dashboard.css';

const RING_RADIUS = 52;
const RING_CIRCUMFERENCE = 2 * Math.PI * RING_RADIUS;

const clampPercent = (value) => Math.min(100, Math.max(0, Number(value) || 0));

const occupancyLevel = (rate) => {
  if (rate > 80) return 'high';
  if (rate > 50) return 'medium';
  return 'low';
};

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
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const [user] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('user')) || {};
    } catch (e) {
      return {};
    }
  });

  // Only the very first load shows skeletons; background refreshes keep data on screen
  const fetchDashboardData = useCallback(async () => {
    setRefreshing(true);
    try {
      setError(null);

      // Fetch summary and department data in parallel
      const [summaryResponse, departmentResponse] = await Promise.all([
        dashboardAPI.getSummary(),
        dashboardAPI.getDepartmentSummary()
      ]);

      setSummary(summaryResponse.data);
      setDepartmentData(Array.isArray(departmentResponse.data) ? departmentResponse.data : []);
      setLastUpdated(new Date());
    } catch (err) {
      console.error('Failed to fetch dashboard data:', err);
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();

    // Refresh data every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, [fetchDashboardData]);

  const occupancyRate = clampPercent(summary.occupancy_rate);
  const hasData = lastUpdated !== null;

  return (
    <div className="dashboard">
      {/* Hero */}
      <section className="dashboard-hero">
        <div className="hero-decor" aria-hidden="true">
          <span className="hero-orb orb-1" />
          <span className="hero-orb orb-2" />
          <svg className="hero-ecg" viewBox="0 0 600 80" preserveAspectRatio="none">
            <path d="M0 40 H170 L186 40 L196 18 L208 62 L220 8 L232 72 L244 40 H360 L372 40 L380 28 L390 52 L398 40 H600" />
          </svg>
        </div>

        <div className="hero-copy">
          <span className="hero-eyebrow">
            <span className="live-dot" aria-hidden="true" />
            Live operations
          </span>
          <h1 className="hero-title">Hospital Operations Dashboard</h1>
          <p className="hero-subtitle">
            Real-time overview of beds, OPD flow, admissions and inventory
            {user.first_name ? ` — welcome back, ${user.first_name}.` : '.'}
          </p>
          <div className="hero-actions">
            <button
              type="button"
              className="hero-refresh"
              onClick={fetchDashboardData}
              disabled={refreshing}
            >
              <svg className={refreshing ? 'spinning' : ''} viewBox="0 0 20 20" fill="none" aria-hidden="true">
                <path d="M16.5 10a6.5 6.5 0 1 1-1.9-4.6M16.5 3.5v3.5H13" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              {refreshing ? 'Refreshing…' : 'Refresh'}
            </button>
            <span className="last-updated">
              {hasData ? `Last updated ${lastUpdated.toLocaleTimeString()}` : 'Fetching live data…'}
            </span>
          </div>
        </div>

        <div className="hero-ring" role="img" aria-label={`Bed occupancy ${occupancyRate.toFixed(0)} percent`}>
          <svg viewBox="0 0 120 120" className="ring-svg">
            <defs>
              <linearGradient id="dashboardRingGradient" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stopColor="#ffffff" />
                <stop offset="100%" stopColor="#5eead4" />
              </linearGradient>
            </defs>
            <circle className="ring-track" cx="60" cy="60" r={RING_RADIUS} />
            <circle
              className="ring-progress"
              cx="60"
              cy="60"
              r={RING_RADIUS}
              strokeDasharray={RING_CIRCUMFERENCE}
              style={{ strokeDashoffset: RING_CIRCUMFERENCE * (1 - occupancyRate / 100) }}
            />
          </svg>
          <div className="ring-label">
            <span className="ring-value">
              <AnimatedNumber value={Math.round(occupancyRate)} duration={1400} />%
            </span>
            <span className="ring-caption">Bed occupancy</span>
          </div>
        </div>
      </section>

      {error && (
        <div className="error-alert" role="alert">
          <AlertIcon />
          <span>{error}</span>
        </div>
      )}

      {loading && (
        <div className="stats-grid" aria-busy="true" aria-label="Loading dashboard data">
          {Array.from({ length: 6 }).map((_, index) => (
            <div key={index} className="skeleton skeleton-card" />
          ))}
        </div>
      )}

      {!loading && hasData && (
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
              <div>
                <h2 className="section-title">Department-wise Bed Occupancy</h2>
                <p className="section-subtitle">Real-time bed availability across all departments</p>
              </div>
              <div className="occupancy-legend" aria-hidden="true">
                <span><i className="legend-dot low" />Under 50%</span>
                <span><i className="legend-dot medium" />50–80%</span>
                <span><i className="legend-dot high" />Over 80%</span>
              </div>
            </div>

            {departmentData.length === 0 ? (
              <div className="empty-state">
                <QueueIcon />
                <p className="empty-state-title">No department data available</p>
                <p className="empty-state-text">Department statistics will appear here once data is available</p>
              </div>
            ) : (
              <div className="department-grid">
                {departmentData.map((dept, index) => {
                  const rate = clampPercent(dept.occupancy_rate);
                  const level = occupancyLevel(rate);

                  return (
                    <div
                      key={dept.department_id || dept.department}
                      className="department-card"
                      style={{ '--i': index }}
                    >
                      <div className="department-header">
                        <div>
                          <h3 className="department-name">{dept.department}</h3>
                          <span className="department-meta">
                            {dept.available} of {dept.total_beds} beds free
                          </span>
                        </div>
                        <span className={`occupancy-badge ${level}`}>
                          {dept.occupancy_rate}%
                        </span>
                      </div>

                      <div className="occupancy-bar">
                        <div className={`occupancy-fill ${level}`} style={{ width: `${rate}%` }} />
                      </div>

                      <div className="department-stats">
                        <div className="stat-item">
                          <span className="stat-value"><AnimatedNumber value={dept.total_beds} /></span>
                          <span className="stat-label">Total</span>
                        </div>
                        <div className="stat-item stat-available">
                          <span className="stat-value"><AnimatedNumber value={dept.available} /></span>
                          <span className="stat-label">Available</span>
                        </div>
                        <div className="stat-item stat-occupied">
                          <span className="stat-value"><AnimatedNumber value={dept.occupied} /></span>
                          <span className="stat-label">Occupied</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
