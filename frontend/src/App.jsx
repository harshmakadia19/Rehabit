/**
 * Main App Component with Routing
 */
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/common/Navbar';
import Landing from './components/landing/Landing';
import Dashboard from './components/dashboard/Dashboard';
import ActivityLog from './components/activity/ActivityLog';
import Loading from './components/common/Loading';

// Placeholder for Insights (to be built later)
const Insights = () => <div className="p-8">Insights page coming soon...</div>;

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          {/* Landing Page */}
          <Route path="/" element={<Landing />} />

          {/* Main App Pages */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/activity" element={<ActivityLog />} />
          <Route path="/insights" element={<Insights />} />

          {/* Redirect unknown routes to landing */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
