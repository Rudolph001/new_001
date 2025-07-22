
#!/usr/bin/env python3
"""
Database migration script to add chunk tracking columns
"""

from app import app, db
from models import ProcessingSession
import sqlite3
import os

def migrate_database():
    """Add missing columns to existing database"""
    db_path = os.path.join('instance', 'email_guardian.db')
    
    if not os.path.exists(db_path):
        print("Database doesn't exist, creating new one...")
        with app.app_context():
            db.create_all()
        print("✓ New database created successfully")
        return
    
    try:
        # Connect directly to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(processing_sessions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add missing columns if they don't exist
        if 'current_chunk' not in columns:
            cursor.execute('ALTER TABLE processing_sessions ADD COLUMN current_chunk INTEGER DEFAULT 0')
            print("✓ Added current_chunk column")
        
        if 'total_chunks' not in columns:
            cursor.execute('ALTER TABLE processing_sessions ADD COLUMN total_chunks INTEGER DEFAULT 0')
            print("✓ Added total_chunks column")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print("✓ Database migration completed successfully")
        
    except Exception as e:
        print(f"✗ Migration failed: {str(e)}")
        if conn:
            conn.close()
        raise

if __name__ == "__main__":
    migrate_database()
