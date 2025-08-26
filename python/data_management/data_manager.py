import sqlite3
from typing import Dict, Optional, Tuple
from datetime import datetime

class DataManager:
    def __init__(self, db_file: str = "3Dev.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_file = db_file
        self.conn = None
        self.create_tables()
    
    def connect(self):
        """Create a database connection with row factory enabled."""
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def create_tables(self):
        """Create tables that mirror the settings menu structure."""
        # Users table - corresponds to Security section
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        # User preferences - corresponds to User Preferences section
        create_user_preferences_table = """
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id INTEGER PRIMARY KEY,
            theme TEXT DEFAULT 'light',
            auto_save BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON DELETE CASCADE
        );
        """
        
        # Render preferences - corresponds to Render Preferences section
        create_render_preferences_table = """
        CREATE TABLE IF NOT EXISTS render_preferences (
            user_id INTEGER PRIMARY KEY,
            render_name TEXT DEFAULT 'Default',
            image_width INTEGER DEFAULT 800,
            aspect_ratio REAL DEFAULT 1.778,
            focus_distance REAL DEFAULT 10.0,
            aperture REAL DEFAULT 2.0,
            max_depth INTEGER DEFAULT 50,
            samples_per_pixel INTEGER DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON DELETE CASCADE
        );
        """
        
        with self.connect() as conn:
            conn.execute(create_users_table)
            conn.execute(create_user_preferences_table)
            conn.execute(create_render_preferences_table)
    
    def add_user(self, username: str, password_hash: str) -> Optional[int]:
        """Add a new user and create their default preferences."""
        sql_user = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        sql_user_prefs = "INSERT INTO user_preferences (user_id) VALUES (?)"
        sql_render_prefs = "INSERT INTO render_preferences (user_id) VALUES (?)"
        
        try:
            with self.connect() as conn:
                cursor = conn.execute(sql_user, (username, password_hash))
                user_id = cursor.lastrowid
                conn.execute(sql_user_prefs, (user_id,))
                conn.execute(sql_render_prefs, (user_id,))
                return user_id
        except sqlite3.IntegrityError:
            return None

    def update_security(self, user_id: int, username: Optional[str] = None, 
                       password_hash: Optional[str] = None) -> bool:
        """Update security settings (username and/or password)."""
        if not username and not password_hash:
            return False
            
        update_fields = []
        values = []
        if username:
            update_fields.append("username = ?")
            values.append(username)
        if password_hash:
            update_fields.append("password_hash = ?")
            values.append(password_hash)
            
        sql = f"""
        UPDATE users
        SET {', '.join(update_fields)},
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
        """
        values.append(user_id)
        
        try:
            with self.connect() as conn:
                cursor = conn.execute(sql, values)
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            return False

    def update_user_preferences(self, user_id: int, **preferences) -> bool:
        """
        Update user interface preferences for a specific user.
    
        This function allows updating the theme and auto-save settings for a user.
        Only valid fields ('theme' and 'auto_save') will be updated.
    
        Args:
            user_id (int): The unique identifier of the user whose preferences are being updated.
            **preferences: Arbitrary keyword arguments representing the preferences to update.
                            Valid keys are 'theme' and 'auto_save'.
    
        Returns:
            bool: True if the update was successful (i.e., at least one row was affected),
                    False otherwise (including when no valid fields were provided).
    
        Note:
            This function will silently ignore any preference keys that are not in the valid_fields set.
        """
        valid_fields = {'theme', 'auto_save'}
        update_fields = {k: v for k, v in preferences.items() if k in valid_fields}
        if not update_fields:
            return False

        sql = f"""
        UPDATE user_preferences
        SET {', '.join(f'{k} = ?' for k in update_fields.keys())},
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
        """

        with self.connect() as conn:
            cursor = conn.execute(sql, (*update_fields.values(), user_id))
            return cursor.rowcount > 0

    def update_render_preferences(self, user_id: int, **preferences) -> bool:
        """Update rendering preferences."""
        valid_fields = {'render_name', 'image_width', 'aspect_ratio',
                       'focus_distance', 'aperture', 'max_depth',
                       'samples_per_pixel'}
        update_fields = {k: v for k, v in preferences.items() if k in valid_fields}
        if not update_fields:
            return False
        
        sql = f"""
        UPDATE render_preferences
        SET {', '.join(f'{k} = ?' for k in update_fields.keys())},
            updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
        """
        
        with self.connect() as conn:
            cursor = conn.execute(sql, (*update_fields.values(), user_id))
            return cursor.rowcount > 0

    def get_user_section(self, username: str, section: str) -> Optional[Dict]:

        section_queries = {
            'security': """
                SELECT user_id, username, password_hash, created_at, updated_at
                FROM users WHERE username = ?
            """,
            'preferences': """
                SELECT up.*
                FROM user_preferences up
                JOIN users u ON u.user_id = up.user_id
                WHERE u.username = ?
            """,
            'render': """
                SELECT rp.*
                FROM render_preferences rp
                JOIN users u ON u.user_id = rp.user_id
                WHERE u.username = ?
            """
        }
        
        if section not in section_queries:
            return None
            
        with self.connect() as conn:
            cursor = conn.execute(section_queries[section], (username,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_settings(self, username: str) -> Optional[Dict]:
        """Retrieve all settings for a user."""
        sql = """
        SELECT 
            u.user_id, u.username, u.created_at,
            up.theme, up.auto_save,
            rp.render_name, rp.image_width, rp.aspect_ratio,
            rp.focus_distance, rp.aperture, rp.max_depth,
            rp.samples_per_pixel
        FROM users u
        LEFT JOIN user_preferences up ON u.user_id = up.user_id
        LEFT JOIN render_preferences rp ON u.user_id = rp.user_id
        WHERE u.username = ?
        """
        with self.connect() as conn:
            cursor = conn.execute(sql, (username,))
            row = cursor.fetchone()
            return dict(row) if row else None