import sqlite3
from typing import Dict, List, Optional
from datetime import datetime
import json

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
        """Create all necessary tables if they don't exist."""
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_user_settings_table = """
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            theme TEXT DEFAULT 'light',
            other_settings TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON DELETE CASCADE
        );
        """
        
        create_render_settings_table = """
        CREATE TABLE IF NOT EXISTS render_settings (
            render_settings_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            image_width INTEGER NOT NULL,
            aspect_ratio REAL NOT NULL,
            focus_distance REAL NOT NULL,
            aperture REAL NOT NULL,
            max_depth INTEGER NOT NULL,
            samples_per_pixel INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
                ON DELETE CASCADE
        );
        """
        
        with self.connect() as conn:
            conn.execute(create_users_table)
            conn.execute(create_user_settings_table)
            conn.execute(create_render_settings_table)
    
    def add_user(self, username: str, password_hash: str) -> Optional[int]:
        """Add a new user and create their default settings."""
        sql_user = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        sql_settings = "INSERT INTO user_settings (user_id, theme) VALUES (?, ?)"
        
        try:
            with self.connect() as conn:
                cursor = conn.execute(sql_user, (username, password_hash))
                user_id = cursor.lastrowid
                conn.execute(sql_settings, (user_id, 'light'))
                return user_id
        except sqlite3.IntegrityError:
            return None
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Retrieve a user and their settings."""
        sql = """
        SELECT u.*, us.theme, us.other_settings
        FROM users u
        LEFT JOIN user_settings us ON u.user_id = us.user_id
        WHERE u.username = ?
        """
        with self.connect() as conn:
            cursor = conn.execute(sql, (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_user_settings(self, user_id: int, theme: str, other_settings: Dict = None) -> bool:
        """Update a user's settings."""
        sql = """
        UPDATE user_settings
        SET theme = ?, other_settings = ?, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = ?
        """
        other_settings_json = json.dumps(other_settings) if other_settings else None
        
        with self.connect() as conn:
            cursor = conn.execute(sql, (theme, other_settings_json, user_id))
            return cursor.rowcount > 0
    
    def add_render_settings(self, user_id: int, name: str, image_width: int,
                          aspect_ratio: float, focus_distance: float, aperture: float,
                          max_depth: int, samples_per_pixel: int) -> Optional[int]:
        """Add new render settings for a user."""
        sql = """
        INSERT INTO render_settings (
            user_id, name, image_width, aspect_ratio, focus_distance,
            aperture, max_depth, samples_per_pixel
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with self.connect() as conn:
                cursor = conn.execute(sql, (
                    user_id, name, image_width, aspect_ratio, focus_distance,
                    aperture, max_depth, samples_per_pixel
                ))
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_render_settings(self, render_settings_id: int) -> Optional[Dict]:
        """Retrieve specific render settings."""
        sql = "SELECT * FROM render_settings WHERE render_settings_id = ?"
        with self.connect() as conn:
            cursor = conn.execute(sql, (render_settings_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_user_render_settings(self, user_id: int) -> List[Dict]:
        """Get all render settings for a user."""
        sql = "SELECT * FROM render_settings WHERE user_id = ? ORDER BY created_at DESC"
        with self.connect() as conn:
            cursor = conn.execute(sql, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def update_render_settings(self, render_settings_id: int, **updates) -> bool:
        """Update specific render settings."""
        current = self.get_render_settings(render_settings_id)
        if not current:
            return False
        
        valid_fields = {'name', 'image_width', 'aspect_ratio', 'focus_distance',
                       'aperture', 'max_depth', 'samples_per_pixel'}
        
        update_fields = {k: v for k, v in updates.items() if k in valid_fields}
        if not update_fields:
            return False
        
        sql = f"""
        UPDATE render_settings
        SET {', '.join(f'{k} = ?' for k in update_fields.keys())},
            updated_at = CURRENT_TIMESTAMP
        WHERE render_settings_id = ?
        """
        
        with self.connect() as conn:
            cursor = conn.execute(sql, (*update_fields.values(), render_settings_id))
            return cursor.rowcount > 0