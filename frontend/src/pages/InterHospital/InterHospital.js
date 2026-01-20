import React, { useState, useEffect } from 'react';
import { Table } from '../../components/Common';
import { interHospitalAPI } from '../../services/api';
import './InterHospital.css';

const InterHospital = () => {
  const [cityData, setCityData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCityData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await interHospitalAPI.getCityDashboard();
      // Handle paginated response - data may be in .results or directly in .data
      const responseData = response.data;
      const cityDataArray = Array.isArray(responseData) 
        ? responseData 
        : (responseData.results || []);
      setCityData(cityDataArray);
    } catch (err) {
      console.error('Failed to fetch inter-hospital data:', err);
      setError('Failed to load inter-hospital data. Please try again.');
      setCityData([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCityData();
  }, []);

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
    totalAvailable: cityData.reduce((sum, h) => sum + (h.available_beds || 0), 0),
    totalICU: cityData.reduce((sum, h) => sum + (h.icu_beds_available || 0), 0),
    avgOccupancy: cityData.length > 0 
      ? Math.round(cityData.reduce((sum, h) => sum + (h.occupancy_rate || 0), 0) / cityData.length) 
      : 0,
  };

  return (
    <div className="inter-hospital">
      <div className="page-header">
        <div>
          <h1>Inter-Hospital Capacity Sharing</h1>
          <p>City-wide bed availability and capacity coordination</p>
        </div>
        <button className="btn btn-primary" onClick={fetchCityData}>🔄 Refresh Data</button>
      </div>

      {loading && <div className="loading">Loading inter-hospital data...</div>}
      {error && <div className="error-message">{error}</div>}

      {!loading && !error && (
        <>
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

          <h2>City-Wide Hospital Capacity</h2>
          {cityData.length === 0 ? (
            <p className="no-data">No hospital data available</p>
          ) : (
            <Table columns={columns} data={cityData} />
          )}
        </>
      )}
    </div>
  );
};

export default InterHospital;
