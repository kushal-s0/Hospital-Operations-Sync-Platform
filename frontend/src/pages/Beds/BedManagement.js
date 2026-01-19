import React, { useState, useEffect } from 'react';
import { StatusBadge } from '../../components/Common';
import { bedsAPI } from '../../services/api';
import './BedManagement.css';

const BedManagement = () => {
  const [selectedDepartment, setSelectedDepartment] = useState('all');
  const [beds, setBeds] = useState([]);
  const [departments, setDepartments] = useState([{ id: 'all', name: 'All Departments' }]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [bedsResponse, occupancyResponse] = await Promise.all([
          bedsAPI.getAll(),
          bedsAPI.getOccupancySummary()
        ]);
        
        // Handle paginated response - data may be in .results or directly in .data
        const responseData = bedsResponse.data;
        const bedsData = Array.isArray(responseData) 
          ? responseData 
          : (responseData.results || []);
        setBeds(bedsData);
        
        // Build departments list from occupancy summary
        const deptList = [{ id: 'all', name: 'All Departments' }];
        const deptData = Array.isArray(occupancyResponse.data) 
          ? occupancyResponse.data 
          : (occupancyResponse.data.results || []);
        deptData.forEach(dept => {
          deptList.push({ id: dept.department, name: dept.department });
        });
        setDepartments(deptList);
      } catch (err) {
        console.error('Failed to fetch beds data:', err);
        setError('Failed to load bed data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Ensure beds is always an array
  const bedsArray = Array.isArray(beds) ? beds : [];
  
  const filteredBeds = selectedDepartment === 'all' 
    ? bedsArray 
    : bedsArray.filter(bed => bed.department_name === selectedDepartment);

  const stats = {
    total: bedsArray.length,
    available: bedsArray.filter(b => b.status === 'Available').length,
    occupied: bedsArray.filter(b => b.status === 'Occupied').length,
    maintenance: bedsArray.filter(b => b.status === 'Maintenance').length,
  };

  return (
    <div className="bed-management">
      <div className="page-header">
        <div>
          <h1>Live Bed Availability Dashboard</h1>
          <p>Real-time bed occupancy and availability status</p>
        </div>
      </div>

      {loading && <div className="loading">Loading bed data...</div>}
      {error && <div className="error-message">{error}</div>}

      {!loading && !error && (
        <>
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
            {filteredBeds.length === 0 ? (
              <p className="no-data">No beds found</p>
            ) : (
              filteredBeds.map(bed => (
                <div key={bed.bed_id} className={`bed-card bed-${bed.status.toLowerCase()}`}>
                  <div className="bed-header">
                    <span className="bed-number">Bed #{bed.bed_id}</span>
                    <StatusBadge status={bed.status.toLowerCase()} />
                  </div>
                  <div className="bed-info">
                    <p><strong>Department:</strong> {bed.department_name}</p>
                    <p><strong>Type:</strong> {bed.bed_type}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default BedManagement;
