# GenEDxAI: AI-Powered Education Platform with Gamification

#### Transform Your Learning Journey with AI-Powered Exams & Gamification

## 🤖 Overview

**GenEDxAI** is a cutting-edge AI-powered education platform designed specifically for modern learners. It combines interactive learning with personalized assessments, gamification rewards, and comprehensive analytics to create an engaging and effective educational experience.

The platform uses OpenRouter's **GPT-3.5-Turbo** model to generate intelligent responses and provide comprehensive exam feedback. Advanced security features protect user data, while a sophisticated gamification system keeps learners motivated.

## ✨ Key Features

### 🎓 Core Learning Features
- **🧠 Interactive Learning**: Ask questions on any topic and get detailed, educational responses
- **📝 Personalized Exams**: Generate custom exams with configurable difficulty (Easy/Medium/Hard) and question count (5-20)
- **⏱️ Timed Exams**: Challenge yourself with time-limited exams featuring auto-submission
- **📊 Practice vs Exam Mode**: Flexible learning with practice mode for unlimited attempts and exam mode for serious testing
- **📚 Exam History Filters**: Filter results by topic, difficulty, mode, and date range for better learning insights

### 🏆 Gamification System
- **⭐ XP & Levels**: Earn XP points based on exam performance and difficulty. Level up as you progress (XP scales: Easy=10, Medium=20, Hard=40 per question)
- **🔥 Streak System**: Build daily learning streaks and celebrate consistency
- **🏅 Achievements & Badges**: Unlock 7 different achievements:
  - First Exam
  - Speed Learner (Complete exam in under 5 minutes)
  - Consistency Master (7-day streak)
  - Perfect Scorer (Score 5/5 on hard difficulty)
  - XP Accumulator (Reach 1000 XP)
  - Elite Performer (Average score 4.5 or higher)
  - Learning Legend (Complete 50 exams)
- **🏅 Leaderboard**: Compete on weekly and monthly leaderboards based on XP and exam performance
- **📈 Performance Analytics**: Track weak areas, performance trends, and learning patterns

### 🔐 Security & Privacy
- **Encrypted Passwords**: bcrypt hashing for all passwords
- **Rate Limiting**: Protect against brute force attacks (5 attempts per 15 minutes)
- **Audit Logging**: Complete audit trail of authentication events
- **CSRF Protection**: Token-based CSRF prevention
- **Session Timeout**: Automatic logout after 30 minutes of inactivity
- **Input Sanitization**: Protection against injection attacks
- **API Key Validation**: Secure environment-based API configuration

### 📱 User Experience
- **Dark Mode by Default**: Easy on the eyes with modern dark theme
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Real-time Feedback**: Instant exam evaluation with detailed explanations
- **Progress Visualization**: Beautiful charts and statistics dashboards

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- MongoDB (local or cloud instance - MongoDB Atlas recommended)
- OpenRouter API key (free tier available)
- Git for version control

### Setup Instructions

#### 1. Clone the Repository
```bash
git clone https://github.com/rakeshkolipakaace/GenEDxAI.git
cd GenEDxAI
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create a `.env` file in the project root:

```env
# OpenRouter API Key (https://openrouter.ai)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
# For local MongoDB: mongodb://localhost:27017/

# Optional - Gemini API Key (if using Gemini)
GEMINI_API_KEY=your_gemini_api_key_here
```

> **⚠️ IMPORTANT SECURITY NOTES:**
> - Never commit `.env` files to git
> - Use `.gitignore` to exclude sensitive files (already configured)
> - For Streamlit Cloud deployment, add secrets via the Streamlit dashboard

#### 5. Get API Keys

**OpenRouter (Recommended):**
1. Visit https://openrouter.ai
2. Sign up for a free account
3. Copy your API key from the settings
4. Add it to `.env` as `OPENROUTER_API_KEY`

**MongoDB:**
1. Visit https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get your connection string
4. Add it to `.env` as `MONGODB_URI`

#### 6. Run the Application
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 🏗️ Project Structure

```
GenEDxAI/
├── app.py                              # Main Streamlit application
├── config/
│   ├── __init__.py
│   └── config.py                       # Configuration and environment setup
├── utils/
│   ├── __init__.py
│   ├── auth.py                         # User authentication & security integration
│   ├── chatbot.py                      # AI-powered learning responses
│   ├── db.py                           # MongoDB operations & queries
│   ├── exam.py                         # Exam generation & evaluation
│   ├── gamification.py                 # Gamification system (streaks, XP, badges)
│   └── security.py                     # Security features & audit logging
├── static/
│   ├── style.css                       # Custom CSS styling
│   └── videos/
│       └── ai.json                     # Lottie animations
├── .env                                # Environment variables (do NOT commit)
├── .gitignore                          # Git ignore rules
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
└── .streamlit/
    └── config.toml                     # Streamlit configuration
