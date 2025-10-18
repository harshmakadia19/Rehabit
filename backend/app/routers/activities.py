"""
Activity logging endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/log", response_model=schemas.ActivityResponse)
def log_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
    """
    Log a new activity
    
    - **user_id**: ID of the user
    - **activity_type**: Type (work, break, exercise, meeting)
    - **duration**: Duration in minutes
    - **productivity_score**: Score from 1-10
    - **focus_level**: low, medium, or high
    """
    # Verify user exists
    user = db.query(models.User).filter(models.User.id == activity.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create activity
    new_activity = models.Activity(**activity.dict())
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity

@router.get("/{user_id}", response_model=List[schemas.ActivityResponse])
def get_activities(user_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """
    Get user's recent activities
    
    - **user_id**: User ID
    - **limit**: Maximum number of activities to return (default 50)
    """
    activities = db.query(models.Activity).filter(
        models.Activity.user_id == user_id
    ).order_by(models.Activity.timestamp.desc()).limit(limit).all()
    
    return activities