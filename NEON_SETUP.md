# BlurDetect - Neon PostgreSQL Setup Guide

Complete step-by-step guide to setting up BlurDetect with Neon serverless PostgreSQL.

## What is Neon?

Neon is a fully managed, serverless PostgreSQL database platform that offers:
- ✅ Automatic scaling
- ✅ Connection pooling
- ✅ Instant provisioning
- ✅ Per-compute billing
- ✅ Built-in backups
- ✅ Free tier available

**Official Site**: https://neon.tech

---

## Step 1: Create Neon Account

### 1.1 Sign Up
1. Visit **https://console.neon.tech/signin** (or https://neon.tech for sign up)
2. Click **Sign Up** 
3. Choose one of the following:
   - Sign up with GitHub
   - Sign up with Google
   - Sign up with email

### 1.2 Verify Account
- Check your email for verification link
- Click the link to verify your account

---

## Step 2: Create Neon Project

### 2.1 Create Project
1. Go to **https://console.neon.tech**
2. Click **+ New Project** button
3. Enter project details:
   - **Project Name**: `blurdetect` (or your preferred name)
   - **Database Name**: `blurdetect` (will be created automatically)
   - **Region**: Choose closest to your location
   - **Postgres Version**: 16 (latest recommended)

### 2.2 Create Database
4. Click **Create Project**
5. Wait for project to be created (1-2 minutes)
6. You'll see the project dashboard

---

## Step 3: Get Connection String

### 3.1 Find Connection String
1. In Neon Console, navigate to your project
2. Click **Connection string** or **Integrations** tab
3. You'll see different connection strings:

```
# Full Connection String (use this)
postgresql://neon_user:abcd1234xyz@ep-cool-lake-123456.us-east-1.neon.tech/blurdetect

# URL Format
postgres://neon_user:abcd1234xyz@ep-cool-lake-123456.us-east-1.neon.tech/blurdetect

# psql Command (for testing)
psql postgresql://neon_user:abcd1234xyz@ep-cool-lake-123456.us-east-1.neon.tech/blurdetect
```

### 3.2 Connection String Parts

```
postgresql://[user]:[password]@[host]/[database]
             └─────────────────────────────────────┘
                    Connection String

postgresql://  ← Protocol
neon_user      ← Username
abcd1234xyz    ← Password
@              ← Separator
ep-cool-lake-123456.us-east-1.neon.tech  ← Host (endpoint)
/blurdetect    ← Database name
```

**Copy the full connection string** - you'll need it in the next step.

---

## Step 4: Configure BlurDetect

### 4.1 Update .env File

1. Open `.env` file in BlurDetect project root:
   ```
   /vercel/share/v0-project/.env
   ```

2. Find the line:
   ```
   DATABASE_URL=postgresql://neon_user:password@ep-xyz.us-east-1.neon.tech/blurdetect
   ```

3. Replace with your **actual Neon connection string**:
   ```
   DATABASE_URL=postgresql://neon_user:abcd1234xyz@ep-cool-lake-123456.us-east-1.neon.tech/blurdetect
   ```

4. Verify other settings:
   ```
   MAIL_USERNAME=aldwin.hamilit44@gmail.com
   MAIL_PASSWORD=krvfmfxbtdopqjxj
   SECRET_KEY=AldwinJohn231
   FLASK_ENV=development
   ```

5. **Save the file**

### 4.2 Verify Configuration

Check that your `.env` looks like this:
```env
DATABASE_URL=postgresql://neon_user:abcd1234xyz@ep-cool-lake-123456.us-east-1.neon.tech/blurdetect
MAIL_USERNAME=aldwin.hamilit44@gmail.com
MAIL_PASSWORD=krvfmfxbtdopqjxj
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=AldwinJohn231
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
SERVER_URL=http://localhost:5000
```

---

## Step 5: Install Dependencies

