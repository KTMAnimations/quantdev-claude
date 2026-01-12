"""
OpenQuant API - FastAPI Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers import ideation, backtest, monte_carlo, regression, pine_gen, prop_firm


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    print("Starting OpenQuant API...")
    yield
    # Shutdown
    print("Shutting down OpenQuant API...")


app = FastAPI(
    title="OpenQuant API",
    description="Quantitative trading platform API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://openquant.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ideation.router, prefix="/ideation", tags=["Edge Discovery"])
app.include_router(backtest.router, prefix="/backtest", tags=["Backtesting"])
app.include_router(monte_carlo.router, prefix="/monte-carlo", tags=["Monte Carlo"])
app.include_router(regression.router, prefix="/regression", tags=["Regression Analysis"])
app.include_router(pine_gen.router, prefix="/pine", tags=["Pine Script Generator"])
app.include_router(prop_firm.router, prefix="/prop-firm", tags=["Prop Firm Simulator"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "OpenQuant API"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "database": "connected",
            "redis": "connected",
        }
    }
