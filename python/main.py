# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from interface.sign_up import SignUp
from interface.login import Login
from utilities.UI import *
# from data_management.user_manager import UserManager

# Constants
APP_TITLE = "3Dev"
DARK_BLUE = "#242436"  # Dark blue color
SELECTED_COLOR = "#0096D6" # Color for selected button

class Application(ctk.CTk):
    def __init__(
        self,
        title: str = APP_TITLE,
        size: tuple = (
            600,  # Reduced width
            600   # Reduced height
        )
    ) -> None:
        """
        * Initializes and manages the application window

        Parameters:
        title (str): The title of the application window.
        size (tuple): The size of the application window in pixels (width, height).
        """
        
        super().__init__()

        ctk.set_appearance_mode("System")
        # ctk.set_default_color_theme()

        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(
            size[0],
            size[1]
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Configure dark blue theme
        self.configure(bg=DARK_BLUE)

        # Remove background image
        # backgroundImg = ctk.CTkImage(
        #     light_image=Image.open("assets/images/mountains.jpg"),
        #     dark_image=Image.open("assets/images/forest.jpg"),
        #     size=size
        # )
        # setBackground(self, backgroundImg)

        # Navigation buttons
        self.button_frame = ctk.CTkFrame(self, fg_color=DARK_BLUE)  # Dark blue background
        self.button_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.button_frame.columnconfigure((0, 1), weight=1)

        self.signup_button = ctk.CTkButton(
            self.button_frame,
            text="Sign Up",
            command=lambda: self.show_frame(self.signUp),
            fg_color=DARK_BLUE,  # Dark blue background
            hover_color="#33334a",  # Slightly lighter on hover
            border_width=0,
            corner_radius=8,
            text_color=SELECTED_COLOR # Initial selected color
        )
        self.signup_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.login_button = ctk.CTkButton(
            self.button_frame,
            text="Login",
            command=lambda: self.show_frame(self.login),
            fg_color=DARK_BLUE,  # Dark blue background
            hover_color="#33334a",  # Slightly lighter on hover
            border_width=0,
            corner_radius=8,
            text_color="white"
        )
        self.login_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.signUp = SignUp(self)
        self.login = Login(self)
        
        self.signUp.grid(row=1, column=0, sticky="nesw")
        self.login.grid(row=1, column=0, sticky="nesw")
        
        self.show_frame(self.signUp)
        self.selected_frame = self.signUp #Keep track of selected frame

    def show_frame(self, frame):
        if frame == self.signUp:
            self.signup_button.configure(text_color=SELECTED_COLOR)
            self.login_button.configure(text_color="white")
        else:
            self.signup_button.configure(text_color="white")
            self.login_button.configure(text_color=SELECTED_COLOR)
        frame.tkraise()
        self.selected_frame = frame

def main() -> None:
    """
    * Main function to initiate the application
    """
    app = Application()
    app.resizable(False, False)
    app.mainloop()

if __name__ == "__main__":
    main()