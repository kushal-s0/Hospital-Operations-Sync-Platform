import React from 'react';
import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../../services/api';

const RoleBasedRoute = ({ children, allowedRoles = [] }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }

  const userData = localStorage.getItem('user');
  if (!userData) {
    return <Navigate to="/login" replace />;
  }

  const user = JSON.parse(userData);
  const userRole = user.role;

  // If no roles specified, allow all authenticated users
  if (allowedRoles.length === 0) {
    return children;
  }

  // Check if user's role is in the allowed roles
  if (allowedRoles.includes(userRole)) {
    return children;
  }

  // Redirect to dashboard if user doesn't have access
  return <Navigate to="/dashboard" replace />;
};

export default RoleBasedRoute;
