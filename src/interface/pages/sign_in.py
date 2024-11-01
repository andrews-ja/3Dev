# Library imports
import customtkinter as ctk
from PIL import Image


class SignInTabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.add("Sign Up")

        self.newUserEntry = self.createEntry(
            True,
            "user")
        self.newUserEntry.pack(pady=10)

        self.newPassEntry = self.createEntry(
            True,
            "password")
        self.newPassEntry.pack(pady=10)

        self.confPassEntry = self.createEntry(
            True,
            "pass2")
        self.confPassEntry.pack(pady=10)

        self.signUpButton = ctk.CTkButton(
            self.tab("Sign Up"),
            text="Sign Up",
            command=self.signupSubmit,
            font=("Source Code Pro", 13),
        )
        self.signUpButton.pack(pady=10)

        self.add("Login")

        self.userEntry = self.createEntry(
            False,
            "user")
        self.userEntry.pack(pady=10)

        self.passEntry = self.createEntry(
            False,
            "password")
        self.passEntry.pack(pady=10)

        self.loginButton = ctk.CTkButton(
            self.tab("Login"),
            text="Login",
            command=self.loginSubmit,
            font=("Source Code Pro", 13),
        )
        self.loginButton.pack(pady=10)

        self.loginMessage = ctk.CTkLabel(
            self.tab("Login"),
            text="",
            font=("Source Code Pro", 10),
        )
        self.loginMessage.pack()

    def signupSubmit(self) -> tuple[bool, str, str]:

        username = self.newUserEntry.get()
        pass1 = self.newPassEntry.get()
        pass2 = self.confPassEntry.get()

        negRetVal = (
            False,
            "",
            ""
        )

        if not(username and pass1 and pass2):
            self.outputMsg(
                "All fields must be filled",
                "red"
            )
            return negRetVal

        specChCount = lambda text: len([ch for ch in text if not ch.isalnum() and not ch.isspace()])

        userValidation = [len(username) in range(2, 51), not specChCount(username)]

        if len(pass1) in range(8, 51):
            validPassLen = True
            for i in range(len(pass1)):
                if pass1[i : i + 3].isnumeric():
                    validPassDigits = not({int(pass1[j + 1]) - int(pass1[j]) for j in range(i, i+2)} == {
                        1,
                        -1
                    })
                else:
                    validPassDigits = True
        else:
            validPassLen = False
            validPassDigits = False

        passValidation = [validPassLen, validPassDigits, specChCount(pass1) >= 2]

        validPass2 = pass2 == pass1

        if all(userValidation) and all(passValidation) and validPass2:
            self.newUserEntry.configure(border_color="white")
            self.newPassEntry.configure(border_color="white")
            self.confPassEntry.configure(border_color="white")
            self.outputMsg(
                    "Credentials valid",
                    "green"
                )
            return True, username, pass1

        if not all(userValidation):
            self.newUserEntry.configure(border_color="red")
            if not userValidation[0]:
                self.outputMsg(
                "Username must be between 2 and 50 characters",
                "red"
            )
            else:
                self.outputMsg(
                    "Username must not contain any special characters",
                    "red"
                )
            return negRetVal
        else:
            self.newUserEntry.configure(border_color="white")

        if not all(passValidation):
            self.newPassEntry.configure(border_color="red")
            if not passValidation[0]:
                self.outputMsg(
                    "Password must be between 8 and 50 characters",
                    "red"
                )
            elif not passValidation[1]:
                self.outputMsg(
                "Password must not contain more than 3 consecutive numbers",
                "red"
            )

            elif not passValidation[2]:
                self.outputMsg(
                    "Password must contain at least 2 special characters",
                    "red"
                )
            return negRetVal
        else:
            self.newPassEntry.configure(border_color="white")

        if not validPass2:
            self.confPassEntry.configure(border_color="red")
            self.outputMsg(
                "Passwords do not match",
                "red"
            )
            return negRetVal
        else:
            self.confPassEntry.configure(border_color="white")

    def loginSubmit(self) -> bool:
        username = self.userEntry.get()
        password = self.passEntry.get()

    def createEntry(self, tab1: bool, field: str):
        fieldDict = {
            "user": ("Enter Username", ""),
            "password": ("Enter Password", "\u2022"),
            "pass2": ("Confirm Password", "\u2022"),
        }

        return ctk.CTkEntry(
            self.tab("Sign Up" if tab1 else "Login"),
            width=210,
            height=42,
            placeholder_text=fieldDict.get(field, "")[0],
            font=("Source Code Pro", 13),
            border_color="white",
            border_width=1,
            show=fieldDict.get(field, "")[1],
        )
    
    def outputMsg(self, msg: str, colour: str):
        signUpMessage = ctk.CTkLabel(
        self.tab("Sign Up"),
        text=msg,
        font=("Source Code Pro", 12.5),
        text_color=colour
        )
        signUpMessage.pack()


class SignIn(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title = ctk.CTkLabel(self, text="3Dev", font=("Source Code Pro", 60))
        self.title.pack()

        self.tabs = SignInTabs(
            master=self,
            corner_radius=10,
        )
        self.tabs.pack(fill="y")

        self.grid(row=1, column=1)
