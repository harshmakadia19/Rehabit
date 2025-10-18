/**
 * Productivity Chart Component
 * Displays 24-hour productivity predictions
 */
import React from 'react';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
export default function ProductivityChart({ predictions }) {
  // Format data for chart
  const chartData = predictions.map(pred => ({
    hour: `${pred.hour}:00`,
    score: pred.score,
    hourNum: pred.hour
  }));
  
  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white px-4 py-2 rounded-lg shadow-lg border border-gray-200">
          <p className="text-sm font-semibold text-gray-900">
            {payload[0].payload.hour}
          </p>
          <p className="text-sm text-primary-600">
            Productivity: <span className="font-bold">{payload[0].value.toFixed(1)}/10</span>
          </p>
        </div>
      );
    }
    return null;
  };
  
  return (
    <div className="card">
      <h3 className="text-lg font-bold text-gray-900 mb-4">
        📊 24-Hour Productivity Forecast
      </h3>
      
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="hour"
            stroke="#888888"
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            stroke="#888888"
            tick={{ fontSize: 12 }}
            domain={[0, 10]}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="score"
            stroke="#3b82f6"
            strokeWidth={2}
            fill="url(#colorScore)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}