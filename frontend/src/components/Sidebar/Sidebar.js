import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  
  const [userRole, setUserRole] = useState(null);

  useEffect(() => {
    // Get user role from localStorage
    const user = JSON.parse(localStorage.getItem('user'));
    if (user && user.role) {
      setUserRole(user.role);
    }
  }, []);

  const isReceptionist = userRole === 'Receptionist';

  const baseMenuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/opd', label: 'OPD Queue', icon: '🎫' },
    { path: '/beds', label: 'Bed Management', icon: '🛏️' },
    { path: '/admissions', label: 'Admissions', icon: '📋' },
    { path: '/inventory', label: 'Inventory', icon: '💊' },
    { path: '/inter-hospital', label: 'Inter-Hospital', icon: '🏥' },
  ];
  const receptionistMenuItems = [
    { path: '/receptionist-dashboard', label: 'Dashboard', icon: '📊', receptionist: true },
    { path: '/receptionist-billing', label: 'Billing', icon: '💳', receptionist: true },
    { path: '/receptionist-transactions', label: 'Transactions', icon: '💰', receptionist: true },
    { path: '/receptionist-treatments', label: 'Treatments', icon: '🏥', receptionist: true },
  ];

  const menuItems = isReceptionist ? receptionistMenuItems : baseMenuItems;
  return (
    <aside className="sidebar">
      {isReceptionist && <div className="sidebar-title">Receptionist Menu</div>}
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
