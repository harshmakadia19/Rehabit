/**
 * Helper utility functions
 */

// Get emoji for activity type
export function getActivityEmoji(activityType) {
    const emojis = {
      work: '💼',
      break: '☕',
      exercise: '🏃',
      meeting: '👥',
      study: '📚',
      hobby: '🎨'
    };
    return emojis[activityType] || '📝';
  }
  
  // Get color class for priority
  export function getPriorityColor(priority) {
    const colors = {
      high: 'text-red-600 bg-red-50 border-red-200',
      medium: 'text-yellow-600 bg-yellow-50 border-yellow-200',
      low: 'text-green-600 bg-green-50 border-green-200'
    };
    return colors[priority] || colors.medium;
  }
  
  // Format date
  export function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  }
  
  // Format time
  export function formatTime(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  }