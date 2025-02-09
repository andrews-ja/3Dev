# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from utilities.UI import *

class Dashboard(ctk.CTkFrame):
    def __init__(
        self,
        master,
        **kwargs
    ) -> None:
        super().__init__(master, fg_color=DARK_BLUE, **kwargs)