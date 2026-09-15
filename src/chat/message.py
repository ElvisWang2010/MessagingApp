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

TIMESTAMP_HIDE_DELAY = 100

TIMESTAMP_GAP = 6


# =========================
# MESSAGE ROW
# =========================

class MessageRow(tk.Frame):

    def __init__(
        self,
        parent,
        message,
        is_me
    ):

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND
        )

        self.message = message
        self.is_me = is_me

        self.hide_job = None

        self._create_row()

    # =========================
    # CREATE
    # =========================

    def _create_row(self):

        self.content_frame = tk.Frame(
            self,
            bg=CHAT_BACKGROUND
        )

        self.content_frame.pack(
            anchor="e" if self.is_me else "w"
        )

        self.timestamp = tk.Label(
            self.content_frame,
            text=self._format_timestamp(),
            font=TIMESTAMP_FONT,
            bg=CHAT_BACKGROUND,
            fg=MUTED_TEXT
        )

        self.timestamp.place_forget()

        self.bubble = MessageBubble(
            self.content_frame,
            self.message.get("content", ""),
            self.is_me,
            on_enter=self._show_timestamp,
            on_leave=self._schedule_hide
        )

        self.bubble.pack()

        self._bind_timestamp_hover()

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

            time_part = timestamp.split("T")[1]

            time_part = time_part.split(".")[0]

            hour = int(
                time_part.split(":")[0]
            )

            minute = time_part.split(":")[1]

            suffix = "AM"

            if hour >= 12:
                suffix = "PM"

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

    def _position_timestamp(self):

        self.timestamp.update_idletasks()

        timestamp_width = (
            self.timestamp.winfo_reqwidth()
        )

        bubble_width = (
            self.bubble.winfo_reqwidth()
        )

        if self.is_me:

            self.timestamp.place(
                relx=1,
                x=TIMESTAMP_GAP,
                y=self.bubble.winfo_reqheight() / 2,
                anchor="w"
            )

        else:

            self.timestamp.place(
                x=-timestamp_width - TIMESTAMP_GAP,
                y=self.bubble.winfo_reqheight() / 2,
                anchor="w"
            )

    # =========================
    # SHOW / HIDE
    # =========================

    def _show_timestamp(self):

        if self.hide_job is not None:

            self.after_cancel(
                self.hide_job
            )

            self.hide_job = None

        self._position_timestamp()

        self._bind_timestamp_hover()

    def _schedule_hide(self):

        if self.hide_job is not None:

            self.after_cancel(
                self.hide_job
            )

        self.hide_job = self.after(
            TIMESTAMP_HIDE_DELAY,
            self._hide_timestamp
        )

    def _hide_timestamp(self):

        self.timestamp.place_forget()

        self.hide_job = None

    # =========================
    # TIMESTAMP HOVER
    # =========================

    def _bind_timestamp_hover(self):

        self.timestamp.bind(
            "<Enter>",
            self._timestamp_enter
        )

        self.timestamp.bind(
            "<Leave>",
            self._timestamp_leave
        )

    def _timestamp_enter(self, event=None):

        if self.hide_job is not None:

            self.after_cancel(
                self.hide_job
            )

            self.hide_job = None

    def _timestamp_leave(self, event=None):

        self._schedule_hide()


# =========================
# MESSAGE GROUP
# =========================

class MessageGroup(tk.Frame):

    def __init__(
        self,
        parent,
        sender,
        is_me
    ):

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND
        )

        self.sender = sender
        self.is_me = is_me

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

        if self.is_me:

            self.sender_label.pack(
                anchor="e",
                padx=8,
                pady=(0, 2)
            )

        else:

            self.sender_label.pack(
                anchor="w",
                padx=8,
                pady=(0, 2)
            )

    # =========================
    # ADD MESSAGE
    # =========================

    def add_message(self, message):

        row = MessageRow(
            self,
            message,
            self.is_me
        )

        row.pack(
            fill="x",
            pady=(0, MESSAGE_SPACING)
        )

        self.messages.append(row)

        return row

    # =========================
    # GROUP SPACING
    # =========================

    def add_group_spacing(self):

        spacer = tk.Frame(
            self,
            height=GROUP_SPACING,
            bg=CHAT_BACKGROUND
        )

        spacer.pack(
            fill="x"
        )

        return spacer

    # =========================
    # MESSAGE COUNT
    # =========================

    def message_count(self):

        return len(self.messages)

    def last_message(self):

        if not self.messages:
            return None

        return self.messages[-1]