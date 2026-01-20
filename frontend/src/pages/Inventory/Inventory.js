import React, { useState, useEffect } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import { inventoryAPI } from '../../services/api';
import './Inventory.css';

const Inventory = () => {
  const [activeTab, setActiveTab] = useState('all');
  const [mlAlerts, setMlAlerts] = useState(null);
  const [demandForecast, setDemandForecast] = useState(null);
  const [weatherPrediction, setWeatherPrediction] = useState(null);
  const [selectedItem, setSelectedItem] = useState(null);
  const [itemPrediction, setItemPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [showRestockModal, setShowRestockModal] = useState(false);
  const [restockMode, setRestockMode] = useState(null); // 'update' or 'add'
  const [restockItem, setRestockItem] = useState(null);
  const [inventoryItems, setInventoryItems] = useState([]);
  const [openDropdownId, setOpenDropdownId] = useState(null); // Track which dropdown is open
  const [restockForm, setRestockForm] = useState({
    sku: '',
    name: '',
    category: '',
    supplier: '',
    unit_price: '',
    expiry_date: '',
    stock_quantity: '',
    reorder_level: ''
  });
  
  // Fetch ML predictions and inventory on mount
  useEffect(() => {
    fetchMLPredictions();
    fetchInventory();
    fetchWeatherPrediction();
  }, []);

  const fetchInventory = async () => {
    try {
      setLoading(true);
      const response = await inventoryAPI.getAll();
      console.log('Inventory response:', response);
      console.log('Response data type:', typeof response.data);
      console.log('Is array?', Array.isArray(response.data));
      
      // Handle both paginated response and direct array
      let items = [];
      if (response.data) {
        if (Array.isArray(response.data)) {
          items = response.data;
        } else if (response.data.results && Array.isArray(response.data.results)) {
          // Paginated response
          items = response.data.results;
        } else if (typeof response.data === 'object') {
          // Try to extract array from object
          const keys = Object.keys(response.data);
          console.log('Response data keys:', keys);
          items = response.data.results || response.data.data || [];
        }
      }
      
      console.log('Items to map:', items);
      
      // Map database fields to frontend format
      const mappedItems = items.map(item => ({
        id: item.item_id,
        name: item.item_name,
        sku: `ITM-${String(item.item_id).padStart(3, '0')}`,
        category: item.category || 'Other',
        item_type: (item.category || '').toLowerCase(),
        current_stock: item.quantity_available || 0,
        minimum_stock: item.reorder_level || 0,
        unit: 'units', // Default unit
        unit_price: item.unit_price || 0,
        expiry_date: item.expiry_date || null,
        is_low_stock: item.quantity_available <= item.reorder_level,
        supplier: item.supplier || 'N/A'
      }));
      
      console.log('Mapped items:', mappedItems);
      setInventoryItems(mappedItems);
    } catch (error) {
      console.error('Error fetching inventory:', error);
      console.error('Error details:', error.response?.data);
      alert('Error loading inventory data: ' + (error.message || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  // Sort inventory by expiry date (soonest first), items without expiry go last
  const sortedInventory = [...inventoryItems].sort((a, b) => {
    if (!a.expiry_date) return 1;
    if (!b.expiry_date) return -1;
    return new Date(a.expiry_date) - new Date(b.expiry_date);
  });

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

  const fetchWeatherPrediction = async () => {
    try {
      const response = await inventoryAPI.getWeatherPrediction();
      setWeatherPrediction(response.data);
      console.log('Weather prediction:', response.data);
    } catch (error) {
      console.error('Error fetching weather prediction:', error);
    }
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

  const handleRestockClick = (item, mode) => {
    setRestockMode(mode);
    setRestockItem(item);
    setOpenDropdownId(null); // Close dropdown
    
    if (mode === 'update') {
      // Pre-fill all fields except stock quantity
      setRestockForm({
        sku: item.sku,
        name: item.name,
        category: item.category,
        supplier: item.supplier,
        unit_price: item.unit_price || '',
        expiry_date: item.expiry_date || '',
        stock_quantity: '',
        reorder_level: item.minimum_stock
      });
    } else if (mode === 'add') {
      // Pre-fill only name and category
      setRestockForm({
        sku: '',
        name: item.name,
        category: item.category,
        supplier: '',
        unit_price: '',
        expiry_date: '',
        stock_quantity: '',
        reorder_level: ''
      });
    }
    
    setShowRestockModal(true);
  };

  const handleAddNewItem = () => {
    setRestockMode('add');
    setRestockItem(null);
    // Reset form to empty
    setRestockForm({
      sku: '',
      name: '',
      category: 'Medicine',
      supplier: '',
      unit_price: '',
      expiry_date: '',
      stock_quantity: '',
      reorder_level: ''
    });
    setShowRestockModal(true);
  };

  const toggleDropdown = (itemId) => {
    setOpenDropdownId(openDropdownId === itemId ? null : itemId);
  };

  const handleRestockSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      
      if (restockMode === 'update') {
        // Update existing stock - add to current quantity
        const response = await inventoryAPI.updateStock(restockItem.id, {
          stock_quantity: parseInt(restockForm.stock_quantity)
        });
        
        if (response.status === 200) {
          alert('Stock updated successfully!');
          setShowRestockModal(false);
          fetchInventory(); // Refresh inventory
        }
      } else if (restockMode === 'add') {
        // Add new stock item
        const newItem = {
          item_name: restockForm.name,
          category: restockForm.category,
          quantity_available: parseInt(restockForm.stock_quantity),
          reorder_level: parseInt(restockForm.reorder_level),
          supplier: restockForm.supplier || null,
          unit_price: restockForm.unit_price ? parseFloat(restockForm.unit_price) : null,
          expiry_date: restockForm.expiry_date || null
        };
        
        console.log('Sending new item data:', newItem);
        const response = await inventoryAPI.addStock(newItem);
        console.log('Add stock response:', response);
        
        if (response.status === 201) {
          alert('New stock item added successfully!');
          setShowRestockModal(false);
          fetchInventory(); // Refresh inventory
        }
      }
    } catch (error) {
      console.error('Error restocking:', error);
      console.error('Error response:', error.response);
      console.error('Error data:', error.response?.data);
      
      let errorMessage = 'Failed to update stock';
      if (error.response?.data) {
        // Parse error messages from backend
        if (typeof error.response.data === 'object') {
          errorMessage = Object.entries(error.response.data)
            .map(([key, value]) => `${key}: ${value}`)
            .join('\n');
        } else {
          errorMessage = error.response.data;
        }
      }
      
      alert(`Error: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRestockFormChange = (e) => {
    setRestockForm({
      ...restockForm,
      [e.target.name]: e.target.value
    });
  };

  const filteredItems = activeTab === 'all' 
    ? sortedInventory 
    : activeTab === 'low_stock' 
      ? sortedInventory.filter(item => item.is_low_stock)
      : activeTab === 'expiring'
        ? sortedInventory.filter(item => {
            if (!item.expiry_date) return false;
            const expiry = new Date(item.expiry_date);
            const today = new Date();
            const fifteenDaysFromNow = new Date();
            fifteenDaysFromNow.setDate(today.getDate() + 15);
            return expiry >= today && expiry <= fifteenDaysFromNow;
          })
        : sortedInventory.filter(item => item.item_type === activeTab);

  // Pagination logic
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredItems.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredItems.length / itemsPerPage);

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  // Reset to page 1 when filter changes
  useEffect(() => {
    setCurrentPage(1);
  }, [activeTab]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (openDropdownId && !event.target.closest('.dropdown')) {
        setOpenDropdownId(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [openDropdownId]);

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
      render: (row) => row.unit_price ? `₹${parseFloat(row.unit_price).toFixed(2)}` : 'N/A'
    },
    { 
      key: 'expiry_date', 
      label: 'Expiry Date',
      render: (row) => {
        if (!row.expiry_date) return 'N/A';
        
        const expiry = new Date(row.expiry_date);
        const today = new Date();
        const fifteenDaysFromNow = new Date();
        fifteenDaysFromNow.setDate(today.getDate() + 15);
        
        const isExpiringSoon = expiry >= today && expiry <= fifteenDaysFromNow;
        const isExpired = expiry < today;
        
        return (
          <span className={isExpired ? 'expiry-expired' : isExpiringSoon ? 'expiry-soon' : 'expiry-ok'}>
            {row.expiry_date} {isExpiringSoon && '⚠️'} {isExpired && '❌'}
          </span>
        );
      }
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
          <div className="dropdown">
            <button 
              className="btn btn-primary btn-sm dropdown-toggle" 
              type="button" 
              onClick={() => toggleDropdown(row.id)}
            >
              Restock
            </button>
            <ul className={`dropdown-menu ${openDropdownId === row.id ? 'show' : ''}`}>
              <li>
                <button className="dropdown-item" onClick={() => handleRestockClick(row, 'update')}>
                  Update Existing Stock
                </button>
              </li>
              <li>
                <button className="dropdown-item" onClick={() => handleRestockClick(row, 'add')}>
                  Add New Stock
                </button>
              </li>
            </ul>
          </div>
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
      const today = new Date();
      const fifteenDaysFromNow = new Date();
      fifteenDaysFromNow.setDate(today.getDate() + 15);
      return expiry >= today && expiry <= fifteenDaysFromNow;
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
          <button className="btn btn-primary" onClick={handleAddNewItem}>
            + Add Item
          </button>
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

      {/* Weather & AQI-Based Prediction Section */}
      {weatherPrediction && (
        <div className="weather-prediction-section">
          <h2>🌤️ Weather & AQI-Based Forecast</h2>
          <p className="forecast-subtitle">
            Real-time environmental data for {weatherPrediction.location?.city || 'your location'}
          </p>
          
          {/* Current Conditions */}
          <div className="current-conditions">
            <div className="condition-card weather">
              <span className="icon">🌡️</span>
              <div className="condition-info">
                <span className="value">{weatherPrediction.current_weather?.temperature}°C</span>
                <span className="label">{weatherPrediction.current_weather?.description}</span>
                <span className="detail">Feels like {weatherPrediction.current_weather?.feels_like}°C</span>
              </div>
            </div>
            
            <div className="condition-card humidity">
              <span className="icon">💧</span>
              <div className="condition-info">
                <span className="value">{weatherPrediction.current_weather?.humidity}%</span>
                <span className="label">Humidity</span>
              </div>
            </div>
            
            <div className={`condition-card aqi ${weatherPrediction.current_aqi?.aqi > 150 ? 'bad' : weatherPrediction.current_aqi?.aqi > 100 ? 'moderate' : 'good'}`}>
              <span className="icon">💨</span>
              <div className="condition-info">
                <span className="value">AQI: {weatherPrediction.current_aqi?.aqi}</span>
                <span className="label">{weatherPrediction.current_aqi?.quality}</span>
                <span className="detail">PM2.5: {weatherPrediction.current_aqi?.pm2_5?.toFixed(1)}</span>
              </div>
            </div>
          </div>
          
          {/* Risk Factors */}
          {weatherPrediction.weather_aqi_factors && weatherPrediction.weather_aqi_factors.length > 0 && (
            <div className="risk-factors">
              <h3>⚠️ Disease Risk Factors Detected</h3>
              <div className="risk-grid">
                {weatherPrediction.weather_aqi_factors.map((factor, idx) => (
                  <div key={idx} className={`risk-card ${factor.severity.toLowerCase()}`}>
                    <div className="risk-header">
                      <span className="risk-trigger">{factor.trigger}</span>
                      <span className={`severity-badge ${factor.severity.toLowerCase()}`}>
                        {factor.severity}
                      </span>
                    </div>
                    <div className="risk-value">{factor.value}</div>
                    <div className="risk-diseases">
                      <strong>Expected diseases:</strong>
                      <ul>
                        {factor.diseases.map((disease, i) => (
                          <li key={i}>{disease}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="risk-recommendation">
                      💡 {factor.recommendation}
                    </div>
                    <div className="risk-multiplier">
                      Demand increase: <strong>{((factor.multiplier - 1) * 100).toFixed(0)}%</strong>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Medicine Demand Predictions */}
          {weatherPrediction.predicted_medicine_demand && Object.keys(weatherPrediction.predicted_medicine_demand).length > 0 && (
            <div className="weather-demand">
              <h3>📦 Recommended Stock Increase</h3>
              <div className="weather-demand-grid">
                {Object.entries(weatherPrediction.predicted_medicine_demand)
                  .sort((a, b) => b[1].quantity - a[1].quantity)
                  .slice(0, 8)
                  .map(([medicine, data]) => (
                    <div key={medicine} className={`weather-demand-card ${data.urgency.toLowerCase()}`}>
                      <div className="medicine-header">
                        <span className="medicine-name">{medicine}</span>
                        <span className={`urgency-badge ${data.urgency.toLowerCase()}`}>
                          {data.urgency}
                        </span>
                      </div>
                      <div className="quantity-info">
                        <span className="quantity-label">Additional Stock Needed:</span>
                        <span className="quantity-value">{data.quantity} units</span>
                      </div>
                      <div className="related-diseases">
                        <span className="diseases-label">Related to:</span>
                        <span className="diseases-list">{data.related_diseases.join(', ')}</span>
                      </div>
                      <div className="base-comparison">
                        Base: {data.base_quantity} → Adjusted: {data.quantity}
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          )}
          
          {weatherPrediction.weather_aqi_factors && weatherPrediction.weather_aqi_factors.length === 0 && (
            <div className="no-risks">
              <p>✅ No significant environmental risk factors detected</p>
              <p>Current conditions are favorable for normal operations</p>
            </div>
          )}
          
          <div className="forecast-meta">
            <span>🔄 Last updated: {new Date(weatherPrediction.last_updated).toLocaleString()}</span>
            <span>📅 Forecast period: {weatherPrediction.forecast_period}</span>
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
          <span className="stat-label">Expiring in 15 Days</span>
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
          className={`tab ${activeTab === 'expiring' ? 'active' : ''}`}
          onClick={() => setActiveTab('expiring')}
        >
          Expiring (15 Days) 📅
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

      <Table columns={columns} data={currentItems} />
      
      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="pagination-controls">
          <button 
            className="btn btn-secondary btn-sm" 
            onClick={handlePreviousPage}
            disabled={currentPage === 1}
          >
            ← Previous
          </button>
          
          <div className="page-numbers">
            {[...Array(totalPages)].map((_, index) => (
              <button
                key={index + 1}
                className={`page-btn ${currentPage === index + 1 ? 'active' : ''}`}
                onClick={() => handlePageChange(index + 1)}
              >
                {index + 1}
              </button>
            ))}
          </div>
          
          <button 
            className="btn btn-secondary btn-sm" 
            onClick={handleNextPage}
            disabled={currentPage === totalPages}
          >
            Next →
          </button>
          
          <div className="page-info">
            Page {currentPage} of {totalPages} | Showing {currentItems.length} of {filteredItems.length} items
          </div>
        </div>
      )}

      {/* Restock Modal */}
      {showRestockModal && (
        <div className="restock-modal-overlay" onClick={() => setShowRestockModal(false)}>
          <div className="restock-modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>
                {restockMode === 'update' 
                  ? '📦 Update Existing Stock' 
                  : restockItem 
                    ? '➕ Add New Stock' 
                    : '🆕 Add New Item'}
              </h3>
              <button className="close-btn" onClick={() => setShowRestockModal(false)}>×</button>
            </div>
            
            <form onSubmit={handleRestockSubmit}>
              {!restockItem && restockMode === 'add' && (
                <div className="alert alert-info">
                  ℹ️ Fill in the details below to add a completely new item to the inventory.
                </div>
              )}
              
              {restockForm.sku && (
                <div className="form-group">
                  <label>SKU</label>
                  <input 
                    type="text" 
                    className="form-control" 
                    name="sku"
                    value={restockForm.sku}
                    readOnly
                  />
                </div>
              )}

              <div className="form-group">
                <label>Item Name *</label>
                <input 
                  type="text" 
                  className="form-control" 
                  name="name"
                  value={restockForm.name}
                  onChange={handleRestockFormChange}
                  readOnly={restockMode === 'update'}
                  placeholder="Enter item name"
                  required
                />
              </div>

              <div className="form-group">
                <label>Category *</label>
                <select 
                  className="form-control" 
                  name="category"
                  value={restockForm.category}
                  onChange={handleRestockFormChange}
                  disabled={restockMode === 'update'}
                  required
                >
                  <option value="">Select Category</option>
                  <option value="Medicine">Medicine</option>
                  <option value="Consumable">Consumable</option>
                  <option value="Equipment">Equipment</option>
                </select>
              </div>

              <div className="form-group">
                <label>Supplier</label>
                <input 
                  type="text" 
                  className="form-control" 
                  name="supplier"
                  value={restockForm.supplier}
                  onChange={handleRestockFormChange}
                  readOnly={restockMode === 'update'}
                  placeholder="Supplier name"
                />
              </div>

              <div className="form-group">
                <label>Unit Price (₹)</label>
                <input 
                  type="number" 
                  step="0.01"
                  className="form-control" 
                  name="unit_price"
                  value={restockForm.unit_price}
                  onChange={handleRestockFormChange}
                  readOnly={restockMode === 'update'}
                  placeholder="Price per unit"
                />
              </div>

              <div className="form-group">
                <label>Expiry Date</label>
                <input 
                  type="date" 
                  className="form-control" 
                  name="expiry_date"
                  value={restockForm.expiry_date}
                  onChange={handleRestockFormChange}
                  readOnly={restockMode === 'update'}
                />
                <small className="form-text text-muted">
                  Leave empty if not applicable (e.g., equipment)
                </small>
              </div>

              {restockMode === 'add' && (
                <div className="form-group">
                  <label>Reorder Level *</label>
                  <input 
                    type="number" 
                    className="form-control" 
                    name="reorder_level"
                    value={restockForm.reorder_level}
                    onChange={handleRestockFormChange}
                    placeholder="Minimum stock threshold"
                    required
                    min="1"
                  />
                </div>
              )}

              {restockMode === 'update' && (
                <div className="form-group">
                  <label>Current Reorder Level</label>
                  <input 
                    type="text" 
                    className="form-control" 
                    value={restockForm.reorder_level}
                    readOnly
                  />
                </div>
              )}

              <div className="form-group">
                <label>Stock Quantity to Add *</label>
                <input 
                  type="number" 
                  className="form-control" 
                  name="stock_quantity"
                  value={restockForm.stock_quantity}
                  onChange={handleRestockFormChange}
                  placeholder="Enter quantity to add"
                  required
                  min="1"
                />
                {restockMode === 'update' && (
                  <small className="form-text text-muted">
                    This will be added to current stock: {restockItem?.current_stock || 0}
                  </small>
                )}
              </div>

              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowRestockModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Processing...' : (restockMode === 'update' ? 'Update Stock' : 'Add Stock')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Inventory;
