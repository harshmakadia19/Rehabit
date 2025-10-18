"""
Pydantic Schemas for Request/Response validation
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    name: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Activity Schemas
class ActivityCreate(BaseModel):
    """Schema for logging a new activity"""
    user_id: int
    activity_type: str
    duration: int  # minutes
    productivity_score: int  # 1-10
    focus_level: str  # low, medium, high
    notes: Optional[str] = None

class ActivityResponse(BaseModel):
    """Schema for activity response"""
    id: int
    user_id: int
    timestamp: datetime
    activity_type: str
    duration: int
    productivity_score: int
    focus_level: str
    
    class Config:
        from_attributes = True

# Dashboard Schema
class DashboardResponse(BaseModel):
    """Schema for complete dashboard data"""
    user_id: int
    today_score: float
    work_time: int  # total minutes
    predictions: List[dict]
    recommendations: List[dict]
    streak: int
    timestamp: datetime