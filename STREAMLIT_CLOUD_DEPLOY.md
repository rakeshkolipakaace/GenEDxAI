# 🚀 Quick Start: Deploy GenEDxAI to Streamlit Cloud

## 5-Minute Deployment Guide

### Step 1: Prepare Your GitHub Repository ✅ (Already Done!)

Your repository is ready at: https://github.com/rakeshkolipakaace/GenEDxAI

Check that these files are committed:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `README.md`
- ✅ `DEPLOYMENT.md`
- ✅ `.gitignore`
- ✅ `.streamlit/config.toml`
- ✅ `utils/` directory (all modules)
- ✅ `config/` directory

### Step 2: Create Streamlit Cloud Account

1. Go to https://streamlit.io/cloud
2. Click **"Sign Up"** or **"Log In"**
3. Choose **"Continue with GitHub"**
4. Authorize Streamlit to access your GitHub repositories
5. You're now ready to deploy! ✨

### Step 3: Deploy the App

1. In Streamlit Cloud dashboard, click **"New App"**
2. Fill in the deployment form:
   - **Repository**: `rakeshkolipakaace/GenEDxAI`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain or leave default

3. Click **"Deploy!"** button
4. Wait 2-5 minutes for deployment to complete
5. Your app URL will be: `https://share.streamlit.io/rakeshkolipakaace/GenEDxAI/main/app.py`

### Step 4: Add Secrets (Environment Variables)

⚠️ **IMPORTANT**: Never hardcode API keys! Use Streamlit Secrets management.

1. Go to your app page on Streamlit Cloud
2. Click the **⋮ (three dots)** menu in the top right
3. Select **"Settings"**
4. Click **"Secrets"** tab
5. Add your secrets in TOML format:

```toml
OPENROUTER_API_KEY = "sk-or-v1-your_actual_key_here"
MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
GEMINI_API_KEY = "AIzaSyxxxx"  # Optional, if using Gemini
```

6. Click **"Save"** 
7. The app will automatically restart and load your secrets

### Step 5: Test Your Deployment

1. Wait for the app to finish loading
2. Click **"Sign Up"** and create a test account
3. Test the features:
   - ✅ Learn tab - Ask a question
   - ✅ Exam tab - Take a practice exam
   - ✅ Results tab - View results with filters
   - ✅ Analytics tab - Check dashboard
   - ✅ Achievements tab - See badges
   - ✅ Leaderboard tab - Check rankings

### Step 6: Share Your App

Your deployed app is live! 🎉

**Share the URL:**
```
https://share.streamlit.io/rakeshkolipakaace/GenEDxAI/main/app.py
```

Or create a custom domain by purchasing one and configuring it in Streamlit Cloud settings.

---

## 🔐 Security Checklist for Deployment

- ✅ API keys stored in Streamlit Secrets (not .env)
- ✅ .env file in .gitignore (never commit)
- ✅ MongoDB IP whitelist configured
- ✅ Strong database password set
- ✅ HTTPS enabled (Streamlit Cloud default)
- ✅ Session timeout configured (30 min)
- ✅ Rate limiting enabled
- ✅ CORS headers set
- ✅ CSRF protection active

## 📱 After Deployment

### Auto-Deployment from Git Pushes

Streamlit Cloud automatically redeploys when you push to the `main` branch:

```bash
git add .
git commit -m "Update features"
git push origin main
# App automatically redeployed in 1-2 minutes!
```

### Monitor App Performance

In Streamlit Cloud dashboard:
- **Status**: Shows if app is running
- **Rerun frequency**: How often the app recalculates
- **Logs**: View application logs for debugging
- **Settings**: Manage resource allocation

### Debugging Tips

If the app doesn't start:

1. **Check Logs**
   - Click on your app
   - Look for red error messages
   - Common issues: Missing API keys, database connection

2. **Verify Secrets**
   - Go to Settings → Secrets
   - Ensure all keys are present
   - Click "Save" to trigger rerun

3. **Check Connections**
   - Verify MongoDB URI is correct
   - Whitelist Streamlit IP if necessary
   - Test API keys in postman/curl

4. **Restart App**
   - Go to Settings
   - Click "Reboot App"

## 💰 Pricing & Limits

**Streamlit Cloud Free Tier:**
- ✅ Free for public projects
- ⚠️ Limited to 1 app per GitHub account
- ⚠️ 1 GB memory allocation
- ⚠️ 5-minute timeout for requests
- ✅ Unlimited users
- ✅ Unlimited chat history
- ✅ Unlimited exams

**For Production/Multiple Apps:**
- Upgrade to Streamlit Pro ($20/month)
- Or use Docker/AWS/Google Cloud (see DEPLOYMENT.md)

---

## 🎯 Next Steps

1. **Customize Your Domain** (optional)
   - Buy a domain from Namecheap/GoDaddy
   - Configure in Streamlit Cloud settings
   - Example: `genedxai.com`

2. **Enable Sharing Features**
   - Users can share their results
   - Analytics dashboard visible to students

3. **Monitor Analytics**
   - Track user growth
   - Monitor API usage
   - Optimize performance

4. **Scale for Growth**
   - Upgrade to Streamlit Pro
   - Increase MongoDB cluster resources
   - Add load balancing

---

## 📞 Support & Troubleshooting

**Common Issues:**

| Issue | Solution |
|-------|----------|
| "Secret not found" | Add keys to Settings → Secrets and save |
| App not starting | Check logs for error messages |
| Slow performance | Reduce cache, optimize MongoDB queries |
| Timeout errors | Increase timeout in settings or optimize code |
| Database connection error | Verify MongoDB URI and IP whitelist |

**Resources:**
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Report Issues](https://github.com/rakeshkolipakaace/GenEDxAI/issues)
- [Streamlit Forum](https://discuss.streamlit.io)

---

## 🎉 Congratulations!

Your GenEDxAI application is now live and accessible to the world!

**Your deployment includes:**
- ✅ Complete learning platform
- ✅ AI-powered exams with gamification
- ✅ 7 achievement badges
- ✅ Weekly/Monthly leaderboards
- ✅ Advanced analytics dashboard
- ✅ Comprehensive security features
- ✅ Exam history filters
- ✅ User authentication & data persistence

Now go share your app and help students learn better! 🎓

---

**Created**: March 2026  
**Version**: 2.0 Gamification Release  
**Last Updated**: Deployment Ready
