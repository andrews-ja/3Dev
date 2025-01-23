# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from python.interface.sign_up import SignUp
from python.interface.login import Login
from python.utilities.UI import *
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
        # ctk.set_default_color_theme()

        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(
            size[0],
            size[1]
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        backgroundImg = ctk.CTkImage(
            light_image=Image.open("assets/images/mountains.jpg"),
            dark_image=Image.open("assets/images/forest.jpg"),
            size=size
        )
        setBackground(self, backgroundImg)

        self.signUp = SignUp(self)
        self.login = Login(self)
        
        for frame in (self.signUp, self.login):
            frame.grid(row=0, column=0, sticky="nsew")
        
        displayFrame(self, self.signUp, True)

def main() -> None:
    """
    * Main function to initiate the application
    """
    app = Application()
    app.resizable(False, False)
    app.mainloop()

if __name__ == "__main__":
    main()