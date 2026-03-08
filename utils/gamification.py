"""Gamification module for GenEDxAI - Streaks, XP, Badges, and Leaderboard"""

from datetime import datetime, timedelta
from pymongo import MongoClient
from config.config import MONGODB_URI, DB_NAME

# MongoDB client
gama_db = None

def get_gama_db():
    """Get gamification database connection"""
    global gama_db
    if gama_db is None:
        try:
            client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            gama_db = client[DB_NAME]
            client.admin.command('ping')
            # Create indexes
            gama_db.gamification.create_index("username")
            gama_db.achievements.create_index("username")
        except Exception as e:
            raise Exception(f"Failed to connect to gamification database: {str(e)}")
    return gama_db


# ========================
# STREAK & XP SYSTEM
# ========================

def initialize_gamification(username: str):
    """Initialize gamification data for new user"""
    try:
        db = get_gama_db()
        existing = db.gamification.find_one({"username": username})
        if not existing:
            db.gamification.insert_one({
                "username": username,
                "streak": 0,
                "max_streak": 0,
                "xp": 0,
                "total_xp": 0,
                "level": 1,
                "last_exam_date": None,
                "created_at": datetime.now().isoformat()
            })
    except Exception as e:
        print(f"Error initializing gamification: {str(e)}")


def update_streak(username: str) -> dict:
    """Update user's daily streak"""
    try:
        db = get_gama_db()
        user_gama = db.gamification.find_one({"username": username})
        
        if not user_gama:
            initialize_gamification(username)
            user_gama = db.gamification.find_one({"username": username})
        
        today = datetime.now().strftime("%Y-%m-%d")
        last_exam = user_gama.get('last_exam_date', None)
        
        if last_exam == today:
            # Already counted today
            return user_gama
        
        # Check if streak should continue or reset
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        if last_exam == yesterday:
            # Continue streak
            new_streak = user_gama.get('streak', 0) + 1
        elif last_exam is None:
            # First exam
            new_streak = 1
        else:
            # Streak broken, reset to 1
            new_streak = 1
        
        # Update max streak if new streak is higher
        max_streak = max(new_streak, user_gama.get('max_streak', 0))
        
        # Update database
        db.gamification.update_one(
            {"username": username},
            {
                "$set": {
                    "streak": new_streak,
                    "max_streak": max_streak,
                    "last_exam_date": today
                }
            }
        )
        
        return db.gamification.find_one({"username": username})
    
    except Exception as e:
        print(f"Error updating streak: {str(e)}")
        return {}


def add_xp(username: str, points: int, reason: str = "exam_completion"):
    """Add XP to user account"""
    try:
        db = get_gama_db()
        user_gama = db.gamification.find_one({"username": username})
        
        if not user_gama:
            initialize_gamification(username)
            user_gama = db.gamification.find_one({"username": username})
        
        current_xp = user_gama.get('xp', 0)
        total_xp = user_gama.get('total_xp', 0)
        current_level = user_gama.get('level', 1)
        
        # XP to level up: 100 XP per level
        xp_needed_for_level = 100 * current_level
        new_xp = current_xp + points
        new_total_xp = total_xp + points
        new_level = current_level
        
        # Check for level up
        while new_xp >= xp_needed_for_level:
            new_xp -= xp_needed_for_level
            new_level += 1
            xp_needed_for_level = 100 * new_level
        
        # Update database
        db.gamification.update_one(
            {"username": username},
            {
                "$set": {
                    "xp": new_xp,
                    "total_xp": new_total_xp,
                    "level": new_level
                }
            }
        )
        
        return {
            "points_added": points,
            "new_xp": new_xp,
            "level_up": new_level > current_level,
            "new_level": new_level
        }
    
    except Exception as e:
        print(f"Error adding XP: {str(e)}")
        return {}