### 5.1 Create Virtual Environment
```bash
cd /vercel/share/v0-project
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 5.2 Install Requirements
```bash
pip install -r requirements.txt
```

**Expected packages installed:**
- Flask 3.1.3
- Flask-SQLAlchemy 3.1.1
- psycopg2-binary 2.9.12 (PostgreSQL driver)
- OpenCV 4.13.0.92
- TensorFlow 2.21.0
- NumPy 2.4.3
- SciPy 1.17.1
- ... and others

---

## Step 6: Initialize Database

### 6.1 Create Tables

Run the database initialization script:
```bash
python init_db.py
```

**This will:**
1. Connect to your Neon database
2. Create 5 tables:
   - `users` - User accounts and authentication
   - `images` - Uploaded images
   - `detection_results` - Blur detection results
   - `model_comparisons` - All 5 model results
   - `system_events` - Activity logging

**Expected Output:**
```
Connected to Neon PostgreSQL
Creating database tables...
Database initialized successfully!
Tables created:
  ✓ users
  ✓ images
  ✓ detection_results
  ✓ model_comparisons
  ✓ system_events
```

### 6.2 Verify in Neon Console

1. Go to **https://console.neon.tech**
2. Click on your project
3. Click **SQL Editor** or **Web console**
4. Run:
   ```sql
   \dt
   ```
5. You should see 5 tables listed

---

## Step 7: Run BlurDetect

### 7.1 Start Flask Application
```bash
python app.py
```

**Expected Output:**
```
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * WARNING: This is a development server. Do not use it in production.
 * Press CTRL+C to quit
```

### 7.2 Access Application
Open your browser and visit:
```
http://localhost:5000
```

You should see the **BlurDetect login page**.

---

## Step 8: Test Application

### 8.1 Create Account
1. Click **Register**
2. Enter:
   - **Username**: `testuser`
   - **Email**: `your-email@gmail.com`
   - **Password**: Create a strong password
3. Click **Register**

### 8.2 Verify Email
1. Check your email inbox
2. Click the verification link
3. You should be redirected to login page

### 8.3 Login
1. Enter your email and password
2. Click **Login**
3. You should see the **Dashboard**

### 8.4 Test Blur Detection
1. Click **Upload Image**
2. Drag and drop an image or click to browse
3. Select an image (PNG, JPG, GIF, BMP, or WebP)
4. Click **Analyze Image**
5. Wait for results (should take < 1 second)
6. View blur type detection from 5 models

---

## Neon Connection Management

### Connection Pooling

Neon automatically provides connection pooling. No additional configuration needed.

### Monitoring Connections

In Neon Console:
1. Go to **Monitoring** tab
2. View:
   - Active connections
   - Database size
   - Query performance
   - Storage usage

### Scale Resources

If you need more computing power:
1. Go to **Settings** → **Compute**
2. Choose compute size:
   - Small (included in free tier)
   - Large (for production)
3. Changes are applied automatically

---

## Troubleshooting

### Issue: "Connection refused" Error

**Cause**: DATABASE_URL is incorrect

**Solution**:
1. Copy connection string from Neon Console
2. Paste into `.env` file
3. Ensure no extra spaces or characters
4. Check username and password are correct

**Example of correct format:**
```
DATABASE_URL=postgresql://neon_user:abcd1234xyz@ep-cool-lake-123456.us-east-1.neon.tech/blurdetect
```

### Issue: "authentication failed" Error

**Cause**: Wrong password

**Solution**:
1. Go to Neon Console
2. Click **Settings** → **Security**
3. Click **Reset password**
4. Create new password
5. Update `.env` with new password

### Issue: "relation 'users' does not exist" Error

**Cause**: Tables not created in database

**Solution**:
```bash
python init_db.py
```

Then verify with Neon SQL Editor:
```sql
SELECT * FROM information_schema.tables;
```

### Issue: Slow Database Queries

**Solution**:
1. In Neon, upgrade compute size
2. Enable query statistics in Settings
3. Check for missing indexes
4. Verify connection pooling is enabled

### Issue: "too many connections" Error

**Cause**: Connection pool exhausted

**Solution**:
1. Check running Flask instances
2. Restart Flask app
3. In production, use Gunicorn with worker limit:
   ```bash
   gunicorn --workers 4 app:app
   ```

---

## Production Deployment

### For Vercel Deployment

1. Go to **Vercel.com**
2. Import your GitHub repository
3. Go to **Settings** → **Environment Variables**
4. Add:
   ```
   DATABASE_URL = postgresql://neon_user:password@ep-xyz.us-east-1.neon.tech/blurdetect
   MAIL_USERNAME = aldwin.hamilit44@gmail.com
   MAIL_PASSWORD = krvfmfxbtdopqjxj
   SECRET_KEY = your-secret-key
   FLASK_ENV = production
   ```
5. Deploy

### For Self-Hosted

1. Use Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn --workers 4 --threads 2 app:app
   ```

