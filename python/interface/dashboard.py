# External imports
import customtkinter as ctk
from typing import Dict

# Internal imports
from utilities.UI import *
from interface.version_control import VersionControl
from interface.asset_gallery import AssetGallery
from interface.settings import Settings

class TopMenuFrame(ctk.CTkFrame):
    def __init__(
        self,
        master: ctk.CTk,
        username: str,
        **kwargs
    ) -> None:
        super().__init__(master, fg_color=DARK_BLUE, **kwargs)

        # Configure grid weights
        self.grid_columnconfigure(3, weight=1)  # Make the middle space expand
        self.grid_rowconfigure(1, weight=1)

        # Initialize frames dictionary to store menu frames
        self.frames: Dict[str, ctk.CTkFrame] = {}
        
        # Create and store menu frames
        self.frames["version_control"] = VersionControl(self)
        self.frames["asset_gallery"] = AssetGallery(self)
        self.frames["settings"] = Settings(self)

        # Create buttons
        self.version_control_btn = ctk.CTkButton(
            self,
            text="Version Control",
            fg_color=BUTTON_COLOUR,
            command=lambda: self.show_menu("version_control"),
            width=175,
            height=BUTTON_HEIGHT
        )
        
        self.asset_gallery_btn = ctk.CTkButton(
            self,
            text="Asset Gallery",
            fg_color="transparent",
            command=lambda: self.show_menu("asset_gallery"),
            width=175,
            height=BUTTON_HEIGHT
        )
        
        self.settings_btn = ctk.CTkButton(
            self,
            text="Settings",
            fg_color="transparent",
            command=lambda: self.show_menu("settings"),
            width=175,
            height=BUTTON_HEIGHT
        )

        # Store buttons in a dictionary for easy access
        self.buttons = {
            "version_control": self.version_control_btn,
            "asset_gallery": self.asset_gallery_btn,
            "settings": self.settings_btn
        }

        # Username label on the right
        self.username_label = ctk.CTkLabel(
            self,
            text=username,
            text_color="gray",
            font=('Source Code Pro', 14, 'bold')
        )

        # Layout using grid
        ypad = (25, 15)
        self.version_control_btn.grid(row=0, column=0, padx=(20, 10), pady=ypad)
        self.asset_gallery_btn.grid(row=0, column=1, padx=10, pady=ypad)
        self.settings_btn.grid(row=0, column=2, padx=10, pady=ypad)
        self.username_label.grid(row=0, column=3, padx=20, pady=ypad, sticky="e")

        # Grid all frames in the same position
        for frame in self.frames.values():
            frame.grid(row=1, column=0, columnspan=4, sticky="nsew")

        # Show initial frame
        self.show_menu("version_control")

    def show_menu(self, menu_name: str) -> None:
        """
        * Show the selected menu frame and update button colors.
        
        Paramaters:
            menu_name: The name of the menu to display
        """
        # Update button colors
        for name, button in self.buttons.items():
            button.configure(fg_color=BUTTON_COLOUR if name == menu_name else DARKER_BLUE)

        # Raise the selected frame
        if menu_name in self.frames:
            self.frames[menu_name].tkraise()