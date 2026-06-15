from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List

from app.repository.mongo_connection import mongo_connection
from app.services.transaction_service import TransactionService
from app.services.stats_service import StatsService
from app.models.transaction import TransactionResponse, TransactionCreate, TransactionUpdate

# Initialize FastAPI app
app = FastAPI(title="Finance Tracker API", version="1.0.0")

# Add CORS middleware for Electron frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services (lazy - don't connect to DB on startup)
transaction_service = None
stats_service = None


def get_transaction_service():
    global transaction_service
    if transaction_service is None:
        transaction_service = TransactionService()
    return transaction_service


def get_stats_service():
    global stats_service
    if stats_service is None:
        stats_service = StatsService()
    return stats_service


# ============================================================================
# Health & Connection Checks
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.get("/api/health")
async def api_health():
    """API health check with MongoDB connection"""
    try:
        db = mongo_connection.get_db()
        db.server_info()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


# ============================================================================
# Transaction Endpoints
# ============================================================================

@app.get("/api/transactions", response_model=List[TransactionResponse])
async def get_transactions(limit: int = Query(100, ge=1, le=1000), skip: int = Query(0, ge=0)):
    """Get all transactions with pagination"""
    try:
        return get_transaction_service().get_all_transactions(limit=limit, skip=skip)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/transactions/search", response_model=List[TransactionResponse])
async def search_transactions(
    query: str = Query(..., min_length=1),
    limit: int = Query(100, ge=1, le=1000),
    skip: int = Query(0, ge=0)
):
    """Search transactions by description or category"""
    try:
        return get_transaction_service().search_transactions(query, limit=limit, skip=skip)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/transactions/by-date", response_model=List[TransactionResponse])
async def get_by_date(
    start: str = Query(..., description="Start date (ISO format)"),
    end: str = Query(..., description="End date (ISO format)"),
    limit: int = Query(1000, ge=1, le=10000),
):
    """Get transactions by date range (ISO format: 2024-09-01)"""
    try:
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)
        return get_transaction_service().get_by_date_range(start_date, end_date, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/transactions/by-pay-period", response_model=List[TransactionResponse])
async def get_by_pay_period(month: str = Query(..., description="Month in format: September2024")):
    """Get transactions by pay period (month)"""
    try:
        return get_transaction_service().get_by_pay_period(month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str):
    """Get single transaction by ID"""
    try:
        transaction = get_transaction_service().get_transaction(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pay-periods", response_model=List[str])
async def get_pay_periods(months: int = Query(12, ge=1, le=60)):
    """Get list of available pay periods (last N months)"""
    try:
        return get_transaction_service().get_available_pay_periods(months_back=months)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/transactions", response_model=dict)
async def create_transaction(transaction: TransactionCreate):
    """Create new transaction"""
    try:
        transaction_id = get_transaction_service().create_transaction(transaction)
        return {"id": transaction_id, "message": "Transaction created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/transactions/{transaction_id}")
async def update_transaction(transaction_id: str, transaction: TransactionUpdate):
    """Update transaction"""
    try:
        success = get_transaction_service().update_transaction(transaction_id, transaction)
        if not success:
            raise HTTPException(status_code=404, detail="Transaction not found or update failed")
        return {"message": "Transaction updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/transactions/{transaction_id}")
async def delete_transaction(transaction_id: str):
    """Delete transaction"""
    try:
        success = get_transaction_service().delete_transaction(transaction_id)
        if not success:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return {"message": "Transaction deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Stats Endpoints
# ============================================================================

@app.get("/api/stats/summary")
async def get_summary(
    start: str = Query(..., description="Start date (ISO format)"),
    end: str = Query(..., description="End date (ISO format)"),
):
    """Get summary statistics for date range"""
    try:
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)
        return get_stats_service().get_summary(start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/category-breakdown")
async def get_category_breakdown(
    start: str = Query(..., description="Start date (ISO format)"),
    end: str = Query(..., description="End date (ISO format)"),
):
    """Get spending breakdown by category"""
    try:
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)
        return get_stats_service().get_category_breakdown(start_date, end_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/spending-trend")
async def get_spending_trend(
    start: str = Query(..., description="Start date (ISO format)"),
    end: str = Query(..., description="End date (ISO format)"),
    granularity: str = Query("daily", pattern="^(daily|weekly|monthly)$"),
):
    """Get spending trend over time"""
    try:
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)
        return get_stats_service().get_spending_trend(start_date, end_date, granularity=granularity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/categories")
async def get_categories():
    """Get list of all categories"""
    try:
        return get_transaction_service().get_categories()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/recurring", response_model=List[TransactionResponse])
async def get_recurring_transactions():
    """Get all transactions marked as recurring"""
    try:
        return get_transaction_service().get_recurring_transactions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Startup & Shutdown
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection on startup"""
    print("[STARTUP] Starting Finance Tracker API...")
    if mongo_connection.connect():
        print("[OK] API ready")
    else:
        print("[ERROR] Failed to connect to MongoDB - API will have limited functionality")


@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    mongo_connection.close()


if __name__ == "__main__":
    import uvicorn
    import os
    
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 5000))
    
    uvicorn.run(app, host=host, port=port)
