import React from 'react';
import './StatusBadge.css';

const StatusBadge = ({ status, type = 'default' }) => {
  const getStatusClass = () => {
    switch (status.toLowerCase()) {
      case 'available':
      case 'completed':
      case 'active':
        return 'success';
      case 'occupied':
      case 'in_consultation':
      case 'admitted':
        return 'warning';
      case 'maintenance':
      case 'emergency':
      case 'urgent':
        return 'danger';
      case 'waiting':
      case 'reserved':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <span className={`status-badge status-${getStatusClass()}`}>
      {status.replace('_', ' ')}
    </span>
  );
};

export default StatusBadge;
