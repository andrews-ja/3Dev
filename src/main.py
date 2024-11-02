# Library imports
import customtkinter as ctk
from PIL import Image

# Internal imports
from interface.sign_in import SignIn

class Application(ctk.CTk):
    def __init__(self, title: str = "3Dev", size: tuple = (950, 950)):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("assets/themes/cobalt.json")

        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(size[0], size[1])

        background = ctk.CTkImage(
            light_image=Image.open("assets/images/light_sign_in.png"),
            dark_image=Image.open("assets/images/dark_sign_in.png"),
            size=size)
        self.background = ctk.CTkLabel(self, image=background, text="")
        self.background.pack()

        self.signIn = SignIn(self)

def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()