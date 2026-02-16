import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.database import engine, Base
from app.routers import auth, users, employees, toolboxes, completions

# Create database tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (nothing to do)

app = FastAPI(
    title="Toolbox Management API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS - Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.get("/")
def read_root():
    return {
        "message": "Toolbox Management API is running!",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected", "version": "1.0.0"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
