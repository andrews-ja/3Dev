# Library imports
import customtkinter as ctk
from PIL import Image

# Local imports
from python.utilities.UI import *


class SignUp(ctk.CTkFrame):
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
                "All fields must be filled",
                self,
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
                    "Creating Account...",
                    self,
                    True
                )

        if not all(userValidation):
            self.newUserEntry.configure(border_color="red")

            if not userValidation[0]:
                outputMsg(
                "Username must be between 2 and 50 characters",
                self,
                False
            )
            else:
                outputMsg(
                    "Username must not contain any special characters",
                    self,
                    False
                )
        else:
            self.newUserEntry.configure(border_color="white")

        if not all(passValidation):
            self.newPassEntry.configure(border_color="red")

            if not passValidation[0]:
                outputMsg(
                    "Password must be between 8 and 50 characters",
                    self,
                    False
                )
            elif not passValidation[1]:
                outputMsg(
                "Password must not contain more than 3 consecutive numbers",
                self,
                False
            )
            elif not passValidation[2]:
                outputMsg(
                    "Password must contain at least 2 special characters",
                    self,
                    False
                )
        else:
            self.newPassEntry.configure(border_color="white")

        if not validPass2:
            self.confPassEntry.configure(border_color="red")

            outputMsg(
                "Passwords do not match",
                self,
                False
            )
        else:
            self.confPassEntry.configure(border_color="white")