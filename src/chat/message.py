import tkinter as tk

from .bubble import MessageBubble

from config import (
    CHAT_BACKGROUND,
    TEXT,
    MUTED_TEXT
)


# =========================
# MESSAGE SETTINGS
# =========================

GROUP_SPACING = 14
MESSAGE_SPACING = 3

SENDER_FONT = (
    "Arial",
    9,
    "bold"
)

TIMESTAMP_FONT = (
    "Arial",
    8
)

TIMESTAMP_HIDE_DELAY = 120
TIMESTAMP_GAP = 8


# =========================
# MESSAGE ROW
# =========================

class MessageRow(tk.Frame):

    def __init__(
        self,
        parent,
        message,
        is_me,
        username
    ):

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND
        )

        self.message = message
        self.is_me = is_me
        self.username = username

        self.hide_job = None

        self.bubble = None
        self.timestamp = None

        self._create_row()

    # =========================
    # CREATE ROW
    # =========================

    def _create_row(self):

        self.content_frame = tk.Frame(
            self,
            bg=CHAT_BACKGROUND
        )

        self.content_frame.pack(
            fill="x"
        )

        self.bubble = MessageBubble(
            self.content_frame,
            self.message.get(
                "content",
                ""
            ),
            self.is_me,
            on_enter=self._show_timestamp,
            on_leave=self._schedule_hide
        )

        self.bubble.pack(
            side=(
                "right"
                if self.is_me
                else "left"
            )
        )

        self.timestamp = tk.Label(
            self,
            text=self._format_timestamp(),
            font=TIMESTAMP_FONT,
            bg=CHAT_BACKGROUND,
            fg=MUTED_TEXT
        )

        self.timestamp.place_forget()

        self.timestamp.bind(
            "<Enter>",
            self._timestamp_enter
        )

        self.timestamp.bind(
            "<Leave>",
            self._timestamp_leave
        )

    # =========================
    # TIMESTAMP
    # =========================

    def _format_timestamp(self):

        timestamp = self.message.get(
            "created_at",
            ""
        )

        if not timestamp:

            return ""

        try:

            time_part = timestamp.split(
                "T",
                1
            )[1]

            time_part = time_part.split(
                ".",
                1
            )[0]

            time_part = time_part.split(
                "+",
                1
            )[0]

            parts = time_part.split(":")

            hour = int(
                parts[0]
            )

            minute = parts[1]

            suffix = (
                "PM"
                if hour >= 12
                else "AM"
            )

            if hour > 12:

                hour -= 12

            if hour == 0:

                hour = 12

            return f"{hour}:{minute} {suffix}"

        except (
            ValueError,
            IndexError
        ):

            return ""

    # =========================
    # SHOW TIMESTAMP
    # =========================

    def _show_timestamp(self):

        self._cancel_hide()

        self.update_idletasks()

        timestamp_width = (
            self.timestamp.winfo_reqwidth()
        )

        bubble_width = (
            self.bubble.winfo_reqwidth()
        )

        bubble_height = (
            self.bubble.winfo_reqheight()
        )

        row_width = (
            self.winfo_width()
        )

        if row_width <= 1:

            self.after(
                1,
                self._show_timestamp
            )

            return

        center_y = (
            bubble_height // 2
        )

        if not self.is_me:

            self.timestamp.place(
                x=(
                    bubble_width
                    + TIMESTAMP_GAP
                ),
                y=center_y,
                anchor="w"
            )

        else:

            self.timestamp.place(
                x=(
                    row_width
                    - bubble_width
                    - TIMESTAMP_GAP
                    - timestamp_width
                ),
                y=center_y,
                anchor="w"
            )

        self.timestamp.lift()

    # =========================
    # HIDE TIMESTAMP
    # =========================

    def _schedule_hide(self):

        self._cancel_hide()

        self.hide_job = self.after(
            TIMESTAMP_HIDE_DELAY,
            self._hide_timestamp
        )

    def _hide_timestamp(self):

        self.timestamp.place_forget()

        self.hide_job = None

    # =========================
    # CANCEL HIDE
    # =========================

    def _cancel_hide(self):

        if self.hide_job is None:

            return

        try:

            self.after_cancel(
                self.hide_job
            )

        except tk.TclError:

            pass

        self.hide_job = None

    # =========================
    # TIMESTAMP HOVER
    # =========================

    def _timestamp_enter(
        self,
        event=None
    ):

        self._cancel_hide()

    def _timestamp_leave(
        self,
        event=None
    ):

        self._schedule_hide()


# =========================
# MESSAGE GROUP
# =========================

class MessageGroup(tk.Frame):

    def __init__(
        self,
        parent,
        sender,
        is_me,
        username
    ):

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND
        )

        self.sender = sender
        self.is_me = is_me
        self.username = username

        self.messages = []

        self._create_group()

    # =========================
    # GROUP HEADER
    # =========================

    def _create_group(self):

        self.sender_label = tk.Label(
            self,
            text=self.sender,
            font=SENDER_FONT,
            bg=CHAT_BACKGROUND,
            fg=TEXT
        )

        self.sender_label.pack(
            anchor=(
                "e"
                if self.is_me
                else "w"
            ),
            padx=8,
            pady=(
                0,
                2
            )
        )

    # =========================
    # ADD MESSAGE
    # =========================

    def add_message(
        self,
        message,
        username=None
    ):

        if username is None:

            username = self.username

        row = MessageRow(
            self,
            message,
            self.is_me,
            username
        )

        row.pack(
            fill="x",
            pady=(
                0,
                MESSAGE_SPACING
            )
        )

        self.messages.append(
            row
        )

        return row

    # =========================
    # MESSAGE COUNT
    # =========================

    def message_count(self):

        return len(
            self.messages
        )

    # =========================
    # LAST MESSAGE
    # =========================

    def last_message(self):

        if not self.messages:

            return None

        return self.messages[-1]