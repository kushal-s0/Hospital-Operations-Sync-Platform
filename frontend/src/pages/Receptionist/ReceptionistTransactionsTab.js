import React, { useState, useEffect } from 'react';
import apiClient from '../../services/api';
import './ReceptionistDashboard.css';

const ReceptionistTransactionsTab = () => {
  const [transactionsData, setTransactionsData] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTransactionsData();
    fetchStatistics();
  }, [currentPage]);

  const fetchTransactionsData = async () => {
    try {
      const response = await apiClient.get('/receptionist/dashboard/financial_transactions_list/', {
        params: { page: currentPage, page_size: 10 }
      });
      console.log('Transactions API Response:', response.data);
      if (response.data && response.data.data) {
        setTransactionsData(response.data.data);
        setTotalPages(response.data.total_pages || 1);
      }
    } catch (err) {
      setError(err.message);
      console.error('Error fetching transactions:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStatistics = async () => {
    try {
      const response = await apiClient.get('/receptionist/dashboard/transaction_statistics/');
      console.log('Transaction Stats Response:', response.data);
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
        <h1>Financial Transactions</h1>
        <p>Track income and expense transactions</p>
      </header>

      {statistics && (
        <div className="stats-grid">
          <div className="stat-card">
            <h4>Income Count</h4>
            <p className="stat-value">{statistics.income_count}</p>
          </div>
          <div className="stat-card">
            <h4>Expense Count</h4>
            <p className="stat-value">{statistics.expense_count}</p>
          </div>
        </div>
      )}

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Transaction ID</th>
              <th>Type</th>
              <th>Reference</th>
              <th>Amount (₹)</th>
              <th>Method</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {transactionsData && transactionsData.length > 0 ? (
              transactionsData.map((transaction, index) => (
                <tr key={index}>
                  <td>{transaction.transaction_id}</td>
                  <td>
                    <span className={`badge badge-${transaction.transaction_type.toLowerCase()}`}>
                      {transaction.transaction_type}
                    </span>
                  </td>
                  <td>{transaction.reference_type}</td>
                  <td>{transaction.amount ? parseFloat(transaction.amount).toFixed(2) : '0.00'}</td>
                  <td>{transaction.payment_method}</td>
                  <td>{transaction.transaction_date ? new Date(transaction.transaction_date).toLocaleDateString() : 'N/A'}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" style={{ textAlign: 'center', padding: '20px' }}>No transaction data available</td>
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

export default ReceptionistTransactionsTab;
