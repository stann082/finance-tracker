from datetime import datetime
from typing import List, Optional, Dict
from app.repository.transaction_repository import TransactionRepository
from app.util.pay_period import PayPeriodTransactionsProvider
from app.models.transaction import TransactionResponse, TransactionCreate, TransactionUpdate, TransactionType


class TransactionService:
    """Business logic for transactions"""
    
    def __init__(self):
        self.repository = TransactionRepository()
    
    def get_all_transactions(self, limit: int = 1000, skip: int = 0) -> List[TransactionResponse]:
        """Get all transactions"""
        transactions = self.repository.get_all(limit=limit, skip=skip)
        return [self._to_response(t) for t in transactions]
    
    def get_transaction(self, transaction_id: str) -> Optional[TransactionResponse]:
        """Get single transaction"""
        transaction = self.repository.get_by_id(transaction_id)
        return self._to_response(transaction) if transaction else None
    
    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: int = 1000,
        skip: int = 0,
    ) -> List[TransactionResponse]:
        """Get transactions in date range"""
        transactions = self.repository.get_by_date_range(
            start_date, end_date, limit=limit, skip=skip
        )
        return [self._to_response(t) for t in transactions]
    
    def search_transactions(
        self,
        query: str,
        limit: int = 100,
        skip: int = 0,
    ) -> List[TransactionResponse]:
        """Search transactions by description/category"""
        transactions = self.repository.search(query, limit=limit, skip=skip)
        return [self._to_response(t) for t in transactions]
    
    def get_by_pay_period(self, month_year: str) -> List[TransactionResponse]:
        """Get transactions for given pay period (month)"""
        all_transactions = self.repository.get_all(limit=10000)
        period_transactions = PayPeriodTransactionsProvider.get_pay_period_transactions(
            all_transactions, month_year
        )
        return [self._to_response(t) for t in period_transactions]
    
    def get_available_pay_periods(self, months_back: int = 12) -> List[str]:
        """Get list of available pay periods"""
        all_transactions = self.repository.get_all(limit=10000)
        return PayPeriodTransactionsProvider.get_available_pay_periods(all_transactions, months_back)
    
    def get_recurring_transactions(self) -> List[TransactionResponse]:
        """Get all transactions marked as recurring"""
        transactions = self.repository.get_recurring()
        return [self._to_response(t) for t in transactions]
    
    def create_transaction(self, transaction_data: TransactionCreate) -> str:
        """Create new transaction"""
        data = transaction_data.model_dump()
        return self.repository.create(data)
    
    def update_transaction(
        self,
        transaction_id: str,
        update_data: TransactionUpdate,
    ) -> bool:
        """Update transaction"""
        data = update_data.model_dump(exclude_unset=True)
        return self.repository.update(transaction_id, data)
    
    def delete_transaction(self, transaction_id: str) -> bool:
        """Delete transaction"""
        return self.repository.delete(transaction_id)
    
    def get_categories(self) -> List[str]:
        """Get list of unique categories"""
        return self.repository.get_categories()
    
    @staticmethod
    def _to_response(transaction: dict) -> TransactionResponse:
        """Convert MongoDB document to TransactionResponse"""
        if not transaction:
            return None

        amount = float(transaction.get('Amount', transaction.get('amount', 0)) or 0)
        balance = float(transaction.get('Balance', transaction.get('balance', 0)) or 0)
        is_deposit = amount >= 0
        tx_type = TransactionType.CREDIT if is_deposit else TransactionType.DEBIT

        return TransactionResponse(
            id=str(transaction.get('_id', '')),
            amount=amount,
            balance=balance,
            category=transaction.get('Category', transaction.get('category')),
            date=transaction.get('Date', transaction.get('date', datetime.now())),
            description=transaction.get('Description', transaction.get('description')),
            is_deposit=is_deposit,
            is_recurring=transaction.get('IsRecurring', transaction.get('is_recurring', False)),
            transaction_id=transaction.get('TransactionId', transaction.get('transaction_id')),
            type=tx_type,
        )
