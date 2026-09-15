import tkinter as tk
from tkinter import messagebox
import os
import asyncio
import threading

from dotenv import load_dotenv
from supabase import create_client, acreate_client


# =========================
# SUPABASE SETUP
# =========================

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY is missing from .env")

supabase = create_client(url, key)


# =========================
# COLORS
# =========================

BACKGROUND = "#FFF7FA"
HEADER = "#FFB6C9"
CHAT_BACKGROUND = "#FFFDFE"
INPUT_BACKGROUND = "#FFFFFF"

TEXT = "#3A3034"
MUTED_TEXT = "#8A7B80"

BUTTON = "#FF8FAB"
BUTTON_HOVER = "#FF7599"


# =========================
# GLOBAL VARIABLES
# =========================

window = tk.Tk()

current_user = None


# =========================
# LOGIN
# =========================

def login():
    global current_user

    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        login_status.config(
            text="Please enter your username and password."
        )
        return

    try:
        response = (
            supabase
            .table("users")
            .select("username, password")
            .eq("username", username)
            .execute()
        )

        if not response.data:
            login_status.config(
                text="Incorrect username or password."
            )
            return

        user = response.data[0]

        if user["password"] != password:
            login_status.config(
                text="Incorrect username or password."
            )
            return

        current_user = user["username"]

        show_chat()

    except Exception as error:
        print("Login error:", error)

        login_status.config(
            text="Could not connect to the server."
        )


# =========================
# CHAT FUNCTIONS
# =========================

def add_message(sender, content):
    chat.config(state="normal")

    chat.insert("end", f"{sender}: {content}\n\n")

    chat.see("end")
    chat.config(state="disabled")


def load_messages():
    try:
        response = (
            supabase
            .table("messages")
            .select("*")
            .order("created_at")
            .execute()
        )

        for message in response.data:
            add_message(
                message["sender"],
                message["content"]
            )

    except Exception as error:
        print("Error loading messages:", error)


def send_message(event=None):
    message = message_entry.get().strip()

    if not message:
        return

    if current_user is None:
        return

    try:
        supabase.table("messages").insert({
            "sender": current_user,
            "content": message
        }).execute()

        message_entry.delete(0, "end")

    except Exception as error:
        print("Error sending message:", error)

        messagebox.showerror(
            "Error",
            "Could not send message."
        )


# =========================
# REALTIME
# =========================

async def realtime_listener():

    realtime_supabase = await acreate_client(
        url,
        key
    )

    def handle_message(payload):

        print("\nREALTIME EVENT RECEIVED")
        print(payload)
        print("=================================")

        try:
            message = payload["data"]["record"]

            sender = message["sender"]
            content = message["content"]

            window.after(
                0,
                add_message,
                sender,
                content
            )

        except Exception as error:
            print(
                "Error processing Realtime message:",
                error
            )

    channel = (
        realtime_supabase
        .channel("messages-channel")
        .on_postgres_changes(
            "INSERT",
            schema="public",
            table="messages",
            callback=handle_message
        )
    )

    await channel.subscribe(
        lambda status, error=None:
        print("REALTIME STATUS:", status)
    )

    print("Realtime subscription started.")

    await asyncio.Event().wait()


def start_realtime():

    asyncio.run(
        realtime_listener()
    )


# =========================
# LOGIN SCREEN
# =========================

def show_login():

    global username_entry
    global password_entry
    global login_status

    window.title("Elvis & Nysa")

    window.geometry("500x650")
    window.minsize(400, 500)

    login_frame = tk.Frame(
        window,
        bg=BACKGROUND
    )

    login_frame.pack(
        fill="both",
        expand=True
    )

    # Title

    title = tk.Label(
        login_frame,
        text="Elvis & Nysa",
        font=("Arial", 28, "bold"),
        bg=BACKGROUND,
        fg=TEXT
    )

    title.pack(
        pady=(130, 10)
    )

    subtitle = tk.Label(
        login_frame,
        text="♡ just for us",
        font=("Arial", 12),
        bg=BACKGROUND,
        fg=MUTED_TEXT
    )

    subtitle.pack(
        pady=(0, 50)
    )

    # Username

    username_label = tk.Label(
        login_frame,
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
        login_frame,
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

    # Password

    password_label = tk.Label(
        login_frame,
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
        login_frame,
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

    # Login button

    login_button = tk.Button(
        login_frame,
        text="Login ♡",
        font=("Arial", 12, "bold"),
        bg=BUTTON,
        fg="white",
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=login
    )

    login_button.pack(
        fill="x",
        padx=80,
        ipady=8
    )

    # Status

    login_status = tk.Label(
        login_frame,
        text="",
        font=("Arial", 10),
        bg=BACKGROUND,
        fg="#D65A70"
    )

    login_status.pack(
        pady=15
    )

    password_entry.bind(
        "<Return>",
        lambda event: login()
    )


# =========================
# CHAT SCREEN
# =========================

def show_chat():

    # Remove login screen

    for widget in window.winfo_children():
        widget.destroy()

    window.title("Elvis & Nysa")

    window.geometry("500x650")
    window.minsize(400, 500)

    # =========================
    # HEADER
    # =========================

    header = tk.Frame(
        window,
        bg=HEADER,
        height=70
    )

    header.pack(
        fill="x"
    )

    header.pack_propagate(False)

    title = tk.Label(
        header,
        text="Elvis & Nysa ♡",
        font=("Arial", 18, "bold"),
        bg=HEADER,
        fg=TEXT
    )

    title.pack(
        pady=(12, 0)
    )

    status = tk.Label(
        header,
        text=f"Logged in as {current_user}",
        font=("Arial", 9),
        bg=HEADER,
        fg=MUTED_TEXT
    )

    status.pack()

    # =========================
    # CHAT
    # =========================

    global chat

    chat = tk.Text(
        window,
        bg=CHAT_BACKGROUND,
        fg=TEXT,
        font=("Arial", 11),
        relief="flat",
        wrap="word",
        state="disabled"
    )

    chat.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # =========================
    # INPUT AREA
    # =========================

    input_frame = tk.Frame(
        window,
        bg=BACKGROUND
    )

    input_frame.pack(
        fill="x",
        padx=10,
        pady=(0, 10)
    )

    global message_entry

    message_entry = tk.Entry(
        input_frame,
        bg=INPUT_BACKGROUND,
        fg=TEXT,
        font=("Arial", 11),
        relief="flat"
    )

    message_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=8
    )

    send_button = tk.Button(
        input_frame,
        text="Send",
        bg=BUTTON,
        fg="white",
        activebackground=BUTTON_HOVER,
        activeforeground="white",
        relief="flat",
        font=("Arial", 10, "bold"),
        cursor="hand2",
        command=send_message
    )

    send_button.pack(
        side="right",
        padx=(8, 0),
        ipadx=10,
        ipady=6
    )

    message_entry.bind(
        "<Return>",
        send_message
    )

    # =========================
    # LOAD OLD MESSAGES
    # =========================

    load_messages()

    # =========================
    # START REALTIME
    # =========================

    realtime_thread = threading.Thread(
        target=start_realtime,
        daemon=True
    )

    realtime_thread.start()

    message_entry.focus()


# =========================
# START APP
# =========================

show_login()

window.mainloop()