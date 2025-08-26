from typing import Optional, Dict, List
from .database import get_db

class UserManager:
    """
    Provides an interface for and manages user-related creation and retrieval operations.
    """
    
    def __init__(self):
        """
        Initializes the UserManager with a database connection.
        """
        self.db = get_db()
    
    def create_user(self, username: str, password_hash: str) -> Optional[int]:
        """
        Creates a new user in the database.
        
        Parameters:
            username (str): The username for the new user.
            password_hash (str): The hashed password for the new user.
            
        Returns:
            Optional[int]: The ID of the newly created user, or None if creation failed.
        """
        return self.db.add_user(username, password_hash)
    
    def get_user(self, username: str) -> Optional[Dict]:
        """
        Retrieves security information for a user by username.
        
        Parameters:
            username (str): The username of the user to retrieve.
            
        Returns:
            Optional[Dict]: A dictionary containing user security information,
                           or None if the user doesn't exist.
        """
        return self.db.get_user_section(username, 'security')


class RenderManager:
    """
    Manages render settings operations including creation, retrieval, and updates.
    
    This class provides methods for handling render settings configurations,
    allowing users to create, retrieve, and modify their rendering preferences.
    """
    
    def __init__(self):
        """
        Initializes the RenderManager with a database connection.
        """
        self.db = get_db()
    
    def create_render_settings(self, user_id: int, name: str, **settings) -> Optional[int]:
        """
        Creates new render settings for a user.
        
        Parameters:
            user_id (int): The ID of the user who owns these settings.
            name (str): A descriptive name for these render settings.
            **settings: Variable keyword arguments representing render configuration options.
            
        Returns:
            Optional[int]: The ID of the newly created settings, or None if creation failed.
        """
        return self.db.add_render_settings(
            user_id=user_id,
            name=name,
            **settings
        )
    
    def get_settings(self, settings_id: int) -> Optional[Dict]:
        """
        Retrieves specific render settings by ID.
        
        Parameters:
            settings_id (int): The ID of the render settings to retrieve.
            
        Returns:
            Optional[Dict]: A dictionary containing the render settings,
                           or None if settings with the given ID don't exist.
        """
        return self.db.get_render_settings(settings_id)
    
    def get_user_settings(self, user_id: int) -> List[Dict]:
        """
        Retrieves all render settings belonging to a user.
        
        Parameters:
            user_id (int): The ID of the user whose settings to retrieve.
            
        Returns:
            List[Dict]: A list of dictionaries, each containing render settings.
                       Returns an empty list if the user has no settings.
        """
        return self.db.get_user_render_settings(user_id)
    
    def update_settings(self, settings_id: int, **updates) -> bool:
        """
        Updates existing render settings.
        
        Parameters:
            settings_id (int): The ID of the settings to update.
            **updates: Variable keyword arguments representing settings to update.
            
        Returns:
            bool: True if the update was successful, False otherwise.
        """
        return self.db.update_render_settings(settings_id, **updates)


class SettingsManager:
    """
    Manages user application settings such as themes and preferences.
    
    This class provides methods for updating user-specific application settings
    that control the appearance and behavior of the application.
    """
    
    def __init__(self):
        """
        Initializes the SettingsManager with a database connection.
        """
        self.db = get_db()  # Should be Database, not DataManager
    
    def update_user_settings(self, user_id: int, theme: str,
                           other_settings: Optional[Dict] = None) -> bool:
        """
        Updates a user's application settings.
        
        Parameters:
            user_id (int): The ID of the user whose settings to update.
            theme (str): The UI theme preference for the user.
            other_settings (Optional[Dict], optional): Additional settings as key-value pairs.
                                                     Defaults to None.
            
        Returns:
            bool: True if the update was successful, False otherwise.
        """
        return self.db.update_user_settings(user_id, theme, other_settings)