import React, { useState, useEffect } from 'react';
import { paymentAPI } from '../../services/api';
import './ReceptionistDashboard.css';

const ReceptionistTransactionsTab = () => {
  const [transactionsData, setTransactionsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPaymentTransactions();
  }, []);

  const fetchPaymentTransactions = async () => {
    try {
      setLoading(true);
      const response = await paymentAPI.getTransactionHistory();
      console.log('Payment Transactions Response:', response.data);
      
      // Backend returns {status: 'success', data: [...]}
      const data = response.data.data || [];
      setTransactionsData(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching payment transactions:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading payment transactions...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  // Calculate statistics from transactions
  const totalAmount = transactionsData.reduce((sum, t) => sum + parseFloat(t.amount || 0), 0);
  const successCount = transactionsData.filter(t => t.status === 'captured').length;
  const failedCount = transactionsData.filter(t => t.status === 'failed').length;

  return (
    <div className="receptionist-container">
      <header className="receptionist-header">
        <h1>Payment Transactions</h1>
        <p>View all Razorpay payment transactions</p>
      </header>

      <div className="stats-grid">
        <div className="stat-card">
          <h4>Total Transactions</h4>
          <p className="stat-value">{transactionsData.length}</p>
        </div>
        <div className="stat-card">
          <h4>Successful</h4>
          <p className="stat-value" style={{ color: '#28a745' }}>{successCount}</p>
        </div>
        <div className="stat-card">
          <h4>Failed</h4>
          <p className="stat-value" style={{ color: '#dc3545' }}>{failedCount}</p>
        </div>
        <div className="stat-card">
          <h4>Total Amount</h4>
          <p className="stat-value">₹{totalAmount.toFixed(2)}</p>
        </div>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Transaction ID</th>
              <th>Bill ID</th>
              <th>Order ID</th>
              <th>Payment ID</th>
              <th>Amount (₹)</th>
              <th>Status</th>
              <th>Payment Method</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {transactionsData && transactionsData.length > 0 ? (
              transactionsData.map((transaction) => (
                <tr key={transaction.transaction_id}>
                  <td>{transaction.transaction_id}</td>
                  <td>{transaction.bill_id || 'N/A'}</td>
                  <td>
                    <code style={{ fontSize: '0.85em', color: '#6c757d' }}>
                      {transaction.razorpay_order_id ? transaction.razorpay_order_id.substring(0, 20) + '...' : 'N/A'}
                    </code>
                  </td>
                  <td>
                    <code style={{ fontSize: '0.85em', color: '#6c757d' }}>
                      {transaction.razorpay_payment_id ? transaction.razorpay_payment_id.substring(0, 20) + '...' : 'N/A'}
                    </code>
                  </td>
                  <td>₹{parseFloat(transaction.amount || 0).toFixed(2)}</td>
                  <td>
                    <span className={`badge badge-${
                      transaction.status === 'captured' ? 'success' :
                      transaction.status === 'failed' ? 'danger' :
                      transaction.status === 'authorized' ? 'warning' :
                      'secondary'
                    }`}>
                      {transaction.status.toUpperCase()}
                    </span>
                  </td>
                  <td>{transaction.payment_method || 'N/A'}</td>
                  <td>{transaction.created_at ? new Date(transaction.created_at).toLocaleString() : 'N/A'}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="8" style={{ textAlign: 'center', padding: '20px' }}>
                  No payment transactions found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ReceptionistTransactionsTab;
