import React, { useState } from 'react';
import { Table } from '../../components/Common';
import './InterHospital.css';

const InterHospital = () => {
  const [cityData, setCityData] = useState([
    { hospital_code: 'HOSP-001', hospital_name: 'City General Hospital', city: 'Metro City', available_beds: 45, icu_beds_available: 5, occupancy_rate: 72, last_updated: '2026-01-19T10:30:00' },
    { hospital_code: 'HOSP-002', hospital_name: 'Central Medical Center', city: 'Metro City', available_beds: 30, icu_beds_available: 2, occupancy_rate: 85, last_updated: '2026-01-19T10:28:00' },
    { hospital_code: 'HOSP-003', hospital_name: 'Community Health Center', city: 'Metro City', available_beds: 60, icu_beds_available: 8, occupancy_rate: 55, last_updated: '2026-01-19T10:25:00' },
    { hospital_code: 'HOSP-004', hospital_name: 'Regional Hospital', city: 'Metro City', available_beds: 20, icu_beds_available: 0, occupancy_rate: 95, last_updated: '2026-01-19T10:20:00' },
  ]);

  const columns = [
    { key: 'hospital_code', label: 'Hospital Code' },
    { key: 'hospital_name', label: 'Hospital Name' },
    { key: 'city', label: 'City' },
    { 
      key: 'available_beds', 
      label: 'Available Beds',
      render: (row) => <span className="bed-count">{row.available_beds}</span>
    },
    { 
      key: 'icu_beds_available', 
      label: 'ICU Beds',
      render: (row) => (
        <span className={row.icu_beds_available === 0 ? 'no-beds' : 'bed-count'}>
          {row.icu_beds_available}
        </span>
      )
    },
    { 
      key: 'occupancy_rate', 
      label: 'Occupancy',
      render: (row) => (
        <div className="occupancy-cell">
          <div className="occupancy-bar-mini">
            <div 
              className={`occupancy-fill-mini ${row.occupancy_rate > 80 ? 'high' : row.occupancy_rate > 60 ? 'medium' : 'low'}`}
              style={{ width: `${row.occupancy_rate}%` }}
            ></div>
          </div>
          <span>{row.occupancy_rate}%</span>
        </div>
      )
    },
    { 
      key: 'last_updated', 
      label: 'Last Updated',
      render: (row) => new Date(row.last_updated).toLocaleTimeString()
    },
  ];

  const totalStats = {
    totalAvailable: cityData.reduce((sum, h) => sum + h.available_beds, 0),
    totalICU: cityData.reduce((sum, h) => sum + h.icu_beds_available, 0),
    avgOccupancy: Math.round(cityData.reduce((sum, h) => sum + h.occupancy_rate, 0) / cityData.length),
  };

  return (
    <div className="inter-hospital">
      <div className="page-header">
        <div>
          <h1>Inter-Hospital Capacity Sharing</h1>
          <p>City-wide bed availability and capacity coordination</p>
        </div>
        <button className="btn btn-primary">🔄 Refresh Data</button>
      </div>

      <div className="city-stats">
        <div className="stat-card">
          <div className="stat-icon">🏥</div>
          <div className="stat-info">
            <span className="stat-value">{cityData.length}</span>
            <span className="stat-label">Connected Hospitals</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🛏️</div>
          <div className="stat-info">
            <span className="stat-value">{totalStats.totalAvailable}</span>
            <span className="stat-label">Total Available Beds</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🚑</div>
          <div className="stat-info">
            <span className="stat-value">{totalStats.totalICU}</span>
            <span className="stat-label">ICU Beds Available</span>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-info">
            <span className="stat-value">{totalStats.avgOccupancy}%</span>
            <span className="stat-label">Avg City Occupancy</span>
          </div>
        </div>
      </div>

      <div className="api-info-card">
        <h3>📡 API Endpoint for City Dashboard</h3>
        <p>Share your hospital's anonymized capacity data with the central city health dashboard</p>
        <code>GET /api/interhospital/city-dashboard/</code>
      </div>

      <h2>City-Wide Hospital Capacity</h2>
      <Table columns={columns} data={cityData} />
    </div>
  );
};

export default InterHospital;
