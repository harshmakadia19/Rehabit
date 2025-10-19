import React, { useState, useEffect } from 'react';
import { TrendingUp, Brain, Target, Calendar, Activity, BarChart3, Zap, Award } from 'lucide-react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { mockInsightsData } from '../services/mockData';

export default function Insights() {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    setTimeout(() => {
      setInsights(mockInsightsData);
      setLoading(false);
    }, 500);
  }, []);

  const processActivityData = () => {
    if (!insights?.activities) return [];
    
    return insights.activities.map(activity => ({
      date: new Date(activity.timestamp).toLocaleDateString('en-US', { weekday: 'short' }),
      productivity: activity.productivity_score || 0,
      duration: activity.duration || 0,
      focus: activity.focus_level === 'high' ? 3 : activity.focus_level === 'medium' ? 2 : 1
    }));
  };

  const calculateWeeklyAverage = () => {
    if (!insights?.activities) return 0;
    const sum = insights.activities.reduce((acc, act) => acc + (act.productivity_score || 0), 0);
    return (sum / insights.activities.length).toFixed(1);
  };

  const getProductivityTrend = () => {
    if (!insights?.activities || insights.activities.length < 2) return 'stable';
    const recent = insights.activities;
    const first = recent.slice(0, 3).reduce((acc, act) => acc + (act.productivity_score || 0), 0) / 3;
    const last = recent.slice(-3).reduce((acc, act) => acc + (act.productivity_score || 0), 0) / 3;
    
    if (last > first + 0.5) return 'increasing';
    if (last < first - 0.5) return 'decreasing';
    return 'stable';
  };

  const getMostProductiveTime = () => {
    if (!insights?.activities) return 'N/A';
    
    const hourCounts = {};
    insights.activities.forEach(activity => {
      const hour = new Date(activity.timestamp).getHours();
      if (!hourCounts[hour]) hourCounts[hour] = { total: 0, count: 0 };
      hourCounts[hour].total += activity.productivity_score || 0;
      hourCounts[hour].count += 1;
    });
    
    let maxAvg = 0;
    let bestHour = 0;
    Object.entries(hourCounts).forEach(([hour, data]) => {
      const avg = data.total / data.count;
      if (avg > maxAvg) {
        maxAvg = avg;
        bestHour = parseInt(hour);
      }
    });
    
    const period = bestHour >= 12 ? 'PM' : 'AM';
    const displayHour = bestHour > 12 ? bestHour - 12 : bestHour === 0 ? 12 : bestHour;
    return `${displayHour}${period}`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const activityData = processActivityData();
  const weeklyAvg = calculateWeeklyAverage();
  const trend = getProductivityTrend();
  const bestTime = getMostProductiveTime();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Insights</h1>
            <p className="text-gray-600 mt-1">Your productivity analytics and AI recommendations</p>
          </div>
          <button className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            <Activity className="w-4 h-4" />
            Refresh
          </button>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg p-6 text-white shadow-lg">
            <div className="flex items-center justify-between mb-2">
              <BarChart3 className="w-8 h-8 opacity-80" />
              <span className="text-3xl font-bold">{weeklyAvg}</span>
            </div>
            <p className="text-blue-100 text-sm font-medium">Weekly Avg Score</p>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-6 text-white shadow-lg">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-8 h-8 opacity-80" />
              <span className="text-3xl font-bold capitalize">{trend}</span>
            </div>
            <p className="text-purple-100 text-sm font-medium">Productivity Trend</p>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white shadow-lg">
            <div className="flex items-center justify-between mb-2">
              <Zap className="w-8 h-8 opacity-80" />
              <span className="text-3xl font-bold">{bestTime}</span>
            </div>
            <p className="text-green-100 text-sm font-medium">Peak Performance</p>
          </div>

          <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-lg p-6 text-white shadow-lg">
            <div className="flex items-center justify-between mb-2">
              <Award className="w-8 h-8 opacity-80" />
              <span className="text-3xl font-bold">{insights?.dashboard?.current_streak || 0}</span>
            </div>
            <p className="text-orange-100 text-sm font-medium">Day Streak</p>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Productivity Trend Chart */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-blue-600" />
              7-Day Productivity Trend
            </h2>
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={activityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[0, 10]} />
                <Tooltip />
                <Area type="monotone" dataKey="productivity" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Activity Duration Chart */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-purple-600" />
              Time Spent (Minutes)
            </h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={activityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="duration" fill="#8b5cf6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* AI Predictions */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Brain className="w-5 h-5 text-indigo-600" />
            AI Predictions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="border-2 border-gray-200 rounded-lg p-4 hover:border-indigo-300 transition-colors">
              <p className="text-sm text-gray-600 mb-1">Predicted Score</p>
              <p className="text-3xl font-bold text-indigo-600">
                {insights?.predictions?.predicted_score?.toFixed(1)}
              </p>
            </div>
            <div className="border-2 border-gray-200 rounded-lg p-4 hover:border-green-300 transition-colors">
              <p className="text-sm text-gray-600 mb-1">Confidence Level</p>
              <p className="text-3xl font-bold text-green-600">
                {(insights?.predictions?.confidence * 100).toFixed(0)}%
              </p>
            </div>
            <div className="border-2 border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors">
              <p className="text-sm text-gray-600 mb-1">Trend</p>
              <p className="text-3xl font-bold text-blue-600 capitalize">
                {insights?.predictions?.trend}
              </p>
            </div>
          </div>
        </div>

        {/* AI Recommendations */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-green-600" />
            Personalized Recommendations
          </h2>
          <div className="space-y-3">
            {insights?.recommendations?.map((rec, index) => (
              <div key={index} className="flex items-start gap-3 p-4 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg hover:shadow-md transition-shadow">
                <div className="bg-green-600 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 font-semibold">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <p className="text-gray-800 font-medium">{rec.recommendation}</p>
                  {rec.reason && (
                    <p className="text-sm text-gray-600 mt-1">💡 {rec.reason}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}