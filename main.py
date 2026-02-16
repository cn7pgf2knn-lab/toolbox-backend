from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import auth, users, employees, toolboxes, completions

# Lifespan context manager voor startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("✅ Database tabellen aangemaakt")
    yield
    # Shutdown (cleanup hier indien nodig)
    print("👋 Shutting down...")

# Create FastAPI app met lifespan
app = FastAPI(
    title="Toolbox Management API",
    version="1.0.0",
    description="Backend API voor Toolbox Management PWA",
    lifespan=lifespan
)

# CORS configuratie
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In productie: specificeer je frontend domein
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
def read_root():
    return {
        "message": "Toolbox Management API is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(toolboxes.router, prefix="/api/toolboxes", tags=["Toolboxes"])
app.include_router(completions.router, prefix="/api/completions", tags=["Completions"])
