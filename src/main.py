import tkinter as tk


# -----------------------------
# Colors
# -----------------------------

BACKGROUND = "#FFF7FA"
HEADER = "#FFB6C9"
CHAT_BACKGROUND = "#FFFDFE"
INPUT_BACKGROUND = "#FFFFFF"
TEXT = "#3A3034"
MUTED_TEXT = "#8A7B80"
BUTTON = "#FF8FAB"
BUTTON_HOVER = "#FF7599"


# -----------------------------
# Functions
# -----------------------------

def send_message():
    message = message_entry.get().strip()

    if message:
        add_message("You", message)
        message_entry.delete(0, tk.END)


def add_message(sender, message):
    chat.config(state="normal")

    chat.insert(tk.END, f"{sender}\n", "sender")
    chat.insert(tk.END, f"{message}\n\n", "message")

    chat.config(state="disabled")
    chat.see(tk.END)


def on_enter(event):
    send_message()


def button_enter(event):
    send_button.config(bg=BUTTON_HOVER)


def button_leave(event):
    send_button.config(bg=BUTTON)


# -----------------------------
# Main Window
# -----------------------------

window = tk.Tk()

window.title("Elvis & Nysa")
window.geometry("500x650")
window.minsize(400, 500)
window.configure(bg=BACKGROUND)


# -----------------------------
# Header
# -----------------------------

header = tk.Frame(
    window,
    bg=HEADER,
    height=75
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


title = tk.Label(
    header,
    text="Elvis & Nysa",
    font=("Segoe UI", 20, "bold"),
    bg=HEADER,
    fg="white"
)

title.pack(
    pady=(12, 0)
)


status = tk.Label(
    header,
    text="♡ just for us",
    font=("Segoe UI", 10),
    bg=HEADER,
    fg="#FFF5F8"
)

status.pack()


# -----------------------------
# Chat Area
# -----------------------------

chat_frame = tk.Frame(
    window,
    bg=CHAT_BACKGROUND
)

chat_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=(15, 5)
)


chat = tk.Text(
    chat_frame,
    bg=CHAT_BACKGROUND,
    fg=TEXT,
    font=("Segoe UI", 11),
    wrap="word",
    bd=0,
    highlightthickness=0,
    state="disabled",
    padx=10,
    pady=10
)

chat.pack(
    fill="both",
    expand=True
)


# Text formatting

chat.tag_config(
    "sender",
    font=("Segoe UI", 9, "bold"),
    foreground=MUTED_TEXT
)

chat.tag_config(
    "message",
    font=("Segoe UI", 11),
    foreground=TEXT
)


# -----------------------------
# Message Input
# -----------------------------

input_frame = tk.Frame(
    window,
    bg=BACKGROUND
)

input_frame.pack(
    fill="x",
    padx=15,
    pady=(5, 15)
)


message_entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 11),
    bg=INPUT_BACKGROUND,
    fg=TEXT,
    bd=0,
    highlightthickness=1,
    highlightbackground="#E8DDE1",
    highlightcolor=BUTTON
)

message_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10,
    padx=(0, 10)
)


send_button = tk.Button(
    input_frame,
    text="Send",
    font=("Segoe UI", 10, "bold"),
    bg=BUTTON,
    fg="white",
    activebackground=BUTTON_HOVER,
    activeforeground="white",
    bd=0,
    padx=18,
    pady=9,
    cursor="hand2",
    command=send_message
)

send_button.pack(
    side="right"
)


# -----------------------------
# Events
# -----------------------------

message_entry.bind(
    "<Return>",
    on_enter
)

send_button.bind(
    "<Enter>",
    button_enter
)

send_button.bind(
    "<Leave>",
    button_leave
)


# -----------------------------
# Start
# -----------------------------

message_entry.focus()

window.mainloop()