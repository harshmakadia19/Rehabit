import React, { useState, useEffect } from 'react';
import { Target, Clock, Flame, TrendingUp } from 'lucide-react';
import { apiService } from '../../services/api';
import StatsCard from './StatsCard';
import ProductivityChart from './ProductivityChart';
import RecommendationCard from './RecommendationCard';
import Loading from '../common/Loading';

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const userId = 1; // Demo user ID

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      
      // Call dashboard API
      const data = await apiService.getDashboard(userId);
      setDashboardData(data);
      setError(null);
    } catch (err) {
      console.error('Error loading dashboard:', err);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  // Show loading state
  if (loading) {
    return <Loading message="Loading your dashboard..." />;
  }

  // Show error state
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 font-semibold mb-4">{error}</p>
          <button onClick={loadDashboard} className="btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 animate-fadeIn">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back! 👋
          </h1>
          <p className="text-gray-600">
            Here's your productivity overview for today
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="animate-fadeIn">
            <StatsCard
              icon={<Target size={24} />}
              label="Today's Productivity"
              value={`${dashboardData?.today_score || 0}/10`}
              subtitle="Above average 🎯"
              color="primary"
            />
          </div>
          <div className="animate-fadeIn">
            <StatsCard
              icon={<Clock size={24} />}
              label="Work Time"
              value={`${Math.floor((dashboardData?.work_time || 0) / 60)}h ${(dashboardData?.work_time || 0) % 60}m`}
              subtitle="4 sessions completed"
              color="green"
            />
          </div>
          <div className="animate-fadeIn">
            <StatsCard
              icon={<Flame size={24} />}
              label="Current Streak"
              value={`${dashboardData?.streak || 0} days`}
              subtitle="Keep it up! 🔥"
              color="orange"
            />
          </div>
          <div className="animate-fadeIn">
            <StatsCard
              icon={<TrendingUp size={24} />}
              label="This Week"
              value="+23%"
              subtitle="vs last week"
              color="purple"
            />
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Chart */}
          <div className="lg:col-span-2 animate-fadeIn">
            <ProductivityChart predictions={dashboardData?.predictions || []} />
          </div>

          {/* Right Column - Recommendations */}
          <div className="lg:col-span-1 animate-fadeIn">
            <div className="card animate-fadeIn">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                🤖 AI Recommendations
              </h3>
              <div className="space-y-3">
                {dashboardData?.recommendations?.map((rec, idx) => (
                  <RecommendationCard key={idx} recommendation={rec} />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
