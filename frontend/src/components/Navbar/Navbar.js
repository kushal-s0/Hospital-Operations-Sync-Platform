import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>🏥 Hospital Operations Platform</h1>
      </div>
      <div className="navbar-actions">
        <span className="navbar-time">{new Date().toLocaleString()}</span>
        <button className="navbar-btn">🔔</button>
        <button className="navbar-btn">👤 Admin</button>
      </div>
    </nav>
  );
};

export default Navbar;
