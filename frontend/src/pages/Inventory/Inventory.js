import React, { useState } from 'react';
import { Table, StatusBadge } from '../../components/Common';
import './Inventory.css';

const Inventory = () => {
  const [activeTab, setActiveTab] = useState('all');
  
  const inventoryItems = [
    { id: 1, name: 'Paracetamol 500mg', sku: 'MED-001', category: 'Medicine', item_type: 'medicine', current_stock: 500, minimum_stock: 100, unit: 'tablets', unit_price: 2.50, expiry_date: '2027-06-15', is_low_stock: false },
    { id: 2, name: 'Surgical Gloves (L)', sku: 'SUP-001', category: 'Consumable', item_type: 'consumable', current_stock: 50, minimum_stock: 100, unit: 'boxes', unit_price: 15.00, expiry_date: '2026-12-01', is_low_stock: true },
    { id: 3, name: 'IV Cannula 20G', sku: 'SUP-002', category: 'Consumable', item_type: 'consumable', current_stock: 200, minimum_stock: 150, unit: 'pieces', unit_price: 5.00, expiry_date: '2027-03-20', is_low_stock: false },
    { id: 4, name: 'Amoxicillin 250mg', sku: 'MED-002', category: 'Medicine', item_type: 'medicine', current_stock: 30, minimum_stock: 50, unit: 'capsules', unit_price: 8.00, expiry_date: '2026-02-10', is_low_stock: true },
    { id: 5, name: 'Oxygen Mask', sku: 'EQP-001', category: 'Equipment', item_type: 'equipment', current_stock: 75, minimum_stock: 30, unit: 'pieces', unit_price: 25.00, expiry_date: null, is_low_stock: false },
    { id: 6, name: 'Surgical Sutures', sku: 'SUR-001', category: 'Surgical', item_type: 'surgical', current_stock: 15, minimum_stock: 25, unit: 'packs', unit_price: 45.00, expiry_date: '2026-08-15', is_low_stock: true },
  ];

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
