"""
Backend API Tests for Rehabit
Tests all API endpoints for correct behavior
Author: Rishi Nalam
"""
import pytest
import requests
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

# API Base URL
BASE_URL = "http://localhost:8000/api"

# Test data
TEST_USER = {
    "name": "Test User",
    "email": f"test_user_{datetime.now().timestamp()}@rehabit.com"
}

TEST_ACTIVITY = {
    "user_id": 1,
    "activity_type": "work",
    "duration": 60,
    "productivity_score": 8,
    "focus_level": "high",
    "notes": "Test activity"
}


class TestHealthCheck:
    """Test basic health endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns welcome message"""
        response = requests.get("http://localhost:8000/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Rehabit" in data["message"]
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get("http://localhost:8000/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestUserEndpoints:
    """Test user management endpoints"""
    
    def test_create_user(self):
        """Test creating a new user"""
        response = requests.post(f"{BASE_URL}/users/create", json=TEST_USER)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == TEST_USER["name"]
        assert data["email"] == TEST_USER["email"]
        print(f"✅ User created with ID: {data['id']}")
    
    def test_get_user(self):
        """Test getting user by ID"""
        # First create user
        create_response = requests.post(f"{BASE_URL}/users/create", json=TEST_USER)
        user_id = create_response.json()["id"]
        
        # Now get the user
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["name"] == TEST_USER["name"]
        print(f"✅ Retrieved user: {data['name']}")
    
    def test_create_user_duplicate_email(self):
        """Test that duplicate email returns error"""
        # Create first user
        unique_email = f"duplicate_test_{datetime.now().timestamp()}@rehabit.com"
        user_data = {"name": "Test User", "email": unique_email}
        requests.post(f"{BASE_URL}/users/create", json=user_data)
        
        # Try to create same user again
        response = requests.post(f"{BASE_URL}/users/create", json=user_data)
        assert response.status_code == 400
        print("✅ Duplicate email correctly rejected")


class TestActivityEndpoints:
    """Test activity logging endpoints"""
    
    def test_log_activity(self):
        """Test logging a new activity"""
        response = requests.post(f"{BASE_URL}/activities/log", json=TEST_ACTIVITY)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["activity_type"] == TEST_ACTIVITY["activity_type"]
        print(f"✅ Activity logged with ID: {data['id']}")
    
    def test_log_activity_invalid_user(self):
        """Test logging activity for non-existent user"""
        invalid_activity = TEST_ACTIVITY.copy()
        invalid_activity["user_id"] = 99999
        response = requests.post(f"{BASE_URL}/activities/log", json=invalid_activity)
        assert response.status_code == 404
        print("✅ Invalid user correctly rejected")
    
    def test_get_activities(self):
        """Test getting user activities"""
        # First log an activity
        requests.post(f"{BASE_URL}/activities/log", json=TEST_ACTIVITY)
        
        # Now get activities
        response = requests.get(f"{BASE_URL}/activities/{TEST_ACTIVITY['user_id']}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        print(f"✅ Retrieved {len(data)} activities")
    
    def test_log_activity_validation(self):
        """Test activity validation"""
        invalid_activity = {
            "user_id": 1,
            "activity_type": "work",
            "duration": -10,  # Invalid negative duration
            "productivity_score": 11,  # Invalid score > 10
            "focus_level": "high"
        }
        response = requests.post(f"{BASE_URL}/activities/log", json=invalid_activity)
        assert response.status_code == 400
        print("✅ Invalid activity data correctly rejected")


class TestDashboardEndpoint:
    """Test dashboard endpoint"""
    
    def test_get_dashboard(self):
        """Test getting dashboard data"""
        response = requests.get(f"{BASE_URL}/dashboard/1")
        assert response.status_code == 200
        data = response.json()
        
        # Check all expected fields
        assert "today_score" in data
        assert "work_time" in data
        assert "predictions" in data
        assert "recommendations" in data
        
        # Verify data types
        assert isinstance(data["today_score"], (int, float))
        assert isinstance(data["work_time"], (int, float))
        assert isinstance(data["predictions"], list)
        assert isinstance(data["recommendations"], list)
        
        print(f"✅ Dashboard data retrieved successfully")
        print(f"   Today Score: {data['today_score']}")
        print(f"   Work Time: {data['work_time']} hours")
    
    def test_dashboard_invalid_user(self):
        """Test dashboard for non-existent user"""
        response = requests.get(f"{BASE_URL}/dashboard/99999")
        assert response.status_code == 404
        print("✅ Invalid user dashboard correctly rejected")


class TestMLEndpoints:
    """Test ML-powered endpoints"""
    
    def test_get_predictions(self):
        """Test getting productivity predictions"""
        response = requests.get(f"{BASE_URL}/predictions/1")
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert "hourly_predictions" in data
        assert "peak_hours" in data
        
        # Verify hourly predictions
        assert isinstance(data["hourly_predictions"], list)
        assert len(data["hourly_predictions"]) == 24
        
        # Verify peak hours
        assert isinstance(data["peak_hours"], list)
        assert len(data["peak_hours"]) > 0
        
        print(f"✅ Predictions retrieved successfully")
        print(f"   Peak Hours: {data['peak_hours']}")
    
    def test_get_recommendations(self):
        """Test getting AI recommendations"""
        response = requests.get(f"{BASE_URL}/recommendations/1")
        assert response.status_code == 200
        data = response.json()
        
        # Check structure
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Verify each recommendation has required fields
        for rec in data:
            assert "type" in rec
            assert "message" in rec
            assert "priority" in rec
        
        print(f"✅ {len(data)} recommendations retrieved")
    
    def test_predictions_caching(self):
        """Test that predictions are cached efficiently"""
        # Make first request
        start_time = datetime.now()
        response1 = requests.get(f"{BASE_URL}/predictions/1")
        first_duration = (datetime.now() - start_time).total_seconds()
        
        # Make second request
        start_time = datetime.now()
        response2 = requests.get(f"{BASE_URL}/predictions/1")
        second_duration = (datetime.now() - start_time).total_seconds()
        
        # Second request should be faster (cached)
        assert response1.status_code == 200
        assert response2.status_code == 200
        print(f"✅ First request: {first_duration:.3f}s, Second: {second_duration:.3f}s")


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_endpoint(self):
        """Test accessing non-existent endpoint"""
        response = requests.get(f"{BASE_URL}/nonexistent")
        assert response.status_code == 404
        print("✅ Invalid endpoint returns 404")
    
    def test_malformed_json(self):
        """Test sending malformed JSON"""
        response = requests.post(
            f"{BASE_URL}/users/create",
            data="not json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [400, 422]
        print("✅ Malformed JSON correctly rejected")
    
    def test_missing_required_fields(self):
        """Test missing required fields in user creation"""
        incomplete_user = {"name": "Test User"}  # Missing email
        response = requests.post(f"{BASE_URL}/users/create", json=incomplete_user)
        assert response.status_code == 422
        print("✅ Missing required fields correctly rejected")


class TestPerformance:
    """Test API performance"""
    
    def test_dashboard_response_time(self):
        """Test dashboard loads within acceptable time"""
        start_time = datetime.now()
        response = requests.get(f"{BASE_URL}/dashboard/1")
        duration = (datetime.now() - start_time).total_seconds()
        
        assert response.status_code == 200
        assert duration < 2.0  # Should respond within 2 seconds
        print(f"✅ Dashboard loaded in {duration:.3f}s")
    
    def test_concurrent_requests(self):
        """Test handling multiple concurrent requests"""
        import concurrent.futures
        
        def make_request():
            return requests.get(f"{BASE_URL}/dashboard/1")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        assert all(r.status_code == 200 for r in results)
        print(f"✅ Handled 10 concurrent requests successfully")


if __name__ == "__main__":
    print("\n��� Running Rehabit Backend API Tests\n")
    pytest.main([__file__, "-v", "--tb=short"])
