
#!/usr/bin/env python3
"""
Migration script to add policy_name column to email_records table
"""

import sqlite3
import os

def migrate_database():
    """Add policy_name column to email_records table"""
    db_path = 'instance/email_guardian.db'
    
    if not os.path.exists(db_path):
        print("Database not found. No migration needed.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if policy_name column already exists
        cursor.execute("PRAGMA table_info(email_records)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'policy_name' not in columns:
            print("Adding policy_name column to email_records table...")
            cursor.execute("ALTER TABLE email_records ADD COLUMN policy_name VARCHAR(255)")
            conn.commit()
            print("Migration completed successfully!")
        else:
            print("policy_name column already exists. No migration needed.")
        
        conn.close()
        
    except Exception as e:
        print(f"Migration failed: {str(e)}")
        raise

if __name__ == "__main__":
    migrate_database()