2. Use Nginx as reverse proxy

3. Enable SSL/HTTPS

4. Set `FLASK_ENV=production`

### For Production Neon Database

1. In Neon Console:
   - Enable **IP Whitelisting**
   - Set up **Read Replicas** (optional)
   - Enable **Backups**

2. In `.env`:
   ```
   FLASK_ENV=production
   SECRET_KEY=generate-strong-secret-key
   DATABASE_URL=postgresql://prod_user:strong_password@ep-xyz.us-east-1.neon.tech/blurdetect
   ```

---

## Useful Neon Commands

### Access Database via psql

```bash
# Using connection string from Neon Console
psql postgresql://neon_user:password@ep-xyz.us-east-1.neon.tech/blurdetect

# Inside psql, useful commands:
\dt                    # List all tables
\d users               # Describe users table
SELECT COUNT(*) FROM users;  # Count users
\q                     # Exit psql
```

### SQL Queries via Web Console

In Neon Console → **SQL Editor**:

```sql
-- View all users
SELECT * FROM users;

-- View recent analyses
SELECT * FROM detection_results ORDER BY detected_at DESC LIMIT 10;

-- Count blur types
SELECT blur_type, COUNT(*) as count FROM detection_results GROUP BY blur_type;

-- View system events
SELECT * FROM system_events ORDER BY timestamp DESC LIMIT 20;
```

---

## Neon Pricing

### Free Tier (Always Available)
- ✅ 1 project
- ✅ 500 MB storage
- ✅ Compute hours (small)
- ✅ Perfect for development

### Paid Tiers (as needed)
- ✅ Additional projects: $14/month each
- ✅ Extra storage: Pay per GB
- ✅ Large compute: Pay per compute hour

**No credit card required for free tier!**

---

## Next Steps

1. ✅ Create Neon account
2. ✅ Create Neon project
3. ✅ Get connection string
4. ✅ Update `.env` file
5. ✅ Install dependencies
6. ✅ Initialize database
7. ✅ Run Flask app
8. ✅ Test application
9. Deploy to production (optional)

---

## Additional Resources

- **Neon Docs**: https://neon.tech/docs
- **Neon API**: https://neon.tech/docs/api-reference
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Flask-SQLAlchemy**: https://flask-sqlalchemy.palletsprojects.com/
- **BlurDetect README**: See README.md

---

## Support

- **BlurDetect Issues**: aldwin.hamilit44@gmail.com
- **Neon Support**: support@neon.tech
- **GitHub Issues**: https://github.com/Aldwinzzz/BlurDetect/issues

---

## Checklist

Before deployment, verify:

- [ ] Neon account created
- [ ] Neon project created
- [ ] Connection string copied
- [ ] `.env` file updated with Neon connection string
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database initialized (`python init_db.py`)
- [ ] Flask app runs successfully (`python app.py`)
- [ ] Can register and login
- [ ] Can upload and analyze images
- [ ] Blur detection works with 5 models
- [ ] System events are logged
- [ ] No database connection errors

---

**BlurDetect with Neon PostgreSQL Setup Complete!** 🚀

Your application is now powered by Neon's serverless PostgreSQL database.
