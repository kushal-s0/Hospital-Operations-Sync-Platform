import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import OPDQueue from './pages/OPD/OPDQueue';
import BedManagement from './pages/Beds/BedManagement';
import Admissions from './pages/Admissions/Admissions';
import Inventory from './pages/Inventory/Inventory';
import InterHospital from './pages/InterHospital/InterHospital';
import './App.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/opd" element={<OPDQueue />} />
          <Route path="/beds" element={<BedManagement />} />
          <Route path="/admissions" element={<Admissions />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/inter-hospital" element={<InterHospital />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
