import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from '../Navbar/Navbar';
import Sidebar from '../Sidebar/Sidebar';
import './Layout.css';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  // Close the mobile drawer whenever the route changes
  useEffect(() => {
    setSidebarOpen(false);
  }, [location.pathname]);

  return (
    <div className={`layout${sidebarOpen ? ' sidebar-is-open' : ''}`}>
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="sidebar-scrim" onClick={() => setSidebarOpen(false)} aria-hidden="true" />
      <Navbar onMenuClick={() => setSidebarOpen((open) => !open)} />
      <main className="main-content">
        <div key={location.pathname} className="page-transition">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
