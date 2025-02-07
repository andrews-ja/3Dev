# Library imports
import customtkinter as ctk
from PIL import Image

def displayFrame(self, master: any, frame: ctk.CTkFrame, clear: bool):
    """
    * Displays a given frame in the application window
    """
    if clear:
        for child in master.winfo_children():
            child.grid_forget()
    frame.tkraise()

def createEntry(
    master: any,
    txt: str,
    hide: bool,
) -> ctk.CTkEntry:
        """
        * Creates entry box to be displayed on the self.tab1 and self.tab2 tabs.

        Parameters:
        tab (bool): True if the entry is for the self.tab1 tab, False for the self.tab2 tab.
        field (str): The field for the entry box (e.g., "user", "password", "passwordConf").

        Returns:
        ctk.CTkEntry: The created entry box.
        """

        return ctk.CTkEntry(
            master,
            width=210,
            height=42,
            placeholder_text=txt,
            font=("Source Code Pro", 13),
            border_color="white",
            border_width=1,
            show="\u2022" if hide else ""
        )

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