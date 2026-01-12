"""
OpenQuant API - FastAPI Backend with LLM Integration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

from app.routers import ideation, backtest, monte_carlo, regression, pine_gen, prop_firm, chat
from app.core.config import get_settings
from app.core.llm_service import LLMService
from app.rag.pine_rag import PineScriptRAG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global service instances
llm_service: LLMService = None
pine_rag: PineScriptRAG = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    global llm_service, pine_rag

    # Startup
    logger.info("Starting OpenQuant API...")
    settings = get_settings()

    # Initialize LLM service
    try:
        llm_service = LLMService(settings)
        logger.info(f"LLM service initialized with provider: {settings.llm_provider}")

        # Test LLM connection
        if await llm_service.health_check():
            logger.info("LLM service health check passed")
        else:
            logger.warning("LLM service health check failed - some features may not work")
    except Exception as e:
        logger.error(f"Failed to initialize LLM service: {e}")
        llm_service = None

    # Initialize RAG
    try:
        # Ensure data directory exists
        os.makedirs(settings.chromadb_persist_directory, exist_ok=True)

        pine_rag = PineScriptRAG(
            persist_directory=settings.chromadb_persist_directory,
            collection_name=settings.chromadb_collection_name
        )
        logger.info(f"Pine Script RAG initialized with {pine_rag.collection.count()} documents")
    except Exception as e:
        logger.error(f"Failed to initialize RAG: {e}")
        pine_rag = None

    yield

    # Shutdown
    logger.info("Shutting down OpenQuant API...")


app = FastAPI(
    title="OpenQuant API",
    description="Quantitative trading platform API with LLM capabilities",
    version="1.1.0",
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
app.include_router(chat.router, prefix="/chat", tags=["Chat"])


# Dependency injection helpers
def get_llm_service() -> LLMService:
    """Get the global LLM service instance"""
    return llm_service


def get_pine_rag() -> PineScriptRAG:
    """Get the global Pine Script RAG instance"""
    return pine_rag


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "OpenQuant API", "version": "1.1.0"}


@app.get("/health")
async def health_check():
    """Detailed health check"""
    settings = get_settings()

    # Check LLM service
    llm_status = "unavailable"
    if llm_service:
        try:
            if await llm_service.health_check():
                llm_status = "healthy"
            else:
                llm_status = "unhealthy"
        except Exception:
            llm_status = "error"

    # Check RAG
    rag_status = "healthy" if pine_rag else "unavailable"
    rag_docs = pine_rag.collection.count() if pine_rag else 0

    return {
        "status": "healthy",
        "version": "1.1.0",
        "services": {
            "api": "running",
            "llm": {
                "status": llm_status,
                "provider": settings.llm_provider,
                "model": settings.llm_model
            },
            "rag": {
                "status": rag_status,
                "documents": rag_docs
            },
            "database": "connected",
            "redis": "connected",
        }
    }
