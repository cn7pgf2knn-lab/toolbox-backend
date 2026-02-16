from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, users, employees, toolboxes, completions

# Create FastAPI app
app = FastAPI(
    title="Toolbox Management API",
    version="1.0.0",
    description="Backend API voor Toolbox Management PWA"
)

# CORS configuratie
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In productie: specificeer je frontend domein
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database tabellen aanmaken bij startup (FastAPI 0.88.0 style)
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tabellen aangemaakt")

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

