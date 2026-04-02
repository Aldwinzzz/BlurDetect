# BlurDetect Setup Guide

Complete step-by-step guide to set up and run the BlurDetect application.

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
Ensure `.env` file is configured with:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///blurdetect.db
MAIL_USERNAME=aldwin.hamilit44@gmail.com
MAIL_PASSWORD=krvfmfxbtdopqjxj
```

### 3. Initialize Database
```bash
python init_db.py
```

### 4. Run Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## Detailed Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Aldwinzzz/BlurDetect.git
cd BlurDetect
```

### Step 2: Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Requirements
```bash
pip install -r requirements.txt
```

This installs:
- Flask and extensions (SQLAlchemy, Mail)
- Computer vision libraries (OpenCV, NumPy, SciPy)
- Deep learning frameworks (TensorFlow, Keras)

### Step 4: Configure Environment Variables

Create/Update `.env` file:
```
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this-in-production

# Database
DATABASE_URL=sqlite:///blurdetect.db

# Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=aldwin.hamilit44@gmail.com
MAIL_PASSWORD=krvfmfxbtdopqjxj

# Upload Settings
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
```

### Step 5: Initialize Database

Run the initialization script:
```bash
python init_db.py
```

Or manually initialize in Python:
```python
from app import app, db

with app.app_context():
    db.create_all()
```

### Step 6: Start the Application

```bash
python app.py
```

The application will be available at:
- **Local:** http://localhost:5000
- **Network:** http://your-machine-ip:5000

---

## First-Time Usage

### Create Your Account
1. Navigate to http://localhost:5000
2. Click "Register"
3. Fill in username, email, and password
4. Check your email for verification link
5. Verify your email by clicking the link
6. Log in with your credentials

### Upload and Analyze Images
1. Click "Upload" in the dashboard
2. Drag and drop an image or click to browse
3. Click "Analyze Image"
4. Wait for analysis to complete
5. View results with confidence scores

### View History and Events
- **History:** Access all previous analyses
- **Events:** Track your account activities
- **Dashboard:** View statistics and recent uploads

---

## Email Configuration

### Gmail Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Google Account
2. **Generate App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or your device)
   - Generate password
   - Copy the 16-character password

3. **Update .env:**
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-char-app-password
   ```

### Other Email Providers

For non-Gmail providers, update:
```
MAIL_SERVER=your-smtp-server
MAIL_PORT=587 or 465
MAIL_USE_TLS=True or False
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-password
```

---

## Database Management

### Create Database
```bash
python init_db.py
```

### Reset Database
```bash
# Delete the database file
rm blurdetect.db

# Reinitialize
python init_db.py
```

### Database Location
- **Development:** `blurdetect.db` (SQLite file in project root)
- **Production:** Set `DATABASE_URL` environment variable

### Backup Database
```bash
# Create backup
cp blurdetect.db blurdetect_backup.db

# Restore from backup
cp blurdetect_backup.db blurdetect.db
```

---

## Troubleshooting

### Issue: Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process and restart
```

### Issue: Email Not Sending
1. Check MAIL_USERNAME and MAIL_PASSWORD in .env
2. Verify SMTP server settings
3. Check email logs: `tail -f *.log`
4. Test email configuration:
   ```python
   from app import app, mail
   from flask_mail import Message
   
   with app.app_context():
       msg = Message('Test', recipients=['test@example.com'])
       mail.send(msg)
   ```

### Issue: Database Errors
1. Delete `blurdetect.db` file
2. Run `python init_db.py` again
3. Restart the application

### Issue: Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or use a fresh virtual environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Images Not Processing
1. Check uploads folder permissions
2. Verify image format (PNG, JPG, GIF, BMP, WebP)
3. Check file size (< 16MB)
4. Review error logs

---

## Development Workflow

### Run in Debug Mode
```bash
FLASK_ENV=development python app.py
```

### Enable Flask Debug Toolbar (Optional)
```bash
pip install flask-debugtoolbar
```

### Database Migrations (Future)
For production, use Alembic:
```bash
pip install flask-migrate
flask db init
flask db migrate
flask db upgrade
```

### Run Tests
```bash
pytest tests/
```

---

## Production Deployment

### Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=generate-a-long-random-string
DATABASE_URL=postgresql://user:pass@host/dbname
```

### Use Production WSGI Server
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Reverse Proxy (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL/TLS
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with SSL
python app.py --cert=cert.pem --key=key.pem
```

---

## File Structure
```
blurdetect/
├── app.py                    # Main Flask app
├── models.py                # Database models
├── blur_models.py           # Detection algorithms
├── auth_utils.py            # Auth helpers
├── email_utils.py           # Email helpers
├── routes_auth.py           # Auth routes
├── routes_detection.py      # Detection routes
├── routes_dashboard.py      # Dashboard routes
├── config.py                # Configuration
├── init_db.py              # Database setup
├── requirements.txt         # Dependencies
├── .env                     # Environment variables
├── .gitignore              # Git ignore rules
├── templates/              # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── results.html
│   ├── history.html
│   ├── events.html
│   ├── profile.html
│   ├── system_events.html
│   ├── 404.html
│   └── 500.html
├── static/                 # Static files
│   ├── style.css
│   └── script.js
├── uploads/               # User images
└── README.md             # Project documentation
```

---

## Common Commands

```bash
# Start development server
python app.py

# Initialize database
python init_db.py

# Install all dependencies
pip install -r requirements.txt

# Freeze current dependencies
pip freeze > requirements.txt

# Format code (optional)
pip install black
black *.py

# Lint code (optional)
pip install pylint
pylint *.py
```

---

## Performance Tips

1. **Database:** Add indexes for frequently queried fields
2. **Images:** Compress uploaded images
3. **Cache:** Cache model predictions
4. **CDN:** Serve static files from CDN
5. **Monitoring:** Log slow requests

---

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Set secure session cookies
- [ ] Validate all user inputs
- [ ] Use environment variables for secrets
- [ ] Enable database backups
- [ ] Monitor access logs
- [ ] Keep dependencies updated

---

## Support & Resources

- **Documentation:** See README.md
- **Issues:** GitHub Issues page
- **Email:** aldwin.hamilit44@gmail.com
- **Requirements:** Python 3.8+, Flask 3.0+

---

## Version Information

- **Python:** 3.8+
- **Flask:** 3.0.0
- **Database:** SQLite (development), PostgreSQL (production)
- **Last Updated:** 2024

---

Happy coding with BlurDetect!
