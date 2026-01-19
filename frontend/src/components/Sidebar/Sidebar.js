import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  const menuItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/opd', label: 'OPD Queue', icon: '🎫' },
    { path: '/beds', label: 'Bed Management', icon: '🛏️' },
    { path: '/admissions', label: 'Admissions', icon: '📋' },
    { path: '/inventory', label: 'Inventory', icon: '💊' },
    { path: '/inter-hospital', label: 'Inter-Hospital', icon: '🏥' },
  ];

  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? 'active' : ''}`
            }
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span className="sidebar-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
