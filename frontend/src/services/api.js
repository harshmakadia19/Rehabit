/**
 * API Service for Rehabit
 * Handles all backend communication
 */
import axios from 'axios';

// Backend URL - change this to Ayush's deployed URL
const API_BASE_URL = 'http://127.0.0.1:8000/api';
// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds
});

// API service object with all endpoints
export const apiService = {
  // ==================== USER ENDPOINTS ====================
  
  /**
   * Create a new user
   * @param {Object} userData - { name, email }
   */
  createUser: async (userData) => {
    try {
      const response = await api.post('/users/create', userData);
      return response.data;
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  },

  /**
   * Get user by ID
   * @param {number} userId - User ID
   */
  getUser: async (userId) => {
    try {
      const response = await api.get(`/users/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user:', error);
      throw error;
    }
  },

  // ==================== ACTIVITY ENDPOINTS ====================
  
  /**
   * Log a new activity
   * @param {Object} activityData - Activity details
   */
  logActivity: async (activityData) => {
    try {
      const response = await api.post('/activities/log', activityData);
      return response.data;
    } catch (error) {
      console.error('Error logging activity:', error);
      throw error;
    }
  },

  /**
   * Get user's activities
   * @param {number} userId - User ID
   * @param {number} limit - Number of activities to fetch
   */
  getActivities: async (userId, limit = 50) => {
    try {
      const response = await api.get(`/activities/${userId}?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching activities:', error);
      throw error;
    }
  },

  // ==================== DASHBOARD ENDPOINT ====================
  
  /**
   * Get complete dashboard data
   * @param {number} userId - User ID
   */
  getDashboard: async (userId) => {
    try {
      const response = await api.get(`/dashboard/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      throw error;
    }
  },

  // ==================== ML ENDPOINTS ====================
  
  /**
   * Get productivity predictions
   * @param {number} userId - User ID
   */
  getPredictions: async (userId) => {
    try {
      const response = await api.get(`/predictions/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching predictions:', error);
      throw error;
    }
  },

  /**
   * Get AI recommendations
   * @param {number} userId - User ID
   */
  getRecommendations: async (userId) => {
    try {
      const response = await api.get(`/recommendations/${userId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      throw error;
    }
  },
};

export default api;

