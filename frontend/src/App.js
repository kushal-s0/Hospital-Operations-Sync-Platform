import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import PrivateRoute from './components/PrivateRoute/PrivateRoute';
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

        {/* Receptionist Dashboard - With Layout for profile/logout */}
        <Route path="/receptionist" element={
          <PrivateRoute>
            <Layout>
              <ReceptionistDashboard />
            </Layout>
          </PrivateRoute>
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
