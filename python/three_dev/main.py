# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "customtkinter",
#   "pillow",
# ]
# ///

# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from interface.sign_in import SignIn
# from data_management.user_manager import UserManager

# Constants
APP_TITLE = "3Dev"

class Application(ctk.CTk):
    def __init__(
        self,
        title: str = APP_TITLE,
        size: tuple = (
            1280,
            720
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
        ctk.set_default_color_theme("assets/themes/cobalt.json")

        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(
            size[0],
            size[1]
        )

        background = ctk.CTkImage(
            light_image=Image.open("assets/images/login_background.jpg"),
            dark_image=Image.open("assets/images/login_background.jpg"),
            size=size
        )
        self.background = ctk.CTkLabel(
            self,
            image=background,
            text=""
        )
        self.background.pack()

        self.signInData = {}

        self.signIn = SignIn(
            self,
            self.signInData
        )
        self.signIn.place(
            relx=0.5,
            rely=0.5,
            # width=320,
            # height=360,
            anchor="center"
        )

def main() -> None:
    """
    * Main function to initiate the application
    """
    app = Application()
    app.mainloop()

if __name__ == "__main__":
    main()