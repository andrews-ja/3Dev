import customtkinter as ctk
from typing import Dict, Any

from data_management.data_manager import DataManager  # Import DataManager
from data_management.user_manager import UserManager    # Import UserManager

from utilities.UI import *

class SettingsSection(ctk.CTkFrame):
    def __init__(self, master, title: str, **kwargs):
        super().__init__(master, fg_color=DARK_BLUE, **kwargs)

        # Configure grid weights - critical for proper label/widget alignment
        self.grid_columnconfigure(1, weight=1)  # Make widget column expandable
        self.grid_columnconfigure(2, weight=0)  # Fixed width for save buttons

        # Section title
        self.title = ctk.CTkLabel(
            self,
            text=title,
            font=("Source Code Pro", 20, "bold"),
            anchor="w"
        )
        self.title.grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(20, 15))

        self.current_row = 1

    def add_setting(self, label: str, widget: ctk.CTkBaseClass, button: ctk.CTkButton = None) -> None:
        """Add a setting row with a label, control widget, and optional button."""
        # Create and position the label
        label = ctk.CTkLabel(
            self,
            text=label,
            anchor="w",
            font=("Source Code Pro", 14)
        )
        label.grid(row=self.current_row, column=0, sticky="w", padx=20, pady=8)

        # Position the widget
        widget.grid(row=self.current_row, column=1, sticky="ew", padx=20, pady=8)

        # Add save button if provided
        if button:
            button.grid(row=self.current_row, column=2, sticky="e", padx=(0, 20), pady=8)

        self.current_row += 1


