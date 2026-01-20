import React, { useState, useEffect } from 'react';
import apiClient from '../../services/api';
import './ReceptionistDashboard.css';

const ReceptionistDashboardTab = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [vizType, setVizType] = useState('cards'); // Default to Stat Cards view

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/receptionist/dashboard/');
      console.log('Dashboard API Response:', response.data);
      if (response.data && response.data.data) {
        setDashboardData(response.data.data);
      } else if (response.data) {
        setDashboardData(response.data);
      }
    } catch (err) {
      setError(err.message);
      console.error('Error fetching dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!dashboardData) return <div className="error">No data available</div>;

  // Helper function to safely format numbers
  const formatNumber = (value) => {
    if (value === undefined || value === null) return '0.00';
    return parseFloat(value).toFixed(2);
  };

  const formatCount = (value) => {
    return value || 0;
  };

  // Calculate profit/loss based on available data
  const currentProfit = (dashboardData.total_income || 0) - (dashboardData.total_expenses || 0);
  const predictedProfit = dashboardData.predicted_profit || currentProfit;
  const lossArea = dashboardData.predicted_loss_area || 'Normal';
  const recommendations = dashboardData.recommendations || [];

  // Helper to get profit status
  const getProfitStatus = (profit) => {
    if (profit < 0) return { status: 'loss', icon: '📉', color: '#e74c3c' };
    if (profit < 50000) return { status: 'low', icon: '📊', color: '#f39c12' };
    return { status: 'healthy', icon: '📈', color: '#27ae60' };
  };

  const profitStatus = getProfitStatus(predictedProfit);
  const expenseRatio = (dashboardData.total_expenses || 0) / Math.max(dashboardData.total_income || 1, 1) * 100;

  return (
    <div className="receptionist-container">
      <header className="receptionist-header">
        <h1>Dashboard Overview</h1>
        <p>Quick summary of your operations</p>
      </header>

      {/* Visualization Type Selector */}
      <div className="viz-selector">
        <button 
          className={`viz-btn ${vizType === 'cards' ? 'active' : ''}`}
          onClick={() => setVizType('cards')}
          title="Simple stat cards"
        >
          📊 Stat Cards
        </button>
        <button 
          className={`viz-btn ${vizType === 'alerts' ? 'active' : ''}`}
          onClick={() => setVizType('alerts')}
          title="Alert status"
        >
          ⚠️ Alerts
        </button>
      </div>

      {/* View 1: Stat Cards (Default) */}
      {vizType === 'cards' && (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">💵</div>
              <div className="stat-content">
                <h3>Total Billing</h3>
                <p className="stat-value">₹{formatNumber(dashboardData.total_billing_amount)}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">✅</div>
              <div className="stat-content">
                <h3>Paid Bills</h3>
                <p className="stat-value">{formatCount(dashboardData.paid_bills_count)}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">⏳</div>
              <div className="stat-content">
                <h3>Pending Bills</h3>
                <p className="stat-value">{formatCount(dashboardData.pending_bills_count)}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">❌</div>
              <div className="stat-content">
                <h3>Failed Bills</h3>
                <p className="stat-value">{formatCount(dashboardData.failed_bills_count)}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">💸</div>
              <div className="stat-content">
                <h3>Total Income</h3>
                <p className="stat-value">₹{formatNumber(dashboardData.total_income)}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">📊</div>
              <div className="stat-content">
                <h3>Total Expenses</h3>
                <p className="stat-value">₹{formatNumber(dashboardData.total_expenses)}</p>
              </div>
            </div>

            <div className="stat-card profit-prediction">
              <div className="stat-icon">{profitStatus.icon}</div>
              <div className="stat-content">
                <h3>Predicted Profit</h3>
                <p className="stat-value" style={{ color: profitStatus.color }}>
                  ₹{formatNumber(predictedProfit)}
                </p>
                <p className="stat-sub">Status: {profitStatus.status}</p>
              </div>
            </div>

            <div className="stat-card loss-prediction">
              <div className="stat-icon">⚠️</div>
              <div className="stat-content">
                <h3>Loss Area</h3>
                <p className="stat-value">{lossArea}</p>
                <p className="stat-sub">Risk Detection</p>
              </div>
            </div>
          </div>
        </>
      )}



      {/* View 2: Alert Status */}
      {vizType === 'alerts' && (
        <div className="alerts-view">
          <div className="alert-container">
            {/* Profit Status Alert */}
            <div className={`alert-card alert-${profitStatus.status}`}>
              <div className="alert-icon">{profitStatus.icon}</div>
              <div className="alert-content">
                <h4>Profit Status: {profitStatus.status.toUpperCase()}</h4>
                <p>Predicted profit is ₹{formatNumber(Math.abs(predictedProfit))}</p>
              </div>
            </div>

            {/* Expense Alert */}
            {expenseRatio > 70 && (
              <div className="alert-card alert-warning">
                <div className="alert-icon">⚠️</div>
                <div className="alert-content">
                  <h4>High Expense Ratio</h4>
                  <p>Expenses are {formatNumber(expenseRatio)}% of income - consider cost optimization</p>
                </div>
              </div>
            )}

            {/* Loss Area Alert */}
            {lossArea !== 'Normal' && (
              <div className="alert-card alert-danger">
                <div className="alert-icon">🚨</div>
                <div className="alert-content">
                  <h4>Loss Area Detected: {lossArea}</h4>
                  <p>Monitor {lossArea.toLowerCase()} for potential losses</p>
                </div>
              </div>
            )}

            {/* Collection Alert */}
            {dashboardData.failed_bills_count > 2 && (
              <div className="alert-card alert-warning">
                <div className="alert-icon">📋</div>
                <div className="alert-content">
                  <h4>Failed Bills Alert</h4>
                  <p>{formatCount(dashboardData.failed_bills_count)} bills failed payment - follow up required</p>
                </div>
              </div>
            )}

            {/* Positive Status */}
            {profitStatus.status === 'healthy' && expenseRatio < 70 && lossArea === 'Normal' && (
              <div className="alert-card alert-success">
                <div className="alert-icon">✅</div>
                <div className="alert-content">
                  <h4>Operations Normal</h4>
                  <p>All metrics are within healthy ranges - maintain current strategy</p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}



      {/* Recommendations Section */}
      {recommendations && recommendations.length > 0 && (
        <div className="recommendations-section">
          <h2>📋 Recommendations</h2>
          <div className="recommendations-list">
            {recommendations.map((rec, idx) => (
              <div key={idx} className="recommendation-item">
                <p>{rec}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ReceptionistDashboardTab;
