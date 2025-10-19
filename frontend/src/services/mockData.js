export const mockInsightsData = {
    activities: [
      { timestamp: "2025-01-13T08:00:00", activity_type: "work", duration: 90, productivity_score: 8, focus_level: "high" },
      { timestamp: "2025-01-14T09:00:00", activity_type: "work", duration: 120, productivity_score: 7, focus_level: "high" },
      { timestamp: "2025-01-15T10:00:00", activity_type: "work", duration: 60, productivity_score: 9, focus_level: "high" },
      { timestamp: "2025-01-16T08:30:00", activity_type: "work", duration: 75, productivity_score: 6, focus_level: "medium" },
      { timestamp: "2025-01-17T09:30:00", activity_type: "work", duration: 100, productivity_score: 8, focus_level: "high" },
      { timestamp: "2025-01-18T10:00:00", activity_type: "work", duration: 85, productivity_score: 7, focus_level: "medium" },
      { timestamp: "2025-01-19T11:00:00", activity_type: "work", duration: 95, productivity_score: 8, focus_level: "high" }
    ],
    predictions: {
      predicted_score: 8.2,
      confidence: 0.87,
      trend: "increasing"
    },
    recommendations: [
      {
        recommendation: "Your productivity is trending upward! Maintain your current routine for best results.",
        reason: "AI detected consistent improvement over the past week"
      },
      {
        recommendation: "Consider scheduling deep work sessions between 9-11 AM when your focus is highest.",
        reason: "Analysis shows 25% higher productivity during morning hours"
      },
      {
        recommendation: "You're on track for a personal best this month. Keep up the momentum!",
        reason: "Current streak indicates strong habit formation"
      }
    ],
    dashboard: {
      current_streak: 5,
      total_tasks: 42,
      avg_score: 7.2
    }
};
