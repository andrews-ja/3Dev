# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from utilities.UI import *

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
        
        super().__init__(master, fg_color="#242436", **kwargs)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Page title - REMOVE
        # self.title_label = ctk.CTkLabel(self, text="Sign Up", font=ctk.CTkFont(size=20, weight="bold"))  # Reduced font size
        # self.title_label.grid(row=0, column=0, padx=10, pady=(10, 5))  # Reduced padding

        # Username input
        self.username_label = ctk.CTkLabel(self, text="Username")
        self.username_label.grid(row=1, column=0, padx=10, pady=(5, 0), sticky="w")  # Reduced padding
        self.newUserEntry = ctk.CTkEntry(self, placeholder_text="Enter username", height=40)  # Increased height
        self.newUserEntry.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="ew")  # Reduced padding

        # Password input
        self.password_label = ctk.CTkLabel(self, text="Password")
        self.password_label.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="w")  # Reduced padding
        self.newPassEntry = ctk.CTkEntry(self, placeholder_text="Enter password", show="*", height=40)  # Increased height
        self.newPassEntry.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="ew")  # Reduced padding

        # Confirm password input
        self.confirm_password_label = ctk.CTkLabel(self, text="Confirm Password")
        self.confirm_password_label.grid(row=5, column=0, padx=10, pady=(5, 0), sticky="w")  # Reduced padding
        self.confPassEntry = ctk.CTkEntry(self, placeholder_text="Confirm password", show="*", height=40)  # Increased height
        self.confPassEntry.grid(row=6, column=0, padx=10, pady=(0, 5), sticky="ew")  # Reduced padding

        # Create account button
        self.create_account_button = ctk.CTkButton(self, text="Create Account", command=self.signupSubmit, height=40)  # Increased height
        self.create_account_button.grid(row=7, column=0, padx=10, pady=(10, 10), sticky="ew")  # Reduced padding
        self.create_account_button.configure(
            fg_color="#0096D6",
            hover_color="#0077B6",
            border_width=0,
            corner_radius=8
        )


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
            self.newUserEntry.configure(border_color="red")

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
            self.newUserEntry.configure(border_color="green")  # Success border color

        if not all(passValidation):
            self.newPassEntry.configure(border_color="red")

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
            self.newPassEntry.configure(border_color="green")  # Success border color

        if not validPass2:
            self.confPassEntry.configure(border_color="red")

            outputMsg(
                self,
                "Passwords do not match",
                False
            )
        else:
            self.confPassEntry.configure(border_color="green")  # Success border color