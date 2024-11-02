# Library imports
import customtkinter as ctk

# Internal imports
from interface.pages.sign_in import SignIn

class Application(ctk.CTk):
    def __init__(self, title: str = "3Dev", size: tuple = (950, 950)):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        self.grid_columnconfigure((0, 2), weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=3, uniform="a")
        self.grid_rowconfigure((0, 2), weight=1, uniform="a")
        self.grid_rowconfigure(1, weight=2, uniform="a")

        self.signIn = SignIn(self, fg_color="transparent")

def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()