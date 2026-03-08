#app.py

import streamlit as st
from streamlit_lottie import st_lottie
import requests
import google.generativeai as genai
from datetime import datetime, timedelta
import time
from utils.auth import login_user, register_user
from utils.chatbot import get_learning_response
from utils.exam import generate_exam, evaluate_exam
from utils.db import store_result, get_user_results, get_user_topics
from utils.db import save_chat, get_chat_history, clear_chat_history
from utils.security import (
    get_secure_headers,
    check_session_timeout,
    generate_csrf_token,
    verify_csrf_token,
    sanitize_input,
    audit_log,
    validate_password_strength
)
from utils.gamification import (
    initialize_gamification,
    update_streak,
    add_xp,
    calculate_xp_reward,
    get_user_gamification,
    unlock_achievement,
    get_user_achievements,
    check_achievements,
    get_leaderboard,
    get_performance_metrics,
    get_weak_areas
)

# from fpdf import FPDF
# import io

# Add security headers
st.markdown(get_secure_headers(), unsafe_allow_html=True)

hide_streamlit_elements = """
<style>
#GithubIcon { 
    visibility: hidden; 
}
.stDeployButton { 
    visibility: hidden; 
}
.viewerBadge_container__1QSob { 
    visibility: hidden; 
}
</style>
"""
st.markdown(hide_streamlit_elements, unsafe_allow_html=True)
# Load custom CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Helper to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["chat_history"] = []
    st.session_state["exam_active"] = False
    st.session_state["exam_questions"] = []
    st.session_state["user_answers"] = {}
    st.session_state["menu"] = "Login"
    st.session_state["last_activity"] = datetime.now()
    st.session_state["csrf_token"] = generate_csrf_token()

# Check session timeout (only if logged in)
if st.session_state["logged_in"]:
    check_session_timeout()

# Sidebar Navigation
st.sidebar.markdown('<h1 style="font-size:36px;">📘 EduBot</h1>', unsafe_allow_html=True)

if not st.session_state["logged_in"]:
    st.sidebar.markdown('<div style="font-size:28px;">🔐 Menu</div>', unsafe_allow_html=True)
    menu = st.sidebar.radio("", ["Login", "Register"], key="menu_radio")
else:
    # Display user profile and gamification stats
    gama = get_user_gamification(st.session_state["username"])
    
    # User profile card - Compact
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, #0f472f 0%, #1a1a1a 100%); padding: 12px; border-radius: 10px; border: 2px solid #1DB679; margin-bottom: 12px; text-align: center;">
        <div style="font-size: 32px; margin-bottom: 4px;">👤</div>
        <div style="font-size: 14px; font-weight: bold; color: #1DB679; margin-bottom: 2px;">{st.session_state['username']}</div>
        <div style="font-size: 11px; color: #888;">Level {gama.get('level', 1)} Learner</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate XP progress to next level
    xp_current = gama.get('xp', 0)
    xp_needed = 100
    xp_progress = (xp_current / xp_needed) * 100
    level = gama.get('level', 1)
    achievements_count = len(get_user_achievements(st.session_state['username']))
    
    # Stats grid - Compact version
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 12px; border-radius: 10px; border: 1px solid #333; margin-bottom: 12px;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px;">
            <div style="background: linear-gradient(135deg, #1a3a1a 0%, #0d2e0d 100%); padding: 10px; border-radius: 8px; border-left: 4px solid #4CAF50; text-align: center;">
                <div style="font-size: 28px; margin-bottom: 2px;">🔥</div>
                <div style="font-size: 22px; font-weight: bold; color: #4CAF50;">{gama.get('streak', 0)}</div>
                <div style="font-size: 9px; color: #aaa;">Streak</div>
                <div style="font-size: 8px; color: #666;">Max: {gama.get('max_streak', 0)}</div>
            </div>
            <div style="background: linear-gradient(135deg, #3a3a1a 0%, #2d2608 100%); padding: 10px; border-radius: 8px; border-left: 4px solid #FFB300; text-align: center;">
                <div style="font-size: 28px; margin-bottom: 2px;">⭐</div>
                <div style="font-size: 22px; font-weight: bold; color: #FFB300;">Lv. {level}</div>
                <div style="font-size: 9px; color: #aaa;">Level</div>
            </div>
        </div>
        <div style="margin-bottom: 8px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <div style="font-size: 10px; color: #aaa; font-weight: bold;">✨ XP</div>
                <div style="font-size: 9px; color: #00BCD4;">{xp_current}/{xp_needed}</div>
            </div>
            <div style="background-color: #0a0a0a; border-radius: 10px; height: 8px; overflow: hidden; border: 1px solid #00BCD4;">
                <div style="background: linear-gradient(90deg, #00BCD4 0%, #00E5FF 100%); height: 100%; width: {xp_progress}%; transition: width 0.3s ease;"></div>
            </div>
        </div>
        <div style="background: linear-gradient(135deg, #2d1a3d 0%, #1a0d2d 100%); padding: 9px; border-radius: 8px; border-left: 4px solid #FF6B9D; text-align: center;">
            <div style="font-size: 26px; margin-bottom: 2px;">🏆</div>
            <div style="font-size: 18px; font-weight: bold; color: #FF6B9D;">{achievements_count}</div>
            <div style="font-size: 9px; color: #aaa;">Achievements</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("", ["Learn", "Exam", "Results", "Analytics", "Leaderboard", "Achievements"], key="menu_radio", label_visibility="collapsed")
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.session_state["chat_history"] = []
        st.session_state["exam_active"] = False
        st.session_state["exam_questions"] = []
        st.session_state["user_answers"] = {}
        st.session_state["menu"] = "Login"
        st.success("✅ Logged out successfully!")
        st.rerun()

