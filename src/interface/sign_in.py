# Library imports
import customtkinter as ctk
from PIL import Image


class SignInTabs(ctk.CTkTabview):
    def __init__(
        self,
        master,
        signInData: dict,
        **kwargs
    ) -> None:
        """
        * Constructs the "Sign Up" and "Login" tabs.

        Parameters:
        master (CTkFrame): The parent frame.
        signInData (dict): A dictionary to store user data.
        """

        super().__init__(master, **kwargs)

        self.signInData = signInData

        self.tab1 = "Sign Up"
        self.tab2 = "Login"

        self.add(self.tab1)

        self.newUserEntry = self.createEntry(
            self.tab1,
            "user"
        )
        self.newUserEntry.pack(pady=10)

        self.newPassEntry = self.createEntry(
            self.tab1,
            "password"
        )
        self.newPassEntry.pack(pady=10)

        self.confPassEntry = self.createEntry(
            self.tab1,
            "passwordConf"
        )
        self.confPassEntry.pack(pady=10)

        self.signUpButton = ctk.CTkButton(
            self.tab(self.tab2),
            text=self.tab1,
            command=self.signupSubmit,
            font=(
                "Source Code Pro",
                13
            ),
        )
        self.signUpButton.pack(pady=10)

        self.add(self.tab2)

        self.userEntry = self.createEntry(
            self.tab2,
            "user"
            )
        self.userEntry.pack(pady=10)

        self.passEntry = self.createEntry(
            self.tab2,
            "password"
        )
        self.passEntry.pack(pady=10)

        self.loginButton = ctk.CTkButton(
            self.tab(self.tab2),
            text=self.tab2,
            command=lambda: self.loginSubmit,
            font=(
                "Source Code Pro",
                13
            ),
        )
        self.loginButton.pack(pady=10)

        self.loginMessage = ctk.CTkLabel(
            self.tab(self.tab2),
            text="",
            font=(
                "Source Code Pro",
                10
            ),
        )
        self.loginMessage.pack()

    def createEntry(
        self,
        tab: str,
        field: str
    ) -> ctk.CTkEntry:
        """
        * Creates entry box to be displayed on the self.tab1 and self.tab2 tabs.

        Parameters:
        tab (bool): True if the entry is for the self.tab1 tab, False for the self.tab2 tab.
        field (str): The field for the entry box (e.g., "user", "password", "passwordConf").

        Returns:
        ctk.CTkEntry: The created entry box.
        """
        
        fieldDict = {
            "user": ("Enter Username", ""),
            "password": ("Enter Password", "\u2022"),
            "passwordConf": ("Confirm Password", "\u2022"),
        }

        return ctk.CTkEntry(
            self.tab(tab),
            width=210,
            height=42,
            placeholder_text=fieldDict.get(field, "")[0],
            font=("Source Code Pro", 13),
            border_color="white",
            border_width=1,
            show=fieldDict.get(field, "")[1],
        )
    
    def passData(
        self,
        username: str,
        password: str,
        tab: str
    ) -> None:
        """
        * Takes username and password credentials and passes them to main to be handeled by the data manager.

        Parameters:
        username (str): The username to be stored/checked.
        password (str): The password to be stored/checked.
        tab (str): The tab where the credentials were inputted (self.tab1/self.tab2).
        """
        
        self.signInData.update(
            {
                "username": username,
                "password": password,
                "tab": tab,
            }
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
            self.outputMsg(
                "All fields must be filled",
                self.tab1,
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
            self.outputMsg(
                    "Creating Account...",
                    self.tab1,
                    True
                )
            
            self.passData(
                username,
                pass1,
                self.tab1
            )

        if not all(userValidation):
            self.newUserEntry.configure(border_color="red")

            if not userValidation[0]:
                self.outputMsg(
                "Username must be between 2 and 50 characters",
                self.tab1,
                False
            )
            else:
                self.outputMsg(
                    "Username must not contain any special characters",
                    self.tab1,
                    False
                )
        else:
            self.newUserEntry.configure(border_color="white")

        if not all(passValidation):
            self.newPassEntry.configure(border_color="red")

            if not passValidation[0]:
                self.outputMsg(
                    "Password must be between 8 and 50 characters",
                    self.tab1,
                    False
                )
            elif not passValidation[1]:
                self.outputMsg(
                "Password must not contain more than 3 consecutive numbers",
                self.tab1,
                False
            )
            elif not passValidation[2]:
                self.outputMsg(
                    "Password must contain at least 2 special characters",
                    self.tab1,
                    False
                )
        else:
            self.newPassEntry.configure(border_color="white")

        if not validPass2:
            self.confPassEntry.configure(border_color="red")

            self.outputMsg(
                "Passwords do not match",
                self.tab1,
                False
            )
        else:
            self.confPassEntry.configure(border_color="white")
    
    def loginSubmit(
        self
    ) -> None:
        """
        * Outputs error message if a field is missing, otherwise, passes credentials through to main to be handled by data manager.
        """

        username = self.userEntry.get()
        password = self.passEntry.get()

        if not (username and password):
            self.outputMsg(
                "All fields must be filled",
                self.tab2,
                False
            )
        else:
            self.outputMsg(
                "Validating Credentials...",
                self.tab2,
                True
            )
            
            self.passData(
                username,
                password,
                self.tab2
            )

    def outputMsg(
        self,
        msg: str,
        tab: str,
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
            self.tab(tab),
            text=msg,
            font=(
                "Source Code Pro",
                12.5
            ),
            text_color="green" if success else "red"
        )
        signUpMessage.pack()

class SignIn(ctk.CTkFrame):
    def __init__(
        self,
        master,
        signInData: dict,
        **kwargs
    ) -> None:
        """
        * Creates and displays sign in page components.

        Parameters:
        @param master (CTk): The parent (main app) window.
        signInData (dict): A dictionary to store user data to be passed to main.
        """
        
        super().__init__(master, **kwargs)

        self.signInData = signInData

        self.title = ctk.CTkLabel(
            self,
            text="3Dev",
            font=(
                "Source Code Pro",
                60
            )
        )
        self.title.pack()

        self.tabs = SignInTabs(
            self,
            self.signInData
        )
        self.tabs.pack()
