import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { logout } from '../../services/api';
import './Navbar.css';

const PAGE_META = {
  '/dashboard': { title: 'Dashboard', subtitle: 'Operations overview' },
  '/opd': { title: 'OPD Queue', subtitle: 'Live outpatient flow' },
  '/appointments': { title: 'Appointments', subtitle: 'Scheduling & approvals' },
  '/beds': { title: 'Bed Management', subtitle: 'Ward capacity in real time' },
  '/admissions': { title: 'Admissions', subtitle: 'Inpatient intake & discharge' },
  '/inventory': { title: 'Inventory', subtitle: 'Stock levels & forecasts' },
  '/inter-hospital': { title: 'Inter-Hospital', subtitle: 'City-wide capacity sharing' },
  '/receptionist-dashboard': { title: 'Reception', subtitle: 'Front-desk overview' },
  '/receptionist-billing': { title: 'Billing', subtitle: 'Invoices & payments' },
  '/receptionist-transactions': { title: 'Transactions', subtitle: 'Payment history' },
  '/receptionist-treatments': { title: 'Treatments', subtitle: 'Treatment catalogue' },
};

const getGreeting = (hour) => {
  if (hour < 12) return 'Good morning';
  if (hour < 17) return 'Good afternoon';
  return 'Good evening';
};

const Navbar = ({ onMenuClick }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const [user, setUser] = useState(null);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }

    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 30000);

    return () => clearInterval(timer);
  }, []);

  // Close the user menu with Escape
  useEffect(() => {
    if (!showUserMenu) return undefined;
    const onKeyDown = (event) => {
      if (event.key === 'Escape') setShowUserMenu(false);
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [showUserMenu]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  const formatDate = (date) => {
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const getUserInitials = () => {
    if (!user) return 'U';
    const firstName = user.first_name || user.username || '';
    const lastName = user.last_name || '';
    return (firstName.charAt(0) + lastName.charAt(0)).toUpperCase() || 'U';
  };

  const getRoleBadgeClass = (role) => {
    const roleMap = {
      'Admin': 'role-admin',
      'Doctor': 'role-doctor',
      'Nurse': 'role-nurse',
      'Receptionist': 'role-receptionist',
      'Pharmacist': 'role-pharmacist'
    };
    return roleMap[role] || 'role-default';
  };

  const meta = PAGE_META[location.pathname] || { title: 'HealthCare Portal', subtitle: 'Hospital Management System' };
  const displayName = user ? (user.first_name || user.username) : '';

  return (
    <header className="header">
      <div className="header-left">
        <button type="button" className="header-icon-btn menu-toggle" onClick={onMenuClick} aria-label="Open menu">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M3 5.5H17M3 10H17M3 14.5H12" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
          </svg>
        </button>

        <div className="header-titles" key={location.pathname}>
          <h1 className="header-title">{meta.title}</h1>
          <span className="header-subtitle">
            {getGreeting(currentTime.getHours())}{displayName ? `, ${displayName}` : ''} · {meta.subtitle}
          </span>
        </div>
      </div>

      <div className="header-right">
        <span className="live-chip">
          <span className="live-dot" aria-hidden="true" />
          Live
        </span>

        <div className="header-datetime">
          <span className="datetime-time">{formatTime(currentTime)}</span>
          <span className="datetime-date">{formatDate(currentTime)}</span>
        </div>

        <button type="button" className="header-icon-btn bell-btn" title="Notifications" aria-label="Notifications">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 2C6.68629 2 4 4.68629 4 8V11.5858L2.29289 13.2929C1.90237 13.6834 2.17157 14.5 2.70711 14.5H17.2929C17.8284 14.5 18.0976 13.6834 17.7071 13.2929L16 11.5858V8C16 4.68629 13.3137 2 10 2Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M8 14.5C8 15.8807 8.89543 17 10 17C11.1046 17 12 15.8807 12 14.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span className="notification-badge">3</span>
        </button>

        <div className="header-divider"></div>

        <div className="user-menu-container">
          <button
            type="button"
            className="user-menu-trigger"
            onClick={() => setShowUserMenu(!showUserMenu)}
            aria-haspopup="menu"
            aria-expanded={showUserMenu}
          >
            <div className="user-avatar">{getUserInitials()}</div>
            <div className="user-info">
              <span className="user-name">{displayName || 'User'}</span>
              <span className={`user-role ${getRoleBadgeClass(user?.role)}`}>
                {user?.role || 'User'}
              </span>
            </div>
            <svg className="chevron-icon" width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M4 6L8 10L12 6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>

          {showUserMenu && (
            <>
              <div className="user-menu-backdrop" onClick={() => setShowUserMenu(false)} />
              <div className="user-menu-dropdown" role="menu">
                <div className="user-menu-header">
                  <div className="user-avatar-large">{getUserInitials()}</div>
                  <div className="user-details">
                    <p className="user-full-name">
                      {user?.first_name} {user?.last_name}
                    </p>
                    <p className="user-email">{user?.username}</p>
                  </div>
                </div>
                <div className="user-menu-divider"></div>
                <button type="button" className="user-menu-item" role="menuitem">
                  <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <path d="M9 9C11.0711 9 12.75 7.32107 12.75 5.25C12.75 3.17893 11.0711 1.5 9 1.5C6.92893 1.5 5.25 3.17893 5.25 5.25C5.25 7.32107 6.92893 9 9 9Z" stroke="currentColor" strokeWidth="1.5"/>
                    <path d="M15.75 16.5C15.75 13.6005 12.7279 11.25 9 11.25C5.27208 11.25 2.25 13.6005 2.25 16.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                  <span>My Profile</span>
                </button>
                <button type="button" className="user-menu-item" role="menuitem">
                  <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <path d="M9 11.25C10.2426 11.25 11.25 10.2426 11.25 9C11.25 7.75736 10.2426 6.75 9 6.75C7.75736 6.75 6.75 7.75736 6.75 9C6.75 10.2426 7.75736 11.25 9 11.25Z" stroke="currentColor" strokeWidth="1.5"/>
                    <path d="M14.25 11.25C14.4489 11.25 14.6397 11.171 14.7803 11.0303C14.921 10.8897 15 10.6989 15 10.5V7.5C15 7.30109 14.921 7.11032 14.7803 6.96967C14.6397 6.82902 14.4489 6.75 14.25 6.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                  <span>Settings</span>
                </button>
                <div className="user-menu-divider"></div>
                <button type="button" className="user-menu-item logout-item" onClick={handleLogout} role="menuitem">
                  <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                    <path d="M6.75 15.75H3.75C3.35218 15.75 2.97064 15.592 2.68934 15.3107C2.40804 15.0294 2.25 14.6478 2.25 14.25V3.75C2.25 3.35218 2.40804 2.97064 2.68934 2.68934C2.97064 2.40804 3.35218 2.25 3.75 2.25H6.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M12 12.75L15.75 9L12 5.25" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M15.75 9H6.75" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                  <span>Logout</span>
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
