# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from utilities.UI import *

class UserMenu(ctk.CTkFrame):
    def __init__(
        self,
        master,
        **kwargs
    ) -> None:
        super().__init__(master, fg_color=DARK_BLUE, **kwargs)

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1, 2), weight=1)

        self.signup_button = ctk.CTkButton(
            self,
            text="Sign Up",
            command=lambda: self.show_menu(self.signUp),
            fg_color=DARK_BLUE,  # Dark blue background
            hover_color=HOVER_COLOUR1,  # Slightly lighter on hover
            border_width=0,
            corner_radius=8,
            text_color=UNSELECTED_COLOR, # Initial selected color
            height=37
        )
        self.signUp = SignUp(self)

        self.login_button = ctk.CTkButton(
            self,
            text="Login",
            command=lambda: self.show_menu(self.login),
            fg_color=LIGHTER_BLUE,  # Dark blue background
            hover_color=HOVER_COLOUR1,  # Slightly lighter on hover
            border_width=0,
            corner_radius=8,
            text_color="white",
            height=37
        )
        self.login = Login(self)

        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="3Dev",
            font=(
                "Source Code Pro",
                30
            ),
            text_color="white"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        
        self.login_button.grid(row=1, column=0, padx=(20, 5), pady=(20, 0), sticky="e")
        self.signup_button.grid(row=1, column=1, padx=(5, 20), pady=(20, 0), sticky="w")

        self.signUp.grid(row=2, column=0, columnspan=2, pady=30, sticky="nesw")
        self.login.grid(row=2, column=0, columnspan=2, pady=30, sticky="nesw")

        self.show_menu(self.login)  # Show login page by default

    def show_menu(self, frame):
        if frame == self.signUp:
            self.signup_button.configure(text_color="white", fg_color=LIGHTER_BLUE)
            self.login_button.configure(text_color=UNSELECTED_COLOR, fg_color=DARKER_BLUE)
        else:
            self.signup_button.configure(text_color=UNSELECTED_COLOR, fg_color=DARKER_BLUE)
            self.login_button.configure(text_color="white", fg_color=LIGHTER_BLUE)
        frame.tkraise()

