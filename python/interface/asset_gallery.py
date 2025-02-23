# External imports
import customtkinter as ctk
from typing import List

# Internal imports
from utilities.UI import *

class AssetCard(ctk.CTkFrame):
    def __init__(self, master, title: str, size: str, import_date: str, **kwargs):
        super().__init__(master, fg_color=LIGHTER_BLUE, **kwargs)

        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header frame for title and size
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=title,
            anchor="w"
        )
        self.size_label = ctk.CTkLabel(
            self.header_frame,
            text=size,
            text_color="gray"
        )
        
        # Image placeholder
        self.image_frame = ctk.CTkFrame(
            self,
            fg_color=IMAGE_COLOUR,
            height=200
        )
        
        # Import date
        self.date_label = ctk.CTkLabel(
            self,
            text=f"Imported: {import_date}",
            text_color="gray"
        )
        
        # Layout
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.title_label.grid(row=0, column=0, sticky="w")
        self.size_label.grid(row=0, column=1, sticky="e")
        self.image_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.date_label.grid(row=2, column=0, sticky="w", padx=10, pady=(5, 10))

class AssetGallery(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=DARK_BLUE, **kwargs)

        # Configure grid weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)  # Make asset grid expandable

        # Search bar
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search assets...",
            height=40,
            fg_color=LIGHTER_BLUE,
            border_width=0
        )
        
        # Category tabs
        self.category_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.categories = ["Textures", "Backgrounds"]
        self.category_buttons: List[ctk.CTkButton] = []
        
        for i, category in enumerate(self.categories):
            btn = ctk.CTkButton(
                self.category_frame,
                text=category,
                fg_color=BUTTON_COLOUR if i == 0 else "transparent",
                height=30
            )
            btn.grid(row=0, column=i, padx=(0 if i == 0 else 10, 10), pady=10)
            self.category_buttons.append(btn)

        # Import section
        self.import_frame = ctk.CTkFrame(self, fg_color=LIGHTER_BLUE)
        self.import_frame.grid_columnconfigure(0, weight=1)
        
        self.import_label = ctk.CTkLabel(
            self.import_frame,
            text="Import New Asset",
            anchor="w"
        )
        
        self.drop_frame = ctk.CTkFrame(
            self.import_frame,
            fg_color=LIGHTER_BLUE,
            height=150
        )
        self.drop_frame.grid_columnconfigure(0, weight=1)
        self.drop_frame.grid_rowconfigure(0, weight=1)
        
        # Drop zone content
        self.drop_icon_label = ctk.CTkLabel(
            self.drop_frame,
            text="↓",  # Simple arrow as placeholder for icon
            font=("Source Code Pro", 24)
        )
        self.drop_text_label = ctk.CTkLabel(
            self.drop_frame,
            text="Drag and drop files here or"
        )
        
        # Import buttons
        self.button_frame = ctk.CTkFrame(
            self.drop_frame,
            fg_color="transparent"
        )
        
        self.select_btn = ctk.CTkButton(
            self.button_frame,
            text="Select File",
            fg_color="#1e222e",
            width=100
        )
        self.import_btn = ctk.CTkButton(
            self.button_frame,
            text="Import Asset",
            fg_color=BUTTON_COLOUR,
            width=100
        )

        # Asset grid
        self.asset_grid = ctk.CTkFrame(self, fg_color="transparent")
        self.asset_grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Sample assets
        self.assets = [
            ("Metal Surface", "2.4 MB", "15-10-2024"),
            ("Brick Pattern", "1.8 MB", "20-10-2024"),
            ("Wood Grain", "2.2 MB", "22-10-2024"),
            ("Marble Texture", "4.1 MB", "25-10-2024"),
            ("Concrete Surface", "2.7 MB", "26-10-2024"),
            ("Fabric Pattern", "3.5 MB", "26-10-2024")
        ]

        # Layout
        # Search bar
        self.search_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.search_entry.grid(row=0, column=0, sticky="ew")
        
        # Category tabs
        self.category_frame.grid(row=1, column=0, sticky="w", padx=20, pady=10)
        
        # Import section
        self.import_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
        self.import_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        self.drop_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        
        # Drop zone content layout
        self.drop_icon_label.grid(row=0, column=0, pady=(20, 0))
        self.drop_text_label.grid(row=1, column=0)
        self.button_frame.grid(row=2, column=0, pady=(0, 20))
        self.select_btn.grid(row=0, column=0, padx=5)
        self.import_btn.grid(row=0, column=1, padx=5)
        
        # Asset grid
        self.asset_grid.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
        
        # Create and layout asset cards
        for i, (title, size, date) in enumerate(self.assets):
            row = i // 3
            col = i % 3
            card = AssetCard(
                self.asset_grid,
                title=title,
                size=size,
                import_date=date
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")