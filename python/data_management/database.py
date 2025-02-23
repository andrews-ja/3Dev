from pathlib import Path
from typing import Optional
from .data_manager import DataManager

class DatabaseSingleton:
    _instance: Optional['DatabaseSingleton'] = None
    _db_manager = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._db_manager is None:
            project_root = Path(__file__).parent.parent
            db_path = project_root / "data" / "graphics_app.db"
            db_path.parent.mkdir(parents=True, exist_ok=True)
            self._db_manager = DataManager(str(db_path))

    @property
    def db(self):
        return self._db_manager

def get_db():
    return DatabaseSingleton().db