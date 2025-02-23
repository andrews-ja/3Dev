import customtkinter as ctk
from typing import Dict, Any

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
        self.user_prefs.add_setting("Theme", self.theme_dropdown)

        # Autosave switch
        autosave_switch = ctk.CTkSwitch(
            self.user_prefs,
            text="",
            height=32,
            width=60
        )
        self.user_prefs.add_setting("Autosave", autosave_switch)

        # Render Preferences Section
        self.render_prefs = SettingsSection(self.scrollable_frame, "Render Preferences")
        self.render_prefs.grid(row=1, column=0, sticky="ew", pady=(0, 25))

        # Image width slider
        width_slider = ctk.CTkSlider(
            self.render_prefs,
            from_=480,
            to=3840,
            number_of_steps=14,
            height=16,
            width=200
        )
        self.render_prefs.add_setting("Image Width", width_slider)

        # Aspect ratio dropdown
        ratio_dropdown = ctk.CTkOptionMenu(
            self.render_prefs,
            values=["16:9", "4:3", "1:1", "21:9"],
            width=200,
            height=32,
            font=("Source Code Pro", 14)
        )
        self.render_prefs.add_setting("Aspect Ratio", ratio_dropdown)

        # Focus distance entry with save button
        focus_entry = ctk.CTkEntry(
            self.render_prefs,
            placeholder_text="Enter focus distance...",
            width=200,
            height=32,
            font=("Source Code Pro", 14)
        )
        focus_save = ctk.CTkButton(
            self.render_prefs,
            text="Save",
            width=60,
            height=32,
            font=("Source Code Pro", 12)
        )
        self.render_prefs.add_setting("Focus Distance", focus_entry, focus_save)

        # Aperture slider
        aperture_slider = ctk.CTkSlider(
            self.render_prefs,
            from_=1.0,
            to=16.0,
            number_of_steps=32,
            height=16,
            width=200
        )
        self.render_prefs.add_setting("Aperture", aperture_slider)

        # Max depth entry with save button
        depth_entry = ctk.CTkEntry(
            self.render_prefs,
            placeholder_text="Enter max depth...",
            width=200,
            height=32,
            font=("Source Code Pro", 14)
        )
        depth_save = ctk.CTkButton(
            self.render_prefs,
            text="Save",
            width=60,
            height=32,
            font=("Source Code Pro", 12)
        )
        self.render_prefs.add_setting("Max Depth", depth_entry, depth_save)

        # Samples per pixel slider
        samples_slider = ctk.CTkSlider(
            self.render_prefs,
            from_=1,
            to=1000,
            number_of_steps=100,
            height=16,
            width=200
        )
        self.render_prefs.add_setting("Samples per Pixel", samples_slider)

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
            fg_color="#e63946",
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