"""
Main FastAPI application for Rehabit
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routers import users, activities, predictions, recommendations, dashboard

# Initialize database tables
init_db()

# Create FastAPI app
app = FastAPI(
    title="Rehabit API",
    description="AI-powered productivity and habit coaching platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    """Root endpoint - health check"""
    return {
        "message": "Welcome to Rehabit API",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "connected"}

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])