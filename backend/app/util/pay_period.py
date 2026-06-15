"""
Pay Period Detection Logic - ported from .NET implementation

Detects pay periods based on paycheck marker transactions.
Marker: "TIMECLOCK PLUS L DES:" in transaction description
"""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from bson import ObjectId


class PayPeriodCalculator:
    """
    Detects pay period boundaries based on paycheck markers.
    
    Strategy:
    1. For a given month (e.g., September 2024)
    2. Find transactions in a 3-month window (Aug-Sep-Oct)
    3. Locate paycheck marker before month start
    4. Locate paycheck marker after month start
    5. Return transactions between these boundaries
    """
    
    PAYCHECK_MARKER = "TIMECLOCK PLUS L DES:"
    
    @staticmethod
    def find_pay_period_window(
        transactions: List[dict],
        target_month_start: datetime,
    ) -> Tuple[Optional[datetime], Optional[datetime]]:
        """
        Find pay period boundaries (start and end dates) for given month.
        
        Args:
            transactions: List of transaction dicts with 'date' and 'description'
            target_month_start: First day of target month
            
        Returns:
            Tuple of (pay_period_start_date, pay_period_end_date)
            or (None, None) if boundaries not found
        """
        # Find month boundaries
        if target_month_start.month == 12:
            next_month_start = target_month_start.replace(year=target_month_start.year + 1, month=1, day=1)
        else:
            next_month_start = target_month_start.replace(month=target_month_start.month + 1, day=1)
        
        # Find paychecks: last before month start and first in/after month start
        paycheck_before = None
        paycheck_after = None
        
        for txn in transactions:
            if PayPeriodCalculator._is_paycheck(txn):
                txn_date = txn.get('Date', txn.get('date'))
                
                # Paycheck BEFORE month start (last one before)
                if txn_date < target_month_start:
                    if paycheck_before is None or txn_date > paycheck_before:
                        paycheck_before = txn_date
                
                # Paycheck IN or AFTER month start (first one)
                if txn_date >= target_month_start:
                    if paycheck_after is None or txn_date < paycheck_after:
                        paycheck_after = txn_date
        
        return paycheck_before, paycheck_after
    
    @staticmethod
    def _is_paycheck(transaction: dict) -> bool:
        """Check if transaction is a paycheck marker"""
        description = transaction.get('Description', transaction.get('description', '')) or ''
        return PayPeriodCalculator.PAYCHECK_MARKER in description


class PayPeriodWindow:
    """
    Determines efficient search window for pay period queries.
    
    For a given month, queries transactions from:
    - Previous month (start)
    - Target month
    - Next month (start)
    
    This ensures we capture paycheck markers that define boundaries.
    """
    
    @staticmethod
    def get_window(target_date: datetime) -> Tuple[datetime, datetime]:
        """
        Get 3-month search window for pay period detection.
        
        For September 2024, returns (Aug 1, 2024) to (Oct 1, 2024)
        """
        # First day of previous month
        if target_date.month == 1:
            window_start = target_date.replace(year=target_date.year - 1, month=12, day=1)
        else:
            window_start = target_date.replace(month=target_date.month - 1, day=1)
        
        # First day of month after target
        if target_date.month == 12:
            window_end = target_date.replace(year=target_date.year + 1, month=1, day=1)
        else:
            window_end = target_date.replace(month=target_date.month + 1, day=1)
        
        return window_start, window_end


class PayPeriodTransactionsProvider:
    """
    Orchestrates fetching transactions for a given pay period.
    """
    
    @staticmethod
    def get_pay_period_transactions(
        all_transactions: List[dict],
        month_year: str,  # Format: "September2024"
    ) -> List[dict]:
        """
        Get all transactions for a given pay period (month).
        
        Args:
            all_transactions: List of all transactions
            month_year: Month identifier in format "September2024" (MMMMYyyy)
            
        Returns:
            List of transactions within pay period boundaries
        """
        try:
            # Parse month_year string
            target_date = datetime.strptime(month_year, "%B%Y")
        except ValueError:
            return []
        
        # Get search window
        window_start, window_end = PayPeriodWindow.get_window(target_date)
        
        # Filter transactions in window
        windowed_txns = [
            t for t in all_transactions
            if window_start <= (t.get('Date', t.get('date')) or datetime.min) < window_end
        ]
        
        # Find pay period boundaries
        period_start, period_end = PayPeriodCalculator.find_pay_period_window(
            windowed_txns,
            target_date
        )
        
        if period_start is None or period_end is None:
            return []
        
        # Filter to transactions within pay period
        result = [
            t for t in windowed_txns
            if period_start <= (t.get('Date', t.get('date')) or datetime.min) < period_end
        ]

        return sorted(result, key=lambda x: x.get('Date', x.get('date', datetime.min)))
    
    @staticmethod
    def get_available_pay_periods(all_transactions: List[dict], months_back: int = 12) -> List[str]:
        """
        Get list of available pay periods (last N months).
        
        Returns:
            List of month strings in format "September2024"
        """
        if not all_transactions:
            return []
        
        # Find date range in transactions
        dates = [t.get('Date', t.get('date')) for t in all_transactions if t.get('Date', t.get('date'))]
        if not dates:
            return []

        dates = sorted([d for d in dates if isinstance(d, datetime)])
        latest_date = dates[-1]
        
        # Generate last N months
        periods = []
        current = latest_date.replace(day=1)
        
        for _ in range(months_back):
            period_str = current.strftime("%B%Y")
            periods.append(period_str)
            
            # Go to previous month
            if current.month == 1:
                current = current.replace(year=current.year - 1, month=12)
            else:
                current = current.replace(month=current.month - 1)
        
        return periods
