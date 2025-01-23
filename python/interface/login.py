# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from python.utilities.UI import *

class Login(ctk.CTkFrame):
    def __init__(
        self,
        master,
        **kwargs
    ) -> None:
        """
        * Creates and displays sign in page components.

        Parameters:
        @param master (CTk): The parent (main app) window.
        signInData (dict): A dictionary to store user data to be passed to main.
        """
        
        super().__init__(master, **kwargs)
        
        self.columnconfigure((1,2,3), weight=1)
        self.rowconfigure((1,2,3,4), weight=1)

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
                "All fields must be filled",
                self,
                False
            )
        else:
            outputMsg(
                "Validating Credentials...",
                self,
                True
            )
            # TODO: insert database check and display window call