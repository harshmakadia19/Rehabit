cat > ActivityLog.jsx << 'EOF'
/**
 * Activity Log Component
 * Form to log new activities
 */
import React, { useState } from 'react';
import { apiService } from '../../services/api';
import { Check, AlertCircle } from 'lucide-react';
import { getActivityEmoji } from '../../utils/helpers';

export default function ActivityLog() {
  const [formData, setFormData] = useState({
    user_id: 1, // Demo user
    activity_type: 'work',
    duration: 60,
    productivity_score: 7,
    focus_level: 'medium',
    notes: ''
  });
  
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'duration' || name === 'productivity_score' 
        ? parseInt(value) 
        : value
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setSubmitting(true);
      setError(null);
      
      // TODO: Call Ayush's API to log activity
      
      // Call the real API to log activity
      await apiService.logActivity(formData);      
      setSuccess(true);
      
      // Reset form after 2 seconds
      setTimeout(() => {
        setSuccess(false);
        setFormData({
          ...formData,
          duration: 60,
          productivity_score: 7,
          notes: ''
        });
      }, 2000);
      
    } catch (err) {
      console.error('Error logging activity:', err);
      setError('Failed to log activity. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Log Activity 📝
          </h1>
          <p className="text-gray-600">
            Track your activities to help our AI understand your patterns
          </p>
        </div>

        {/* Success Message */}
        {success && (
          <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4 flex items-center space-x-3">
            <Check size={20} className="text-green-600" />
            <span className="text-green-800 font-medium">
              Activity logged successfully! 🎉
            </span>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-center space-x-3">
            <AlertCircle size={20} className="text-red-600" />
            <span className="text-red-800 font-medium">{error}</span>
          </div>
        )}

        {/* Form */}
        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Activity Type */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Activity Type
              </label>
              <select
                name="activity_type"
                value={formData.activity_type}
                onChange={handleChange}
                className="input-field"
                required
              >
                <option value="work">{getActivityEmoji('work')} Work</option>
                <option value="break">{getActivityEmoji('break')} Break</option>
                <option value="exercise">{getActivityEmoji('exercise')} Exercise</option>
                <option value="meeting">{getActivityEmoji('meeting')} Meeting</option>
                <option value="study">{getActivityEmoji('study')} Study</option>
                <option value="hobby">{getActivityEmoji('hobby')} Hobby</option>
              </select>
            </div>

            {/* Duration */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Duration (minutes)
              </label>
              <input
                type="number"
                name="duration"
                value={formData.duration}
                onChange={handleChange}
                min="1"
                max="480"
                className="input-field"
                required
              />
              <p className="text-sm text-gray-500 mt-1">
                {Math.floor(formData.duration / 60) > 0 && `${Math.floor(formData.duration / 60)}h `}
                {formData.duration % 60}m
              </p>
            </div>

            {/* Productivity Score */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Productivity Score: <span className="text-primary-600">{formData.productivity_score}/10</span>
              </label>
              <input
                type="range"
                name="productivity_score"
                value={formData.productivity_score}
                onChange={handleChange}
                min="1"
                max="10"
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer 
                         accent-primary-600"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Low (1)</span>
                <span>Medium (5)</span>
                <span>High (10)</span>
              </div>
            </div>

            {/* Focus Level */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Focus Level
              </label>
              <div className="grid grid-cols-3 gap-3">
                {['low', 'medium', 'high'].map(level => (
                  <button
                    key={level}
                    type="button"
                    onClick={() => setFormData(prev => ({ ...prev, focus_level: level }))}
                    className={`
                      px-4 py-3 rounded-lg font-medium capitalize
                      transition-all duration-200
                      ${formData.focus_level === level
                        ? 'bg-primary-600 text-white shadow-lg scale-105'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }
                    `}
                  >
                    {level}
                  </button>
                ))}
              </div>
            </div>

            {/* Notes */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Notes (optional)
              </label>
              <textarea
                name="notes"
                value={formData.notes}
                onChange={handleChange}
                className="input-field resize-none"
                rows="4"
                placeholder="Any additional thoughts or observations..."
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={submitting}
              className={`
                w-full btn-primary
                ${submitting ? 'opacity-50 cursor-not-allowed' : ''}
              `}
            >
              {submitting ? 'Logging Activity...' : 'Log Activity'}
            </button>
          </form>
        </div>

        {/* Quick Log Buttons */}
        <div className="mt-8">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">
            Quick Log:
          </h3>
          <div className="grid grid-cols-2 gap-3">
            <QuickLogButton
              label="Work Session"
              emoji="💼"
              onClick={() => setFormData({
                ...formData,
                activity_type: 'work',
                duration: 60,
                focus_level: 'high'
              })}
            />
            <QuickLogButton
              label="Quick Break"
              emoji="☕"
              onClick={() => setFormData({
                ...formData,
                activity_type: 'break',
                duration: 15,
                focus_level: 'low'
              })}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

// Quick Log Button Component
function QuickLogButton({ label, emoji, onClick }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="bg-white border-2 border-gray-200 rounded-lg p-4 
               hover:border-primary-400 hover:bg-primary-50 
               transition-all duration-200 text-left group"
    >
      <div className="text-2xl mb-1">{emoji}</div>
      <div className="text-sm font-medium text-gray-700 group-hover:text-primary-700">
        {label}
      </div>
    </button>
  );
}
EOF
