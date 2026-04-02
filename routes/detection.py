from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models import db, Image, DetectionResult, ModelComparison, SystemEvent, User
from utils import BlurDetector, validate_image, get_blur_color
import os
from datetime import datetime

detection_bp = Blueprint('detection', __name__)


def is_logged_in():
    """Check if user is logged in and verified."""
    return 'user_id' in session


@detection_bp.before_request
def check_login():
    """Ensure user is logged in for protected routes."""
    protected_routes = ['upload', 'analyze', 'results', 'history']
    if request.endpoint and request.endpoint.split('.')[-1] in protected_routes:
        if not is_logged_in():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))


@detection_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """Image upload page and handler."""
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, GIF, BMP, WebP'}), 400
        
        try:
            # Create uploads directory if it doesn't exist
            uploads_dir = 'static/uploads'
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            
            # Save file
            filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
            filepath = os.path.join(uploads_dir, filename)
            file.save(filepath)
            
            # Validate image
            is_valid, message = validate_image(filepath)
            if not is_valid:
                os.remove(filepath)
                return jsonify({'error': f'Invalid image: {message}'}), 400
            
            # Create image record in database
            user_id = session.get('user_id')
            image = Image(
                user_id=user_id,
                filename=file.filename,
                upload_path=filepath
            )
            db.session.add(image)
            db.session.commit()
            
            # Log event
            event = SystemEvent(
                event_type='IMAGE_UPLOADED',
                user_id=user_id,
                message=f'User uploaded image: {file.filename}',
                details={'filename': file.filename, 'image_id': image.id}
            )
            db.session.add(event)
            db.session.commit()
            
            return jsonify({'success': True, 'image_id': image.id}), 200
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Error uploading file: {str(e)}'}), 500
    
    return render_template('upload.html')


@detection_bp.route('/analyze/<int:image_id>', methods=['GET'])
def analyze(image_id):
    """Analyze image with all 5 models."""
    user_id = session.get('user_id')
    
    image = Image.query.filter_by(id=image_id, user_id=user_id).first()
    
    if not image:
        flash('Image not found.', 'danger')
        return redirect(url_for('detection.history'))
    
    # Check if already analyzed
    existing_result = DetectionResult.query.filter_by(image_id=image_id).first()
    if existing_result:
        return redirect(url_for('detection.results', result_id=existing_result.id))
    
    try:
        # Run blur detection
        detector = BlurDetector(image.upload_path)
        all_results = detector.detect_all_models()
        primary_result = detector.get_primary_result()
        
        # Save primary result
        result = DetectionResult(
            image_id=image_id,
            user_id=user_id,
            model_used=primary_result['model_name'],
            blur_type=primary_result['blur_type'],
            confidence=primary_result['confidence'],
            blur_score=primary_result['blur_score'],
            explanation=primary_result['explanation'],
            processing_time=primary_result['processing_time']
        )
        db.session.add(result)
        
        # Save all model comparisons
        for model_key, model_result in all_results.items():
            comparison = ModelComparison(
                image_id=image_id,
                model_name=model_result['model_name'],
                blur_type=model_result['blur_type'],
                confidence=model_result['confidence'],
                processing_time=model_result['processing_time']
            )
            db.session.add(comparison)
        
        db.session.commit()
        
        # Log detection event
        event_type = 'SHARP_IMAGE' if primary_result['blur_type'] == 'Sharp' else 'BLUR_TYPE_DETECTED'
        event = SystemEvent(
            event_type=event_type,
            user_id=user_id,
            message=f'Detected {primary_result["blur_type"]} blur in image',
            details={
                'image_id': image_id,
                'blur_type': primary_result['blur_type'],
                'confidence': primary_result['confidence']
            }
        )
        db.session.add(event)
        db.session.commit()
        
        return redirect(url_for('detection.results', result_id=result.id))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error analyzing image: {str(e)}', 'danger')
        return redirect(url_for('detection.upload'))


@detection_bp.route('/results/<int:result_id>', methods=['GET'])
def results(result_id):
    """Display analysis results."""
    user_id = session.get('user_id')
    
    result = DetectionResult.query.filter_by(id=result_id, user_id=user_id).first()
    
    if not result:
        flash('Result not found.', 'danger')
        return redirect(url_for('detection.history'))
    
    # Get all model comparisons for this image
    comparisons = ModelComparison.query.filter_by(image_id=result.image_id).all()
    
    # Get image
    image = Image.query.get(result.image_id)
    
    # Get blur color
    blur_color = get_blur_color(result.blur_type)
    
    return render_template(
        'results.html',
        result=result,
        image=image,
        comparisons=comparisons,
        blur_color=blur_color
    )


@detection_bp.route('/history', methods=['GET'])
def history():
    """Display analysis history."""
    user_id = session.get('user_id')
    
    page = request.args.get('page', 1, type=int)
    results = DetectionResult.query.filter_by(user_id=user_id).order_by(
        DetectionResult.detected_at.desc()
    ).paginate(page=page, per_page=10)
    
    return render_template('history.html', results=results)
