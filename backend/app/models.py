"""
Database Models for Rehabit
Defines the structure of our database tables
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User account table"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship: one user has many activities
    activities = relationship("Activity", back_populates="user")


class Activity(Base):
    """User activity log table"""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    activity_type = Column(String)  # work, break, exercise, etc.
    duration = Column(Integer)  # minutes
    productivity_score = Column(Integer)  # 1-10 scale
    focus_level = Column(String)  # low, medium, high
    notes = Column(String, nullable=True)
    
    # Relationship: activity belongs to one user
    user = relationship("User", back_populates="activities")


class Prediction(Base):
    """ML predictions cache table"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    predicted_score = Column(Float)
    confidence = Column(Float)
    hour_ahead = Column(Integer)  # Prediction for which hour