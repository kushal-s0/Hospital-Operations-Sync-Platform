import React, { useState, useEffect } from 'react';
import apiClient from '../../services/api';
import './ReceptionistDashboard.css';

const ReceptionistDashboardTab = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [vizType, setVizType] = useState('cards'); // cards, trends, alerts, comparison

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
          className={`viz-btn ${vizType === 'trends' ? 'active' : ''}`}
          onClick={() => setVizType('trends')}
          title="Trends and metrics"
        >
          📈 Trends
        </button>
        <button 
          className={`viz-btn ${vizType === 'alerts' ? 'active' : ''}`}
          onClick={() => setVizType('alerts')}
          title="Alert status"
        >
          ⚠️ Alerts
        </button>
        <button 
          className={`viz-btn ${vizType === 'comparison' ? 'active' : ''}`}
          onClick={() => setVizType('comparison')}
          title="Current vs Predicted"
        >
          ⚔️ Comparison
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

      {/* View 2: Trends & Breakdown */}
      {vizType === 'trends' && (
        <div className="trends-view">
          <div className="trends-container">
            {/* Income vs Expense Ratio */}
            <div className="trend-card">
              <h3>💰 Financial Ratio</h3>
              <div className="ratio-display">
                <div className="ratio-bars">
                  <div className="ratio-bar income-bar" style={{ width: `${100 - expenseRatio}%` }}>
                    <span>{formatNumber(100 - expenseRatio)}% Income</span>
                  </div>
                  <div className="ratio-bar expense-bar" style={{ width: `${expenseRatio}%` }}>
                    <span>{formatNumber(expenseRatio)}% Expense</span>
                  </div>
                </div>
              </div>
              <p className="trend-subtext">Expense ratio: {formatNumber(expenseRatio)}%</p>
            </div>

            {/* Profit Trend Card */}
            <div className="trend-card">
              <h3>📈 Profit Analysis</h3>
              <div className="profit-trend">
                <div className="trend-metric">
                  <span className="metric-label">Current Profit</span>
                  <span className="metric-value" style={{ color: currentProfit >= 0 ? '#27ae60' : '#e74c3c' }}>
                    ₹{formatNumber(currentProfit)}
                  </span>
                </div>
                <div className="trend-arrow">→</div>
                <div className="trend-metric">
                  <span className="metric-label">Predicted Profit</span>
                  <span className="metric-value" style={{ color: predictedProfit >= 0 ? '#27ae60' : '#e74c3c' }}>
                    ₹{formatNumber(predictedProfit)}
                  </span>
                </div>
              </div>
              <p className="trend-change" style={{ color: predictedProfit >= currentProfit ? '#27ae60' : '#e74c3c' }}>
                {predictedProfit >= currentProfit ? '📈 Trending up' : '📉 Trending down'}
                ({formatNumber(Math.abs(predictedProfit - currentProfit))})
              </p>
            </div>

            {/* Collection Efficiency */}
            <div className="trend-card">
              <h3>💳 Bill Collection</h3>
              <div className="collection-stats">
                <div className="coll-stat">
                  <span className="coll-label">Paid</span>
                  <span className="coll-badge paid">{formatCount(dashboardData.paid_bills_count)}</span>
                </div>
                <div className="coll-stat">
                  <span className="coll-label">Pending</span>
                  <span className="coll-badge pending">{formatCount(dashboardData.pending_bills_count)}</span>
                </div>
                <div className="coll-stat">
                  <span className="coll-label">Failed</span>
                  <span className="coll-badge failed">{formatCount(dashboardData.failed_bills_count)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* View 3: Alert Status */}
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

      {/* View 4: Current vs Predicted Comparison */}
      {vizType === 'comparison' && (
        <div className="comparison-view">
          <div className="comparison-grid">
            {/* Income Comparison */}
            <div className="comparison-card">
              <h3>Income</h3>
              <div className="comparison-bars">
                <div className="comp-item">
                  <span className="comp-label">Current</span>
                  <div className="comp-bar">
                    <div className="comp-fill income" style={{ width: '100%' }}>
                      ₹{formatNumber(dashboardData.total_income)}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Expense Comparison */}
            <div className="comparison-card">
              <h3>Expenses</h3>
              <div className="comparison-bars">
                <div className="comp-item">
                  <span className="comp-label">Current</span>
                  <div className="comp-bar">
                    <div className="comp-fill expense" style={{ width: Math.min((dashboardData.total_expenses / dashboardData.total_income) * 100, 100) + '%' }}>
                      ₹{formatNumber(dashboardData.total_expenses)}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Profit Comparison */}
            <div className="comparison-card">
              <h3>Profit</h3>
              <div className="comparison-bars">
                <div className="comp-item">
                  <span className="comp-label">Current</span>
                  <div className="comp-bar">
                    <div className={`comp-fill ${currentProfit >= 0 ? 'profit' : 'loss'}`} style={{ width: Math.min(Math.abs(currentProfit) / 100000 * 100, 100) + '%' }}>
                      ₹{formatNumber(currentProfit)}
                    </div>
                  </div>
                </div>
                <div className="comp-item">
                  <span className="comp-label">Predicted</span>
                  <div className="comp-bar">
                    <div className={`comp-fill ${predictedProfit >= 0 ? 'profit-predicted' : 'loss-predicted'}`} style={{ width: Math.min(Math.abs(predictedProfit) / 100000 * 100, 100) + '%' }}>
                      ₹{formatNumber(predictedProfit)}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Metrics Table */}
            <div className="comparison-card metrics-table">
              <h3>Key Metrics</h3>
              <table>
                <tbody>
                  <tr>
                    <td>Total Billing</td>
                    <td>₹{formatNumber(dashboardData.total_billing_amount)}</td>
                  </tr>
                  <tr>
                    <td>Paid Bills</td>
                    <td>{formatCount(dashboardData.paid_bills_count)}</td>
                  </tr>
                  <tr>
                    <td>Failed Bills</td>
                    <td>{formatCount(dashboardData.failed_bills_count)}</td>
                  </tr>
                  <tr>
                    <td>Expense Ratio</td>
                    <td>{formatNumber(expenseRatio)}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
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
