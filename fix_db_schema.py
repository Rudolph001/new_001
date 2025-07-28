#!/usr/bin/env python3
"""Fix database schema by adding missing columns"""

import sqlite3
import os

def fix_database_schema():
    """Add missing columns to the email_records table"""
    db_path = 'instance/email_guardian.db'
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if policy_name column exists
        cursor.execute("PRAGMA table_info(email_records)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'policy_name' not in columns:
            print("Adding policy_name column...")
            cursor.execute("ALTER TABLE email_records ADD COLUMN policy_name VARCHAR(255)")
            print("✓ Added policy_name column")
        else:
            print("✓ policy_name column already exists")
        
        conn.commit()
        conn.close()
        print("Database schema update completed successfully!")
        
    except Exception as e:
        print(f"Error updating database schema: {e}")

if __name__ == "__main__":
    fix_database_schema()