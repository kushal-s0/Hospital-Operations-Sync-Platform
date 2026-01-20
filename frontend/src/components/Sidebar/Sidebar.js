import React, { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import './Sidebar.css';

// Professional Icon Components
const DashboardIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M2.5 7.5H8.75V2.5H2.5V7.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M11.25 17.5H17.5V12.5H11.25V17.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M11.25 7.5H17.5V2.5H11.25V7.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M2.5 17.5H8.75V10H2.5V17.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const OPDIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M6.25 7.5H13.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M6.25 10H13.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M6.25 12.5H10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M4.375 17.5H15.625C16.1773 17.5 16.625 17.0523 16.625 16.5V5L12.5 2.5H4.375C3.82272 2.5 3.375 2.94772 3.375 3.5V16.5C3.375 17.0523 3.82272 17.5 4.375 17.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12.5 2.5V5H16.625" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const BedIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M2.5 13.75V6.25C2.5 5.69772 2.94772 5.25 3.5 5.25H16.5C17.0523 5.25 17.5 5.69772 17.5 6.25V13.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M2.5 13.75H17.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M2.5 13.75V16.25" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M17.5 13.75V16.25" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <circle cx="6.25" cy="8.75" r="1.25" stroke="currentColor" strokeWidth="1.5"/>
  </svg>
);

const AdmissionsIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M10 12.5C12.0711 12.5 13.75 10.8211 13.75 8.75C13.75 6.67893 12.0711 5 10 5C7.92893 5 6.25 6.67893 6.25 8.75C6.25 10.8211 7.92893 12.5 10 12.5Z" stroke="currentColor" strokeWidth="1.5"/>
    <path d="M10 12.5V17.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M5 15.625H15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M16.25 6.875L13.75 8.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M3.75 6.875L6.25 8.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
  </svg>
);

const InventoryIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M3.75 6.25L10 3.125L16.25 6.25V13.75L10 16.875L3.75 13.75V6.25Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M3.75 6.25L10 9.375" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M10 9.375V16.875" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M10 9.375L16.25 6.25" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const HospitalIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M3.75 17.5H16.25V7.5L10 3.75L3.75 7.5V17.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M10 10V13.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M8.125 11.875H11.875" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
  </svg>
);

const ReceptionistIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <circle cx="10" cy="6.25" r="2.5" stroke="currentColor" strokeWidth="1.5"/>
    <path d="M5 15C5 12.5 7 10.625 10 10.625C13 10.625 15 12.5 15 15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M2.5 17.5H17.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
  </svg>
);

const BillingIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <rect x="3.75" y="2.5" width="12.5" height="15" rx="1" stroke="currentColor" strokeWidth="1.5"/>
    <path d="M6.25 6.25H13.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M6.25 9.375H13.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M6.25 12.5H10" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
  </svg>
);

const TransactionsIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <circle cx="10" cy="10" r="6.25" stroke="currentColor" strokeWidth="1.5"/>
    <path d="M10 6.875V10L12.5 11.875" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

const TreatmentsIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M10 5V15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M5 10H15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <circle cx="10" cy="10" r="6.25" stroke="currentColor" strokeWidth="1.5"/>
  </svg>
);

const iconMap = {
  dashboard: <DashboardIcon />,
  opd: <OPDIcon />,
  beds: <BedIcon />,
  admissions: <AdmissionsIcon />,
  inventory: <InventoryIcon />,
  hospital: <HospitalIcon />,
  receptionist: <ReceptionistIcon />,
  billing: <BillingIcon />,
  transactions: <TransactionsIcon />,
  treatments: <TreatmentsIcon />
};

const Sidebar = () => {
  
  const [userRole, setUserRole] = useState(null);
  const location = useLocation();

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
  
  // Check if current path is a receptionist page
  const isOnReceptionistPage = location.pathname.startsWith('/receptionist');

  const baseMenuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: 'dashboard', roles: ['Admin', 'Doctor', 'Nurse', 'Pharmacist', 'Receptionist'] },
    { path: '/opd', label: 'OPD Queue', icon: 'opd', roles: ['Admin', 'Doctor', 'Nurse', 'Receptionist'] },
    { path: '/beds', label: 'Bed Management', icon: 'beds', roles: ['Admin', 'Nurse', 'Receptionist'] },
    { path: '/admissions', label: 'Admissions', icon: 'admissions', roles: ['Admin', 'Nurse', 'Receptionist'] },
    { path: '/inventory', label: 'Inventory', icon: 'inventory', roles: ['Admin', 'Pharmacist', 'Receptionist'] },
    { path: '/inter-hospital', label: 'Inter-Hospital', icon: 'hospital', roles: ['Admin'] },
    { path: '/receptionist-dashboard', label: 'Receptionist Portal', icon: 'receptionist', roles: ['Admin'] },
  ];
  
  const receptionistMenuItems = [
    { path: '/receptionist-dashboard', label: 'Dashboard', icon: 'dashboard', receptionist: true },
    { path: '/receptionist-billing', label: 'Billing', icon: 'billing', receptionist: true },
    { path: '/receptionist-transactions', label: 'Transactions', icon: 'transactions', receptionist: true },
    { path: '/receptionist-treatments', label: 'Treatments', icon: 'treatments', receptionist: true },
  ];

  // Show receptionist menu if user is receptionist OR if admin is on receptionist page
  const showReceptionistMenu = isReceptionist || (isAdmin && isOnReceptionistPage);

  const menuItems = showReceptionistMenu ? receptionistMenuItems : (userRole
    ? baseMenuItems.filter(item => item.roles.includes(userRole))
    : []);

  return (
    <aside className="sidebar">
      {showReceptionistMenu && (
        <div className="sidebar-header">
          <span className="sidebar-title">Receptionist Menu</span>
        </div>
      )}
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? 'active' : ''}`
            }
          >
            <span className="sidebar-icon">{iconMap[item.icon]}</span>
            <span className="sidebar-label">{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
