import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  
  const [userRole, setUserRole] = useState(null);

  useEffect(() => {
    // Get user role from localStorage
    const userData = localStorage.getItem('user');
    if (userData) {
      const user = JSON.parse(userData);
      if (user && user.role) {
        setUserRole(user.role);
      }
    }
  }, []);

  const isReceptionist = userRole === 'Receptionist';
  const isAdmin = userRole === 'Admin';

  const baseMenuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊', roles: ['Admin', 'Doctor', 'Nurse', 'Pharmacist', 'Receptionist'] },
    { path: '/opd', label: 'OPD Queue', icon: '🎫', roles: ['Admin', 'Doctor', 'Nurse', 'Receptionist'] },
    { path: '/beds', label: 'Bed Management', icon: '🛏️', roles: ['Admin', 'Nurse', 'Receptionist'] },
    { path: '/admissions', label: 'Admissions', icon: '📋', roles: ['Admin', 'Nurse', 'Receptionist'] },
    { path: '/appointments', label: 'Appointments', icon: '📅', roles: ['Admin', 'Nurse'] },
    { path: '/inventory', label: 'Inventory', icon: '💊', roles: ['Admin', 'Pharmacist', 'Receptionist'] },
    { path: '/inter-hospital', label: 'Inter-Hospital', icon: '🏥', roles: ['Admin'] },
    { path: '/receptionist', label: 'Receptionist Portal', icon: '👨‍💼', roles: ['Admin'] },
  ];
  
  const receptionistMenuItems = [
    { path: '/receptionist-dashboard', label: 'Dashboard', icon: '📊', receptionist: true },
    { path: '/receptionist-billing', label: 'Billing', icon: '💳', receptionist: true },
    { path: '/receptionist-transactions', label: 'Transactions', icon: '💰', receptionist: true },
    { path: '/receptionist-treatments', label: 'Treatments', icon: '🏥', receptionist: true },
  ];

  const menuItems = isReceptionist ? receptionistMenuItems : (userRole
    ? baseMenuItems.filter(item => item.roles.includes(userRole))
    : []);
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
