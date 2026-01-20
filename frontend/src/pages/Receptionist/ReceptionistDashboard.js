import React, { useState, useEffect } from 'react';
import apiClient from '../../services/api';
import ReceptionistDashboardTab from './ReceptionistDashboardTab';
import './ReceptionistDashboard.css';

const ReceptionistDashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/receptionist/dashboard/');
      if (response.data.status === 'success') {
        setDashboardData(response.data.data);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="receptionist-container">
      <header className="receptionist-header">
        <h1>Receptionist Dashboard</h1>
        <p>Welcome to your workspace</p>
      </header>

      <div className="receptionist-main">
        <div className="receptionist-sidebar">
          <button
            className={`sidebar-btn ${activeTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('dashboard')}
          >
            📊 Dashboard
          </button>
          <button
            className={`sidebar-btn ${activeTab === 'billing' ? 'active' : ''}`}
            onClick={() => setActiveTab('billing')}
          >
            💳 Billing
          </button>
          <button
            className={`sidebar-btn ${activeTab === 'transactions' ? 'active' : ''}`}
            onClick={() => setActiveTab('transactions')}
          >
            💰 Transactions
          </button>
          <button
            className={`sidebar-btn ${activeTab === 'treatments' ? 'active' : ''}`}
            onClick={() => setActiveTab('treatments')}
          >
            🏥 Treatments
          </button>
        </div>

        <div className="receptionist-content">
          {loading && <div className="loading">Loading...</div>}
          {error && <div className="error">Error: {error}</div>}

          {activeTab === 'dashboard' && !loading && dashboardData && (
            <ReceptionistDashboardTab data={dashboardData} />
          )}
          {activeTab === 'billing' && <BillingTab />}
          {activeTab === 'transactions' && <TransactionsTab />}
          {activeTab === 'treatments' && <TreatmentsTab />}
        </div>
      </div>
    </div>
  );
};

const BillingTab = () => {
  const [billingData, setBillingData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [stats, setStats] = useState(null);
  const [processingPayment, setProcessingPayment] = useState(null);

  useEffect(() => {
    fetchBillingData(currentPage);
    fetchBillingStats();
  }, [currentPage]);

  useEffect(() => {
    // Load Razorpay script
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const fetchBillingData = async (page) => {
    try {
      setLoading(true);
      const response = await apiClient.get(`/receptionist/dashboard/billing_list/?page=${page}&page_size=10`);
      if (response.data.status === 'success') {
        setBillingData(response.data.data);
        setTotalPages(response.data.pagination.total_pages);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchBillingStats = async () => {
    try {
      const response = await apiClient.get('/receptionist/dashboard/billing_statistics/');
      if (response.data.status === 'success') {
        setStats(response.data);
      }
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const handlePayBill = async (bill) => {
    setProcessingPayment(bill.bill_id);
    
    try {
      // Create Razorpay order
      const orderResponse = await apiClient.post('/payments/create_order/', {
        bill_id: bill.bill_id
      });

      if (orderResponse.data.status !== 'success') {
        throw new Error(orderResponse.data.message || 'Failed to create order');
      }

      const { order_id, amount, currency, key } = orderResponse.data.data;

      // Configure Razorpay options
      const options = {
        key: key,
        amount: amount,
        currency: currency,
        name: 'Hospital Management System',
        description: `Payment for Bill #${bill.bill_id}`,
        order_id: order_id,
        handler: async function (response) {
          // Payment successful - verify payment
          try {
            const verifyResponse = await apiClient.post('/payments/verify_payment/', {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature
            });

            if (verifyResponse.data.status === 'success') {
              alert('Payment successful! Bill has been marked as paid.');
              // Refresh billing data
              fetchBillingData(currentPage);
              fetchBillingStats();
            } else {
              alert('Payment verification failed. Please contact support.');
            }
          } catch (error) {
            console.error('Verification error:', error);
            alert('Payment verification failed. Please contact support.');
          } finally {
            setProcessingPayment(null);
          }
        },
        prefill: {
          name: 'Patient',
          email: 'patient@example.com',
          contact: '9999999999'
        },
        notes: {
          bill_id: bill.bill_id,
          patient_id: bill.patient_id
        },
        theme: {
          color: '#3399cc'
        },
        modal: {
          ondismiss: function() {
            setProcessingPayment(null);
            console.log('Payment cancelled by user');
          }
        }
      };

      // Open Razorpay checkout
      const rzp = new window.Razorpay(options);
      rzp.on('payment.failed', function (response) {
        alert(`Payment failed: ${response.error.description}`);
        setProcessingPayment(null);
      });
      rzp.open();

    } catch (error) {
      console.error('Payment error:', error);
      alert(error.message || 'Failed to initiate payment. Please try again.');
      setProcessingPayment(null);
    }
  };

  return (
    <div className="billing-tab">
      <h2>Billing Records</h2>

      {stats && (
        <div className="stats-summary">
          <div className="summary-section">
            <h3>By Status</h3>
            <div className="summary-items">
              {stats.by_status.map((item, idx) => (
                <div key={idx} className="summary-item">
                  <span>{item.status}: {item.count} bills</span>
                  <span className="amount">₹{item.total.toFixed(2)}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="summary-section">
            <h3>By Payment Method</h3>
            <div className="summary-items">
              {stats.by_method.map((item, idx) => (
                <div key={idx} className="summary-item">
                  <span>{item.method}: {item.count} bills</span>
                  <span className="amount">₹{item.total.toFixed(2)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {loading && <div className="loading">Loading billing data...</div>}
      {error && <div className="error">Error: {error}</div>}

      {billingData.length > 0 && (
        <div className="data-table">
          <table>
            <thead>
              <tr>
                <th>Bill ID</th>
                <th>Patient ID</th>
                <th>Treatment ID</th>
                <th>Date</th>
                <th>Amount</th>
                <th>Payment Method</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {billingData.map((bill) => {
                console.log('Bill data:', bill); // Debug log
                console.log('Payment status:', bill.payment_status); // Debug log
                return (
                <tr key={bill.bill_id}>
                  <td>{bill.bill_id}</td>
                  <td>{bill.patient_id}</td>
                  <td>{bill.treatment_id}</td>
                  <td>{new Date(bill.bill_date).toLocaleDateString()}</td>
                  <td>₹{bill.amount.toFixed(2)}</td>
                  <td>{bill.payment_method}</td>
                  <td>
                    <span className={`status-badge status-${bill.payment_status.toLowerCase()}`}>
                      {bill.payment_status}
                    </span>
                  </td>
                  <td>
                    {(bill.payment_status && bill.payment_status.toLowerCase() === 'pending') ? (
                      <button 
                        className="pay-bill-btn"
                        onClick={() => handlePayBill(bill)}
                        disabled={processingPayment === bill.bill_id}
                        title="Process payment for this bill"
                      >
                        {processingPayment === bill.bill_id ? 'Processing...' : 'Pay Bill'}
                      </button>
                    ) : bill.payment_status && bill.payment_status.toLowerCase() === 'paid' ? (
                      <span className="paid-badge">✓ Paid</span>
                    ) : (
                      <span style={{color: '#999', fontSize: '12px'}}>-</span>
                    )}
                  </td>
                </tr>
                );
              })}
            </tbody>
          </table>

          <div className="pagination">
            <button
              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              disabled={currentPage === 1}
            >
              Previous
            </button>
            <span>Page {currentPage} of {totalPages}</span>
            <button
              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

const TransactionsTab = () => {
  const [transactionData, setTransactionData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchTransactionData(currentPage);
    fetchTransactionStats();
  }, [currentPage]);

  const fetchTransactionData = async (page) => {
    try {
      setLoading(true);
      const response = await apiClient.get(`/receptionist/dashboard/financial_transactions_list/?page=${page}&page_size=10`);
      if (response.data.status === 'success') {
        setTransactionData(response.data.data);
        setTotalPages(response.data.pagination.total_pages);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchTransactionStats = async () => {
    try {
      const response = await apiClient.get('/receptionist/dashboard/transaction_statistics/');
      if (response.data.status === 'success') {
        setStats(response.data);
      }
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  return (
    <div className="transactions-tab">
      <h2>Financial Transactions</h2>

      {stats && (
        <div className="stats-summary">
          <div className="summary-section">
            <h3>By Type</h3>
            <div className="summary-items">
              {stats.by_type.map((item, idx) => (
                <div key={idx} className="summary-item">
                  <span>{item.type}: {item.count} transactions</span>
                  <span className={`amount ${item.type === 'INCOME' ? 'income' : 'expense'}`}>
                    ₹{item.total.toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="summary-section">
            <h3>By Reference Type</h3>
            <div className="summary-items">
              {stats.by_reference_type.map((item, idx) => (
                <div key={idx} className="summary-item">
                  <span>{item.reference_type}: {item.count}</span>
                  <span className="amount">₹{item.total.toFixed(2)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {loading && <div className="loading">Loading transaction data...</div>}
      {error && <div className="error">Error: {error}</div>}

      {transactionData.length > 0 && (
        <div className="data-table">
          <table>
            <thead>
              <tr>
                <th>Transaction ID</th>
                <th>Hospital ID</th>
                <th>Reference Type</th>
                <th>Type</th>
                <th>Amount</th>
                <th>Payment Method</th>
                <th>Description</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {transactionData.map((trans) => (
                <tr key={trans.transaction_id}>
                  <td>{trans.transaction_id}</td>
                  <td>{trans.hospital_id}</td>
                  <td>{trans.reference_type}</td>
                  <td>
                    <span className={`badge badge-${trans.transaction_type.toLowerCase()}`}>
                      {trans.transaction_type}
                    </span>
                  </td>
                  <td>₹{trans.amount.toFixed(2)}</td>
                  <td>{trans.payment_method}</td>
                  <td>{trans.description}</td>
                  <td>{new Date(trans.transaction_date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="pagination">
            <button
              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              disabled={currentPage === 1}
            >
              Previous
            </button>
            <span>Page {currentPage} of {totalPages}</span>
            <button
              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

const TreatmentsTab = () => {
  const [treatmentData, setTreatmentData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchTreatmentData(currentPage);
  }, [currentPage]);

  const fetchTreatmentData = async (page) => {
    try {
      setLoading(true);
      const response = await apiClient.get(`/receptionist/dashboard/treatments_list/?page=${page}&page_size=10`);
      if (response.data.status === 'success') {
        setTreatmentData(response.data.data);
        setTotalPages(response.data.pagination.total_pages);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="treatments-tab">
      <h2>Treatment Records</h2>

      {loading && <div className="loading">Loading treatment data...</div>}
      {error && <div className="error">Error: {error}</div>}

      {treatmentData.length > 0 && (
        <div className="data-table">
          <table>
            <thead>
              <tr>
                <th>Treatment ID</th>
                <th>Appointment ID</th>
                <th>Type</th>
                <th>Description</th>
                <th>Cost</th>
                <th>Date</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {treatmentData.map((treatment) => (
                <tr key={treatment.treatment_id}>
                  <td>{treatment.treatment_id}</td>
                  <td>{treatment.appointment_id}</td>
                  <td>{treatment.treatment_type}</td>
                  <td>{treatment.description}</td>
                  <td>₹{treatment.cost.toFixed(2)}</td>
                  <td>{new Date(treatment.treatment_date).toLocaleDateString()}</td>
                  <td>{new Date(treatment.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="pagination">
            <button
              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              disabled={currentPage === 1}
            >
              Previous
            </button>
            <span>Page {currentPage} of {totalPages}</span>
            <button
              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ReceptionistDashboard;
