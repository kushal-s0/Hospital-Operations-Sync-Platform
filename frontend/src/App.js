import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import PrivateRoute from './components/PrivateRoute/PrivateRoute';
import Login from './pages/Login/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import OPDQueue from './pages/OPD/OPDQueue';
import BedManagement from './pages/Beds/BedManagement';
import Admissions from './pages/Admissions/Admissions';
import Inventory from './pages/Inventory/Inventory';
import InterHospital from './pages/InterHospital/InterHospital';
import { isAuthenticated } from './services/api';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public route - Login */}
        <Route 
          path="/login" 
          element={
            isAuthenticated() ? <Navigate to="/" replace /> : <Login />
          } 
        />
        
        {/* Protected routes - wrapped in Layout */}
        <Route path="/" element={
          <PrivateRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </PrivateRoute>
        } />
        
        <Route path="/opd" element={
          <PrivateRoute>
            <Layout>
              <OPDQueue />
            </Layout>
          </PrivateRoute>
        } />
        
        <Route path="/beds" element={
          <PrivateRoute>
            <Layout>
              <BedManagement />
            </Layout>
          </PrivateRoute>
        } />
        
        <Route path="/admissions" element={
          <PrivateRoute>
            <Layout>
              <Admissions />
            </Layout>
          </PrivateRoute>
        } />
        
        <Route path="/inventory" element={
          <PrivateRoute>
            <Layout>
              <Inventory />
            </Layout>
          </PrivateRoute>
        } />
        
        <Route path="/inter-hospital" element={
          <PrivateRoute>
            <Layout>
              <InterHospital />
            </Layout>
          </PrivateRoute>
        } />

        {/* Redirect any other routes to dashboard or login */}
        <Route 
          path="*" 
          element={
            <Navigate to={isAuthenticated() ? "/" : "/login"} replace />
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;
