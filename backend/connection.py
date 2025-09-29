from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from os import environ
import logging

logger = logging.getLogger(__name__)

MONGO_URL = environ.get('MONGO_URL', 'mongodb://localhost:27017/gehenna')

# Global client variable
client = None

def get_mongo_client():
    """Get MongoDB client with error handling"""
    global client
    if client is None:
        try:
            client = MongoClient(
                MONGO_URL,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            # Test the connection
            client.admin.command('ping')
            logger.info("MongoDB connection established")
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"MongoDB connection failed: {str(e)}")
            client = None
            return None
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {str(e)}")
            client = None
            return None
    return client

def get_collection():
    """Get the names collection with error handling"""
    try:
        mongo_client = get_mongo_client()
        if mongo_client is None:
            return None
        
        db = mongo_client['gehenna']
        return db['names']
    except Exception as e:
        logger.error(f"Error getting collection: {str(e)}")
        return None
