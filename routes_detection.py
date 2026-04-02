from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, current_app
from models import db, Image, DetectionResult, ModelComparison, SystemEvent
from auth_utils import login_required
from blur_models import BlurDetectionModels
from werkzeug.utils import secure_filename
import os
from datetime import datetime

detection_bp = Blueprint('detection_bp', __name__, url_prefix='/detection')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@detection_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(url_for('detection_bp.upload'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(url_for('detection_bp.upload'))
        
        if not allowed_file(file.filename):
            flash('File type not allowed. Please upload an image.', 'danger')
            return redirect(url_for('detection_bp.upload'))
        
        # Create uploads folder if it doesn't exist
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Store in database
        image = Image(
            user_id=session['user_id'],
            filename=filename,
            upload_path=filepath
        )
        db.session.add(image)
        db.session.commit()
        
        # Log event
        event = SystemEvent(
            event_type='IMAGE_UPLOADED',
            user_id=session['user_id'],
            message=f'Image uploaded: {filename}'
        )
        db.session.add(event)
        db.session.commit()
        
        return redirect(url_for('detection_bp.analyze', image_id=image.id))
    
    return render_template('upload.html')


@detection_bp.route('/analyze/<int:image_id>', methods=['GET'])
@login_required
def analyze(image_id):
    image = Image.query.get(image_id)
    
    if not image or image.user_id != session['user_id']:
        flash('Image not found.', 'danger')
        return redirect(url_for('detection_bp.upload'))
    
    # Check if analysis already done
    result = DetectionResult.query.filter_by(image_id=image_id).first()
    
    if not result:
        # Run all models
        results = BlurDetectionModels.run_all_models(image.upload_path)
        primary = results['primary_result']
        
        # Store primary result
        result = DetectionResult(
            image_id=image_id,
            user_id=session['user_id'],
            model_used=primary['model'],
            blur_type=primary['blur_type'],
            confidence=primary['confidence'],
            blur_score=primary['blur_score'],
            explanation=primary['explanation'],
            processing_time=primary['processing_time']
        )
        db.session.add(result)
        db.session.commit()
        
        # Store all model comparisons
        for model_key, model_result in results['all_models'].items():
            if 'error' not in model_result:
                comparison = ModelComparison(
                    image_id=image_id,
                    model_name=model_result['model'],
                    blur_type=model_result['blur_type'],
                    confidence=model_result['confidence'],
                    processing_time=model_result['processing_time']
                )
                db.session.add(comparison)
        
        db.session.commit()
        
        # Log event
        event = SystemEvent(
            event_type='BLUR_TYPE_DETECTED' if result.blur_type != 'Sharp' else 'SHARP_IMAGE',
            user_id=session['user_id'],
            message=f'Blur type detected: {result.blur_type} (confidence: {result.confidence:.2%})',
            details={
                'image_id': image_id,
                'blur_type': result.blur_type,
                'confidence': result.confidence,
                'model': primary['model']
            }
        )
        db.session.add(event)
        db.session.commit()
    
    # Get comparisons
    comparisons = ModelComparison.query.filter_by(image_id=image_id).all()
    
    return render_template('results.html', 
                         image=image, 
                         result=result, 
                         comparisons=comparisons,
                         justification=BlurDetectionModels().primary_model_justification)


@detection_bp.route('/history', methods=['GET'])
@login_required
def history():
    images = Image.query.filter_by(user_id=session['user_id']).order_by(Image.uploaded_at.desc()).all()
    
    # Get latest detection for each image
    image_data = []
    for img in images:
        result = DetectionResult.query.filter_by(image_id=img.id).first()
        image_data.append({
            'image': img,
            'result': result
        })
    
    return render_template('history.html', image_data=image_data)


@detection_bp.route('/api/upload-progress', methods=['POST'])
@login_required
def upload_progress():
    """API endpoint for tracking upload progress"""
    return jsonify({'status': 'progress'}), 200
