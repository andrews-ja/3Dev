# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from utilities.UI import *

class Login(ctk.CTkFrame):
    def __init__(
        self,
        master,
        **kwargs
    ) -> None:
        """
        * Creates and displays login page components.

        Parameters:
        @param master (CTk): The parent (main app) window.
        signInData (dict): A dictionary to store user data to be passed to main.
        """
        
        super().__init__(master, fg_color="#242436", **kwargs)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Page title - REMOVE
        # self.title_label = ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=20, weight="bold"))  # Reduced font size
        # self.title_label.grid(row=0, column=0, padx=10, pady=(10, 5))  # Reduced padding

        # Username input
        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="w")  # Reduced padding
        self.userEntry = ctk.CTkEntry(self, placeholder_text="Enter username", height=40)  # Increased height
        self.userEntry.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")  # Reduced padding

        # Password input
        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="w")  # Reduced padding
        self.passEntry = ctk.CTkEntry(self, placeholder_text="Enter password", show="*", height=40)  # Increased height
        self.passEntry.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="ew")  # Reduced padding

        # Login button
        self.login_button = ctk.CTkButton(self, text="Login", command=self.loginSubmit, height=40)  # Increased height
        self.login_button.grid(row=5, column=0, padx=10, pady=(10, 10), sticky="ew")  # Reduced padding
        self.login_button.configure(
            fg_color="#0096D6",
            hover_color="#0077B6",
            border_width=0,
            corner_radius=8
        )

    def loginSubmit(
        self
    ) -> None:
        """
        * Outputs error message if a field is missing, otherwise, passes credentials through to main to be handled by data manager.
        """

        username = self.userEntry.get()
        password = self.passEntry.get()

        if not (username and password):
            outputMsg(
                self,
                "All fields must be filled",
                False
            )
        else:
            outputMsg(
                self,
                "Validating Credentials...",
                True
            )
            # TODO: insert database check and display window call
        
        self.userEntry.configure(border_color="green") #Success border color
        self.passEntry.configure(border_color="green") #Success border color