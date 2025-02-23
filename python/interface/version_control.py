import customtkinter as ctk
import os
from datetime import datetime

from utilities.UI import *

class ProjectCard(ctk.CTkFrame):
    def __init__(
        self,
        master: ctk.CTkFrame,
        title: str,
        version: str,
        created_date,
        **kwargs
    ) -> None:
        super().__init__(master, fg_color=LIGHTER_BLUE, **kwargs)
        
        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        
        # Project title and version
        self.title_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.title_frame.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text=title,
            anchor="w"
        )
        self.version_label = ctk.CTkLabel(
            self.title_frame,
            text=f"v{version}",
            text_color="gray"
        )
        
        # Placeholder image frame
        self.image_frame = ctk.CTkFrame(
            self,
            fg_color=IMAGE_COLOUR,
            height=200
        )
        
        # Created date
        self.date_label = ctk.CTkLabel(
            self,
            text=f"Created: {created_date}",
            text_color="gray"
        )
        
        # Launch button
        self.launch_btn = ctk.CTkButton(
            self,
            text="Launch Scene",
            fg_color=BUTTON_COLOUR,
            height=BUTTON_HEIGHT
        )
        
        # Layout
        self.title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.title_label.grid(row=0, column=0, sticky="w")
        self.version_label.grid(row=0, column=1, sticky="e")
        
        self.image_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.date_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.launch_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 10))

class VersionControl(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color = DARK_BLUE, **kwargs)
        
        # Configure grid weights
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create New Project section
        self.title_label = ctk.CTkLabel(
            self,
            text="Create New Project",
            anchor="center"
        )
        self.new_scene_btn = ctk.CTkButton(
            self,
            text="New Scene",
            fg_color=BUTTON_COLOUR,
            width=150,
            height=BUTTON_HEIGHT
        )
        
        # Project cards
        self.projects_label = ctk.CTkLabel(
            self,
            text="Your Projects",
            anchor="center"
        )

        self.projects = [
            ("Project Alpha", "1.2.0", "15-10-2024"),
            ("Scene Builder Pro", "2.0.1", "20-10-2024"),
            ("Environment Test", "0.9.0", "22-10-2024"),
            ("Character Setup", "1.0.0", "25-10-2024")
        ]
        
        # Layout
        self.title_label.grid(row=0, column=0, sticky="nw", padx=20, pady=(50, 10))
        self.new_scene_btn.grid(row=0, column=0, sticky="nw", padx=20, pady=(75, 100))
        self.projects_label.grid(row=0, column=0, sticky="w", padx=30, pady=(200, 0))
        
        # Create and layout project cards
        for i, (title, version, date) in enumerate(self.projects):
            row = (i // 2) + 1
            col = i % 2
            card = ProjectCard(
                self,
                title=title,
                version=version,
                created_date=date
            )
            card.grid(row=row, column=col, padx=(20, 30) if col else (30, 20), pady=20 if row else (0, 20), sticky="nsew")