from pymongo import MongoClient
from config.config import MONGODB_URI, DB_NAME
from datetime import datetime
import bcrypt

# Lazy-load MongoDB connection
client = None
db = None
chat_collection = None

def get_db():
    """Get database connection, creating it if necessary"""
    global client, db, chat_collection
    if db is None:
        try:
            client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            db = client[DB_NAME]
            chat_collection = db["chat_history"]
            # Verify connection
            client.admin.command('ping')
            db.users.create_index("username", unique=True)
        except Exception as e:
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")
    return db

# User authentication
def create_user(username, password):
    try:
        database = get_db()
        if database.users.find_one({"username": username}):
            raise ValueError("Username already exists.")
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        database.users.insert_one({
            "username": username,
            "password": hashed_password,
            "created_at": datetime.now().strftime("%Y-%m-%d")
        })
    except Exception as e:
        raise Exception(f"Error creating user: {str(e)}")

def verify_user(username, password):
    try:
        database = get_db()
        user = database.users.find_one({"username": username})
        if not user:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user["password"])
    except Exception as e:
        raise Exception(f"Error verifying user: {str(e)}")

# Store and get exam results
def store_result(username, topic, marks, mistakes, difficulty="medium", time_spent=0, mode="exam"):
    try:
        database = get_db()
        if not database.users.find_one({"username": username}):
            raise Exception("User does not exist.")
        database.results.insert_one({
            "username": username,
            "topic": topic,
            "marks": marks,
            "mistakes": mistakes,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "difficulty": difficulty,
            "time_spent": time_spent,  # in seconds
            "mode": mode  # 'exam' or 'practice'
        })
    except Exception as e:
        raise Exception(f"Error storing result: {str(e)}")

def get_user_results(username, filters=None):
    """Get user results with optional filtering
    
    Args:
        username: User's username
        filters: Dict with optional keys: topic, difficulty, mode, date_from, date_to
    """
    try:
        database = get_db()
        if not database.users.find_one({"username": username}):
            raise Exception("User does not exist.")
        
        query = {"username": username}
        
        # Apply filters if provided
        if filters:
            if 'topic' in filters and filters['topic']:
                query['topic'] = filters['topic']
            if 'difficulty' in filters and filters['difficulty']:
                query['difficulty'] = filters['difficulty']
            if 'mode' in filters and filters['mode']:
                query['mode'] = filters['mode']
            if 'date_from' in filters and filters['date_from']:
                query['timestamp'] = {"$gte": filters['date_from']}
            if 'date_to' in filters and filters['date_to']:
                if 'timestamp' in query:
                    query['timestamp']["$lte"] = filters['date_to']
                else:
                    query['timestamp'] = {"$lte": filters['date_to']}
        
        # Sort by _id in descending order to get newest results first (based on insertion time)
        return list(database.results.find(query).sort("_id", -1))
    except Exception as e:
        raise Exception(f"Error fetching results: {str(e)}")

def get_user_topics(username):
    """Get all topics for a user"""
    try:
        database = get_db()
        results = database.results.find({"username": username})
        topics = set(result.get('topic', 'Unknown') for result in results)
        return sorted(list(topics))
    except Exception as e:
        raise Exception(f"Error fetching topics: {str(e)}")

# Chat History
def save_chat(username, user_msg, ai_msg):
    try:
        database = get_db()
        database["chat_history"].insert_one({
            "username": username,
            "user_msg": user_msg,
            "ai_msg": ai_msg,
            "timestamp": datetime.utcnow()
        })
    except Exception as e:
        raise Exception(f"Error saving chat: {str(e)}")

def get_chat_history(username):
    try:
        database = get_db()
        return list(database["chat_history"].find({"username": username}).sort("timestamp", -1).limit(10))
    except Exception as e:
        raise Exception(f"Error fetching chat history: {str(e)}")

def clear_chat_history(username):
    try:
        database = get_db()
        database["chat_history"].delete_many({"username": username})
    except Exception as e:
        raise Exception(f"Error clearing chat history: {str(e)}")