```

## 📖 How the Gamification System Works

### 🎯 XP (Experience Points) System
- **Earning XP**: You earn XP based on your exam performance and difficulty level
  - Easy Exam: 10 XP per correct answer
  - Medium Exam: 20 XP per correct answer
  - Hard Exam: 40 XP per correct answer
  - Bonus: Extra points for speed (under 5 minutes)
  
- **Calculation**: Total XP = (Marks/5) × XP_per_difficulty × Time_Bonus
- **Visible everywhere**: Your XP is displayed in the sidebar

### 📊 Levels System
- Levels are automatically calculated from your total XP
- **Level Threshold**: Every 100 XP = 1 Level
- **Formula**: Level = floor(Total_XP / 100) + 1
- Encourages consistent learning and long-term engagement

### 🔥 Streak System
- **Daily Streaks**: Complete 1 exam per day to maintain your streak
- **Streak Counter**: See your current streak in the sidebar
- **Reset**: Missing a day resets your streak to 0
- **Motivation**: Longer streaks unlock achievements and leaderboard ranking

### 🏅 Achievements & Badges
Unlock special achievements by completing specific tasks:

| Achievement | Condition | Badge |
|------------|-----------|-------|
| 🎬 First Exam | Complete your first exam | 🎬 |
| ⚡ Speed Learner | Complete exam in under 5 minutes | ⚡ |
| 🔥 Consistency Master | Maintain a 7-day learning streak | 🔥 |
| 💎 Perfect Scorer | Score 5/5 on hard difficulty exam | 💎 |
| 🚀 XP Accumulator | Reach 1000 total XP | 🚀 |
| 👑 Elite Performer | Maintain average score of 4.5 or higher | 👑 |
| 🌟 Learning Legend | Complete 50 exams | 🌟 |

### 🏆 Leaderboard Rankings
- **Weekly Leaderboard**: Top performers based on XP earned this week
- **Monthly Leaderboard**: Top performers based on total XP this month
- **Ranking Criteria**: 
  - Primary: Total XP in period
  - Secondary: Number of exams completed
  - Tertiary: Average exam score

## 🎮 How to Use GenEDxAI

### Getting Started

#### Step 1: Create an Account
1. Click on the **"Register"** menu option
2. Enter a unique username (alphanumeric characters)
3. Create a strong password (minimum 8 characters)
4. Click **"Register"**

#### Step 2: Login
1. Return to **"Login"** menu
2. Enter your credentials
3. Click **"Login"** to access your personalized dashboard

### 📚 Learn Section
1. Navigate to **"Learn"** tab
2. Type your question or topic (e.g., "Explain photosynthesis", "Python decorators")
3. Click **"Submit"** or press Enter
4. Receive AI-powered educational responses with detailed explanations
5. View your learning history in the sidebar

### 📝 Exam Section
1. Go to **"Exam"** tab
2. Select a **Topic** (e.g., Biology, Python, History)
3. Choose **Difficulty Level**:
   - 🟢 Easy: Basic concepts (10 XP per answer)
   - 🟡 Medium: In-depth knowledge (20 XP per answer)
   - 🔴 Hard: Advanced/Complex topics (40 XP per answer)
4. Set **Number of Questions** (5-20)
5. Choose **Mode**:
   - 📖 Practice: Unlimited attempts, no time limit
   - ⏱️ Exam: Timed, auto-submits when time expires
6. If Exam mode, set time limit
7. Answer all questions
8. Submit to receive:
   - Immediate score
   - Detailed feedback for each question
   - XP and gamification updates
   - Achievement unlocks (if any)

### 📊 Results Section
1. Navigate to **"Results"** tab
2. **Filter** your results by:
   - 📚 Topic (dropdown)
   - 📊 Difficulty (easy/medium/hard)
   - 🎮 Mode (exam/practice)
   - 📅 Date Range (all time/7 days/30 days/custom)
3. View statistics:
   - Average Score
   - Success Rate
   - Total Exams Filtered
4. **Expand** each result to view:
   - Detailed feedback
   - Topic information
   - Difficulty level & mode
   - Time spent
   - Question-by-question analysis

### 📈 Analytics Section
1. Go to **"Analytics"** tab
2. View your learning dashboard:
   - **Performance Chart**: XP growth over time
   - **Weak Areas**: Topics needing improvement with pie charts
   - **Performance Metrics**: Key statistics
   - **Recent Results**: Latest 5 exam attempts

### 🏅 Achievements Section
1. Navigate to **"Achievements"** tab
2. See all 7 available achievements
3. **Unlocked** achievements show:
   - Achievement name & description
   - Date unlocked
   - Progress statistics
4. **Locked** achievements show:
   - Requirements to unlock
   - Your progress toward unlocking
5. **Share** achievements (coming soon)

### 🏆 Leaderboard Section
1. Go to **"Leaderboard"** tab
2. Switch between:
   - **Weekly**: Top XP earners this week
   - **Monthly**: Top XP earners this month
3. See your rank, username, and total XP
4. Check friends' rankings and compete

## 🚀 Deployment Guide

### Deploy to Streamlit Cloud (Recommended)

#### Step 1: Prepare Repository
```bash
# Ensure everything is committed
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

