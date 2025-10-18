cat > RecommendationCard.jsx << 'EOF'
/**
 * Recommendation Card Component
 * Displays AI-generated recommendations
 */
import React from 'react';
import { AlertCircle, Clock, Activity, Lightbulb } from 'lucide-react';
import { getPriorityColor } from '../../utils/helpers';

export default function RecommendationCard({ recommendation }) {
  const { type, priority, message, action } = recommendation;
  
  // Get icon based on type
  const getIcon = () => {
    switch(type) {
      case 'timing': return <Clock size={20} />;
      case 'break': return <Activity size={20} />;
      case 'health': return <AlertCircle size={20} />;
      default: return <Lightbulb size={20} />;
    }
  };
  
  return (
    <div className={`
      p-4 rounded-lg border-l-4 transition-all duration-200
      hover:shadow-md cursor-pointer
      ${getPriorityColor(priority)}
    `}>
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0 mt-1">
          {getIcon()}
        </div>
        <div className="flex-1 min-w-0">
          <p className="font-medium leading-relaxed">
            {message}
          </p>
          <div className="flex items-center mt-2 space-x-2">
            <span className="text-xs uppercase font-semibold tracking-wider">
              {type}
            </span>
            <span className="text-xs">•</span>
            <span className="text-xs uppercase font-semibold">
              {priority}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
EOF
