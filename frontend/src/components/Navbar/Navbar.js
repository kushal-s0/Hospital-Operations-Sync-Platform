import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { logout } from '../../services/api';
import './Navbar.css';

const Navbar = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h1>🏥 Hospital Operations Platform</h1>
      </div>
      <div className="navbar-actions">
        <span className="navbar-time">{new Date().toLocaleString()}</span>
        <button className="navbar-btn">🔔</button>
        <span className="navbar-user">
          👤 {user ? `${user.first_name || user.username}` : 'User'}
        </span>
        <button className="navbar-btn logout-btn" onClick={handleLogout}>
          🚪 Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