class SignUp(ctk.CTkFrame):
    def __init__(
        self,
        master,
        **kwargs
    ) -> None:
        """
        * Creates and displays sign up page components.

        Parameters:
        @param master (CTk): The parent (main app) window.
        signInData (dict): A dictionary to store user data to be passed to main.
        """
        
        super().__init__(master, fg_color=DARK_BLUE, **kwargs)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(tuple(range(11)), weight=1)

        # Username input
        self.username_label = ctk.CTkLabel(
            self,
            text="Username",
            fg_color=DARK_BLUE)
        self.username_label.grid(row=1, column=0, padx=50, pady=(5, 0), sticky="w")

        self.newUserEntry = ctk.CTkEntry(
            self,
            placeholder_text="Enter username",
            height=50,
            fg_color=LIGHTER_BLUE,
            border_width=0)
        self.newUserEntry.grid(row=2, column=0, padx=50, pady=(0, 5), sticky="ew")

        # Password input
        self.password_label = ctk.CTkLabel(
            self,
            text="Password",
            fg_color=DARK_BLUE)
        self.password_label.grid(row=4, column=0, padx=50, pady=(5, 0), sticky="w")

        self.newPassEntry = ctk.CTkEntry(
            self,
            placeholder_text="Enter password",
            show="\u2022", height=50,
            fg_color=LIGHTER_BLUE,
            border_width=0)
        self.newPassEntry.grid(row=5, column=0, padx=50, pady=(0, 5), sticky="ew")

        # Confirm password input
        self.confirm_password_label = ctk.CTkLabel(
            self,
            text="Confirm Password",
            fg_color=DARK_BLUE)
        self.confirm_password_label.grid(row=7, column=0, padx=50, pady=(5, 0), sticky="w")

        self.confPassEntry = ctk.CTkEntry(
            self,
            placeholder_text="Confirm password",
            show="\u2022",
            height=50,
            fg_color=LIGHTER_BLUE,
            border_width=0)
        self.confPassEntry.grid(row=8, column=0, padx=50, pady=(0, 5), sticky="ew")

        # Create account button
        self.create_account_button = ctk.CTkButton(
            self,
            text="Create Account",
            command=self.signupSubmit,
            height=50,
            fg_color=BUTTON_COLOUR,
            hover_color=HOVER_COLOUR2)
        self.create_account_button.grid(row=10, column=0, padx=35, pady=(30, 10), sticky="ew")

    def signupSubmit(
        self
    ) -> None:
        """
        * Validates credentials to ensure they fit the required format - displays error messages if invalid, otherwise, passes credentials through to main to be handled by the data manager.
        """
        
        username = self.newUserEntry.get()
        pass1 = self.newPassEntry.get()
        pass2 = self.confPassEntry.get()

        if not(username and pass1 and pass2):
            outputMsg(
                self,
                "All fields must be filled",
                False
            )

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
            outputMsg(
                    self,
                    "Creating Account...",
                    True
                )

        if not all(userValidation):
            self.newUserEntry.configure(border_color="red", border_width=1)

            if not userValidation[0]:
                outputMsg(
                self,
                "Username must be between 2 and 50 characters",
                False
            )
            else:
                outputMsg(
                    self,
                    "Username must not contain any special characters",
                    False
                )
        else:
            self.newUserEntry.configure(border_color="green", border_width=1)

        if not all(passValidation):
            self.newPassEntry.configure(border_color="red", border_width=1)

            if not passValidation[0]:
                outputMsg(
                    self,
                    self,
                    "Password must be between 8 and 50 characters",
                    False
                )
            elif not passValidation[1]:
                outputMsg(
                self,
                "Password must not contain more than 3 consecutive numbers",
                False
            )
            elif not passValidation[2]:
                outputMsg(
                    self,
                    "Password must contain at least 2 special characters",
                    False
                )
        else:
            self.newPassEntry.configure(border_color="green", border_width=1)

        if not validPass2:
            self.confPassEntry.configure(border_color="red", border_width=1)

            outputMsg(
                self,
                "Passwords do not match",
                False
            )
        else:
            self.confPassEntry.configure(border_color="green", border_width=1)

class Login(ctk.CTkFrame):
    def __init__(
        self,
        master,
        **kwargs
    ) -> None:
        """
        * Creates and displays login page components.

        Parameters:
        @param master (CTk): The parent (main app) window.
        signInData (dict): A dictionary to store user data to be passed to main.
        """
        
        super().__init__(master, fg_color=DARK_BLUE, **kwargs)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(tuple(range(6)), weight=1)

        # Username input
        self.username_label = ctk.CTkLabel(
            self,
            text="Username")
        self.username_label.grid(row=1, column=0, padx=50, pady=(5, 0), sticky="w")
        self.userEntry = ctk.CTkEntry(
            self,
            placeholder_text="Enter username",
            height=50,
            fg_color=LIGHTER_BLUE,
            border_width=0)
        self.userEntry.grid(row=2, column=0, padx=50, pady=(0, 5), sticky="ew")

        # Password input
        self.password_label = ctk.CTkLabel(
            self,
            text="Password")
        self.password_label.grid(row=3, column=0, padx=50, pady=(5, 0), sticky="w")
        self.passEntry = ctk.CTkEntry(
            self,
            placeholder_text="Enter password",
            show="\u2022",
            height=50,
            fg_color=LIGHTER_BLUE,
            border_width=0)
        self.passEntry.grid(row=4, column=0, padx=50, pady=(0, 5), sticky="ew")

        # Login button
        self.login_button = ctk.CTkButton(
            self,
            text="Login",
            command=self.loginSubmit,
            height=50,
            fg_color=BUTTON_COLOUR,
            hover_color=HOVER_COLOUR2)
        self.login_button.grid(row=5, column=0, padx=35, pady=(30, 10), sticky="ew")

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
                self,
                "All fields must be filled",
                False
            )
        else:
            outputMsg(
                self,
                "Validating Credentials...",
                True
            )
            # TODO: insert database check and display window call
        
        self.userEntry.configure(border_color="green", border_width=1)
        self.passEntry.configure(border_color="green", border_width=1)