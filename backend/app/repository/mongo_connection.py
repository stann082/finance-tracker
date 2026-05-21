import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "financial_data")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "transactions")


class MongoDBConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
            cls._instance._connected = False
        return cls._instance
    
    def connect(self):
        """Establish MongoDB connection"""
        if self._connected:
            return True
            
        try:
            self.client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            # Verify connection
            self.client.server_info()
            self.db = self.client[DATABASE_NAME]
            self._connected = True
            print(f"✓ Connected to MongoDB: {DATABASE_NAME}")
            return True
        except (ServerSelectionTimeoutError, Exception) as e:
            print(f"⚠ Warning: MongoDB connection failed: {e}")
            print(f"  URI: {MONGODB_URI}")
            print(f"  API will start but database operations will fail until MongoDB is available")
            # Don't fail - allow app to start
            return False
    
    def get_db(self):
        """Get database instance"""
        if self.db is None:
            self.connect()
        return self.db
    
    def get_collection(self, collection_name: str = None):
        """Get collection instance"""
        if collection_name is None:
            collection_name = COLLECTION_NAME
        db = self.get_db()
        return db[collection_name]
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")


# Global connection instance
mongo_connection = MongoDBConnection()
