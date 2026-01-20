import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import PrivateRoute from './components/PrivateRoute/PrivateRoute';
import RoleBasedRoute from './components/RoleBasedRoute/RoleBasedRoute';
import Landing from './pages/Landing/Landing';
import Login from './pages/Login/Login';
import Dashboard from './pages/Dashboard/Dashboard';
import OPDQueue from './pages/OPD/OPDQueue';
import BedManagement from './pages/Beds/BedManagement';
import Admissions from './pages/Admissions/Admissions';
import Inventory from './pages/Inventory/Inventory';
import InterHospital from './pages/InterHospital/InterHospital';
import ReceptionistDashboard from './pages/Receptionist/ReceptionistDashboard';
import ReceptionistDashboardTab from './pages/Receptionist/ReceptionistDashboardTab';
import ReceptionistBillingTab from './pages/Receptionist/ReceptionistBillingTab';
import ReceptionistTransactionsTab from './pages/Receptionist/ReceptionistTransactionsTab';
import ReceptionistTreatmentsTab from './pages/Receptionist/ReceptionistTreatmentsTab';
import { isAuthenticated } from './services/api';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public route - Landing Page */}
        <Route path="/" element={<Landing />} />
        
        {/* Public route - Login */}
        <Route 
          path="/login" 
          element={
            isAuthenticated() ? <Navigate to="/dashboard" replace /> : <Login />
          } 
        />
        
        {/* Protected routes - wrapped in Layout */}
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </PrivateRoute>
        } />
        
        <Route path="/opd" element={
          <RoleBasedRoute allowedRoles={['Admin', 'Doctor', 'Nurse', 'Receptionist']}>
            <Layout>
              <OPDQueue />
            </Layout>
          </RoleBasedRoute>
        } />
        
        <Route path="/beds" element={
          <RoleBasedRoute allowedRoles={['Admin', 'Nurse', 'Receptionist']}>
            <Layout>
              <BedManagement />
            </Layout>
          </RoleBasedRoute>
        } />
        
        <Route path="/admissions" element={
          <RoleBasedRoute allowedRoles={['Admin', 'Nurse', 'Receptionist']}>
            <Layout>
              <Admissions />
            </Layout>
          </RoleBasedRoute>
        } />
        
        <Route path="/inventory" element={
          <RoleBasedRoute allowedRoles={['Admin', 'Pharmacist', 'Receptionist']}>
            <Layout>
              <Inventory />
            </Layout>
          </RoleBasedRoute>
        } />
        
        <Route path="/inter-hospital" element={
          <RoleBasedRoute allowedRoles={['Admin']}>
            <Layout>
              <InterHospital />
            </Layout>
          </RoleBasedRoute>
        } />

        {/* Receptionist Portal - Full dashboard with internal navigation (Admin & Receptionist access) */}
        <Route path="/receptionist" element={
          <RoleBasedRoute allowedRoles={['Admin', 'Receptionist']}>
            <ReceptionistDashboard />
          </RoleBasedRoute>
        } />

        {/* Receptionist Routes - Separate page views */}
        <Route path="/receptionist-dashboard" element={
          <PrivateRoute>
            <Layout>
              <ReceptionistDashboardTab />
            </Layout>
          </PrivateRoute>
        } />

        <Route path="/receptionist-billing" element={
          <PrivateRoute>
            <Layout>
              <ReceptionistBillingTab />
            </Layout>
          </PrivateRoute>
        } />

        <Route path="/receptionist-transactions" element={
          <PrivateRoute>
            <Layout>
              <ReceptionistTransactionsTab />
            </Layout>
          </PrivateRoute>
        } />

        <Route path="/receptionist-treatments" element={
          <PrivateRoute>
            <Layout>
              <ReceptionistTreatmentsTab />
            </Layout>
          </PrivateRoute>
        } />

        {/* Redirect any other routes to dashboard or landing */}
        <Route 
          path="*" 
          element={
            <Navigate to={isAuthenticated() ? "/dashboard" : "/"} replace />
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;
