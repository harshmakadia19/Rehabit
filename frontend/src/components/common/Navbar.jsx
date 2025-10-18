/**
 * Navigation Bar Component
 */
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Activity, TrendingUp, User } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();
  
  // Check if current route is active
  const isActive = (path) => location.pathname === path;
  
  // Don't show navbar on landing page
  if (location.pathname === '/') return null;
  
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-accent-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">R</span>
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-primary-600 to-accent-600 bg-clip-text text-transparent">
              Rehabit
            </span>
          </Link>
          
          {/* Navigation Links */}
          <div className="flex items-center space-x-1">
            <NavLink 
              to="/dashboard" 
              icon={<LayoutDashboard size={20} />}
              label="Dashboard"
              active={isActive('/dashboard')}
            />
            <NavLink 
              to="/activity" 
              icon={<Activity size={20} />}
              label="Log Activity"
              active={isActive('/activity')}
            />
            <NavLink 
              to="/insights" 
              icon={<TrendingUp size={20} />}
              label="Insights"
              active={isActive('/insights')}
            />
          </div>
          
          {/* User Info */}
          <div className="flex items-center space-x-3">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-medium text-gray-700">Demo User</p>
              <p className="text-xs text-gray-500">demo@rehabit.com</p>
            </div>
            <div className="w-10 h-10 bg-gradient-to-br from-primary-400 to-accent-400 rounded-full flex items-center justify-center">
              <User size={20} className="text-white" />
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

// Navigation Link Component
function NavLink({ to, icon, label, active }) {
  return (
    <Link
      to={to}
      className={`
        flex items-center space-x-2 px-4 py-2 rounded-lg
        transition-all duration-200
        ${active 
          ? 'bg-primary-50 text-primary-700 font-semibold' 
          : 'text-gray-600 hover:bg-gray-100'
        }
      `}
    >
      {icon}
      <span className="hidden sm:inline">{label}</span>
    </Link>
  );
}
