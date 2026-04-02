#!/usr/bin/env python
"""
Database initialization script.
Run this once to create all tables in PostgreSQL.
"""

import os
from dotenv import load_dotenv
from app import app, db
from models import User, Image, DetectionResult, ModelComparison, SystemEvent

# Load environment variables
load_dotenv()

def init_database():
    """Create all database tables."""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database initialized successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - images")
        print("  - detection_results")
        print("  - model_comparisons")
        print("  - system_events")
        print("\nYou can now run: python app.py")

if __name__ == '__main__':
    init_database()
