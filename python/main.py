# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from interface.sign_in import *
from utilities.UI import *
from interface.dashboard import *
# from data_management.user_manager import UserManager

class Application(ctk.CTk):
    def __init__(
        self,
        min_size: tuple = (
            600,
            600
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

        self.title("3Dev")
        
        self.min_size = min_size
        self.minsize(
            self.min_size[0],
            self.min_size[1]
        )
        
        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.display_sign_in()

    def _clear_window(self):
        for frame in self.grid_slaves():
            frame.grid_forget()

    def display_sign_in(self):
        self.geometry(f"{self.min_size[0]}x{self.min_size[1]}")

        self._clear_window()

        # Sign In frame
        self.user_menu = UserMenu(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.user_menu.grid(row=0, column=0, sticky="nesw")
        
    def display_dashboard(
        self,
        username: str
    ) -> None:
        self._clear_window()

        self.geometry("1920x1200")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Dashboard frames
        self.top_menu = TopMenuFrame(self, username, fg_color=DARK_BLUE)

        self.top_menu.grid(row=0, column=0, sticky="nesw")
        self.main_content.grid(row=1, column=0, sticky="nsew")

def main() -> None:
    """
    * Main function to initiate the application
    """
    app = Application()
    app.resizable(True, True)
    app.mainloop()

if __name__ == "__main__":
    main()