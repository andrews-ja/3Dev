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
        self.grid_rowconfigure(4, weight=1)
        
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
        
        # Created date - display in formatted form
        self.date_label = ctk.CTkLabel(
            self,
            text=f"Created: {created_date.strftime('%d-%m-%Y')}",
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

class AddProjectDialog(ctk.CTkFrame):
    def __init__(self, master, close_callback, create_callback, **kwargs):
        super().__init__(master, fg_color=DARK_BLUE, **kwargs)
        
        # Save callbacks
        self.close_callback = close_callback
        self.create_callback = create_callback
        
        # Configure grid
        self.grid_columnconfigure((0, 1), weight=1)
        
        # Add dialog title
        self.title_label = ctk.CTkLabel(
            self, 
            text="Add Project",
            font=("Helvetica", 18, "bold")
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 30), sticky="n")
        
        # Project title input
        self.title_label = ctk.CTkLabel(
            self,
            text="Project Title:",
            anchor="w"
        )
        self.title_label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.title_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="Enter project title",
            fg_color=LIGHTER_BLUE,
            border_width=0
        )
        self.title_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        
        # Version number input
        self.version_label = ctk.CTkLabel(
            self,
            text="Version Number:",
            anchor="w"
        )
        self.version_label.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.version_entry = ctk.CTkEntry(
            self,
            width=300,
            placeholder_text="e.g., 1.0.0",
            border_width=0,
            fg_color=LIGHTER_BLUE
        )
        self.version_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 30), sticky="ew")
        
        # Buttons
        self.cancel_btn = ctk.CTkButton(
            self,
            text="Cancel",
            fg_color=RED,
            command=self.close_callback,
            width=120,
            height=BUTTON_HEIGHT
        )
        self.cancel_btn.grid(row=5, column=0, padx=(20, 10), pady=(0, 20), sticky="e")
        
        self.create_btn = ctk.CTkButton(
            self,
            text="Create Project",
            fg_color=BUTTON_COLOUR,
            command=self.create_project,
            width=120,
            height=BUTTON_HEIGHT
        )
        self.create_btn.grid(row=5, column=1, padx=(10, 20), pady=(0, 20), sticky="w")
    
    def create_project(self):
        title = self.title_entry.get()
        version = self.version_entry.get()
        
        # Basic validation
        if not title or not version:
            # You could add a proper error message here
            return
        
        # Call the callback with the project details
        self.create_callback(title, version)
        
        # Close the dialog
        self.close_callback()

class VersionControl(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=DARK_BLUE, **kwargs)
        
        # Configure grid weights for main frame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Make row with scrollable frame expandable

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
            height=BUTTON_HEIGHT,
            command=self.open_add_project_dialog
        )
        
        # Project cards section title
        self.projects_label = ctk.CTkLabel(
            self,
            text="Your Projects",
            anchor="center"
        )
        
        # Create a scrollable frame for projects
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0
        )
        
        # Configure the scrollable frame's grid
        self.scrollable_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Convert string dates to datetime objects
        self.projects = []
        
        # Dialog reference
        self.dialog = None
        
        # Layout
        self.title_label.grid(row=0, column=0, sticky="nw", padx=20, pady=(50, 10))
        self.new_scene_btn.grid(row=0, column=0, sticky="nw", padx=20, pady=(75, 10))
        self.projects_label.grid(row=1, column=0, sticky="w", padx=30, pady=(10, 10))
        
        # Add the scrollable frame to the main layout
        self.scrollable_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create and layout project cards
        self.refresh_project_cards()
    
    def refresh_project_cards(self):
        # Clear existing cards from the scrollable frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
                
        # Create and layout project cards in the scrollable frame
        for i, (title, version, date) in enumerate(self.projects):
            row = i // 2
            col = i % 2
            card = ProjectCard(
                self.scrollable_frame,
                title=title,
                version=version,
                created_date=date
            )
            card.grid(
                row=row,
                column=col,
                padx=(10, 5) if col == 0 else (5, 10),
                pady=10,
                sticky="nsew"
            )
    
    def open_add_project_dialog(self):
        # Define dialog dimensions
        dialog_width = 400
        dialog_height = 300
        
        # Get parent dimensions
        self.update_idletasks()  # Ensure geometry info is up to date
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()
        
        # Calculate center position
        x_position = (parent_width - dialog_width) // 2 if parent_width > 0 else 100
        y_position = (parent_height - dialog_height) // 2 if parent_height > 0 else 100
        
        # Create the dialog frame with width and height in constructor
        self.dialog = AddProjectDialog(
            self,
            close_callback=self.close_dialog,
            create_callback=self.add_new_project,
            width=dialog_width,
            height=dialog_height,
            border_width=0
        )
        
        # Place the dialog at the calculated position (without width/height)
        self.dialog.place(x=x_position, y=y_position)
        
        # Bring the dialog to the front
        self.dialog.lift()
    
    def close_dialog(self):
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None
    
    def add_new_project(self, title, version):
        # Add the new project with current date
        current_date = datetime.now()
        self.projects.append((title, version, current_date))
        
        # Refresh the project cards display
        self.refresh_project_cards()
        
        # Scroll to the bottom to show the new project
        self.scrollable_frame._parent_canvas.yview_moveto(1.0)