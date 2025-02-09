# Library imports
import customtkinter as ctk
from PIL import Image

#Constants
DARK_BLUE = "#121221"
DARKER_BLUE = "#0f0f1c"
LIGHTER_BLUE = "#242436"
UNSELECTED_COLOR = "#989696"
BUTTON_COLOUR = "#6f6fd6"
HOVER_COLOUR1 = "#33334a"
HOVER_COLOUR2 = "#505099"

def outputMsg(
    master: str,
    msg: str,
    success: bool
) -> None:
    """
    * Displays a message below the "Sign Up" or "Login" button in either red or green to indicate an error in the users input or what the app is doing next.

    Parameters:
    msg (str): The message to be displayed.
    tab (str): The tab where the message will be displayed.
    success (bool): A boolean indicating whether the input was valid.
    """
    
    signUpMessage = ctk.CTkLabel(
        master,
        text=msg,
        font=(
            "Source Code Pro",
            12.5
        ),
        text_color="green" if success else "red"
    )
    signUpMessage.grid(row=0, column=0, sticky="nsew")

def setBackground(
    master: any,
    img: ctk.CTkImage
) -> None:
    """
    * Sets the background of the main application window.
    """

    master.background = ctk.CTkLabel(
        master,
        image=img,
        text=""
    )
    master.background.grid(row=0, column=0, sticky="nsew")