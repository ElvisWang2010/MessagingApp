import tkinter as tk
import ctypes
import os
import sys

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


def resource_path(relative_path):
    """
    Get the correct path to a bundled resource.

    Works both when running normally from the source code
    and when running the PyInstaller-built application.
    """

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                ".."
            )
        )

    return os.path.join(
        base_path,
        relative_path
    )


def sys_platform_is_windows():

    try:
        return ctypes.windll.kernel32.GetVersion() is not None
    except Exception:
        return False


class PetalApp:

    def __init__(self):

        # ---------------------------------------------------------
        # Windows taskbar identity
        # ---------------------------------------------------------

        if sys_platform_is_windows():
            try:
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                    "ElvisWang.Petal"
                )
            except Exception:
                pass

        # ---------------------------------------------------------
        # Create main application window
        # ---------------------------------------------------------

        self.root = tk.Tk()

        # ---------------------------------------------------------
        # Application icon
        # ---------------------------------------------------------

        try:
            icon_path = resource_path("petal.ico")

            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)

        except Exception:
            pass

        # ---------------------------------------------------------
        # Window settings
        # ---------------------------------------------------------

        self.root.title(APP_TITLE)

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.root.minsize(
            MIN_WIDTH,
            MIN_HEIGHT
        )

        # Keep track of launcher
        self.launcher = None

        # Keep track of whether app is currently open
        self.app_open = False

        # ---------------------------------------------------------
        # Window events
        # ---------------------------------------------------------

        # When user presses X on the main window,
        # minimize Petal back to the launcher.
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.minimize_to_launcher
        )

        # Detect when Petal is restored from the Windows taskbar.
        self.root.bind(
            "<Map>",
            self.on_window_restored
        )

        # Detect a new incoming message.
        self.root.bind(
            "<<PetalNewMessage>>",
            self.on_new_message
        )

        # ---------------------------------------------------------
        # Hide main window BEFORE creating UI
        # ---------------------------------------------------------

        # This prevents the login/chat window from flashing
        # on screen during startup.
        self.root.withdraw()

        # ---------------------------------------------------------
        # Create login screen while hidden
        # ---------------------------------------------------------

        self.show_login()

        # Make sure Tk finishes creating the UI while
        # the window is still hidden.
        self.root.update_idletasks()

        # ---------------------------------------------------------
        # Put Petal into the Windows taskbar
        # ---------------------------------------------------------

        self.root.iconify()

        # ---------------------------------------------------------
        # Create launcher
        # ---------------------------------------------------------

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
    # Destroy launcher
    # ---------------------------------------------------------

    def destroy_launcher(self):

        if self.launcher is not None:

            self.launcher.destroy()

            self.launcher = None

    # ---------------------------------------------------------
    # New message notification
    # ---------------------------------------------------------

    def on_new_message(self, event=None):

        # Only show the notification when Petal is minimized.
        if self.root.state() != "normal":

            if self.launcher is not None:
                self.launcher.show_notification()

    # ---------------------------------------------------------
    # Window restored from taskbar
    # ---------------------------------------------------------

    def on_window_restored(self, event=None):

        # Ignore events that occur while Petal is still minimized.
        if self.root.state() != "normal":
            return

        # If the user clicked the Petal taskbar icon,
        # remove the floating launcher.
        self.destroy_launcher()

        self.app_open = True

    # ---------------------------------------------------------
    # Open Petal from launcher
    # ---------------------------------------------------------

    def open_app(self):

        # Remove launcher
        self.destroy_launcher()

        # Restore the main application window
        self.root.deiconify()

        self.root.state("normal")

        self.root.lift()

        self.root.focus_force()

        self.app_open = True

    # ---------------------------------------------------------
    # Minimize Petal
    # ---------------------------------------------------------

    def minimize_to_launcher(self):

        # Keep Petal represented in the Windows taskbar.
        self.root.iconify()

        self.app_open = False

        # Show launcher again
        self.create_launcher()

    # ---------------------------------------------------------
    # Run
    # ---------------------------------------------------------

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    app = PetalApp()

    app.run()