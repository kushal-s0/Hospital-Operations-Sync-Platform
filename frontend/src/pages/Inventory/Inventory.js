import React, { useState, useEffect } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import { inventoryAPI } from '../../services/api';
import './Inventory.css';

const Inventory = () => {
  const [activeTab, setActiveTab] = useState('all');
  const [mlAlerts, setMlAlerts] = useState(null);
  const [demandForecast, setDemandForecast] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
  const [itemPrediction, setItemPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const inventoryItems = [
    { id: 1, name: 'Paracetamol 500mg', sku: 'MED-001', category: 'Medicine', item_type: 'medicine', current_stock: 500, minimum_stock: 100, unit: 'tablets', unit_price: 2.50, expiry_date: '2027-06-15', is_low_stock: false },
    { id: 2, name: 'Surgical Gloves (L)', sku: 'SUP-001', category: 'Consumable', item_type: 'consumable', current_stock: 50, minimum_stock: 100, unit: 'boxes', unit_price: 15.00, expiry_date: '2026-12-01', is_low_stock: true },
    { id: 3, name: 'IV Cannula 20G', sku: 'SUP-002', category: 'Consumable', item_type: 'consumable', current_stock: 200, minimum_stock: 150, unit: 'pieces', unit_price: 5.00, expiry_date: '2027-03-20', is_low_stock: false },
    { id: 4, name: 'Amoxicillin 250mg', sku: 'MED-002', category: 'Medicine', item_type: 'medicine', current_stock: 30, minimum_stock: 50, unit: 'capsules', unit_price: 8.00, expiry_date: '2026-02-10', is_low_stock: true },
    { id: 5, name: 'Oxygen Mask', sku: 'EQP-001', category: 'Equipment', item_type: 'equipment', current_stock: 75, minimum_stock: 30, unit: 'pieces', unit_price: 25.00, expiry_date: null, is_low_stock: false },
    { id: 6, name: 'Surgical Sutures', sku: 'SUR-001', category: 'Surgical', item_type: 'surgical', current_stock: 15, minimum_stock: 25, unit: 'packs', unit_price: 45.00, expiry_date: '2026-08-15', is_low_stock: true },
  ];

  // Fetch ML predictions on mount
  useEffect(() => {
    fetchMLPredictions();
  }, []);

  const fetchMLPredictions = async () => {
    setLoading(true);
    try {
      // Fetch ML alerts
      const alertsResponse = await inventoryAPI.getAllAlerts();
      setMlAlerts(alertsResponse.data);
      
      // Fetch demand forecast
      const forecastResponse = await inventoryAPI.getDemandForecast();
      setDemandForecast(forecastResponse.data);
    } catch (error) {
      console.error('Error fetching ML predictions:', error);
    }
    setLoading(false);
  };

  const fetchItemPrediction = async (itemId) => {
    try {
      const response = await inventoryAPI.getPrediction(itemId);
      setItemPrediction(response.data);
      setSelectedItem(itemId);
    } catch (error) {
      console.error('Error fetching item prediction:', error);
    }
  };

  const filteredItems = activeTab === 'all' 
    ? inventoryItems 
    : activeTab === 'low_stock' 
      ? inventoryItems.filter(item => item.is_low_stock)
      : inventoryItems.filter(item => item.item_type === activeTab);

  const columns = [
    { key: 'sku', label: 'SKU' },
    { key: 'name', label: 'Item Name' },
    { key: 'category', label: 'Category' },
    { 
      key: 'current_stock', 
      label: 'Stock',
      render: (row) => (
        <span className={row.is_low_stock ? 'stock-low' : 'stock-ok'}>
          {row.current_stock} {row.unit}
        </span>
      )
    },
    { key: 'minimum_stock', label: 'Min Stock' },
    { 
      key: 'unit_price', 
      label: 'Unit Price',
      render: (row) => `$${row.unit_price.toFixed(2)}`
    },
    { 
      key: 'expiry_date', 
      label: 'Expiry Date',
      render: (row) => row.expiry_date || 'N/A'
    },
    { 
      key: 'status', 
      label: 'Status',
      render: (row) => row.is_low_stock 
        ? <StatusBadge status="urgent" /> 
        : <StatusBadge status="available" />
    },
    {
      key: 'actions',
      label: 'Actions',
      render: (row) => (
        <div className="action-buttons">
          <button className="btn btn-primary btn-sm">Restock</button>
          <button 
            className="btn btn-secondary btn-sm"
            onClick={() => fetchItemPrediction(row.id)}
          >
            🔮 Predict
          </button>
        </div>
      )
    }
  ];

  const stats = {
    total: inventoryItems.length,
    lowStock: inventoryItems.filter(i => i.is_low_stock).length,
    expiringSoon: inventoryItems.filter(i => {
      if (!i.expiry_date) return false;
      const expiry = new Date(i.expiry_date);
      const threshold = new Date();
      threshold.setDate(threshold.getDate() + 30);
      return expiry <= threshold;
    }).length,
    mlHighPriority: mlAlerts?.high_priority || 0,
  };

  return (
    <div className="inventory">
      <div className="page-header">
        <div>
          <h1>Inventory Usage Tracking</h1>
          <p>Monitor medicine and consumable usage with ML-powered predictions</p>
        </div>
        <div className="header-actions">
          <button className="btn btn-secondary" onClick={fetchMLPredictions}>
            🔄 Refresh Predictions
          </button>
          <button className="btn btn-primary">+ Add Item</button>
        </div>
      </div>

      {/* ML Predictions Section */}
      {mlAlerts && (
        <div className="ml-predictions-section">
          <h2>🤖 ML Stock Predictions</h2>
          <div className="ml-stats">
            <div className="ml-stat-card">
              <span className="stat-value">{mlAlerts.total_items_scanned}</span>
              <span className="stat-label">Items Analyzed</span>
            </div>
            <div className="ml-stat-card warning">
              <span className="stat-value">{mlAlerts.high_priority}</span>
              <span className="stat-label">🚨 High Priority</span>
            </div>
            <div className="ml-stat-card info">
              <span className="stat-value">{mlAlerts.medium_priority}</span>
              <span className="stat-label">⚠️ Medium Priority</span>
            </div>
          </div>
          
          {mlAlerts.alerts?.length > 0 && (
            <div className="alerts-list">
              <h3>Items Needing Attention</h3>
              <div className="alerts-grid">
                {mlAlerts.alerts.slice(0, 5).map(alert => (
                  <div key={alert.item_id} className={`alert-card ${alert.urgency.toLowerCase()}`}>
                    <div className="alert-header">
                      <span className="item-name">{alert.item_name}</span>
                      <span className={`urgency-badge ${alert.urgency.toLowerCase()}`}>
                        {alert.urgency}
                      </span>
                    </div>
                    <div className="alert-details">
                      <p>📦 Current Stock: {alert.current_stock}</p>
                      <p>⏱️ Days Left: {alert.usage_days_left}</p>
                      <p>📈 Risk Score: {(alert.combined_risk * 100).toFixed(1)}%</p>
                    </div>
                    <p className="recommendation">{alert.recommendation}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Disease-Based Demand Forecast */}
      {demandForecast && demandForecast.predicted_demand && (
        <div className="demand-forecast-section">
          <h2>📊 Disease-Based Demand Forecast</h2>
          <p className="forecast-subtitle">
            Based on {demandForecast.total_patients} current admissions
          </p>
          <div className="demand-grid">
            {Object.entries(demandForecast.predicted_demand).slice(0, 6).map(([medicine, qty]) => (
              <div key={medicine} className="demand-card">
                <span className="medicine-name">{medicine}</span>
                <span className="demand-qty">{qty} units</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Item Prediction Modal */}
      {itemPrediction && (
        <div className="prediction-modal-overlay" onClick={() => setItemPrediction(null)}>
          <div className="prediction-modal" onClick={e => e.stopPropagation()}>
            <h3>🔮 Stock Prediction: {itemPrediction.item?.name}</h3>
            <button className="close-btn" onClick={() => setItemPrediction(null)}>×</button>
            
            <div className="prediction-content">
              <div className="prediction-section">
                <h4>📦 Current Status</h4>
                <p>Stock: {itemPrediction.item?.current_stock}</p>
                <p>Reorder Level: {itemPrediction.item?.reorder_level}</p>
              </div>
              
              <div className="prediction-section">
                <h4>📈 Usage-Based Prediction</h4>
                <p>Days Until Stockout: {itemPrediction.usage_based_prediction?.days_until_stockout}</p>
                <p>Stockout Probability: {(itemPrediction.usage_based_prediction?.stockout_probability * 100).toFixed(1)}%</p>
              </div>
              
              <div className="prediction-section">
                <h4>🏥 Disease-Based Demand</h4>
                <p>Expected Demand This Week: {itemPrediction.disease_based_prediction?.expected_demand_this_week}</p>
                <p>Days of Stock: {itemPrediction.disease_based_prediction?.days_of_stock}</p>
              </div>
              
              <div className={`prediction-result ${itemPrediction.combined_analysis?.urgency?.toLowerCase()}`}>
                <h4>🎯 Combined Analysis</h4>
                <p className="risk-score">Risk Score: {(itemPrediction.combined_analysis?.combined_risk_score * 100).toFixed(1)}%</p>
                <p className="urgency">Urgency: {itemPrediction.combined_analysis?.urgency}</p>
                <p className="recommendation">{itemPrediction.combined_analysis?.recommendation}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="inventory-stats">
        <div className="stat-card">
          <span className="stat-value">{stats.total}</span>
          <span className="stat-label">Total Items</span>
        </div>
        <div className="stat-card warning">
          <span className="stat-value">{stats.lowStock}</span>
          <span className="stat-label">Low Stock Items</span>
        </div>
        <div className="stat-card danger">
          <span className="stat-value">{stats.expiringSoon}</span>
          <span className="stat-label">Expiring Soon</span>
        </div>
        <div className="stat-card ml-priority">
          <span className="stat-value">{stats.mlHighPriority}</span>
          <span className="stat-label">🤖 ML High Priority</span>
        </div>
      </div>

      <div className="inventory-tabs">
        <button 
          className={`tab ${activeTab === 'all' ? 'active' : ''}`}
          onClick={() => setActiveTab('all')}
        >
          All Items
        </button>
        <button 
          className={`tab ${activeTab === 'low_stock' ? 'active' : ''}`}
          onClick={() => setActiveTab('low_stock')}
        >
          Low Stock ⚠️
        </button>
        <button 
          className={`tab ${activeTab === 'medicine' ? 'active' : ''}`}
          onClick={() => setActiveTab('medicine')}
        >
          Medicines
        </button>
        <button 
          className={`tab ${activeTab === 'consumable' ? 'active' : ''}`}
          onClick={() => setActiveTab('consumable')}
        >
          Consumables
        </button>
        <button 
          className={`tab ${activeTab === 'surgical' ? 'active' : ''}`}
          onClick={() => setActiveTab('surgical')}
        >
          Surgical
        </button>
      </div>

      <Table columns={columns} data={filteredItems} />
    </div>
  );
};

export default Inventory;
