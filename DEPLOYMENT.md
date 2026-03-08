# GenEDxAI Deployment Guide

## 🚀 Deployment Options

This guide covers multiple deployment options for GenEDxAI. Choose the one that best suits your needs.

## Option 1: Streamlit Cloud (Recommended - Fastest)

Streamlit Cloud is the easiest way to deploy Streamlit apps. It's free for public repos and includes built-in CI/CD.

### Prerequisites
- GitHub account with GenEDxAI repository
- Streamlit account (create at https://streamlit.io/cloud)
- API keys stored securely

### Step-by-Step

1. **Push to GitHub**
```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

2. **Connect Streamlit Cloud**
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repository
   - Choose branch: `main`
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Add Secrets**
   - In the Streamlit Cloud dashboard, click on your app
   - Go to Settings → Secrets
   - Add your environment variables in TOML format:
```toml
OPENROUTER_API_KEY = "sk-or-v1-xxxx"
MONGODB_URI = "mongodb+srv://xxx:xxx@cluster.mongodb.net/?retryWrites=true&w=majority"
GEMINI_API_KEY = "AIzaSyxxxxxx"
```

4. **Access Your App**
   - Your app will be available at: `https://share.streamlit.io/[username]/GenEDxAI/main/app.py`

### Streamlit Cloud Features
- ✅ Free for public projects
- ✅ Automatic deployment on git push
- ✅ Custom domain support
- ✅ SSL certificate included
- ✅ Environment secrets management
- ✅ Analytics dashboard

---

## Option 2: Docker

Deploy using Docker for maximum portability and control.

### Prerequisites
- Docker installed
- Docker account (optional for Docker Hub)
- Hosting platform (AWS, Google Cloud, DigitalOcean, etc.)

### Create Docker Files

**Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**.dockerignore**
```
.env
.git
.gitignore
__pycache__
*.pyc
venv/
.streamlit/secrets.toml
.DS_Store
node_modules/
```

### Build & Run Locally

```bash
# Build the image
docker build -t genedxai:latest .

# Run the container
docker run -p 8501:8501 \
  -e OPENROUTER_API_KEY=your_key \
  -e MONGODB_URI=your_uri \
  genedxai:latest
```

### Deploy to Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag the image
docker tag genedxai:latest yourname/genedxai:latest

# Push to Docker Hub
docker push yourname/genedxai:latest
```

### Deploy to AWS ECS

```bash
# Create ECS task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service --cluster default --service-name genedxai --task-definition genedxai-task --desired-count 1

# Scale service
aws ecs update-service --cluster default --service genedxai --desired-count 3
```

---

## Option 3: Heroku

Deploy to Heroku using the Heroku CLI.

### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

### Deployment Steps

1. **Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
heroku --version
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku App**
```bash
heroku create genedxai-app
```

4. **Create Procfile**
```bash
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
```

5. **Set Environment Variables**
```bash
heroku config:set OPENROUTER_API_KEY=your_key
heroku config:set MONGODB_URI=your_uri
heroku config:set GEMINI_API_KEY=your_key
```

6. **Deploy**
```bash
git push heroku main
```

7. **View Logs**
```bash
heroku logs --tail
```

### Heroku Free Tier Limitations
- 30-minute request timeout
- Limited to 550 hours/month of dyno
- Dyno sleeps if inactive

---

## Option 4: DigitalOcean App Platform

Simple deployment with automatic CI/CD from GitHub.

### Steps

1. **Create DigitalOcean Account**
   - Visit https://www.digitalocean.com
   - Sign up and create a project

2. **Create App**
   - Go to Apps → Create Apps
   - Connect GitHub repository
   - Select `GenEDxAI` repository

3. **Configure App**
   - Set main resource: Python (Streamlit)
   - Build command: `pip install -r requirements.txt`
   - Run command: `streamlit run app.py`

4. **Set Environment Variables**
   - In App settings, add environment variables:
   - `OPENROUTER_API_KEY`
   - `MONGODB_URI`
   - `GEMINI_API_KEY`

5. **Deploy**
   - Click "Create Resources"
   - Wait for deployment (2-5 minutes)

6. **Access Your App**
   - DigitalOcean provides a unique URL
   - You can connect custom domain in settings

---

## Option 5: Google Cloud Run

Serverless containerized deployment.

### Prerequisites
- Google Cloud account
- Google Cloud SDK installed
- Docker

### Deployment

1. **Create Google Cloud Project**
```bash
gcloud projects create genedxai
gcloud config set project genedxai
```

2. **Enable Required APIs**
```bash
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

3. **Build and Push Image**
```bash
# Configure Docker authentication
gcloud auth configure-docker gcr.io

# Build image
docker build -t gcr.io/genedxai/app .

# Push to Container Registry
docker push gcr.io/genedxai/app
```

4. **Set Environment Variables**
```bash
gcloud secrets create OPENROUTER_API_KEY --data-file=-
gcloud secrets create MONGODB_URI --data-file=-
```

5. **Deploy to Cloud Run**
```bash
gcloud run deploy genedxai \
  --image gcr.io/genedxai/app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "OPENROUTER_API_KEY=sk-or-xxx,MONGODB_URI=mongodb+srv://xxx"
```

---

## Option 6: AWS EC2 with Nginx

Full control with traditional server setup.

### Prerequisites
- AWS account
- EC2 instance (Ubuntu 20.04)
- Domain name (optional)

### Setup Steps

1. **SSH into EC2 Instance**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

2. **Update System**
```bash
sudo apt update
sudo apt upgrade -y
```

3. **Install Dependencies**
```bash
sudo apt install -y python3 python3-pip nginx
```

4. **Clone Repository**
```bash
cd /home/ubuntu
git clone https://github.com/yourusername/GenEDxAI.git
cd GenEDxAI
```

5. **Setup Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Configure Environment**
```bash
echo 'OPENROUTER_API_KEY=your_key' >> .env
echo 'MONGODB_URI=your_uri' >> .env
```

7. **Setup Systemd Service**
```bash
sudo nano /etc/systemd/system/genedxai.service
```

Add:
```ini
[Unit]
Description=GenEDxAI Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/GenEDxAI
Environment="PATH=/home/ubuntu/GenEDxAI/venv/bin"
ExecStart=/home/ubuntu/GenEDxAI/venv/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

8. **Start Service**
```bash
sudo systemctl daemon-reload
sudo systemctl enable genedxai
sudo systemctl start genedxai
```

9. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/genedxai
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /_stcore/stream {
        proxy_pass http://127.0.0.1:8501/_stcore/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

10. **Enable Site**
```bash
sudo ln -s /etc/nginx/sites-available/genedxai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Environment Variables Reference

| Variable | Required | Example |
|----------|----------|---------|
| `OPENROUTER_API_KEY` | Yes | `sk-or-v1-xxxx` |
| `MONGODB_URI` | Yes | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `GEMINI_API_KEY` | No | `AIzaSyxxxx` |

## Security Checklist

- ✅ `.env` file is in `.gitignore`
- ✅ API keys stored in environment secrets (not hardcoded)
- ✅ HTTPS enabled (if using custom domain)
- ✅ API key rotated regularly
- ✅ Database connection uses strong password
- ✅ Firewall rules configured
- ✅ MongoDB IP whitelist configured
- ✅ Application CORS headers properly set
- ✅ Session timeout configured
- ✅ Rate limiting enabled

## Monitoring & Maintenance

### View Logs
```bash
# Streamlit Cloud
# Available in dashboard

# Docker
docker logs container-id

# Heroku
heroku logs --tail

# AWS EC2
sudo tail -f /var/log/auth.log
```

### Update Application
```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
pip install -r requirements.txt

# Restart service (if using systemd)
sudo systemctl restart genedxai
```

### Database Backups
```bash
# Export MongoDB
mongodump --uri "mongodb+srv://user:pass@cluster.mongodb.net/edu_chatbot" --out ./backup

# Restore MongoDB
mongorestore --uri "mongodb+srv://user:pass@cluster.mongodb.net/edu_chatbot" ./backup
```

## Troubleshooting

### App Not Starting
```
Check logs:
- docker logs
- heroku logs --tail
- journalctl -u genedxai -f

Common causes:
- Missing environment variables
- Port already in use
- Database connection failure
```

### Slow Performance
```
Solutions:
- Enable caching in MongoDB
- Optimize database queries
- Use CDN for static files
- Scale horizontally (more instances)
```

### High Memory Usage
```
Solutions:
- Reduce cache size in Streamlit
- Clear old chat history periodically
- Optimize data structures
- Use pagination for results
```

## Recommended Deployment

**For Production**: Streamlit Cloud (easiest) or Docker on AWS ECS (most scalable)

**For Development**: Local with Streamlit

**For Learning**: Heroku Free Tier (limited but free)

---

**Need Help?** 
- GitHub Issues: https://github.com/rakeshkolipakaace/GenEDxAI/issues
- Streamlit Forums: https://discuss.streamlit.io
- Stack Overflow: Tag with `streamlit`
