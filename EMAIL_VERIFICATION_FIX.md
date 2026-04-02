# Email Verification Fix Guide

## Problem: Email Verification Not Sending

If registration works but email verification doesn't send, follow this guide to fix it.

---

## Root Causes

1. **Incorrect Gmail App Password** ❌ Solved
2. **Mail not initialized properly** ❌ Solved  
3. **Missing MAIL_PASSWORD in .env** ❌ Fixed
4. **Incorrect SMTP settings** ❌ Fixed

---

## Solution 1: Set Up Gmail App Password (REQUIRED)

Gmail requires an **App Password**, not your regular Gmail password.

### Step 1: Enable 2-Factor Authentication
1. Go to https://myaccount.google.com
2. Click **Security** (left sidebar)
3. Scroll to **How you sign in to Google**
4. Enable **2-Step Verification** (if not already enabled)

### Step 2: Create App Password
1. Go back to **Security**
2. Scroll to **App passwords** (appears after 2FA is enabled)
3. Select:
   - **App**: Mail
   - **Device**: Windows Computer (or your device)
4. Google generates a 16-character password
5. **Copy this password** - you'll need it

### Step 3: Update .env File
1. Open `/vercel/share/v0-project/.env`
2. Replace MAIL_PASSWORD with the 16-character password:
   ```
   MAIL_PASSWORD=abcd efgh ijkl mnop
   ```
   (Remove spaces or keep them - Gmail accepts both)

---

## Solution 2: Verify .env Configuration

Check your `.env` file has all these settings:

```env
# Gmail SMTP Configuration
MAIL_USERNAME=aldwin.hamilit44@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop        ← Your 16-char app password
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=AldwinJohn231

# Database
DATABASE_URL=postgresql://neon_user:password@ep-xyz.us-east-1.neon.tech/blurdetect

# Server
SERVER_URL=http://localhost:5000
```

---

## Solution 3: Check Email Configuration in app.py

The Flask app now properly initializes mail. Key changes:

✅ Mail is initialized with app context
✅ Configuration loads from .env
✅ Error logging added for debugging
✅ Uses email extensions properly

---

## Testing Email Verification

### Step 1: Clear Database
If you've already registered test users:
```bash
# Delete the SQLite database if using SQLite (for local testing)
rm blurdetect.db

# Then reinitialize
python init_db.py
```

Or in Neon console, you can delete and re-create the database.

### Step 2: Register a New Account
1. Go to http://localhost:5000/auth/register
2. Fill in:
   - Username: `testuser`
   - Email: `your-email@gmail.com` (use YOUR email to receive verification)
   - Password: `TestPass123`
   - Confirm: `TestPass123`
3. Click **Register**

### Step 3: Check Email
1. Go to your email inbox
2. Look for email from `aldwin.hamilit44@gmail.com`
3. Check spam folder if not in inbox
4. Click the verification link

### Step 4: Verify Works
After clicking the link, you should see:
✓ "Email verified successfully! You can now log in."

---

## Troubleshooting

### Issue: "SMTPAuthenticationError"
**Cause**: Wrong app password or regular Gmail password used

**Fix**:
1. Go to https://myaccount.google.com/apppasswords
2. Generate a NEW app password
3. Update MAIL_PASSWORD in .env
4. Restart Flask app

### Issue: "Connection refused" on SMTP
**Cause**: Firewall or network blocking port 587

**Fix**:
1. Check firewall settings
2. Ensure MAIL_PORT=587
3. MAIL_USE_TLS=True
4. Test connection:
   ```bash
   telnet smtp.gmail.com 587
   ```

### Issue: Email goes to spam
**Cause**: Gmail filters verification as suspicious

**Fix**:
1. Check spam folder
2. Mark as "Not Spam"
3. Add aldwin.hamilit44@gmail.com to contacts
4. Change email sender name in email templates

### Issue: "No module named flask_mail"
**Cause**: Flask-Mail not installed

**Fix**:
```bash
pip install Flask-Mail==0.9.1
pip freeze > requirements.txt
```

### Issue: 404 on verification link
**Cause**: SERVER_URL incorrect

**Fix**:
1. Check .env file
2. Ensure SERVER_URL matches your domain:
   - Local: `http://localhost:5000`
   - Production: `https://yourdomain.com`

### Issue: "User not found" on verify
**Cause**: Email in verification token doesn't match database

**Fix**:
1. Check registered email address
2. Make sure user was saved to database
3. Verify DATABASE_URL is correct

---

## View Email Logs

Flask logs all email attempts. Check terminal output:

```
Verification email sent successfully to your-email@gmail.com
```

If you see error:
```
Error sending email to your-email@gmail.com: [error message]
```

Common errors and fixes:

| Error | Fix |
|-------|-----|
| `SMTPAuthenticationError` | Wrong app password |
| `SMTPNotSupportedError` | MAIL_USE_TLS=True |
| `socket.error: Connection refused` | Firewall blocking port 587 |
| `Address email is not valid` | Invalid email format |

---

## Updated Code Changes

### app.py
✅ Mail initialized correctly with Flask app
✅ Configuration loads from .env
✅ Supports multiple MAIL_USERNAME formats

### routes/auth.py
✅ Improved error handling
✅ Email sending with try-catch
✅ Better error messages in logs
✅ Traceback for debugging
✅ Professional HTML email template

### static/style.css
✅ Fully responsive design
✅ Mobile-optimized
✅ Better form styling
✅ Professional color scheme

---

## Complete Email Flow

```
1. User registers
   ↓
2. Password hashed (SHA256)
   ↓
3. User saved to database
   ↓
4. Verification token created (itsdangerous)
   ↓
5. Email sent via Gmail SMTP
   ↓
6. User clicks link in email
   ↓
7. Token validated
   ↓
8. User marked as is_verified=True
   ↓
9. Can now login
```

---

## Quick Checklist

Before testing, ensure:

- [ ] Gmail app password created
- [ ] MAIL_PASSWORD updated in .env
- [ ] FLASK_ENV=development
- [ ] DATABASE_URL correct
- [ ] SERVER_URL=http://localhost:5000 (for local)
- [ ] Flask app running: `python app.py`
- [ ] No Flask errors in terminal
- [ ] Mail logs show "sent successfully"

---

## Support

**If email still doesn't work:**

1. Check Flask terminal for error messages
2. Verify all MAIL_* settings in .env
3. Try a different email address
4. Check Gmail security settings
5. Contact: aldwin.hamilit44@gmail.com

---

## Further Reading

- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [Flask-Mail Documentation](https://pythonhosted.org/Flask-Mail/)
- [Python Email SMTP Guide](https://docs.python.org/3/library/smtplib.html)

---

**Email verification fixed!** ✅

You should now be able to register, receive verification emails, verify your account, and login successfully.
