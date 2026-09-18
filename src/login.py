import tkinter as tk

from auth import authenticate

from config import (
    BACKGROUND,
    TEXT,
    MUTED_TEXT,
    INPUT_BACKGROUND,
    BUTTON,
    BUTTON_HOVER,
    ERROR
)


def create_login_screen(window, on_login):

    frame = tk.Frame(
        window,
        bg=BACKGROUND
    )

    frame.pack(
        fill="both",
        expand=True
    )


    # =========================
    # TITLE
    # =========================

    title = tk.Label(
        frame,
        text="Petal",
        font=("Arial", 28, "bold"),
        bg=BACKGROUND,
        fg=TEXT
    )

    title.pack(
        pady=(130, 10)
    )


    subtitle = tk.Label(
        frame,
        text="♡ just for us",
        font=("Arial", 12),
        bg=BACKGROUND,
        fg=MUTED_TEXT
    )

    subtitle.pack(
        pady=(0, 50)
    )


    # =========================
    # USERNAME
    # =========================

    username_label = tk.Label(
        frame,
        text="Username",
        font=("Arial", 11, "bold"),
        bg=BACKGROUND,
        fg=TEXT
    )

    username_label.pack(
        anchor="w",
        padx=80
    )


    username_entry = tk.Entry(
        frame,
        font=("Arial", 13),
        bg=INPUT_BACKGROUND,
        fg=TEXT,
        relief="flat"
    )

    username_entry.pack(
        fill="x",
        padx=80,
        ipady=10,
        pady=(5, 20)
    )


    # =========================
    # PASSWORD
    # =========================

    password_label = tk.Label(
        frame,
        text="Password",
        font=("Arial", 11, "bold"),
        bg=BACKGROUND,
        fg=TEXT
    )

    password_label.pack(
        anchor="w",
        padx=80
    )


    password_entry = tk.Entry(
        frame,
        font=("Arial", 13),
        bg=INPUT_BACKGROUND,
        fg=TEXT,
        relief="flat",
        show="•"
    )

    password_entry.pack(
        fill="x",
        padx=80,
        ipady=10,
        pady=(5, 25)
    )


    # =========================
    # STATUS
    # =========================

    status = tk.Label(
        frame,
        text="",
        font=("Arial", 10),
        bg=BACKGROUND,
        fg=ERROR
    )

    status.pack(
        pady=10
    )


    # =========================
    # LOGIN FUNCTION
    # =========================

    def attempt_login():

        username = username_entry.get()
        password = password_entry.get()

        try:

            success = authenticate(
                username,
                password
            )

            if success:

                on_login(
                    username.strip()
                )

            else:

                status.config(
                    text="Incorrect username or password."
                )

        except Exception as error:

            print()
            print("LOGIN ERROR:")
            print(error)
            print()

            status.config(
                text="Could not connect to the server."
            )


    # =========================
    # LOGIN BUTTON
    # =========================

    login_button = tk.Button(
        frame,
        text="Login ♡",
        font=("Arial", 12, "bold"),
        bg=BUTTON,
        fg="white",
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=attempt_login
    )

    login_button.pack(
        fill="x",
        padx=80,
        ipady=8
    )


    # =========================
    # ENTER KEY
    # =========================

    password_entry.bind(
        "<Return>",
        lambda event: attempt_login()
    )


    username_entry.focus()

    return frame