def calculate_xp_reward(marks: int, difficulty: str = "medium") -> int:
    """Calculate XP reward based on score and difficulty"""
    base_xp = marks * 10
    
    difficulty_multiplier = {
        "easy": 0.5,
        "medium": 1.0,
        "hard": 1.5
    }
    
    multiplier = difficulty_multiplier.get(difficulty, 1.0)
    return int(base_xp * multiplier)


def get_user_gamification(username: str) -> dict:
    """Get user's gamification stats"""
    try:
        db = get_gama_db()
        user_gama = db.gamification.find_one({"username": username})
        if not user_gama:
            initialize_gamification(username)
            user_gama = db.gamification.find_one({"username": username})
        return user_gama
    except Exception as e:
        print(f"Error fetching gamification: {str(e)}")
        return {}


# ========================
# ACHIEVEMENT SYSTEM
# ========================

ACHIEVEMENTS = {
    "first_exam": {
        "name": "First Step",
        "description": "Complete your first exam",
        "icon": "🎯",
        "xp_reward": 50
    },
    "perfect_score": {
        "name": "Perfect!",
        "description": "Score 5/5 on any exam",
        "icon": "🌟",
        "xp_reward": 200
    },
    "week_warrior": {
        "name": "Week Warrior",
        "description": "Maintain a 7-day streak",
        "icon": "🔥",
        "xp_reward": 300
    },
    "month_master": {
        "name": "Month Master",
        "description": "Maintain a 30-day streak",
        "icon": "👑",
        "xp_reward": 500
    },
    "ten_exams": {
        "name": "Dedicated Learner",
        "description": "Complete 10 exams",
        "icon": "📚",
        "xp_reward": 150
    },
    "hundred_exams": {
        "name": "Knowledge Seeker",
        "description": "Complete 100 exams",
        "icon": "🧠",
        "xp_reward": 1000
    },
    "high_scorer": {
        "name": "High Achiever",
        "description": "Get 90%+ average score across 5 exams",
        "icon": "🏆",
        "xp_reward": 250
    }
}


def unlock_achievement(username: str, achievement_key: str) -> bool:
    """Unlock an achievement for user"""
    try:
        db = get_gama_db()
        
        # Check if already unlocked
        existing = db.achievements.find_one({
            "username": username,
            "key": achievement_key
        })
        
        if existing:
            return False  # Already unlocked
        
        if achievement_key not in ACHIEVEMENTS:
            return False
        
        achievement = ACHIEVEMENTS[achievement_key]
        
        # Insert achievement
        db.achievements.insert_one({
            "username": username,
            "key": achievement_key,
            "name": achievement["name"],
            "description": achievement["description"],
            "icon": achievement["icon"],
            "unlocked_at": datetime.now().isoformat()
        })
        
        # Add XP reward
        add_xp(username, achievement["xp_reward"], f"achievement_unlock:{achievement_key}")
        
        return True
    
    except Exception as e:
        print(f"Error unlocking achievement: {str(e)}")
        return False


def get_user_achievements(username: str) -> list:
    """Get all achievements unlocked by user"""
    try:
        db = get_gama_db()
        achievements = list(db.achievements.find({"username": username}).sort("unlocked_at", -1))
        return achievements
    except Exception as e:
        print(f"Error fetching achievements: {str(e)}")
        return []


def check_achievements(username: str, results_count: int, avg_score: float, streak: int, marks: int):
    """Check and unlock achievements based on conditions"""
    try:
        # First exam
        if results_count == 1:
            unlock_achievement(username, "first_exam")
        
        # Perfect score
        if marks == 5:
            unlock_achievement(username, "perfect_score")
        
        # 7-day streak
        if streak >= 7:
            unlock_achievement(username, "week_warrior")
        
        # 30-day streak
        if streak >= 30:
            unlock_achievement(username, "month_master")
        
        # 10 exams
        if results_count == 10:
            unlock_achievement(username, "ten_exams")
        
        # 100 exams
        if results_count == 100:
            unlock_achievement(username, "hundred_exams")
        
        # High scorer (90%+ average across 5+ exams)
        if results_count >= 5 and avg_score >= 90:
            unlock_achievement(username, "high_scorer")
    
    except Exception as e:
        print(f"Error checking achievements: {str(e)}")


