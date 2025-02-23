from typing import Optional, Dict, List
from .database import get_db

class UserManager:
    def __init__(self):
        self.db = get_db()
    
    def create_user(self, username: str, password_hash: str) -> Optional[int]:
        return self.db.add_user(username, password_hash)
    
    def get_user(self, username: str) -> Optional[Dict]:
        return self.db.get_user(username)

class RenderManager:
    def __init__(self):
        self.db = get_db()
    
    def create_render_settings(self, user_id: int, name: str, **settings) -> Optional[int]:
        return self.db.add_render_settings(
            user_id=user_id,
            name=name,
            **settings
        )
    
    def get_settings(self, settings_id: int) -> Optional[Dict]:
        return self.db.get_render_settings(settings_id)
    
    def get_user_settings(self, user_id: int) -> List[Dict]:
        return self.db.get_user_render_settings(user_id)
    
    def update_settings(self, settings_id: int, **updates) -> bool:
        return self.db.update_render_settings(settings_id, **updates)

class SettingsManager:
    def __init__(self):
        self.db = get_db()
    
    def update_user_settings(self, user_id: int, theme: str, 
                           other_settings: Optional[Dict] = None) -> bool:
        return self.db.update_user_settings(user_id, theme, other_settings)