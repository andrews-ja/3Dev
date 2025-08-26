from pathlib import Path
from typing import Optional
from .data_manager import DataManager

class DatabaseSingleton:
    """
    A singleton class that manages database connections.
    Ensures only one instance of the database connection is created and reused.
    """
    _instance: Optional['DatabaseSingleton'] = None
    _db_manager = None

    def __new__(cls):
        """
        Controls instance creation to enforce the singleton pattern.
        
        Returns:
            DatabaseSingleton: The single instance of this class.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the database manager if it doesn't exist yet.
        Creates necessary directories and establishes the database connection.
        """
        if self._db_manager is None:
            project_root = Path(__file__).parent.parent
            db_path = project_root / "data" / "3Dev.db"
            db_path.parent.mkdir(parents=True, exist_ok=True)
            self._db_manager = DataManager(str(db_path))

    @property
    def db(self):
        """
        Provides access to the database manager.
        
        Returns:
            DataManager: The database manager instance.
        """
        return self._db_manager

def get_db():
    """
    A helper function to access the database manager.
    
    Returns:
        DataManager: The database manager instance from the DatabaseSingleton.
    """
    return DatabaseSingleton().db