"""Security module for GenEDxAI - Comprehensive security features"""

import re
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Tuple, Dict
import streamlit as st
from pymongo import MongoClient
from config.config import MONGODB_URI, DB_NAME

# MongoDB client for security logs
security_db = None

def get_security_db():
    """Get security database connection"""
    global security_db
    if security_db is None:
        try:
            client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            security_db = client[DB_NAME]
            client.admin.command('ping')
            # Create indexes for efficient querying
            security_db.login_attempts.create_index("username")
            security_db.audit_logs.create_index("username")
            security_db.audit_logs.create_index("timestamp")
            security_db.csrf_tokens.create_index("token_hash")
        except Exception as e:
            raise Exception(f"Failed to connect to security database: {str(e)}")
    return security_db


# ========================
# PASSWORD STRENGTH VALIDATION
# ========================

def validate_password_strength(password: str) -> Tuple[bool, str]:
    """
    Validate password strength requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character (!@#$%^&*)
    
    Returns: (is_valid, message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password):
        return False, "Password must contain at least one special character (!@#$%^&*)"
    
    return True, "Password strength is excellent"


# ========================
# INPUT VALIDATION & SANITIZATION
# ========================

def validate_username(username: str) -> Tuple[bool, str]:
    """
    Validate username format:
    - 3-20 characters
    - Alphanumeric and underscores only
    - No spaces
    
    Returns: (is_valid, message)
    """
    if not username or len(username) < 3 or len(username) > 20:
        return False, "Username must be 3-20 characters long"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, "Username is valid"


def sanitize_input(user_input: str, max_length: int = 500) -> str:
    """
    Sanitize user input by removing potential XSS/injection attacks
    """
    if not isinstance(user_input, str):
        return ""
    
    # Trim to max length
    user_input = user_input[:max_length]
    
    # Remove dangerous HTML/script tags
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'<iframe[^>]*>.*?</iframe>',
        r'<object[^>]*>.*?</object>',
        r'on\w+\s*=',  # Event handlers like onclick=
        r'javascript:',
    ]
    
    for pattern in dangerous_patterns:
        user_input = re.sub(pattern, '', user_input, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove any remaining HTML tags
    user_input = re.sub(r'<[^>]+>', '', user_input)
    
    return user_input.strip()


# ========================
# RATE LIMITING & ACCOUNT LOCKOUT
# ========================

MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15
ATTEMPT_RESET_HOURS = 24

def log_login_attempt(username: str, success: bool, ip_address: str = "unknown"):
    """Log login attempt for rate limiting and audit"""
    try:
        db = get_security_db()
        db.login_attempts.insert_one({
            "username": username,
            "success": success,
            "ip_address": ip_address,
            "timestamp": datetime.now()
        })
    except Exception as e:
        print(f"Error logging login attempt: {str(e)}")


def check_rate_limit(username: str) -> Tuple[bool, str]:
    """
    Check if user has exceeded login attempts.
    Returns: (is_allowed, message)
    """
    try:
        db = get_security_db()
        
        # Clean old attempts (older than ATTEMPT_RESET_HOURS)
        cutoff_time = datetime.now() - timedelta(hours=ATTEMPT_RESET_HOURS)
        db.login_attempts.delete_many({
            "username": username,
            "timestamp": {"$lt": cutoff_time}
        })
        
        # Get recent failed attempts
        recent_attempts = list(db.login_attempts.find({
            "username": username,
            "success": False,
            "timestamp": {"$gt": datetime.now() - timedelta(hours=ATTEMPT_RESET_HOURS)}
        }).sort("timestamp", -1).limit(MAX_LOGIN_ATTEMPTS + 1))
        
        failed_count = len(recent_attempts)
        
        if failed_count >= MAX_LOGIN_ATTEMPTS:
            # Check if account is locked (last attempt was recent)
            last_attempt = recent_attempts[0]
            lockout_expiry = last_attempt["timestamp"] + timedelta(minutes=LOCKOUT_DURATION_MINUTES)
            
            if datetime.now() < lockout_expiry:
                remaining_minutes = int((lockout_expiry - datetime.now()).total_seconds() / 60)
                return False, f"Account locked. Try again in {remaining_minutes} minutes."
            else:
                # Lockout period expired, allow login
                db.login_attempts.delete_many({"username": username})
                return True, "Account unlocked"
        
        return True, "Login allowed"
    
    except Exception as e:
        print(f"Error checking rate limit: {str(e)}")
        return True, "Login allowed"  # Allow on error


def reset_login_attempts(username: str):
    """Reset login attempts after successful login"""
    try:
        db = get_security_db()
        db.login_attempts.delete_many({"username": username})
    except Exception as e:
        print(f"Error resetting login attempts: {str(e)}")


# ========================
# AUDIT LOGGING
# ========================

def audit_log(username: str, action: str, details: Dict = None, status: str = "success"):
    """
    Log security-related actions for audit trail
    
    Args:
        username: Username performing the action
        action: Type of action (login, register, password_change, etc.)
        details: Additional details about the action
        status: success or failure
    """
    try:
        db = get_security_db()
        db.audit_logs.insert_one({
            "username": username,
            "action": action,
            "status": status,
            "details": details or {},
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d")
        })
    except Exception as e:
        print(f"Error logging audit: {str(e)}")


def get_audit_logs(username: str, limit: int = 100) -> list:
    """Get audit logs for a user"""
    try:
        db = get_security_db()
        return list(db.audit_logs.find(
            {"username": username}
        ).sort("timestamp", -1).limit(limit))
    except Exception as e:
        print(f"Error fetching audit logs: {str(e)}")
        return []


# ========================
# CSRF PROTECTION
# ========================

def generate_csrf_token() -> str:
    """Generate a secure CSRF token"""
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    
    try:
        db = get_security_db()
        db.csrf_tokens.insert_one({
            "token_hash": token_hash,
            "created_at": datetime.now(),
            "used": False
        })
        
        # Clean up old tokens (older than 1 hour)
        db.csrf_tokens.delete_many({
            "created_at": {"$lt": datetime.now() - timedelta(hours=1)}
        })
    except Exception as e:
        print(f"Error generating CSRF token: {str(e)}")
    
    return token


def verify_csrf_token(token: str) -> bool:
    """Verify CSRF token"""
    try:
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        db = get_security_db()
        
        result = db.csrf_tokens.find_one({
            "token_hash": token_hash,
            "used": False,
            "created_at": {"$gt": datetime.now() - timedelta(hours=1)}
        })
        
        if result:
            # Mark token as used
            db.csrf_tokens.update_one(
                {"token_hash": token_hash},
                {"$set": {"used": True}}
            )
            return True
        
        return False
    except Exception as e:
        print(f"Error verifying CSRF token: {str(e)}")
        return False


# ========================
# SESSION TIMEOUT
# ========================

SESSION_TIMEOUT_MINUTES = 30

def check_session_timeout():
    """Check if user session has timed out"""
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        if "last_activity" not in st.session_state:
            st.session_state["last_activity"] = datetime.now()
        
        elapsed = datetime.now() - st.session_state["last_activity"]
        
        if elapsed > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
            # Session expired
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.session_state["chat_history"] = []
            st.session_state["exam_active"] = False
            st.session_state["exam_questions"] = []
            st.session_state["user_answers"] = {}
            
            audit_log(st.session_state.get("username", "unknown"), "session_timeout", status="success")
            
            st.warning("⏰ Your session has timed out. Please login again.")
            st.stop()
        
        # Update last activity
        st.session_state["last_activity"] = datetime.now()


# ========================
# API KEY SECURITY
# ========================

def validate_api_key_configured() -> bool:
    """Validate that API keys are configured securely"""
    import os
    
    # Check if sensitive keys are in environment variables
    required_keys = {
        "OPENROUTER_API_KEY": "OpenRouter API Key",
        "MONGODB_URI": "MongoDB URI",
    }
    
    missing_keys = []
    for key, name in required_keys.items():
        if not os.getenv(key):
            missing_keys.append(name)
    
    return len(missing_keys) == 0, missing_keys


def mask_sensitive_data(data: str, show_chars: int = 4) -> str:
    """Mask sensitive data like API keys for logging"""
    if len(data) <= show_chars:
        return "*" * len(data)
    return data[:show_chars] + "*" * (len(data) - show_chars)


# ========================
# SECURITY HEADERS
# ========================

def get_secure_headers() -> str:
    """Generate secure HTTP headers as HTML meta tags"""
    return """
    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <meta name="referrer" content="strict-origin-when-cross-origin">
    <meta http-equiv="X-Content-Type-Options" content="nosniff">
    <meta http-equiv="X-Frame-Options" content="DENY">
    <meta http-equiv="X-XSS-Protection" content="1; mode=block">
    """
