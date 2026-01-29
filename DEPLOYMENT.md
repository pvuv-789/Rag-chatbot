# Deployment Guide

This guide covers deploying your RAG Chatbot to production.

## Pre-Deployment Checklist

- [ ] All features tested locally
- [ ] Environment variables configured
- [ ] Security review completed
- [ ] API rate limits understood
- [ ] Backup strategy planned
- [ ] Monitoring setup ready

## Deployment Options

### Option 1: Railway (Recommended for Beginners)

**Backend on Railway:**

1. Create account at [railway.app](https://railway.app)
2. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

3. Login and initialize:
   ```bash
   railway login
   cd backend
   railway init
   ```

4. Add environment variables in Railway dashboard:
   - `GEMINI_API_KEY`
   - `CHROMA_DB_PATH=/app/db`
   - `MODEL_NAME=gemini-1.5-flash`

5. Create `railway.json`:
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
       "healthcheckPath": "/health"
     }
   }
   ```

6. Deploy:
   ```bash
   railway up
   ```

**Frontend on Vercel:**

1. Create account at [vercel.com](https://vercel.com)
2. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

3. Deploy:
   ```bash
   cd frontend
   vercel
   ```

4. Set environment variable in Vercel dashboard:
   - `VITE_API_BASE_URL=https://your-backend-url.railway.app`

### Option 2: Docker Deployment

**Create Dockerfile for Backend:**

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p db documents

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Create Dockerfile for Frontend:**

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build application
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Create nginx.conf:**

```nginx
# frontend/nginx.conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```

**Create docker-compose.yml:**

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - CHROMA_DB_PATH=/app/db
      - MODEL_NAME=gemini-1.5-flash
    volumes:
      - backend_data:/app/db
      - backend_docs:/app/documents
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  backend_data:
  backend_docs:
```

**Deploy with Docker:**

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 3: AWS Deployment

**Backend on AWS Elastic Beanstalk:**

1. Install EB CLI:
   ```bash
   pip install awsebcli
   ```

2. Initialize:
   ```bash
   cd backend
   eb init -p python-3.11 rag-chatbot-backend
   ```

3. Create environment:
   ```bash
   eb create production
   ```

4. Set environment variables:
   ```bash
   eb setenv GEMINI_API_KEY=your_key
   ```

5. Deploy:
   ```bash
   eb deploy
   ```

**Frontend on AWS S3 + CloudFront:**

1. Build frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Upload to S3:
   ```bash
   aws s3 sync dist/ s3://your-bucket-name
   ```

3. Create CloudFront distribution pointing to S3 bucket

### Option 4: Traditional VPS (DigitalOcean, Linode, etc.)

**Backend Setup:**

```bash
# SSH into server
ssh user@your-server-ip

# Install Python
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Clone repository
git clone your-repo-url
cd rag-chatbot/backend

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
nano .env
# Add your environment variables

# Install and configure systemd service
sudo nano /etc/systemd/system/rag-backend.service
```

**Systemd Service File:**

```ini
[Unit]
Description=RAG Chatbot Backend
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/rag-chatbot/backend
Environment="PATH=/path/to/rag-chatbot/backend/venv/bin"
ExecStart=/path/to/rag-chatbot/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Start Service:**

```bash
sudo systemctl enable rag-backend
sudo systemctl start rag-backend
sudo systemctl status rag-backend
```

**Frontend with Nginx:**

```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs

# Build frontend
cd ../frontend
npm install
npm run build

# Install Nginx
sudo apt install nginx

# Configure Nginx
sudo nano /etc/nginx/sites-available/rag-chatbot
```

**Nginx Configuration:**

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/rag-chatbot/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

**Enable Site:**

```bash
sudo ln -s /etc/nginx/sites-available/rag-chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL/HTTPS Setup with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (certbot sets this up automatically)
sudo certbot renew --dry-run
```

## Production Configuration

### Backend Updates

**Use production ASGI server (Gunicorn):**

```bash
# Add to requirements.txt
gunicorn==21.2.0

# Run with Gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Update CORS for production:**

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-domain.com",
        "https://www.your-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Frontend Updates

**Update API URL:**

```javascript
// src/components/ChatBox.jsx
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.your-domain.com';
```

**Create production .env:**

```env
VITE_API_BASE_URL=https://api.your-domain.com
```

## Monitoring & Logging

### Backend Logging

```python
# Add to main.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Application Monitoring

**Option 1: Sentry**

```bash
pip install sentry-sdk[fastapi]
```

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
)
```

**Option 2: Prometheus**

```bash
pip install prometheus-fastapi-instrumentator
```

```python
from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)
```

## Database Backup

**Backup ChromaDB:**

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz db/
# Upload to S3 or storage service
```

**Automated backup with cron:**

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/backup-script.sh
```

## Performance Optimization

### Backend

1. **Use connection pooling**
2. **Implement caching (Redis)**
3. **Optimize vector search parameters**
4. **Use CDN for static assets**
5. **Enable gzip compression**

### Frontend

1. **Code splitting**
2. **Lazy loading components**
3. **Optimize images**
4. **Use CDN**
5. **Enable caching**

## Security Hardening

### Backend Security

```python
# Add rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/ask")
@limiter.limit("10/minute")
async def ask_question(request: Request, question: QuestionRequest):
    # ... existing code
```

### Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## Post-Deployment Testing

- [ ] Test PDF upload
- [ ] Test question answering
- [ ] Test error handling
- [ ] Load testing
- [ ] Security scanning
- [ ] SSL certificate verification
- [ ] Mobile responsiveness
- [ ] API rate limits
- [ ] Backup restoration

## Maintenance

### Regular Tasks

- Monitor API usage and costs
- Review logs for errors
- Update dependencies
- Backup database
- Monitor disk space
- Review security updates
- Performance optimization

### Updating the Application

```bash
# Backend
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart rag-backend

# Frontend
git pull
npm install
npm run build
sudo systemctl reload nginx
```

## Cost Estimation

### Gemini API Costs
- Embedding: ~$0.00001 per 1K characters
- Generation: ~$0.0001-$0.0005 per 1K tokens

### Hosting Costs (Monthly estimates)
- Railway: $5-20
- Vercel: $0-20 (depending on usage)
- AWS: $10-50
- VPS: $5-20

## Support & Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Deployment](https://react.dev/learn/start-a-new-react-project#deploying-to-production)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)

---

Choose the deployment option that best fits your needs and budget!