class Settings(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=DARK_BLUE, **kwargs)

        self.data_manager = DataManager()
        self.user_manager = UserManager()
        self.current_user_id = None  # Initialize to None
        # self.current_user_id = self.user_manager.get_current_user_id() # This method does not exist
        # Instead, you should retrieve the user ID when displaying the settings, e.g., from master or session
        self.user_preferences = None
        self.render_settings = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # User Preferences Section
        self.user_prefs = SettingsSection(self.scrollable_frame, "User Preferences")
        self.user_prefs.grid(row=0, column=0, sticky="ew", pady=(0, 25))

        # Theme dropdown with implementation
        self.theme_dropdown = ctk.CTkOptionMenu(
            self.user_prefs,
            values=["Dark", "Light", "System"],
            width=200,
            height=32,
            font=("Source Code Pro", 14),
            command=self.change_theme
        )
        current_theme = "System" # Default to system if no theme in db
        if self.user_preferences:
            current_theme = self.user_preferences.theme
        self.theme_dropdown.set(current_theme.capitalize()) # Set default value from db
        self.user_prefs.add_setting("Theme", self.theme_dropdown)

        # Autosave switch
        self.autosave_switch = ctk.CTkSwitch( # Make autosave_switch an instance variable
            self.user_prefs,
            text="",
            height=32,
            width=60,
            command=self.toggle_autosave # Add command for autosave switch
        )
        autosave_selected = False # Default to deselect
        if self.user_preferences and self.user_preferences.auto_save:
            autosave_selected = True
        self.autosave_switch.select() if autosave_selected else self.autosave_switch.deselect() # Set default value from db
        self.user_prefs.add_setting("Autosave", self.autosave_switch)

        # Render Preferences Section
        self.render_prefs = SettingsSection(self.scrollable_frame, "Render Preferences")
        self.render_prefs.grid(row=1, column=0, sticky="ew", pady=(0, 25))

        # Image width slider
        self.width_slider = ctk.CTkSlider(
            self.render_prefs,
            from_=480,
            to=3840,
            number_of_steps=14,
            height=16,
            width=200,
            command=self.save_image_width # Add command to slider
        )
        current_width = 1920 # Default width
        if self.render_settings and self.render_settings.image_width:
            current_width = self.render_settings.image_width
        self.width_slider.set(current_width) # Set default value from db
        self.render_prefs.add_setting("Image Width", self.width_slider)

        # Aspect ratio dropdown
        self.ratio_dropdown = ctk.CTkOptionMenu(
            self.render_prefs,
            values=["16:9", "4:3", "1:1", "21:9"],
            width=200,
            height=32,
            font=("Source Code Pro", 14),
            command=self.save_aspect_ratio # Add command
        )
        current_ratio = "16:9" # Default ratio
        if self.render_settings and self.render_settings.aspect_ratio:
            current_ratio = self.render_settings.aspect_ratio
        self.ratio_dropdown.set(current_ratio) # Set default value from db
        self.render_prefs.add_setting("Aspect Ratio", self.ratio_dropdown)

        # Focus distance entry with save button
        self.focus_entry = ctk.CTkEntry(
            self.render_prefs,
            placeholder_text="Enter focus distance...",
            width=200,
            height=32,
            font=("Source Code Pro", 14)
        )
        current_focus = "" # Default empty
        if self.render_settings and self.render_settings.focus_distance is not None:
            current_focus = str(self.render_settings.focus_distance)
        self.focus_entry.insert(0, current_focus) # Set default value from db
        focus_save = ctk.CTkButton(
            self.render_prefs,
            text="Save",
            width=60,
            height=32,
            font=("Source Code Pro", 12),
            command=lambda: self.save_focus_distance(self.focus_entry.get()) # Add command to save button
        )
        self.render_prefs.add_setting("Focus Distance", self.focus_entry, focus_save)

        # Aperture slider
        self.aperture_slider = ctk.CTkSlider(
            self.render_prefs,
            from_=1.0,
            to=16.0,
            number_of_steps=32,
            height=16,
            width=200,
            command=self.save_aperture # Add command
        )
        current_aperture = 1.8 # Default aperture
        if self.render_settings and self.render_settings.aperture:
            current_aperture = self.render_settings.aperture
        self.aperture_slider.set(current_aperture) # Set default value from db
        self.render_prefs.add_setting("Aperture", self.aperture_slider)

        # Max depth entry with save button
        self.depth_entry = ctk.CTkEntry(
            self.render_prefs,
            placeholder_text="Enter max depth...",
            width=200,
            height=32,
            font=("Source Code Pro", 14)
        )
        current_depth = "" # Default empty
        if self.render_settings and self.render_settings.max_depth is not None:
            current_depth = str(self.render_settings.max_depth)
        self.depth_entry.insert(0, current_depth) # Set default value from db
        depth_save = ctk.CTkButton(
            self.render_prefs,
            text="Save",
            width=60,
            height=32,
            font=("Source Code Pro", 12),
            command=lambda: self.save_max_depth(self.depth_entry.get()) # Add command to save button
        )
        self.render_prefs.add_setting("Max Depth", self.depth_entry, depth_save)

        # Samples per pixel slider
        self.samples_slider = ctk.CTkSlider(
            self.render_prefs,
            from_=1,
            to=1000,
            number_of_steps=100,
            height=16,
            width=200,
            command=self.save_samples_per_pixel # Add command
        )
        current_samples = 100 # Default samples
        if self.render_settings and self.render_settings.samples_per_pixel:
            current_samples = self.render_settings.samples_per_pixel
        self.samples_slider.set(current_samples) # Set default value from db
        self.render_prefs.add_setting("Samples per Pixel", self.samples_slider)

        # Security Section
        self.security = SettingsSection(self.scrollable_frame, "Security")
        self.security.grid(row=2, column=0, sticky="ew", pady=(0, 25))

        # Username field with save button
        username_entry = ctk.CTkEntry(
            self.security,
            placeholder_text="Enter new username...",
            width=200,
            height=32,
            font=("Source Code Pro", 14)
        )
        # Do not load username here for security reasons, only allow changing password
        username_save = ctk.CTkButton(
            self.security,
            text="Save",
            width=60,
            height=32,
            font=("Source Code Pro", 12)
        )
        self.security.add_setting("Username", username_entry, username_save)

        # Password field with save button
        password_entry = ctk.CTkEntry(
            self.security,
            placeholder_text="Enter new password...",
            width=200,
            height=32,
            font=("Source Code Pro", 14),
            show="•"
        )
        password_save = ctk.CTkButton(
            self.security,
            text="Save",
            width=60,
            height=32,
            font=("Source Code Pro", 12)
        )
        self.security.add_setting("Password", password_entry, password_save)

        # Logout button
        logout_btn = ctk.CTkButton(
            self.security,
            text="Log Out",
            fg_color=RED,
            width=200,
            height=32,
            font=("Source Code Pro", 14)
        )
        self.security.add_setting("Session", logout_btn)

    def change_theme(self, new_theme: str) -> None:
        """Change the application theme."""
        if new_theme == "System":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode(new_theme.lower())
    
    def toggle_autosave(self):
        """Toggle the autosave setting in the database."""
        current_autosave = self.autosave_switch.get() == 1 # Get current state of the switch (1 for checked, 0 for unchecked)
        self.data_manager.update_user_preferences(self.current_user_id, autosave=current_autosave) # Update autosave in db
        print(f"Autosave toggled to: {'on' if current_autosave else 'off'}") # Optional: print status to console

    def save_image_width(self, new_width: float):
        """Save the image width to the database."""
        new_width_int = int(new_width) # Convert to integer
        self.data_manager.update_render_preferences(self.current_user_id, image_width=new_width_int) # Update image_width in db
        print(f"Image width saved: {new_width_int}") # Optional: print status to console

    def save_aspect_ratio(self, new_ratio: str):
        """Save the aspect ratio to the database."""
        self.data_manager.update_render_preferences(self.current_user_id, aspect_ratio=new_ratio) # Update aspect_ratio in db
        print(f"Aspect ratio saved: {new_ratio}") # Optional: print status to console

    def save_focus_distance(self, new_focus: str):
        """Save the focus distance to the database."""
        try:
            new_focus_float = float(new_focus) # Convert to float
            self.data_manager.update_render_preferences(self.current_user_id, focus_distance=new_focus_float) # Update focus_distance in db
            print(f"Focus distance saved: {new_focus_float}") # Optional: print status to console
        except ValueError:
            print("Invalid focus distance. Please enter a number.") # Handle invalid input
            # Optionally, provide visual feedback to the user in the UI

    def save_aperture(self, new_aperture: float):
        """Save the aperture to the database."""
        self.data_manager.update_render_preferences(self.current_user_id, aperture=new_aperture) # Update aperture in db
        print(f"Aperture saved: {new_aperture}") # Optional: print status to console

    def save_max_depth(self, new_depth: str):
        """Save the max depth to the database."""
        try:
            new_depth_int = int(new_depth) # Convert to integer
            self.data_manager.update_render_preferences(self.current_user_id, max_depth=new_depth_int) # Update max_depth in db
            print(f"Max depth saved: {new_depth_int}") # Optional: print status to console
        except ValueError:
            print("Invalid max depth. Please enter an integer.") # Handle invalid input
            # Optionally, provide visual feedback to the user in the UI

    def save_samples_per_pixel(self, new_samples: float):
        """Save samples per pixel to the database."""
        new_samples_int = int(new_samples) # Convert to integer
        self.data_manager.update_render_preferences(self.current_user_id, samples_per_pixel=new_samples_int) # Update samples_per_pixel in db
        print(f"Samples per pixel saved: {new_samples_int}") # Optional: print status to console