"""
Main FastAPI application for Rehabit
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db

# Initialize database tables
init_db()

# Create FastAPI app
app = FastAPI(
    title="Rehabit API",
    description="AI-powered productivity and habit coaching platform",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc"  # ReDoc at /redoc
)

# CORS middleware - allows frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact frontend URL
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

# TODO: Include routers here (will add on Day 2)
# from app.routers import users, activities, predictions, recommendations, dashboard
# app.include_router(users.router, prefix="/api/users", tags=["users"])