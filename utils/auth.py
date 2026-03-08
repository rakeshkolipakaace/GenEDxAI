import bcrypt
from datetime import datetime
from pymongo import MongoClient
from config.config import MONGODB_URI, DB_NAME
from utils.security import (
    validate_password_strength,
    validate_username,
    sanitize_input,
    log_login_attempt,
    check_rate_limit,
    reset_login_attempts,
    audit_log
)

# Lazy-load MongoDB connection to avoid blocking on import
client = None
db = None

def get_db():
    """Get database connection, creating it if necessary"""
    global client, db
    if db is None:
        try:
            client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            db = client[DB_NAME]
            # Verify connection
            client.admin.command('ping')
        except Exception as e:
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")
    return db

def register_user(username, password):
    """
    Register a new user with comprehensive security validation.
    
    Raises:
        ValueError: If input validation fails or user already exists
    """
    database = get_db()
    
    # Validate username format
    is_valid_username, username_msg = validate_username(username)
    if not is_valid_username:
        raise ValueError(username_msg)
    
    # Sanitize username
    username = sanitize_input(username, max_length=20)
    
    # Validate password strength
    is_valid_password, password_msg = validate_password_strength(password)
    if not is_valid_password:
        raise ValueError(password_msg)
    
    # Check if user already exists
    if database.users.find_one({"username": username}):
        raise ValueError("Username already exists.")
    
    # Hash password with bcrypt
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Create user with additional security metadata
    database.users.insert_one({
        "username": username,
        "password": hashed_pw,
        "created_at": datetime.now().isoformat(),
        "last_login": None,
        "login_count": 0,
        "failed_attempts": 0,
        "locked_until": None
    })
    
    # Log audit entry
    audit_log(username, "user_registration", status="success")

def login_user(username, password):
    """
    Authenticate user with rate limiting and audit logging.
    
    Returns:
        bool: True if authentication successful, False otherwise
    """
    database = get_db()
    
    # Sanitize username
    username = sanitize_input(username, max_length=20)
    
    # Check rate limiting and account lockout
    is_allowed, rate_limit_msg = check_rate_limit(username)
    if not is_allowed:
        audit_log(username, "login_attempt", {"status": rate_limit_msg}, status="failure")
        raise ValueError(rate_limit_msg)
    
    # Attempt authentication
    user = database.users.find_one({"username": username})
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        # Successful login
        reset_login_attempts(username)
        
        # Update user metadata
        database.users.update_one(
            {"username": username},
            {
                "$set": {"last_login": datetime.now().isoformat()},
                "$inc": {"login_count": 1}
            }
        )
        
        # Log successful login
        log_login_attempt(username, success=True)
        audit_log(username, "user_login", status="success")
        
        return True
    else:
        # Failed login
        log_login_attempt(username, success=False)
        audit_log(username, "user_login", status="failure")
        
        return False
