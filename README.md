# 🚀 GenEDxAI: AI-Powered Educational Revolution

<div align="center">

![GenEDxAI Logo](https://img.shields.io/badge/GenEDxAI-AI%20Education-blue?style=for-the-badge&logo=artificial-intelligence&logoColor=white)

### 🎓 A Revolutionary Way of Learning with AI-Powered Intelligence

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Try_Now-success?style=for-the-badge)](https://genedxai.onrender.com)
[![GitHub Stars](https://img.shields.io/github/stars/mohan13krishna/GenEDxAI?style=for-the-badge&logo=github)](https://github.com/mohan13krishna/GenEDxAI/stargazers)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://python.org)

*Transforming GenZ education through intelligent AI-powered learning experiences*

</div>

---

## 🌟 Overview

**GenEDxAI** is a cutting-edge AI-powered education platform specifically designed for the modern GenZ learner. Our platform revolutionizes traditional learning by combining interactive AI conversations with personalized assessment systems, creating an engaging and dynamic educational ecosystem.

Powered by **Google's Gemini AI**, GenEDxAI delivers intelligent, contextual responses to learning queries while generating customized examinations that adapt to individual learning patterns.

---

## ✨ Key Features

### 🧠 **Interactive AI Learning**
- **Smart Q&A System**: Ask questions on any topic and receive detailed, educational responses
- **Context-Aware Responses**: AI understands learning context and provides relevant information
- **Multi-Subject Support**: From mathematics to literature, science to history

### 📝 **Personalized Assessment Engine**
- **Custom Exam Generation**: Create tailored exams on any subject matter
- **Automatic Evaluation**: Instant scoring with detailed feedback
- **Adaptive Difficulty**: Questions adjust based on your learning progress

### 📊 **Comprehensive Progress Tracking**
- **Learning Analytics**: Monitor your educational journey with detailed insights
- **Performance History**: Track improvement over time
- **Achievement System**: Celebrate learning milestones

### 🔐 **Secure & Personal**
- **User Authentication**: Secure personal accounts with encrypted data
- **Privacy First**: Your learning data remains private and secure
- **Multi-Device Sync**: Access your progress across all devices

### 📱 **Modern Experience**
- **Responsive Design**: Seamless experience on desktop, tablet, and mobile
- **Intuitive Interface**: Clean, modern UI designed for GenZ preferences
- **Real-time Interactions**: Instant responses and dynamic content loading

---

## 🎯 Quick Start

### 🔧 Prerequisites

Before you begin, ensure you have the following installed:

```bash
Python 3.9 or higher
MongoDB (local instance or cloud)
Google Gemini API key
Git
```

### 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/rakeshkolipakaace/GenEDxAI.git
   cd GenEDxAI
   ```

2. **Set Up Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   
   Create `config/config.py`:
   ```python
   # Google Gemini AI Configuration
   GEMINI_API_KEY = "your_gemini_api_key_here"
   
   # Database Configuration
   MONGODB_URI = "mongodb://localhost:27017/"
   DB_NAME = "edu_chatbot"
   
   # Security Configuration
   SECRET_KEY = "your_secret_key_here"
   ```

5. **Launch Application**
   ```bash
   streamlit run app.py
   ```

6. **Access Platform**
   
   Open your browser and navigate to: `http://localhost:8501`

---

## 🏗️ Project Architecture

```
GenEDxAI/
├── 📁 .devcontainer/           # Development container configuration
│   └── devcontainer.json
├── 📁 config/                  # Configuration management
│   ├── __init__.py
│   └── config.py              # API keys & database settings
├── 📁 static/                  # Static assets
│   ├── videos/                # UI video assets
│   ├── ai.json                # AI animation configurations
│   └── style.css              # Custom styling
├── 📁 utils/                   # Core utilities
│   ├── __init__.py
│   ├── auth.py                # Authentication system
│   ├── chatbot.py             # AI chatbot engine
│   ├── db.py                  # Database operations
│   └── exam.py                # Exam generation & evaluation
├── 📁 venv/                    # Virtual environment
├── app.py                     # Main Streamlit application
├── .env                       # Environment variables
├── .gitignore                # Git ignore rules
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

---

## 🔧 Configuration Guide

### 🤖 Google Gemini AI Setup

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Generate your API key
3. Add the key to `config/config.py`

### 🗄️ MongoDB Configuration

**Local MongoDB:**
```python
MONGODB_URI = "mongodb://localhost:27017/"
```

**MongoDB Atlas (Cloud):**
```python
MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
```

### 🔐 Security Configuration

Generate a secure secret key:
```python
import secrets
SECRET_KEY = secrets.token_hex(32)
```

---

## 📚 How to Use GenEDxAI

### 1️⃣ **Getting Started**
- Launch the application
- Create a new account or sign in
- Complete your profile setup

### 2️⃣ **Learning Mode**
- Navigate to the "Learn" section
- Type your question or topic
- Receive intelligent, educational responses
- Explore follow-up questions and deeper insights

### 3️⃣ **Exam Mode**
- Go to the "Exam" section
- Enter your desired topic
- Start your personalized 5-question quiz
- Submit answers for instant evaluation

### 4️⃣ **Progress Tracking**
- Check the "Results" section
- Review your learning history
- Analyze performance trends
- Set new learning goals

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive web interface |
| **Backend** | Python | Core application logic |
| **AI Engine** | Google Gemini AI | Natural language processing |
| **Database** | MongoDB | User data & progress storage |
| **Authentication** | Custom Auth System | Secure user management |
| **Deployment** | Render | Cloud hosting platform |

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🔀 **Contribution Process**

1. **Fork the Repository**
   ```bash
   git fork https://github.com/rakeshkolipakaace/GenEDxAI.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests where applicable

4. **Commit Changes**
   ```bash
   git commit -m "Add amazing feature"
   ```

5. **Push to Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Create Pull Request**
   - Describe your changes
   - Link any related issues
   - Wait for review

### 🐛 **Bug Reports**

Found a bug? Please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)

### 💡 **Feature Requests**

Have an idea? We'd love to hear it! Submit a feature request with:
- Detailed description
- Use case examples
- Potential implementation ideas

---

## 🌟 Meet Our Amazing Team

<div align="center">

### 💫 The Brilliant Minds Behind GenEDxAI 💫

</div>

<table align="center">
<tr>
<td align="center" width="25%">
<a href="https://github.com/udaykiran2102">
<img src="https://github.com/udaykiran2102.png" width="120px" style="border-radius: 50%;"/><br/>
<h3><b>Uday Kiran</b></h3>
<h4>🎨 Frontend Developer</h4>
<p><i>"Crafting beautiful experiences"</i></p>
</a>
</td>
<td align="center" width="25%">
<a href="https://github.com/mohan13krishna">
<img src="https://github.com/mohan13krishna.png" width="120px" style="border-radius: 50%;"/><br/>
<h3><b>Mohan Krishna</b></h3>
<h4>⚙️ Backend Developer</h4>
<p><i>"Building robust architecture"</i></p>
</a>
</td>
<td align="center" width="25%">
<a href="https://github.com/rakeshkolipakaace">
<img src="https://github.com/rakeshkolipakaace.png" width="120px" style="border-radius: 50%;"/><br/>
<h3><b>Rakesh</b></h3>
<h4>🤖 AI Integration Engineer</h4>
<p><i>"Integrating AI solutions"</i></p>
</a>
</td>
<td align="center" width="25%">
<a href="https://github.com/ranjith93250">
<img src="https://github.com/ranjith93250.png" width="120px" style="border-radius: 50%;"/><br/>
<h3><b>Ranjith Kumar</b></h3>
<h4>🗄️ Database Manager</h4>
<p><i>"Managing data architecture"</i></p>
</a>
</td>
</tr>
</table>

---

## 🎯 Mission & Vision

### 🚀 **Our Mission**
*"Revolutionizing education through AI-powered learning experiences designed specifically for the next generation of learners."*

### 🎯 **Our Vision**
*"Creating a world where quality education is accessible, interactive, and personalized for every GenZ learner, anywhere, anytime."*

---

## 📈 Project Stats

<div align="center">

![GitHub commit activity](https://img.shields.io/github/commit-activity/m/mohan13krishna/GenEDxAI?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/mohan13krishna/GenEDxAI?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/mohan13krishna/GenEDxAI?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/mohan13krishna/GenEDxAI?style=for-the-badge)

</div>

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 GenEDxAI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

We extend our heartfelt gratitude to:

- **[Streamlit](https://streamlit.io/)** - For the incredible web framework
- **[Google Gemini AI](https://ai.google.dev/)** - For powering our AI capabilities  
- **[MongoDB](https://www.mongodb.com/)** - For robust database solutions
- **[Render](https://render.com/)** - For seamless deployment platform
- **[Lottie Files](https://lottiefiles.com/)** - For beautiful animations
- **Open Source Community** - For continuous inspiration and support

---

## 📞 Contact & Support

<div align="center">

### 🔗 **Important Links**

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-GenEDxAI-success?style=for-the-badge)](https://genedxai.onrender.com)
[![GitHub Repository](https://img.shields.io/badge/📁_Repository-GitHub-black?style=for-the-badge&logo=github)](https://github.com/rakeshkolipakaace/GenEDxAI)
[![Documentation](https://img.shields.io/badge/📚_Docs-Wiki-blue?style=for-the-badge)](https://github.com/rakeshkolipakaace/GenEDxAI/wiki)

### 💬 **Get in Touch**

Have questions? Need support? Want to collaborate?

[![Email](https://img.shields.io/badge/📧_Email-Contact_Us-red?style=for-the-badge)](mailto:genedxai@gmail.com)
[![Issues](https://img.shields.io/badge/🐛_Issues-Report_Bug-orange?style=for-the-badge)](https://github.com/rakeshkolipakaace/GenEDxAI/issues)
[![Discussions](https://img.shields.io/badge/💭_Discussions-Join_Chat-purple?style=for-the-badge)](https://github.com/rakeshkolipakaace/GenEDxAI/discussions)

</div>

---

<div align="center">

### ⭐ **Show Your Support**

If you find GenEDxAI helpful, please consider giving us a star!

[![Star History Chart](https://api.star-history.com/svg?repos=rakeshkolipakaace/GenEDxAI&type=Date)](https://star-history.com/#rakeshkolipakaace/GenEDxAI&Date)

---

### 🚀 **Ready to Transform Education?**

**[🎓 Try GenEDxAI Now →](https://genedxai.onrender.com)**

---

*Built with ❤️ by the GenEDxAI Team | Empowering GenZ Learning Since 2024*

**© 2024 GenEDxAI. All rights reserved.**

</div>

---

> **⚠️ Important Note**: This project is developed for educational purposes. Please use responsibly and respect the terms of service of all integrated APIs and services.