#### Step 2: Connect to Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Click "New App"
3. Connect your GitHub account
4. Select your GenEDxAI repository
5. Choose main branch and `app.py` as entry file

#### Step 3: Add Secrets
1. In Streamlit Cloud dashboard, click on your app
2. Go to **Settings** → **Secrets**
3. Add your environment variables:
```toml
OPENROUTER_API_KEY = "your_key_here"
MONGODB_URI = "your_mongodb_connection_string"
GEMINI_API_KEY = "optional_key"
```

#### Step 4: Deploy
- Click "Deploy"
- Wait for the deployment to complete
- Your app is now live!

**Your app URL**: `https://share.streamlit.io/[username]/GenEDxAI/main/app.py`

### Deploy to Heroku (Alternative)

```bash
# Create Heroku app
heroku create your-app-name

# Add environment variables
heroku config:set OPENROUTER_API_KEY=your_key
heroku config:set MONGODB_URI=your_mongodb_uri

# Create Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
git push heroku main
```

### Deploy to Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

```bash
# Build and run
docker build -t genedxai .
docker run -p 8501:8501 -e OPENROUTER_API_KEY=your_key genedxai
```

## 🔑 API Keys & Security

### Getting API Keys

**OpenRouter (Recommended for cost-effectiveness):**
- Free tier with trial credits
- Supports multiple models
- Easy to switch between providers
- Link: https://openrouter.ai

**MongoDB Atlas (Database):**
- Free tier with 512MB storage
- Auto-scaling clusters
- Automatic backups
- Link: https://mongodb.com/cloud/atlas

### Security Best Practices

1. **Never commit API keys** to version control
2. **Use `.env` files** for local development
3. **Use Streamlit Secrets** for cloud deployment
4. **Rotate keys regularly** for production apps
5. **Use least-privilege** API key permissions
6. **Monitor API usage** for unauthorized access

## 📚 Dependencies

All required packages:
- `streamlit` - Web framework
- `pymongo` - MongoDB driver
- `bcrypt` - Password hashing
- `requests` - HTTP client for APIs
- `python-dotenv` - Environment variables
- `streamlit-lottie` - Animations
- Additional dependencies in `requirements.txt`

Install with:
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to your branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Tips
- Follow PEP 8 style guide
- Add comments for complex logic
- Test locally before pushing
- Update README for new features
- Add error handling for robustness

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

## 🐛 Troubleshooting

### MongoDB Connection Issues
```
Error: Failed to connect to MongoDB
Solution: 
1. Check MongoDB_URI in .env is correct
2. Ensure MongoDB service is running (local)
3. Whitelist your IP in MongoDB Atlas (cloud)
4. Check firewall settings
```

### API Key Errors
```
Error: Invalid API key or unauthorized
Solution:
1. Verify API key is correct in .env
2. Check API key permissions
3. Ensure API key hasn't expired
4. Verify .env file is being loaded
```

### Port Already in Use
```
Error: Port 8501 is already in use
Solution: streamlit run app.py --server.port 8502
```

## 📞 Support & Contact

- **Website**: [GenEDxAI](https://github.com/rakeshkolipakaace/GenEDxAI)
- **Issues**: [GitHub Issues](https://github.com/rakeshkolipakaace/GenEDxAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rakeshkolipakaace/GenEDxAI/discussions)

## 👥 Team & Contributors

### Original Team
- **Rakesh Kolipaka** - [🔗 GitHub](https://github.com/rakeshkolipakaace)
- **Udaykiran Neelam** - [🔗 GitHub](https://github.com/udaykiran2102)
- **Mohan Krishna Thalla** - [🔗 GitHub](https://github.com/mohan13krishna)
- **Ranjith Kumar Digutla** - [🔗 GitHub](https://github.com/ranjith93250)

### Phase 2 Contributors
- Enhanced with comprehensive security system
- Implemented full gamification with achievements & leaderboards
- Added advanced exam configurations & timed mode
- Implemented exam history filtering & analytics

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) - Amazing web framework
- [MongoDB](https://mongodb.com) - Database excellence
- [OpenRouter](https://openrouter.ai) - AI model marketplace
- [LottieFiles](https://lottiefiles.com) - Beautiful animations
- [GitHub](https://github.com) - Version control

## 📊 Project Statistics

- **Pages**: 8 (Learn, Exam, Results, Analytics, Achievements, Leaderboard, Profile)
- **Features**: 20+
- **Security Features**: 8
- **Achievements**: 7
- **Database Collections**: 5+
- **Lines of Code**: 2500+

## 🚀 Road Map

Upcoming features:
- [ ] User profile customization
- [ ] Social sharing of achievements
- [ ] Group/classroom support
- [ ] AI-powered study recommendations
- [ ] Mobile app (React Native)
- [ ] Offline mode support
- [ ] Integration with educational APIs
- [ ] Video tutorials
- [ ] Community forums

---

⭐ **If you find this project helpful, please give it a star!** ⭐

> **Happy Learning!** 🎓 Keep climbing the leaderboard and unlocking achievements! 🏆

**Last Updated**: March 2026 | **Version**: 2.0 (Gamification & Analytics Release)
