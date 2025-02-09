# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from interface.sign_in import *
from utilities.UI import *
# from data_management.user_manager import UserManager

# Constants
APP_TITLE = "3Dev"

class Application(ctk.CTk):
    def __init__(
        self,
        title: str = APP_TITLE,
        size: tuple = (
            500,
            550
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
        ctk.set_default_color_theme("dark-blue")

        self.title(title)
        
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(
            size[0],
            size[1]
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Sign In Page
        self.user_menu = UserMenu(self)
        self.user_menu.grid(row=0, column=0, sticky="nesw")

    def displayFrame(self, master: any, frame: ctk.CTkFrame, clear: bool):
        """
        * Displays a given frame in the application window

        Parameters:
        master (any): The parent of the given frame.
        frame (ctk.CTkFrame): The frame to be displayed.
        clear (bool): A boolean indicating whether to clear the previous frames or not.
        """
        if clear:
            for child in master.winfo_children():
                child.grid_forget()
        frame.tkraise()

def main() -> None:
    """
    * Main function to initiate the application
    """
    app = Application()
    app.resizable(True, True)
    app.mainloop()

if __name__ == "__main__":
    main()