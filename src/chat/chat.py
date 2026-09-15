import tkinter as tk

from database import (
    get_messages,
    send_message,
    send_image_message
)

from realtime_listener import (
    start_realtime_listener
)

from .message import MessageGroup

from .image import (
    upload_selected_image
)

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


# =========================
# SETTINGS
# =========================

HEADER_HEIGHT = 60
INPUT_HEIGHT = 55

MESSAGE_PADDING_X = 12

SCROLL_SPEED = 3


# =========================
# CHAT VIEW
# =========================

class ChatView(tk.Frame):

    def __init__(
        self,
        parent,
        username
    ):

        super().__init__(
            parent,
            bg=BACKGROUND
        )

        self.username = username

        self.current_group = None
        self.last_sender = None

        self._create_header()
        self._create_chat_area()
        self._create_input_area()

        self._load_existing_messages()

        start_realtime_listener(
            self._receive_realtime_message
        )

    # =========================
    # HEADER
    # =========================

    def _create_header(self):

        self.header = tk.Frame(
            self,
            bg=HEADER,
            height=HEADER_HEIGHT
        )

        self.header.pack(
            fill="x"
        )

        self.header.pack_propagate(
            False
        )

        self.title_label = tk.Label(
            self.header,
            text="Elvis & Nysa",
            font=(
                "Arial",
                17,
                "bold"
            ),
            bg=HEADER,
            fg=TEXT
        )

        self.title_label.pack(
            side="left",
            padx=18
        )

        self.status_label = tk.Label(
            self.header,
            text="♡ connected",
            font=(
                "Arial",
                9
            ),
            bg=HEADER,
            fg=MUTED_TEXT
        )

        self.status_label.pack(
            side="right",
            padx=18
        )

    # =========================
    # CHAT AREA
    # =========================

    def _create_chat_area(self):

        self.chat_container = tk.Frame(
            self,
            bg=CHAT_BACKGROUND
        )

        self.chat_container.pack(
            fill="both",
            expand=True
        )

        self.chat_canvas = tk.Canvas(
            self.chat_container,
            bg=CHAT_BACKGROUND,
            highlightthickness=0,
            bd=0
        )

        self.chat_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar = tk.Scrollbar(
            self.chat_container,
            orient="vertical",
            command=self.chat_canvas.yview
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.chat_canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.messages_frame = tk.Frame(
            self.chat_canvas,
            bg=CHAT_BACKGROUND
        )

        self.canvas_window = (
            self.chat_canvas.create_window(
                0,
                0,
                window=self.messages_frame,
                anchor="nw"
            )
        )

        self.messages_frame.bind(
            "<Configure>",
            self._update_scroll_region
        )

        self.chat_canvas.bind(
            "<Configure>",
            self._resize_messages_frame
        )

        self._setup_scrolling()

    # =========================
    # SCROLLING
    # =========================

    def _setup_scrolling(self):

        self.chat_container.bind(
            "<Enter>",
            self._enter_chat_area,
            add="+"
        )

        self.chat_container.bind(
            "<Leave>",
            self._leave_chat_area,
            add="+"
        )

    def _enter_chat_area(
        self,
        event=None
    ):

        self.chat_container.bind_all(
            "<MouseWheel>",
            self._mouse_wheel,
            add="+"
        )

        self.chat_container.bind_all(
            "<Button-4>",
            self._scroll_up,
            add="+"
        )

        self.chat_container.bind_all(
            "<Button-5>",
            self._scroll_down,
            add="+"
        )

    def _leave_chat_area(
        self,
        event=None
    ):

        self.chat_container.unbind_all(
            "<MouseWheel>"
        )

        self.chat_container.unbind_all(
            "<Button-4>"
        )

        self.chat_container.unbind_all(
            "<Button-5>"
        )

    def _mouse_wheel(
        self,
        event
    ):

        if event.delta > 0:

            self.chat_canvas.yview_scroll(
                -SCROLL_SPEED,
                "units"
            )

        elif event.delta < 0:

            self.chat_canvas.yview_scroll(
                SCROLL_SPEED,
                "units"
            )

    def _scroll_up(
        self,
        event=None
    ):

        self.chat_canvas.yview_scroll(
            -SCROLL_SPEED,
            "units"
        )

    def _scroll_down(
        self,
        event=None
    ):

        self.chat_canvas.yview_scroll(
            SCROLL_SPEED,
            "units"
        )

    def _update_scroll_region(
        self,
        event=None
    ):

        self.chat_canvas.configure(
            scrollregion=self.chat_canvas.bbox(
                "all"
            )
        )

    def _resize_messages_frame(
        self,
        event
    ):

        self.chat_canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )

    # =========================
    # INPUT AREA
    # =========================

    def _create_input_area(self):

        self.input_container = tk.Frame(
            self,
            bg=BACKGROUND,
            height=INPUT_HEIGHT
        )

        self.input_container.pack(
            fill="x"
        )

        self.input_container.pack_propagate(
            False
        )

        # -------------------------
        # IMAGE BUTTON
        # -------------------------

        self.image_button = tk.Button(
            self.input_container,
            text="＋",
            font=(
                "Arial",
                18,
                "bold"
            ),
            bg=BACKGROUND,
            fg=BUTTON,
            activebackground=BACKGROUND,
            activeforeground=BUTTON_HOVER,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self._send_image
        )

        self.image_button.pack(
            side="left",
            padx=(10, 2),
            pady=8
        )

        # -------------------------
        # MESSAGE ENTRY
        # -------------------------

        self.message_entry = tk.Entry(
            self.input_container,
            font=(
                "Arial",
                11
            ),
            bg=INPUT_BACKGROUND,
            fg=TEXT,
            relief="flat",
            bd=0
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(4, 6),
            pady=10,
            ipady=8
        )

        # -------------------------
        # SEND BUTTON
        # -------------------------

        self.send_button = tk.Button(
            self.input_container,
            text="Send ♡",
            font=(
                "Arial",
                10,
                "bold"
            ),
            bg=BUTTON,
            fg="white",
            activebackground=BUTTON_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self._send_current_message
        )

        self.send_button.pack(
            side="right",
            padx=(4, 12),
            pady=10,
            ipadx=8
        )

        self.message_entry.bind(
            "<Return>",
            self._enter_pressed
        )

        self.message_entry.focus()

    # =========================
    # LOAD MESSAGES
    # =========================

    def _load_existing_messages(self):

        try:

            messages = get_messages()

            for message in messages:

                self._add_message(
                    message,
                    scroll=False
                )

            self.update_idletasks()

            self._move_to_bottom()

        except Exception as error:

            print()
            print("MESSAGE LOAD ERROR:")
            print(error)
            print()

    # =========================
    # ADD MESSAGE
    # =========================

    def _add_message(
        self,
        message,
        scroll=True
    ):

        sender = message.get(
            "sender",
            ""
        )

        is_me = (
            sender == self.username
        )

        if sender != self.last_sender:

            self.current_group = MessageGroup(
                self.messages_frame,
                sender,
                is_me,
                self.username
            )

            self.current_group.pack(
                fill="x",
                padx=MESSAGE_PADDING_X,
                pady=(8, 0)
            )

            self.last_sender = sender

        self.current_group.add_message(
            message
        )

        if scroll:

            self._scroll_to_bottom()

    # =========================
    # SEND TEXT
    # =========================

    def _send_current_message(self):

        content = (
            self.message_entry
            .get()
            .strip()
        )

        if not content:
            return

        self.send_button.config(
            state="disabled"
        )

        try:

            send_message(
                self.username,
                content
            )

            self.message_entry.delete(
                0,
                tk.END
            )

        except Exception as error:

            print()
            print("==============================")
            print("MESSAGE SEND ERROR")
            print("==============================")
            print(error)
            print("==============================")
            print()

        finally:

            self.send_button.config(
                state="normal"
            )

            self.message_entry.focus()

    # =========================
    # SEND IMAGE
    # =========================

    def _send_image(self):

        self.image_button.config(
            state="disabled"
        )

        try:

            image_url = (
                upload_selected_image()
            )

            if not image_url:

                return

            print(
                "Image uploaded successfully."
            )

            send_image_message(
                self.username,
                image_url
            )

            print(
                "Image message sent."
            )

        except Exception as error:

            print()
            print("==============================")
            print("IMAGE MESSAGE ERROR")
            print("==============================")
            print(error)
            print("==============================")
            print()

        finally:

            self.image_button.config(
                state="normal"
            )

            self.message_entry.focus()

    # =========================
    # ENTER
    # =========================

    def _enter_pressed(
        self,
        event
    ):

        self._send_current_message()

        return "break"

    # =========================
    # REALTIME
    # =========================

    def _receive_realtime_message(
        self,
        message
    ):

        self.after(
            0,
            lambda: self._add_realtime_message(
                message
            )
        )

    def _add_realtime_message(
        self,
        message
    ):

        self._add_message(
            message,
            scroll=True
        )

    # =========================
    # SCROLL BOTTOM
    # =========================

    def _scroll_to_bottom(self):

        self.after(
            30,
            self._move_to_bottom
        )

    def _move_to_bottom(self):

        self.update_idletasks()

        self.chat_canvas.configure(
            scrollregion=self.chat_canvas.bbox(
                "all"
            )
        )

        self.chat_canvas.yview_moveto(
            1.0
        )


# =========================
# CREATE SCREEN
# =========================

def create_chat_screen(
    window,
    username
):

    chat_view = ChatView(
        window,
        username
    )

    chat_view.pack(
        fill="both",
        expand=True
    )

    return chat_view