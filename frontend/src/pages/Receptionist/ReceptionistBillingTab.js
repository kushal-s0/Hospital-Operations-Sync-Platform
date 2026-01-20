import React, { useState, useEffect } from 'react';
import apiClient from '../../services/api';
import './ReceptionistDashboard.css';

const ReceptionistBillingTab = () => {
  const [billingData, setBillingData] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchBillingData();
    fetchStatistics();
  }, [currentPage]);

  const fetchBillingData = async () => {
    try {
      const response = await apiClient.get('/receptionist/dashboard/billing_list/', {
        params: { page: currentPage, page_size: 10 }
      });
      console.log('Billing API Response:', response.data);
      if (response.data && response.data.data) {
        setBillingData(response.data.data);
        setTotalPages(response.data.total_pages || 1);
      }
    } catch (err) {
      setError(err.message);
      console.error('Error fetching billing:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await apiClient.get('/receptionist/dashboard/billing_statistics/');
      console.log('Billing Stats Response:', response.data);
      if (response.data && response.data.data) {
        setStatistics(response.data.data);
      }
    } catch (err) {
      console.error('Error fetching statistics:', err);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="receptionist-container">
      <header className="receptionist-header">
        <h1>Billing Records</h1>
        <p>View and manage all billing transactions</p>
      </header>

      {statistics && (
        <div className="stats-grid">
          <div className="stat-card">
            <h4>Paid</h4>
            <p className="stat-value">{statistics.paid_count}</p>
          </div>
          <div className="stat-card">
            <h4>Pending</h4>
            <p className="stat-value">{statistics.pending_count}</p>
          </div>
          <div className="stat-card">
            <h4>Failed</h4>
            <p className="stat-value">{statistics.failed_count}</p>
          </div>
        </div>
      )}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Bill ID</th>
              <th>Patient ID</th>
              <th>Amount (₹)</th>
              <th>Method</th>
              <th>Status</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {billingData && billingData.length > 0 ? (
              billingData.map((bill, index) => (
                <tr key={index}>
                  <td>{bill.bill_id}</td>
                  <td>{bill.patient_id}</td>
                  <td>{bill.amount ? parseFloat(bill.amount).toFixed(2) : '0.00'}</td>
                  <td>{bill.payment_method}</td>
                  <td>
                    <span className={`status-badge status-${bill.payment_status.toLowerCase()}`}>
                      {bill.payment_status}
                    </span>
                  </td>
                  <td>{bill.bill_date ? new Date(bill.bill_date).toLocaleDateString() : 'N/A'}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', padding: '20px' }}>No billing data available</td>
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

export default ReceptionistBillingTab;
