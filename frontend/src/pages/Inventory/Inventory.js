import React, { useState, useEffect } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import { inventoryAPI } from '../../services/api';
import './Inventory.css';

const Inventory = () => {
  const [activeTab, setActiveTab] = useState('all');
  const [inventoryItems, setInventoryItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        setLoading(true);
        setError(null);
        const response = await inventoryAPI.getItems();
        // Handle paginated response - data may be in .results or directly in .data
        const responseData = response.data;
        const items = Array.isArray(responseData) 
          ? responseData 
          : (responseData.results || []);
        setInventoryItems(items);
      } catch (err) {
        console.error('Failed to fetch inventory:', err);
        setError('Failed to load inventory data. Please try again.');
        setInventoryItems([]);
      } finally {
        setLoading(false);
      }
    };

    fetchInventory();
  }, []);

  // Ensure inventoryItems is always an array
  const itemsArray = Array.isArray(inventoryItems) ? inventoryItems : [];
  
  const filteredItems = activeTab === 'all' 
    ? itemsArray 
    : activeTab === 'low_stock' 
      ? itemsArray.filter(item => item.is_low_stock)
      : itemsArray.filter(item => item.category?.toLowerCase() === activeTab);

  const columns = [
    { key: 'item_id', label: 'ID' },
    { key: 'item_name', label: 'Item Name' },
    { key: 'category', label: 'Category' },
    { 
      key: 'quantity_available', 
      label: 'Stock',
      render: (row) => (
        <span className={row.is_low_stock ? 'stock-low' : 'stock-ok'}>
          {row.quantity_available}
        </span>
      )
    },
    { key: 'reorder_level', label: 'Reorder Level' },
    { key: 'supplier', label: 'Supplier' },
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
        </div>
      )
    }
  ];

  const stats = {
    total: itemsArray.length,
    lowStock: itemsArray.filter(i => i.is_low_stock).length,
  };

  return (
    <div className="inventory">
      <div className="page-header">
        <div>
          <h1>Inventory Usage Tracking</h1>
          <p>Monitor medicine and consumable usage with low-stock alerts</p>
        </div>
        <button className="btn btn-primary">+ Add Item</button>
      </div>

      {loading && <div className="loading">Loading inventory...</div>}
      {error && <div className="error-message">{error}</div>}

      {!loading && !error && (
        <>
          <div className="inventory-stats">
            <div className="stat-card">
              <span className="stat-value">{stats.total}</span>
              <span className="stat-label">Total Items</span>
            </div>
            <div className="stat-card warning">
              <span className="stat-value">{stats.lowStock}</span>
              <span className="stat-label">Low Stock Items</span>
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
          </div>

          {filteredItems.length === 0 ? (
            <p className="no-data">No inventory items found</p>
          ) : (
            <Table columns={columns} data={filteredItems} />
          )}
        </>
      )}
    </div>
  );
};

export default Inventory;
