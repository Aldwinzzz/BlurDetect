# BlurDetect - Professional Blur Type Detection System

A sophisticated Flask web application that detects and classifies five different types of blur in images using advanced computer vision techniques and machine learning models.

## Features

### Core Functionality
- **5 Blur Type Detection**: Gaussian, Motion, Defocus, Lens, and Sharp image classification
- **5 Advanced Detection Models**: Each using different computer vision techniques
- **Model Comparison**: Side-by-side analysis from all 5 models
- **Confidence Scoring**: Detailed confidence metrics for each detection

### User Features
- User registration and email verification
- Secure SHA256 password hashing
- Session-based authentication
- User dashboard with statistics
- Analysis history with pagination
- System events logging and tracking

### Technical Stack
- **Backend**: Flask 3.1.3 (Python)
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy 3.1.1
- **Computer Vision**: OpenCV 4.13.0.92
- **Scientific Computing**: NumPy 2.4.3, SciPy 1.17.1
- **Deep Learning**: TensorFlow 2.21.0
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Email**: Flask-Mail 0.9.1 with Gmail SMTP
- **Authentication**: Flask-Login 0.6.3, itsdangerous 2.1.2

## Installation & Setup

### Requirements
- Python 3.9+
- PostgreSQL (Supabase instance)
- pip package manager

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
Edit `.env` file with your Supabase credentials:
```
DATABASE_URL=postgresql://postgres:AldwinJohn231@db.vgstezkqpcqcoqbznzvg.supabase.co:5432/postgres
MAIL_USERNAME=Mail
MAIL_PASSWORD=krvfmfxbtdopqjxj
SECRET_KEY=AldwinJohn231
FLASK_APP=app.py
FLASK_ENV=development
```

### Step 5: Initialize Database
```bash
python init_db.py
```

### Step 6: Run Application
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Usage Guide

### Registration
1. Click "Register" on the login page
2. Enter username, email, and password
3. Check your email for verification link
4. Click the verification link to activate account

### Uploading Images
1. Log in to your account
2. Navigate to "Upload" page
3. Drag and drop an image or click to browse
4. Supported formats: PNG, JPG, JPEG, GIF, BMP, WebP
5. Maximum file size: 16 MB

### Viewing Results
1. After upload, the system runs all 5 models
2. Primary result (Model 1) is displayed prominently
3. View confidence score and explanation
4. Compare all 5 models side-by-side

## Detection Models

### Model 1 — Hybrid Laplacian + FFT (Primary) ⭐
Combines spatial and frequency domain analysis for fast, accurate detection.

### Model 2 — Sobel Directional Gradient
Analyzes gradient directions to detect motion blur patterns.

### Model 3 — FFT Power Spectrum
Analyzes frequency domain characteristics for blur classification.

### Model 4 — Blind Deconvolution PSF
Estimates Point Spread Function to identify blur type.

### Model 5 — Deep Learning CNN
TensorFlow-based feature extraction and classification.

## Supported Blur Types

- **Gaussian**: Uniform softness from out-of-focus capture
- **Motion**: Directional streaking from movement
- **Defocus**: Bokeh-like blur from shallow depth of field
- **Lens**: Optical distortion from lens imperfections
- **Sharp**: Clear image with no detectable blur

## System Events

The application logs all user activities:
- USER_REGISTERED, USER_VERIFIED, USER_LOGIN, USER_LOGOUT
- IMAGE_UPLOADED, BLUR_TYPE_DETECTED, SHARP_IMAGE
- LOGIN_FAILED

## Database Schema

5 tables optimized for blur detection and analysis:
- Users (with email verification)
- Images (uploaded files tracking)
- Detection Results (analysis outcomes)
- Model Comparisons (5-model comparison data)
- System Events (activity logging)

## Supported Image Formats
- PNG, JPG, JPEG, GIF, BMP, WebP
- Maximum file size: 16 MB

## Security Features
- SHA256 password hashing
- Email verification required
- Session-based authentication
- Input validation and sanitization
- CSRF protection

## Support
Email: aldwin.hamilit44@gmail.com
GitHub: https://github.com/Aldwinzzz/BlurDetect

## License
MIT License

---

**BlurDetect** — Advanced Blur Type Detection System v1.0.0