# =============================
# -------- Login Page ---------
# =============================
if menu == "Login":
    st.title("🤖 GenEDxAI")
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 5])
    with col1:
        st.markdown("""
        <div style="padding: 20px 0;">
            <h3>😊 Welcome to GenEDxAI!</h3>
            <p style="font-size: 18px; line-height: 1.5;">
                👋 A platform that uses AI to create educational content and evaluate your learning. 
                Whether you're a student or educator, we provide personalized support and quizzes 
                to help you succeed!
            </p>
            <p style="margin-top: 20px; font-size: 16px;">
                Please login using the sidebar to get started.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        lottie_login = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_1pxqjqps.json")
        if lottie_login:
            st_lottie(lottie_login, height=450, key="welcome_animation")
        else:
            st.warning("⚠ Could not load animation")

    # Sidebar login fields
    st.sidebar.markdown('<div style="margin-top:15px;"><label style="font-size:25px;">👤 Username</label></div>', unsafe_allow_html=True)
    login_username = st.sidebar.text_input("", key="login_user_input", placeholder="Enter username")

    st.sidebar.markdown('<div style="margin-top:20px;"><label style="font-size:25px;">🔒 Password</label></div>', unsafe_allow_html=True)
    login_password = st.sidebar.text_input("", type="password", key="login_pass_input", placeholder="Enter password")

    login_clicked = st.sidebar.button("🔐 *Login*")

    if login_clicked:
        try:
            if login_user(login_username, login_password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = login_username
                st.session_state["menu"] = "Learn"
                st.success(f"✅ Logged in as {login_username}!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")
        except Exception as e:
            st.error(f"❌ Login failed: {str(e)}")

# =============================
# ------- Register Page -------
# =============================
elif menu == "Register":
    st.title("📝 Register for EduBot")
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 5])
    with col1:
        st.markdown("""
        <div style="padding: 20px 0;">
            <h3>Join our learning community!</h3>
            <p style="font-size: 16px; line-height: 1.5;">
                Create your account to access personalized learning content,
                take exams, and track your progress.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        lottie_login = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_1pxqjqps.json")
        if lottie_login:
            st_lottie(lottie_login, height=450, key="register_animation")
        else:
            st.warning("⚠ Could not load animation")

    # Sidebar register fields
    st.sidebar.markdown('<div style="margin-top:15px;"><label style="font-size:25px;">👤 New Username</label></div>', unsafe_allow_html=True)
    register_username = st.sidebar.text_input("", key="register_user_input", placeholder="Choose a unique username (3-20 chars, alphanumeric)")

    st.sidebar.markdown('<div style="margin-top:20px;"><label style="font-size:25px;">🔒 New Password</label></div>', unsafe_allow_html=True)
    register_password = st.sidebar.text_input("", type="password", key="register_pass_input", placeholder="Min 8 chars: uppercase, lowercase, digit, special char")
    
    # Show password strength requirement
    if register_password:
        is_valid, msg = validate_password_strength(register_password)
        if is_valid:
            st.sidebar.success(f"✅ {msg}")
        else:
            st.sidebar.warning(f"⚠️ {msg}")

    register_clicked = st.sidebar.button("📝 *Register*")

    if register_clicked:
        try:
            register_user(register_username, register_password)
            st.success("✅ Registered successfully! Please log in.")
            st.session_state["menu"] = "Login"
            st.rerun()
        except Exception as e:
            st.error(f"❌ Registration failed: {str(e)}")
            
            
            
elif menu == "Learn":
    st.title(f"👋 Welcome, {st.session_state['username']}!")

    prompt = st.text_area("💬 Ask me anything to learn!")

    if st.button("🚀 Submit", key="submit_prompt"):
        if prompt:
            # Sanitize input to prevent XSS attacks
            sanitized_prompt = sanitize_input(prompt)
            response = get_learning_response(sanitized_prompt)
            # Append consistent keys for user and ai messages
            st.session_state["chat_history"].append({"user_msg": sanitized_prompt, "ai_msg": response})
            save_chat(st.session_state["username"], sanitized_prompt, response)
            st.success("✅ Response received!")

    # Get chat history safely, default empty list
    chat_history = get_chat_history(st.session_state["username"]) or []

    if chat_history:
        st.subheader("📜 Chat History")

        # Clear chat button with a unique key
        if st.button("🧹 Clear Chat History", key="clear_history"):
            st.session_state["chat_history"] = []
            clear_chat_history(st.session_state["username"])
            st.success("🧼 History cleared!")
            st.experimental_rerun()

        # Display chat in reverse order (latest first)
        for chat in reversed(chat_history):
            user_text = chat.get("user_msg", "")
            ai_text = chat.get("ai_msg", "")

            # Safe multiline markdown with formatting
            st.markdown(f"""
                <p><strong>🧑 You:</strong> {user_text}</p>
                <p><strong>🤖 AI:</strong> {ai_text}</p>
                <hr>
            """, unsafe_allow_html=True)



elif menu == "Exam":
    st.title("📝 Take an Exam")
    
    # Initialize exam session state
    if "exam_settings" not in st.session_state:
        st.session_state["exam_settings"] = {
            "difficulty": "medium",
            "num_questions": 5,
            "time_limit": 0,
            "mode": "exam"
        }
    if "exam_start_time" not in st.session_state:
        st.session_state["exam_start_time"] = None
    if "exam_time_remaining" not in st.session_state:
        st.session_state["exam_time_remaining"] = 0
    if "exam_topic" not in st.session_state:
        st.session_state["exam_topic"] = None
    
    # Settings section (only show when exam not active)
    if not st.session_state["exam_active"]:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            topic = st.text_input("📚 Enter a topic for the exam", label_visibility="collapsed")
        
        with col2:
            st.empty()
        
        # Settings expander
        with st.expander("⚙️ Exam Settings", expanded=False):
            settings_col1, settings_col2 = st.columns(2)
            
            with settings_col1:
                difficulty = st.selectbox(
                    "Difficulty Level",
                    ["easy", "medium", "hard"],
                    index=["easy", "medium", "hard"].index(st.session_state["exam_settings"]["difficulty"]),
                    key="difficulty_select"
                )
                st.session_state["exam_settings"]["difficulty"] = difficulty
                
                num_questions = st.slider(
                    "Number of Questions",
                    min_value=5,
                    max_value=20,
                    value=st.session_state["exam_settings"]["num_questions"],
                    step=1,
                    key="num_questions_slider"
                )
                st.session_state["exam_settings"]["num_questions"] = num_questions
            
            with settings_col2:
                mode = st.selectbox(
                    "Mode",
                    ["exam", "practice"],
                    index=["exam", "practice"].index(st.session_state["exam_settings"]["mode"]),
                    key="mode_select"
                )
                st.session_state["exam_settings"]["mode"] = mode
                
                use_timer = st.checkbox("Enable Time Limit", value=st.session_state["exam_settings"]["time_limit"] > 0, key="use_timer")
                
                if use_timer:
                    time_limit = st.number_input(
                        "Time Limit (minutes)",
                        min_value=1,
                        max_value=120,
                        value=max(1, st.session_state["exam_settings"]["time_limit"] // 60),
                        key="time_limit_input"
                    )
                    st.session_state["exam_settings"]["time_limit"] = time_limit * 60  # Convert to seconds
                else:
                    st.session_state["exam_settings"]["time_limit"] = 0
            
            # Display settings summary
            st.markdown("---")
            st.markdown(f"""
            **Exam Summary:**
            - 📊 Difficulty: `{difficulty.upper()}`
            - 📝 Questions: `{num_questions}`
            - 🎮 Mode: `{mode.upper()}`
            - ⏱️ Time Limit: `{f'{time_limit} min' if use_timer else 'Unlimited'}`
            """)
        
        # Start exam button
        if st.button("🎯 Start Exam", use_container_width=True, type="primary") and topic:
            try:
                sanitized_topic = sanitize_input(topic)
                st.session_state["exam_topic"] = sanitized_topic
                questions = generate_exam(
                    sanitized_topic,
                    difficulty=st.session_state["exam_settings"]["difficulty"],
                    num_questions=st.session_state["exam_settings"]["num_questions"]
                )
                st.session_state["exam_questions"] = questions
                st.session_state["exam_active"] = True
                st.session_state["user_answers"] = {}
                st.session_state["exam_start_time"] = datetime.now()
                st.success("✅ Exam started! Select your answers below.")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error generating exam: {str(e)}")

    if st.session_state["exam_active"]:
        st.subheader("📄 Questions")
        
        questions = st.session_state["exam_questions"]
        
        # Display timer if time limit is set
        if st.session_state["exam_settings"]["time_limit"] > 0:
            time_col1, time_col2, time_col3 = st.columns([1, 2, 1])
            
            with time_col2:
                if st.session_state["exam_start_time"]:
                    elapsed_seconds = (datetime.now() - st.session_state["exam_start_time"]).total_seconds()
                    time_remaining = st.session_state["exam_settings"]["time_limit"] - int(elapsed_seconds)
                    
                    if time_remaining <= 0:
                        st.error("⏱️ Time's up! Auto-submitting exam...")
                        st.session_state["exam_time_remaining"] = 0
                        # Auto-submit - submit whatever answers have been provided
                        try:
                            marks, feedback = evaluate_exam(questions, st.session_state["user_answers"])
                            store_result(
                                st.session_state["username"],
                                st.session_state["exam_topic"],
                                marks,
                                feedback,
                                difficulty=st.session_state["exam_settings"]["difficulty"],
                                time_spent=int(elapsed_seconds),
                                mode=st.session_state["exam_settings"]["mode"]
                            )
                            # Update gamification
                            update_streak(st.session_state["username"])
                            xp_reward = calculate_xp_reward(marks, st.session_state["exam_settings"]["difficulty"])
                            add_xp(st.session_state["username"], xp_reward)
                            
                            # Get user stats for achievement checking
                            user_gama = get_user_gamification(st.session_state["username"])
                            user_results = get_user_results(st.session_state["username"])
                            results_count = len(user_results) if user_results else 1
                            avg_score = sum([r.get('marks', 0) for r in user_results]) / results_count if user_results else (marks / len(questions) * 5)
                            streak = user_gama.get('streak', 0)
                            
                            check_achievements(st.session_state["username"], results_count, avg_score * 20, streak, marks)
                            
                            st.markdown(f"""
                            <div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; margin: 20px 0; color: #fff;">
                                <h3 style="color: #4CAF50; margin: 0; font-size: 28px;">🎓 Your Score: {marks}/{len(questions)}</h3>
                                <p style="color: #aaa; font-size: 18px; margin: 10px 0;">Percentage: <strong style="color: #fff;">{(marks/len(questions))*100:.1f}%</strong></p>
                                <p style="color: #FFB300; font-size: 14px; margin: 10px 0;">✨ XP Earned: +{xp_reward}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown("### 🧠 Feedback & Explanations")
                            st.markdown(feedback, unsafe_allow_html=True)
                            st.session_state["exam_active"] = False
                        except Exception as e:
                            st.error(f"❌ Error auto-submitting exam: {str(e)}")
                    else:
                        minutes = time_remaining // 60
                        seconds = time_remaining % 60
                        timer_color = "#f44336" if time_remaining < 60 else "#ff9800" if time_remaining < 300 else "#4CAF50"
                        st.markdown(f"""
                        <div style="background-color: {timer_color}; padding: 12px; border-radius: 8px; text-align: center; color: #fff; font-size: 28px; font-weight: bold;">
                        ⏱️ {minutes:02d}:{seconds:02d}
                        </div>
                        """, unsafe_allow_html=True)
                        st.session_state["exam_time_remaining"] = time_remaining
        
        # Display each question with clickable option buttons
        for idx, q_data in enumerate(questions):
            st.markdown(f"### Q{idx + 1}. {q_data['question']}")
            
            # Create button columns for options
            cols = st.columns(2)
            options_list = sorted(q_data['options'].items())
            
            for col_idx, (option_key, option_text) in enumerate(options_list):
                with cols[col_idx % 2]:
                    button_label = f"{option_key.upper()}) {option_text}"
                    
                    # Check if this option is already selected
                    is_selected = st.session_state["user_answers"].get(idx) == option_key
                    
                    # Create button with visual feedback
                    if st.button(
                        button_label,
                        key=f"q{idx}_opt{option_key}",
                        use_container_width=True,
                        type="secondary" if not is_selected else "primary"
                    ):
                        st.session_state["user_answers"][idx] = option_key
                        st.rerun()
            
            # Show selected answer
            selected = st.session_state["user_answers"].get(idx)
            if selected:
                st.success(f"✓ Your answer: **{selected.upper()}**", icon="✅")
            st.divider()
        
        # Progress indicator
        answered_count = len(st.session_state["user_answers"])
        total_count = len(questions)
        st.progress(answered_count / total_count, text=f"Progress: {answered_count}/{total_count} answered")
        
        # Submit button
        if st.button("📤 Submit Answers", use_container_width=True, type="primary"):
            if len(st.session_state["user_answers"]) == len(questions):
                try:
                    marks, feedback = evaluate_exam(questions, st.session_state["user_answers"])
                    
                    # Calculate time spent
                    if st.session_state["exam_start_time"]:
                        time_spent = int((datetime.now() - st.session_state["exam_start_time"]).total_seconds())
                    else:
                        time_spent = 0
                    
                    store_result(
                        st.session_state["username"],
                        st.session_state["exam_topic"],
                        marks,
                        feedback,
                        difficulty=st.session_state["exam_settings"]["difficulty"],
                        time_spent=time_spent,
                        mode=st.session_state["exam_settings"]["mode"]
                    )
                    
                    # Update gamification
                    update_streak(st.session_state["username"])
                    xp_reward = calculate_xp_reward(marks, st.session_state["exam_settings"]["difficulty"])
                    add_xp(st.session_state["username"], xp_reward)
                    
                    # Get user stats for achievement checking
                    user_gama = get_user_gamification(st.session_state["username"])
                    user_results = get_user_results(st.session_state["username"])
                    results_count = len(user_results) if user_results else 1
                    avg_score = sum([r.get('marks', 0) for r in user_results]) / results_count if user_results else (marks / len(questions) * 5)
                    streak = user_gama.get('streak', 0)
                    
                    check_achievements(st.session_state["username"], results_count, avg_score * 20, streak, marks)
                    
                    # Results display
                    st.markdown(f"""
                    <div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; margin: 20px 0; color: #fff;">
                        <h3 style="color: #4CAF50; margin: 0; font-size: 28px;">🎓 Your Score: {marks}/{len(questions)}</h3>
                        <p style="color: #aaa; font-size: 18px; margin: 10px 0;">Percentage: <strong style="color: #fff;">{(marks/len(questions))*100:.1f}%</strong></p>
                        <p style="color: #aaa; font-size: 14px; margin: 10px 0;">⏱️ Time Spent: {time_spent // 60}m {time_spent % 60}s | 📊 Difficulty: {st.session_state['exam_settings']['difficulty'].upper()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 🧠 Feedback & Explanations")
                    st.markdown(feedback, unsafe_allow_html=True)
                    
                    st.session_state["exam_active"] = False
                    if st.button("🔄 Take Another Exam"):
                        st.session_state["exam_active"] = False
                        st.session_state["user_answers"] = {}
                        st.session_state["exam_start_time"] = None
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error evaluating exam: {str(e)}")
            else:
                st.warning(f"⚠️ Please answer all questions! ({len(st.session_state['user_answers'])}/{len(questions)} answered)")


elif menu == "Results":
    st.title("📊 Your Results")

    try:
        # Get all topics for the filter
        all_topics = get_user_topics(st.session_state["username"])
        
        # Add filter section
        st.markdown("### 🔍 Filter Your Results")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            selected_topic = st.selectbox(
                "📚 Topic",
                ["All Topics"] + all_topics,
                key="filter_topic"
            )
        
        with col2:
            selected_difficulty = st.selectbox(
                "📊 Difficulty",
                ["All Levels", "easy", "medium", "hard"],
                key="filter_difficulty"
            )
        
        with col3:
            selected_mode = st.selectbox(
                "🎮 Mode",
                ["All Modes", "exam", "practice"],
                key="filter_mode"
            )
        
        with col4:
            date_range = st.selectbox(
                "📅 Date Range",
                ["All Time", "Last 7 Days", "Last 30 Days", "Custom"],
                key="filter_date"
            )
        
        # Build filters dict
        filters = {}
        
        if selected_topic != "All Topics":
            filters['topic'] = selected_topic
        
        if selected_difficulty != "All Levels":
            filters['difficulty'] = selected_difficulty
        
        if selected_mode != "All Modes":
            filters['mode'] = selected_mode
        
        # Handle date range filtering
        if date_range == "Last 7 Days":
            filters['date_from'] = (datetime.now() - timedelta(days=7)).isoformat()
        elif date_range == "Last 30 Days":
            filters['date_from'] = (datetime.now() - timedelta(days=30)).isoformat()
        elif date_range == "Custom":
            date_col1, date_col2 = st.columns(2)
            with date_col1:
                from_date = st.date_input("From Date", value=datetime.now() - timedelta(days=30), key="custom_from_date")
                if from_date:
                    filters['date_from'] = from_date.isoformat()
            with date_col2:
                to_date = st.date_input("To Date", value=datetime.now(), key="custom_to_date")
                if to_date:
                    filters['date_to'] = to_date.isoformat()
        
        st.markdown("---")
        
        # Get filtered results
        results = get_user_results(st.session_state["username"], filters=filters if filters else None)
        
        if results:
            st.markdown(f"### 📌 Your Exam Results ({len(results)} found)")
            
            # Display stats
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            
            with stats_col1:
                avg_marks = sum([r['marks'] for r in results]) / len(results)
                st.metric("📈 Average Score", f"{avg_marks:.1f}/5")
            
            with stats_col2:
                success_count = len([r for r in results if r['marks'] >= 3])
                success_rate = (success_count / len(results) * 100) if results else 0
                st.metric("✅ Success Rate", f"{success_rate:.0f}%")
            
            with stats_col3:
                st.metric("📝 Total Exams Filtered", len(results))
            
            st.markdown("---")
            
            # Display results as compact thumbnails with expandable details
            # Results are already sorted by newest first from database
            for i, result in enumerate(results):
                # Score percentage calculation
                percentage = (result['marks'] / 5) * 100
                score_color = '#4CAF50' if result['marks'] >= 3 else '#ff9800' if result['marks'] >= 2 else '#f44336'
                border_color = '#4CAF50' if result['marks'] >= 3 else '#ff9800' if result['marks'] >= 2 else '#f44336'
                
                # Get difficulty and mode info
                difficulty = result.get('difficulty', 'medium')
                mode = result.get('mode', 'exam')
                
                # Create compact thumbnail card
                with st.expander(
                    f"📌 {result['topic']} • Score: {result['marks']}/5 ({percentage:.0f}%) • {result['date']} • 📊 {difficulty} • 🎮 {mode}",
                    expanded=False
                ):
                    # Expanded view with details
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="background-color: #1a1a1a; padding: 20px; border-radius: 10px; border-left: 5px solid {border_color};">
                            <h4 style="color: #fff; margin-top: 0;">📚 Exam: {result['topic']}</h4>
                            <p style="color: #bbb; font-size: 14px;">Date: {result['date']}</p>
                            <p style="color: #bbb; font-size: 12px;">Difficulty: <span style="color: #FFB300;">{difficulty.upper()}</span> | Mode: <span style="color: #00BCD4;">{mode.upper()}</span></p>
                            <p style="color: #bbb; font-size: 12px;">Time Spent: {result.get('time_spent', 0) // 60}m {result.get('time_spent', 0) % 60}s</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style="background-color: {score_color}; padding: 20px; border-radius: 10px; text-align: center;">
                            <h3 style="color: #fff; margin: 0; font-size: 36px;">{result['marks']}/5</h3>
                            <p style="color: #fff; margin: 5px 0 0 0; font-size: 14px;">{percentage:.0f}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Detailed feedback section
                    st.markdown("---")
                    st.markdown("### 📝 Detailed Feedback")
                    st.markdown(result['mistakes'], unsafe_allow_html=True)
                    
        else:
            # Empty state with animation
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.markdown("""
                <div style="padding: 20px 0;">
                    <h3>No results match your filters!</h3>
                    <p>Try adjusting your filter criteria to see your exam results.</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                lottie_empty = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_ydo1amjm.json")
                if lottie_empty:
                    st_lottie(lottie_empty, height=200, key="empty_results")
                    
    except Exception as e:
        st.error(f"❌ Error fetching results: {str(e)}") 


# =============================
# ---- Analytics Dashboard ----
# =============================
elif menu == "Analytics":
    st.title("📊 Your Analytics")
    
    try:
        metrics = get_performance_metrics(st.session_state["username"])
        
        if metrics.get('total_exams', 0) > 0:
            # Performance summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📝 Total Exams", metrics['total_exams'])
            with col2:
                st.metric("⭐ Average Score", f"{metrics['average_score']}/5")
            with col3:
                st.metric("🏆 Highest Score", f"{metrics['highest_score']}/5")
            with col4:
                st.metric("📈 Success Rate", f"{metrics['success_rate']:.1f}%")
            
            # Improvement rate
            if metrics['improvement_rate'] != 0:
                direction = "📈" if metrics['improvement_rate'] > 0 else "📉"
                st.success(f"{direction} Improvement Rate: {metrics['improvement_rate']:.1f}% (comparing first 5 to last 5 exams)")
            
            # Score trends chart
            st.markdown("### 📈 Score Trends Over Time")
            scores_df = __import__('pandas').DataFrame({
                'Exam': [f"Exam {i+1}" for i in range(len(metrics['marks_list']))],
                'Score': metrics['marks_list']
            })
            st.line_chart(scores_df.set_index('Exam'))
            
            # Weak areas analysis
            st.markdown("### 🎯 Topics to Focus On")
            weak_areas = get_weak_areas(st.session_state["username"])
            
            if weak_areas:
                weakness_data = []
                for topic, data in list(weak_areas.items())[:5]:
                    weakness_data.append({
                        'Topic': topic,
                        'Avg Score': data['average'],
                        'Attempts': data['attempts']
                    })
                
                weakness_df = __import__('pandas').DataFrame(weakness_data)
                st.dataframe(weakness_df, use_container_width=True)
                
                st.info("💡 Focus on improving scores in these topics!")
        else:
            st.info("📚 Take some exams to see your analytics!")
    
    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")


# =============================
# ---- Leaderboard Page -------
# =============================
elif menu == "Leaderboard":
    st.title("🏆 Leaderboard")
    
    try:
        # Tab for weekly/monthly
        tab1, tab2 = st.tabs(["🔥 This Week", "📅 This Month"])
        
        with tab1:
            st.markdown("### Top Performers This Week")
            weekly_leaders = get_leaderboard(limit=10, timeframe="week")
            
            if weekly_leaders:
                leader_data = []
                for idx, leader in enumerate(weekly_leaders, 1):
                    leader_data.append({
                        '🥇 Rank': idx,
                        'User': leader['username'],
                        'Level': leader.get('level', 1),
                        '⭐ XP': leader.get('total_xp', 0),
                        '🔥 Streak': leader.get('streak', 0)
                    })
                
                leader_df = __import__('pandas').DataFrame(leader_data)
                st.dataframe(leader_df, use_container_width=True, hide_index=True)
            else:
                st.info("📊 No data available yet!")
        
        with tab2:
            st.markdown("### Top Performers This Month")
            monthly_leaders = get_leaderboard(limit=10, timeframe="month")
            
            if monthly_leaders:
                leader_data = []
                for idx, leader in enumerate(monthly_leaders, 1):
                    leader_data.append({
                        '🥇 Rank': idx,
                        'User': leader['username'],
                        'Level': leader.get('level', 1),
                        '⭐ XP': leader.get('total_xp', 0),
                        '🔥 Streak': leader.get('streak', 0)
                    })
                
                leader_df = __import__('pandas').DataFrame(leader_data)
                st.dataframe(leader_df, use_container_width=True, hide_index=True)
            else:
                st.info("📊 No data available yet!")
    
    except Exception as e:
        st.error(f"❌ Error loading leaderboard: {str(e)}")


# =============================
# ---- Achievements Page ------
# =============================
elif menu == "Achievements":
    st.title("🏅 Achievements")
    
    try:
        achievements = get_user_achievements(st.session_state["username"])
        
        if achievements:
            st.markdown("### 🎯 Your Unlocked Achievements")
            
            # Display achievements in a grid
            cols = st.columns(3)
            for idx, achievement in enumerate(achievements):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style="background-color: #1a1a1a; padding: 15px; border-radius: 10px; 
                                border-left: 4px solid #FFB300; text-align: center; margin-bottom: 10px;">
                        <div style="font-size: 40px; margin-bottom: 10px;">{achievement.get('icon', '🏆')}</div>
                        <div style="color: #FFB300; font-weight: bold; font-size: 14px;">{achievement.get('name', 'Achievement')}</div>
                        <div style="color: #aaa; font-size: 12px; margin-top: 5px;">{achievement.get('description', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("🚀 Start taking exams to unlock achievements!")
    
    except Exception as e:
        st.error(f"❌ Error loading achievements: {str(e)}")
        
st.markdown("""
<hr style="border: none; border-top: 2px solid #ccc; margin: 40px 0;" />

<div style="text-align: center; padding: 10px 0;">
    <p style="font-size: 16px; color: gray;">
        © 2025 <strong>GenEDxAI</strong>. All rights reserved.
    </p>
    <p style="font-size: 14px; color: gray;">
        Crafted with <span style="color: #e74c3c;">❤</span> using <strong>Streamlit</strong>. Designed for Lifelong Learners.
    </p>
</div>
""", unsafe_allow_html=True)
