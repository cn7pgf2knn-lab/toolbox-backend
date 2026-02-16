"""
TOOLBOX MANAGEMENT - FASTAPI BACKEND
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import users, employees, toolboxes, completions, auth
from app.config import settings


# Lifecycle events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting Toolbox Management API...")

    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

    yield

    # Shutdown
    print("👋 Shutting down Toolbox Management API...")


# Create FastAPI app
app = FastAPI(
    title="Toolbox Management API",
    description="Backend API for Toolbox Training Management System",
    version="1.0.0",
    lifespan=lifespan
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cn7pgf2knn-lab.github.io",  # GitHub Pages
        "http://localhost:3000",  # Local development
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(toolboxes.router, prefix="/api/toolboxes", tags=["Toolboxes"])
app.include_router(completions.router, prefix="/api/completions", tags=["Completions"])


# Root endpoint
@app.get("/")
async def root():
    """API Root - Health check"""
    return {
        "message": "Toolbox Management API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs"
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload tijdens development
    )
