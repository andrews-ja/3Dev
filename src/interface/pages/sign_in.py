# Library imports
import customtkinter as ctk
from PIL import Image


class SignInTabs(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.credentials = (None, None)

        self.add("Sign Up")

        self.newUserEntry = self.createEntry(
            True,
            "user"
        )
        self.newUserEntry.pack(pady=10)

        self.newPassEntry = self.createEntry(
            True,
            "password"
        )
        self.newPassEntry.pack(pady=10)

        self.confPassEntry = self.createEntry(
            True,
            "passwordConf"
        )
        self.confPassEntry.pack(pady=10)

        self.signUpButton = ctk.CTkButton(
            self.tab("Sign Up"),
            text="Sign Up",
            command=self.signupSubmit,
            font=(
                "Source Code Pro",
                13
            ),
        )
        self.signUpButton.pack(pady=10)

        self.add("Login")

        self.userEntry = self.createEntry(
            False,
            "user"
            )
        self.userEntry.pack(pady=10)

        self.passEntry = self.createEntry(
            False,
            "password"
        )
        self.passEntry.pack(pady=10)

        self.loginButton = ctk.CTkButton(
            self.tab("Login"),
            text="Login",
            command=lambda: self.output(
                "Validating Credentials...",
                (
                    True,
                    self.userEntry.get(),
                    self.passEntry.get(),
                    True
                    )
                ),
            font=(
                "Source Code Pro",
                13
            ),
        )
        self.loginButton.pack(pady=10)

        self.loginMessage = ctk.CTkLabel(
            self.tab("Login"),
            text="",
            font=(
                "Source Code Pro",
                10
            ),
        )
        self.loginMessage.pack()

    def signupSubmit(self) -> tuple[bool, str, str]:

        username = self.newUserEntry.get()
        pass1 = self.newPassEntry.get()
        pass2 = self.confPassEntry.get()

        negRetVal = (
            False,
            "",
            "",
            False
        )

        if not(username and pass1 and pass2):
            self.output(
                "All fields must be filled",
                "red"
            )
            return negRetVal

        specChCount = lambda text: len([ch for ch in text if not ch.isalnum() and not ch.isspace()])

        userValidation = [len(username) in range(2, 51), not specChCount(username)]

        if len(pass1) in range(8, 51):
            validPassLen = True

            noDigits = True
            for i in range(len(pass1)-3):
                if pass1[i : i + 4].isnumeric():
                    noDigits = False
                    validPassDigits = not(
                        {int(pass1[j + 1]) - int(pass1[j]) for j in range(i, i+3)} == {1}
                    )
            if noDigits: validPassDigits = True
        else:
            validPassLen = False
            validPassDigits = False

        passValidation = [validPassLen, validPassDigits, specChCount(pass1) >= 2]

        validPass2 = pass2 == pass1

        if all(userValidation) and all(passValidation) and validPass2:
            self.output(
                    "Credentials valid",
                    (
                        True,
                        username,
                        pass1,
                        False
                    )
                )

        if not all(userValidation):
            self.newUserEntry.configure(border_color="red")
            if not userValidation[0]:
                self.output(
                "Username must be between 2 and 50 characters",
                negRetVal
            )
            else:
                self.output(
                    "Username must not contain any special characters",
                    negRetVal
                )
        else:
            self.newUserEntry.configure(border_color="white")

        if not all(passValidation):
            self.newPassEntry.configure(border_color="red")
            if not passValidation[0]:
                self.output(
                    "Password must be between 8 and 50 characters",
                    negRetVal
                )
            elif not passValidation[1]:
                self.output(
                "Password must not contain more than 3 consecutive numbers",
                negRetVal
            )
            elif not passValidation[2]:
                self.output(
                    "Password must contain at least 2 special characters",
                    negRetVal
                )
        else:
            self.newPassEntry.configure(border_color="white")

        if not validPass2:
            self.confPassEntry.configure(border_color="red")
            self.output(
                "Passwords do not match",
                negRetVal
            )
        else:
            self.confPassEntry.configure(border_color="white")

    def createEntry(self, tab1: bool, field: str):
        fieldDict = {
            "user": ("Enter Username", ""),
            "password": ("Enter Password", "\u2022"),
            "passwordConf": ("Confirm Password", "\u2022"),
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
    
    def output(self, msg: str, retVal: tuple[bool, str, str, bool]) -> tuple[str, str]:
        signUpMessage = ctk.CTkLabel(
            self.tab("Login" if retVal[-1] else "Sign Up"),
            text=msg,
            font=(
                "Source Code Pro",
                12.5
            ),
            text_color="green" if retVal[0] else "red"
        )
        signUpMessage.pack()

        self.credentials = retVal[1:]

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