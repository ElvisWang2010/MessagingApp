import tkinter as tk

from config import (
    APP_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MIN_WIDTH,
    MIN_HEIGHT
)

from login import create_login_screen
from chat import create_chat_screen
from launcher import PetalLauncher


class PetalApp:

    def __init__(self):

        # Create the main application window
        self.root = tk.Tk()

        # IMPORTANT:
        # Hide the main window immediately.
        # This prevents the login/chat window from flashing
        # on screen while Petal is starting.
        self.root.withdraw()

        # Window settings
        self.root.title(APP_TITLE)

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.root.minsize(
            MIN_WIDTH,
            MIN_HEIGHT
        )

        # Keep track of the launcher
        self.launcher = None

        # Keep track of whether the app is currently open
        self.app_open = False

        # When the user presses X on the main window,
        # minimize Petal back to the launcher instead of exiting.
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.minimize_to_launcher
        )

        # Create the login screen
        self.show_login()

        # Create the launcher AFTER the main window has
        # already been withdrawn.
        self.create_launcher()

    # ---------------------------------------------------------
    # Login
    # ---------------------------------------------------------

    def show_login(self):

        self.clear_window()

        create_login_screen(
            self.root,
            self.login_success
        )

    # ---------------------------------------------------------
    # Login success
    # ---------------------------------------------------------

    def login_success(self, username):

        self.show_chat(username)

    # ---------------------------------------------------------
    # Chat
    # ---------------------------------------------------------

    def show_chat(self, username):

        self.clear_window()

        create_chat_screen(
            self.root,
            username
        )

    # ---------------------------------------------------------
    # Clear current screen
    # ---------------------------------------------------------

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------------------------------------------------------
    # Launcher
    # ---------------------------------------------------------

    def create_launcher(self):

        # Prevent duplicate launchers
        if self.launcher is not None:
            return

        self.launcher = PetalLauncher(
            self.root,
            self.open_app
        )

    # ---------------------------------------------------------
    # Open Petal
    # ---------------------------------------------------------

    def open_app(self):

        # Remove the launcher
        if self.launcher is not None:

            self.launcher.destroy()
            self.launcher = None

        # Show the actual Petal window
        self.root.deiconify()

        self.root.lift()

        self.root.focus_force()

        self.app_open = True

    # ---------------------------------------------------------
    # Minimize Petal
    # ---------------------------------------------------------

    def minimize_to_launcher(self):

        # Hide the main application window immediately
        self.root.withdraw()

        self.app_open = False

        # Create launcher again
        self.create_launcher()

    # ---------------------------------------------------------
    # Run
    # ---------------------------------------------------------

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    app = PetalApp()

    app.run()