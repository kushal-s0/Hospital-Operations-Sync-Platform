import React, { useState, useEffect } from 'react';
import apiClient from '../../services/api';
import './ReceptionistDashboard.css';

const ReceptionistTreatmentsTab = () => {
  const [treatmentsData, setTreatmentsData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTreatmentsData();
  }, [currentPage]);

  const fetchTreatmentsData = async () => {
    try {
      const response = await apiClient.get('/receptionist/dashboard/treatments_list/', {
        params: { page: currentPage, page_size: 10 }
      });
      console.log('Treatments API Response:', response.data);
      if (response.data && response.data.data) {
        setTreatmentsData(response.data.data);
        setTotalPages(response.data.total_pages || 1);
      }
    } catch (err) {
      setError(err.message);
      console.error('Error fetching treatments:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="receptionist-container">
      <header className="receptionist-header">
        <h1>Treatments</h1>
        <p>View all treatment records</p>
      </header>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Treatment ID</th>
              <th>Appointment ID</th>
              <th>Type</th>
              <th>Cost (₹)</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {treatmentsData && treatmentsData.length > 0 ? (
              treatmentsData.map((treatment, index) => (
                <tr key={index}>
                  <td>{treatment.treatment_id}</td>
                  <td>{treatment.appointment_id}</td>
                  <td>{treatment.treatment_type}</td>
                  <td>{treatment.cost ? parseFloat(treatment.cost).toFixed(2) : '0.00'}</td>
                  <td>{treatment.treatment_date ? new Date(treatment.treatment_date).toLocaleDateString() : 'N/A'}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center', padding: '20px' }}>No treatment data available</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="pagination">
        <button 
          onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <span>Page {currentPage} of {totalPages}</span>
        <button 
          onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default ReceptionistTreatmentsTab;
