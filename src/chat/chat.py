import tkinter as tk
from tkinter import messagebox

from config import (
    BACKGROUND,
    HEADER,
    CHAT_BACKGROUND,
    INPUT_BACKGROUND,
    TEXT,
    MUTED_TEXT,
    BUTTON,
    BUTTON_HOVER
)

from database import send_message, send_image_message

from .message import MessageRow
from image import upload_selected_image

from realtime_listener import start_realtime_listener


def create_chat_screen(window, username):

    # ==========================================================
    # MAIN FRAME
    # ==========================================================

    frame = tk.Frame(
        window,
        bg=BACKGROUND
    )

    frame.pack(
        fill="both",
        expand=True
    )

    # ==========================================================
    # HEADER
    # ==========================================================

    header = tk.Frame(
        frame,
        bg=HEADER,
        height=70
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(False)

    title = tk.Label(
        header,
        text="Elvis & Nysa",
        font=("Arial", 18, "bold"),
        bg=HEADER,
        fg=TEXT
    )

    title.pack(
        pady=(12, 0)
    )

    subtitle = tk.Label(
        header,
        text=f"Logged in as {username}",
        font=("Arial", 9),
        bg=HEADER,
        fg=MUTED_TEXT
    )

    subtitle.pack()

    # ==========================================================
    # CHAT AREA
    # ==========================================================

    chat_area = tk.Frame(
        frame,
        bg=CHAT_BACKGROUND
    )

    chat_area.pack(
        fill="both",
        expand=True
    )

    # ----------------------------------------------------------
    # CANVAS
    # ----------------------------------------------------------

    canvas = tk.Canvas(
        chat_area,
        bg=CHAT_BACKGROUND,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        chat_area,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ----------------------------------------------------------
    # MESSAGE CONTAINER
    # ----------------------------------------------------------

    messages_frame = tk.Frame(
        canvas,
        bg=CHAT_BACKGROUND
    )

    canvas_window = canvas.create_window(
        (0, 0),
        window=messages_frame,
        anchor="nw"
    )

    def update_scroll_region(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    messages_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    def resize_messages(event):

        canvas.itemconfigure(
            canvas_window,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        resize_messages
    )

    # ==========================================================
    # MOUSE WHEEL
    # ==========================================================

    def mouse_enter(event):

        canvas.bind_all(
            "<MouseWheel>",
            mouse_wheel
        )

    def mouse_leave(event):

        canvas.unbind_all(
            "<MouseWheel>"
        )

    def mouse_wheel(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    chat_area.bind(
        "<Enter>",
        mouse_enter
    )

    chat_area.bind(
        "<Leave>",
        mouse_leave
    )

    canvas.bind(
        "<Enter>",
        mouse_enter
    )

    canvas.bind(
        "<Leave>",
        mouse_leave
    )

    messages_frame.bind(
        "<Enter>",
        mouse_enter
    )

    messages_frame.bind(
        "<Leave>",
        mouse_leave
    )

    # ==========================================================
    # ADD MESSAGE TO UI
    # ==========================================================

    def add_message(message):

        row = MessageRow(
            messages_frame,
            message,
            username
        )

        row.pack(
            fill="x",
            padx=10,
            pady=5
        )

        window.update_idletasks()

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

        canvas.yview_moveto(1.0)

    # ==========================================================
    # LOAD EXISTING MESSAGES
    # ==========================================================

    try:

        from database import load_messages

        existing_messages = load_messages()

        for message in existing_messages:

            add_message(
                message
            )

    except Exception as error:

        print()
        print("==============================")
        print("MESSAGE LOAD ERROR")
        print("==============================")
        print(error)
        print()

    # ==========================================================
    # REALTIME
    # ==========================================================

    def realtime_message(message):

        def add_on_ui():

            add_message(
                message
            )

        window.after(
            0,
            add_on_ui
        )

    start_realtime_listener(
        realtime_message
    )

    # ==========================================================
    # INPUT AREA
    # ==========================================================

    input_area = tk.Frame(
        frame,
        bg=BACKGROUND
    )

    input_area.pack(
        fill="x",
        padx=10,
        pady=10
    )

    # ==========================================================
    # INPUT CONTAINER
    # ==========================================================

    input_container = tk.Frame(
        input_area,
        bg=INPUT_BACKGROUND,
        highlightthickness=1,
        highlightbackground="#E8DDE1"
    )

    input_container.pack(
        fill="x"
    )

    # ==========================================================
    # IMAGE BUTTON
    # ==========================================================

    def choose_image():

        try:

            result = upload_selected_image()

            if not result:
                return

            image_url = result["url"]

            message = send_image_message(
                username,
                image_url
            )

            if message:

                add_message(
                    message
                )

        except Exception as error:

            print()
            print("==============================")
            print("IMAGE SEND ERROR")
            print("==============================")
            print(error)
            print()

            messagebox.showerror(
                "Image Upload Error",
                f"Could not upload image.\n\n{error}"
            )

    image_button = tk.Button(
        input_container,
        text="+",
        font=("Arial", 20, "bold"),
        bg=INPUT_BACKGROUND,
        fg=BUTTON,
        activebackground=INPUT_BACKGROUND,
        activeforeground=BUTTON_HOVER,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=choose_image
    )

    image_button.pack(
        side="left",
        padx=(8, 2),
        pady=5
    )

    # ==========================================================
    # TEXT INPUT
    # ==========================================================

    message_entry = tk.Entry(
        input_container,
        font=("Arial", 12),
        bg=INPUT_BACKGROUND,
        fg=TEXT,
        relief="flat",
        bd=0
    )

    message_entry.pack(
        side="left",
        fill="x",
        expand=True,
        padx=5,
        pady=10
    )

    # ==========================================================
    # SEND BUTTON
    # ==========================================================

    def send_current_message():

        content = message_entry.get().strip()

        if not content:
            return

        try:

            message = send_message(
                username,
                content
            )

            if message:

                add_message(
                    message
                )

                message_entry.delete(
                    0,
                    "end"
                )

        except Exception as error:

            print()
            print("==============================")
            print("MESSAGE SEND ERROR")
            print("==============================")
            print(error)
            print()

            messagebox.showerror(
                "Message Error",
                f"Could not send message.\n\n{error}"
            )

    send_button = tk.Button(
        input_container,
        text="♡",
        font=("Arial", 15, "bold"),
        bg=INPUT_BACKGROUND,
        fg=BUTTON,
        activebackground=INPUT_BACKGROUND,
        activeforeground=BUTTON_HOVER,
        relief="flat",
        bd=0,
        cursor="hand2",
        command=send_current_message
    )

    send_button.pack(
        side="right",
        padx=(2, 8),
        pady=5
    )

    # ==========================================================
    # ENTER TO SEND
    # ==========================================================

    message_entry.bind(
        "<Return>",
        lambda event: send_current_message()
    )

    message_entry.focus()

    return frame