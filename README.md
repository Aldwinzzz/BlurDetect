# BlurDetect - Professional Blur Type Detection System

A sophisticated Flask web application that detects and classifies five different types of blur in images using advanced computer vision techniques.

## Features

✨ **Advanced Blur Detection**
- Gaussian Blur Detection
- Motion Blur Detection  
- Defocus Blur Detection
- Lens Blur Detection
- Sharp Image Classification

🔐 **Secure User Authentication**
- User registration and login system
- Email verification for new accounts
- SHA512 password hashing
- Session-based authentication

📊 **5 Different Detection Models**
1. Laplacian Variance + FFT Frequency Analysis (Hybrid) - Primary Model
2. Sobel Directional Gradient Analysis
3. FFT Power Spectrum Classification
4. Blind Deconvolution PSF Estimation
5. Deep Learning CNN Classifier (TensorFlow/Keras)

📈 **Comprehensive Dashboard**
- User statistics and analysis history
- Blur type distribution visualization
- Recent uploads tracking
- Detailed detection results with confidence scores

📧 **Email Notifications**
- Email verification on registration
- Password reset functionality
- Professional email templates

📝 **System Events Logging**
- Track all user actions (registration, login, logout)
- Log all image uploads and analysis
- Monitor failed login attempts
- Complete audit trail

🎨 **Professional UI/UX**
- Modern Bootstrap 5 design
- Responsive across all devices
- Drag-and-drop file upload
- Real-time analysis progress
- Interactive data visualization

## Project Structure

```
blurdetect/
├── app.py                  # Main Flask application
├── models.py              # SQLAlchemy database models
├── blur_models.py         # 5 blur detection algorithms
├── auth_utils.py          # Authentication utilities
├── email_utils.py         # Email sending functionality
├── routes_auth.py         # Authentication routes
├── routes_detection.py    # Image detection routes
├── routes_dashboard.py    # Dashboard routes
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
├── templates/             # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── upload.html       # Image upload page
│   ├── results.html      # Detection results page
│   ├── history.html      # Analysis history page
│   ├── events.html       # User events page
│   ├── profile.html      # User profile page
│   ├── system_events.html # System events log
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
├── uploads/              # User uploaded images directory
└── static/               # Static files directory
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Step 1: Clone Repository
```bash
git clone https://github.com/Aldwinzzz/BlurDetect.git
cd BlurDetect
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
Edit `.env` file with your settings:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///blurdetect.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Step 5: Initialize Database
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Step 6: Run Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Usage

### Registration & Login
1. Click "Register" to create a new account
2. Enter username, email, and password
3. Verify your email via the confirmation link
4. Login with your credentials

### Uploading Images
1. Click "Upload" in the dashboard
2. Drag and drop an image or click to browse
3. Click "Analyze Image" to process

### Viewing Results
- See the primary blur type with confidence score
- Review explanations for detected blur types
- Compare results from all 5 detection models
- View processing time for each model

### Tracking History
- Access "History" to view all previous analyses
- Filter by blur type
- Re-analyze previous images

### System Events
- Track your account activities
- View login/logout events
- Monitor image uploads and detections

## Blur Detection Models

### Model 1: Laplacian + FFT Hybrid (Selected Primary)
Combines spatial and frequency domain analysis:
- Laplacian variance identifies overall blur level
- FFT spectrum distinguishes blur type
- No training data required
- Fast real-time inference

### Model 2: Sobel Directional Gradient
Analyzes directional gradients:
- Identifies horizontal vs vertical motion blur
- Compares gradient magnitudes
- Effective for motion detection

### Model 3: FFT Power Spectrum
Analyzes frequency domain characteristics:
- Detects directional streaks (motion)
- Identifies circular drop-off (Gaussian/Defocus)
- Measures high-frequency richness (sharpness)

### Model 4: Blind Deconvolution
Estimates Point Spread Function:
- Circular PSF = Defocus/Lens Blur
- Linear PSF = Motion Blur
- Gaussian PSF = Gaussian Blur

### Model 5: Deep Learning CNN
TensorFlow/Keras based classification:
- MobileNetV2 backbone
- Trained on blur type dataset
- Provides probability distribution

## Database Schema

### Users Table
- id, username, email, password (SHA512), email_verified, verification_token, created_at

### Images Table
- id, user_id, filename, upload_path, uploaded_at

### Detection Results Table
- id, image_id, user_id, model_used, blur_type, confidence, blur_score, explanation, processing_time, detected_at

### Model Comparisons Table
- id, image_id, model_name, blur_type, confidence, processing_time, ran_at

### System Events Table
- id, event_type, user_id, message, details (JSON), timestamp

## Supported Image Formats
- PNG
- JPG/JPEG
- GIF
- BMP
- WebP

Maximum file size: 16 MB

## Security Features

🔒 **Password Security**
- SHA512 hashing algorithm
- No plain-text password storage
- Secure session management

🔐 **Email Verification**
- Required for account activation
- Time-limited verification tokens
- Prevents spam registrations

📊 **Input Validation**
- File type validation
- File size restrictions
- XSS protection via template escaping

## Performance Optimization

- Image caching for re-analysis
- Optimized model inference
- Database indexing on frequently queried fields
- CDN-ready static files

## Troubleshooting

### Email Not Sending
1. Check MAIL_USERNAME and MAIL_PASSWORD in .env
2. Enable "Less secure app access" for Gmail
3. Use app-specific passwords for Gmail accounts
4. Check spam/junk folder

### Images Not Analyzing
1. Verify upload folder permissions
2. Check file format (must be PNG, JPG, GIF, BMP, or WebP)
3. Ensure file size < 16 MB
4. Check server logs for errors

### Database Errors
1. Delete blurdetect.db to reset database
2. Re-run database initialization
3. Check database file permissions

## API Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout
- `GET /dashboard` - User dashboard
- `POST /detection/upload` - Upload image
- `GET /detection/analyze/<image_id>` - Analyze image
- `GET /detection/history` - View history
- `GET /events` - View user events
- `GET /auth/profile` - View profile

## Environment Variables

- `FLASK_APP` - Flask application file
- `FLASK_ENV` - Environment (development/production)
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database connection string
- `MAIL_SERVER` - SMTP server address
- `MAIL_PORT` - SMTP server port
- `MAIL_USE_TLS` - Use TLS encryption
- `MAIL_USERNAME` - Email sender username
- `MAIL_PASSWORD` - Email sender password
- `UPLOAD_FOLDER` - Directory for uploaded images
- `MAX_CONTENT_LENGTH` - Maximum upload size in bytes

## Dependencies

Core:
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Mail 0.9.1
- Werkzeug 3.0.1
- python-dotenv 1.0.0

Computer Vision:
- opencv-python 4.8.1.78
- numpy 1.24.3
- scikit-image 0.21.0
- scipy 1.11.4
- pillow 10.0.1

Deep Learning:
- tensorflow 2.15.0
- keras 2.15.0

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: aldwin.hamilit44@gmail.com

## Changelog

### Version 1.0.0 (Current)
- Initial release
- 5 blur detection models
- Email verification system
- Complete user dashboard
- System events logging
- Professional UI/UX

---

**BlurDetect** - Professional Blur Type Detection System
Built with Flask, OpenCV, and TensorFlow
