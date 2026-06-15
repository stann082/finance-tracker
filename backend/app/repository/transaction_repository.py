from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId
from pymongo.collection import Collection

from app.repository.mongo_connection import mongo_connection, COLLECTION_NAME


class TransactionRepository:
    """MongoDB repository for Transaction operations"""
    
    def __init__(self):
        # Don't connect immediately - let it be lazy
        self.collection = None
    
    def _get_collection(self):
        """Get collection, connecting if needed"""
        if self.collection is None:
            self.collection = mongo_connection.get_collection(COLLECTION_NAME)
        return self.collection
    
    def get_all(self, limit: int = 1000, skip: int = 0) -> List[Dict]:
        """Get all transactions with pagination"""
        try:
            collection = self._get_collection()
            return list(
                collection.find({})
                .sort("Date", -1)
                .skip(skip)
                .limit(limit)
            )
        except Exception as e:
            print(f"Error in get_all: {e}")
            return []
    
    def get_by_id(self, transaction_id: str) -> Optional[Dict]:
        """Get transaction by MongoDB ObjectId"""
        try:
            return self._get_collection().find_one({"_id": ObjectId(transaction_id)})
        except Exception:
            return None
    
    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: int = 1000,
        skip: int = 0,
    ) -> List[Dict]:
        """Get transactions within date range"""
        try:
            query = {
                "Date": {"$gte": start_date, "$lt": end_date}
            }
            return list(
                self._get_collection().find(query)
                .sort("Date", -1)
                .skip(skip)
                .limit(limit)
            )
        except Exception as e:
            print(f"Error in get_by_date_range: {e}")
            return []
    
    def search(
        self,
        query: str,
        limit: int = 100,
        skip: int = 0,
    ) -> List[Dict]:
        """Search transactions by description or category"""
        try:
            search_query = {
                "$or": [
                    {"Description": {"$regex": query, "$options": "i"}},
                    {"Category": {"$regex": query, "$options": "i"}},
                ]
            }
            return list(
                self._get_collection().find(search_query)
                .sort("Date", -1)
                .skip(skip)
                .limit(limit)
            )
        except Exception as e:
            print(f"Error in search: {e}")
            return []
    
    def get_by_category(
        self,
        category: str,
        limit: int = 1000,
        skip: int = 0,
    ) -> List[Dict]:
        """Get transactions by category"""
        try:
            query = {"Category": category}
            return list(
                self._get_collection().find(query)
                .sort("Date", -1)
                .skip(skip)
                .limit(limit)
            )
        except Exception as e:
            print(f"Error in get_by_category: {e}")
            return []
    
    def get_recurring(self) -> List[Dict]:
        """Get all transactions marked as recurring"""
        try:
            query = {"IsRecurring": True}
            return list(
                self._get_collection().find(query)
                .sort("Date", -1)
            )
        except Exception as e:
            print(f"Error in get_recurring: {e}")
            return []
    
    def create(self, transaction_data: Dict) -> str:
        """Create new transaction, return ObjectId as string"""
        try:
            result = self._get_collection().insert_one(transaction_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error in create: {e}")
            return ""
    
    def update(self, transaction_id: str, update_data: Dict) -> bool:
        """Update transaction, return True if successful"""
        try:
            result = self._get_collection().update_one(
                {"_id": ObjectId(transaction_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error in update: {e}")
            return False
    
    def delete(self, transaction_id: str) -> bool:
        """Delete transaction, return True if successful"""
        try:
            result = self._get_collection().delete_one({"_id": ObjectId(transaction_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error in delete: {e}")
            return False
    
    def get_categories(self) -> List[str]:
        """Get list of unique categories"""
        try:
            return self._get_collection().distinct("Category")
        except Exception as e:
            print(f"Error in get_categories: {e}")
            return []
    
    def get_count(self) -> int:
        """Get total transaction count"""
        try:
            return self._get_collection().count_documents({})
        except Exception:
            return 0
    
    def get_count_by_date_range(self, start_date: datetime, end_date: datetime) -> int:
        """Get transaction count in date range"""
        try:
            query = {
                "date": {"$gte": start_date, "$lt": end_date}
            }
            return self._get_collection().count_documents(query)
        except Exception:
            return 0
    
    def check_duplicate(self, amount: float, date: datetime, description: str) -> Optional[Dict]:
        """
        Check if transaction already exists (deduplication).
        
        Matches on: amount, date (same day), and description similarity
        """
        try:
            query = {
                "amount": amount,
                "date": {
                    "$gte": date.replace(hour=0, minute=0, second=0),
                    "$lt": date.replace(hour=23, minute=59, second=59)
                },
                "description": {"$regex": description[:20], "$options": "i"}  # First 20 chars
            }
            return self._get_collection().find_one(query)
        except Exception as e:
            print(f"Error in check_duplicate: {e}")
            return None
