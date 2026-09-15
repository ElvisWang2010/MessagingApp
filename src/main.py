import tkinter as tk

from config import (
    APP_TITLE,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MIN_WIDTH,
    MIN_HEIGHT
)

from login import create_login_screen


# =========================
# LOGIN SUCCESS
# =========================

def login_success(username):

    print()
    print("==============================")
    print("LOGIN SUCCESS")
    print("Username:", username)
    print("==============================")
    print()


# =========================
# WINDOW
# =========================

window = tk.Tk()

window.title(APP_TITLE)

window.geometry(
    f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
)

window.minsize(
    MIN_WIDTH,
    MIN_HEIGHT
)


# =========================
# LOGIN SCREEN
# =========================

login_frame = create_login_screen(
    window,
    login_success
)


# =========================
# START
# =========================

window.mainloop()