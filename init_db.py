#!/usr/bin/env python
"""
Database initialization script for BlurDetect
Run this script to create all database tables and initialize the database
"""

import os
from app import app, db
from models import User, Image, DetectionResult, ModelComparison, SystemEvent

def init_database():
    """Initialize the database"""
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully")
        
        # Verify tables exist
        tables = db.inspect(db.engine).get_table_names()
        print("\nCreated tables:")
        for table in tables:
            print(f"  - {table}")
        
        # Create uploads directory if it doesn't exist
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            print(f"\n✓ Created uploads folder: {upload_folder}")
        
        print("\n✓ Database initialization complete!")
        print("\nYou can now run the application with: python app.py")

if __name__ == '__main__':
    init_database()