# ========================
# LEADERBOARD
# ========================

def get_leaderboard(limit: int = 10, timeframe: str = "week") -> list:
    """Get top performers leaderboard
    
    Args:
        limit: Number of users to return
        timeframe: 'week' or 'month'
    """
    try:
        db = get_gama_db()
        
        # Calculate date cutoff
        if timeframe == "week":
            days = 7
        else:  # month
            days = 30
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        # Get leaderboard based on XP gained in timeframe
        pipeline = [
            {
                "$addFields": {
                    "recent_xp": {
                        "$cond": [
                            {"$gte": ["$created_at", cutoff_date]},
                            "$total_xp",
                            0
                        ]
                    }
                }
            },
            {"$sort": {"total_xp": -1}},
            {"$limit": limit}
        ]
        
        leaderboard = list(db.gamification.aggregate(pipeline))
        return leaderboard
    
    except Exception as e:
        print(f"Error fetching leaderboard: {str(e)}")
        return []


# ========================
# ANALYTICS
# ========================

def get_performance_metrics(username: str) -> dict:
    """Get user's performance metrics"""
    try:
        from utils.db import get_db
        db = get_db()
        
        results = list(db.results.find({"username": username}))
        
        if not results:
            return {
                "total_exams": 0,
                "average_score": 0,
                "highest_score": 0,
                "lowest_score": 0,
                "success_rate": 0,
                "improvement_rate": 0
            }
        
        marks_list = [r.get('marks', 0) for r in results]
        total_exams = len(results)
        average_score = sum(marks_list) / total_exams
        highest_score = max(marks_list)
        lowest_score = min(marks_list)
        success_rate = (sum(1 for m in marks_list if m >= 3) / total_exams) * 100
        
        # Improvement rate: compare first 5 exams to last 5
        improvement_rate = 0
        if total_exams >= 5:
            first_five_avg = sum(marks_list[:5]) / 5
            last_five_avg = sum(marks_list[-5:]) / 5
            improvement_rate = ((last_five_avg - first_five_avg) / first_five_avg) * 100 if first_five_avg > 0 else 0
        
        return {
            "total_exams": total_exams,
            "average_score": round(average_score, 2),
            "highest_score": highest_score,
            "lowest_score": lowest_score,
            "success_rate": round(success_rate, 1),
            "improvement_rate": round(improvement_rate, 1),
            "marks_list": marks_list
        }
    
    except Exception as e:
        print(f"Error calculating performance metrics: {str(e)}")
        return {}


def get_weak_areas(username: str) -> dict:
    """Identify topics where user scores lowest"""
    try:
        from utils.db import get_db
        db = get_db()
        
        results = list(db.results.find({"username": username}))
        
        if not results:
            return {}
        
        # Group by topic and calculate average score
        topic_scores = {}
        for result in results:
            topic = result.get('topic', 'Unknown')
            marks = result.get('marks', 0)
            
            if topic not in topic_scores:
                topic_scores[topic] = []
            topic_scores[topic].append(marks)
        
        # Calculate averages
        weak_areas = {}
        for topic, scores in topic_scores.items():
            avg_score = sum(scores) / len(scores)
            weak_areas[topic] = {
                "average": round(avg_score, 2),
                "attempts": len(scores),
                "highest": max(scores),
                "lowest": min(scores)
            }
        
        # Sort by average score (lowest first)
        sorted_weak_areas = dict(sorted(weak_areas.items(), key=lambda x: x[1]['average']))
        
        return sorted_weak_areas
    
    except Exception as e:
        print(f"Error analyzing weak areas: {str(e)}")
        return {}
