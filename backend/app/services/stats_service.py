from datetime import datetime
from typing import Dict, List
from app.repository.transaction_repository import TransactionRepository


class StatsService:
    """Business logic for statistics and aggregations"""
    
    def __init__(self):
        self.repository = TransactionRepository()
    
    def get_category_breakdown(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, float]:
        """
        Get spending by category for date range.
        
        Returns: {category: total_spent}
        """
        transactions = self.repository.get_by_date_range(start_date, end_date, limit=10000)
        
        breakdown = {}
        for txn in transactions:
            category = txn.get('category') or 'Uncategorized'
            amount = txn.get('amount', 0)
            
            # Only count expenses (negative amounts)
            if amount < 0:
                breakdown[category] = breakdown.get(category, 0) + abs(amount)
        
        return breakdown
    
    def get_spending_trend(
        self,
        start_date: datetime,
        end_date: datetime,
        granularity: str = "daily",  # daily, weekly, monthly
    ) -> List[Dict]:
        """
        Get spending trend over time.
        
        Returns: [{"date": "2024-09-01", "total": 150.00}, ...]
        """
        transactions = self.repository.get_by_date_range(start_date, end_date, limit=10000)
        
        if granularity == "daily":
            return self._aggregate_by_day(transactions)
        elif granularity == "weekly":
            return self._aggregate_by_week(transactions)
        elif granularity == "monthly":
            return self._aggregate_by_month(transactions)
        else:
            return self._aggregate_by_day(transactions)
    
    def get_summary(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict:
        """
        Get summary statistics for date range.
        
        Returns:
        {
            "total_spent": 1500.00,
            "total_income": 2000.00,
            "net": 500.00,
            "avg_transaction": 75.50,
            "transaction_count": 20,
            "category_count": 5,
        }
        """
        transactions = self.repository.get_by_date_range(start_date, end_date, limit=10000)
        
        total_spent = 0.0
        total_income = 0.0
        
        for txn in transactions:
            amount = txn.get('amount', 0)
            if amount < 0:
                total_spent += abs(amount)
            else:
                total_income += amount
        
        avg_transaction = 0.0
        if transactions:
            total_abs = sum(abs(t.get('amount', 0)) for t in transactions)
            avg_transaction = total_abs / len(transactions)
        
        categories = set(t.get('category') for t in transactions if t.get('category'))
        
        return {
            "total_spent": round(total_spent, 2),
            "total_income": round(total_income, 2),
            "net": round(total_income - total_spent, 2),
            "avg_transaction": round(avg_transaction, 2),
            "transaction_count": len(transactions),
            "category_count": len(categories),
        }
    
    @staticmethod
    def _aggregate_by_day(transactions: List[dict]) -> List[Dict]:
        """Aggregate spending by day"""
        daily = {}
        
        for txn in transactions:
            date_obj = txn.get('date')
            if not isinstance(date_obj, datetime):
                continue
            
            date_str = date_obj.strftime("%Y-%m-%d")
            amount = txn.get('amount', 0)
            
            # Only count expenses
            if amount < 0:
                daily[date_str] = daily.get(date_str, 0) + abs(amount)
        
        # Convert to sorted list
        result = [
            {"date": date, "total": round(amount, 2)}
            for date, amount in sorted(daily.items())
        ]
        return result
    
    @staticmethod
    def _aggregate_by_week(transactions: List[dict]) -> List[Dict]:
        """Aggregate spending by week"""
        weekly = {}
        
        for txn in transactions:
            date_obj = txn.get('date')
            if not isinstance(date_obj, datetime):
                continue
            
            # ISO week
            week_str = date_obj.strftime("%Y-W%V")
            amount = txn.get('amount', 0)
            
            if amount < 0:
                weekly[week_str] = weekly.get(week_str, 0) + abs(amount)
        
        result = [
            {"date": week, "total": round(amount, 2)}
            for week, amount in sorted(weekly.items())
        ]
        return result
    
    @staticmethod
    def _aggregate_by_month(transactions: List[dict]) -> List[Dict]:
        """Aggregate spending by month"""
        monthly = {}
        
        for txn in transactions:
            date_obj = txn.get('date')
            if not isinstance(date_obj, datetime):
                continue
            
            month_str = date_obj.strftime("%Y-%m")
            amount = txn.get('amount', 0)
            
            if amount < 0:
                monthly[month_str] = monthly.get(month_str, 0) + abs(amount)
        
        result = [
            {"date": month, "total": round(amount, 2)}
            for month, amount in sorted(monthly.items())
        ]
        return result
