import tkinter as tk

from .bubble import MessageBubble
from .image import ChatImage
from .reaction import ReactionPicker, ReactionDisplay

from database import (
    get_reactions,
    add_reaction
)

from config import (
    CHAT_BACKGROUND,
    TEXT,
    MUTED_TEXT,
    BUTTON
)


# =========================
# MESSAGE SETTINGS
# =========================

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

REACTION_BUTTON_FONT = (
    "Arial",
    11
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
        self.reaction_picker = None
        self.reaction_display = None

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
            fill="x"
        )

        self.message_line = tk.Frame(
            self.content_frame,
            bg=CHAT_BACKGROUND
        )

        self.message_line.pack(
            anchor=(
                "e"
                if self.is_me
                else "w"
            )
        )

        # -------------------------
        # MESSAGE CONTENT
        # -------------------------

        message_type = self.message.get(
            "message_type",
            "text"
        )

        if (
            message_type == "image"
            and self.message.get("image_url")
        ):

            self.content = ChatImage(
                self.message_line,
                image_url=self.message.get(
                    "image_url"
                ),
                on_enter=self._show_timestamp,
                on_leave=self._schedule_hide
            )

        else:

            self.content = MessageBubble(
                self.message_line,
                self.message.get(
                    "content",
                    ""
                ),
                self.is_me,
                on_enter=self._show_timestamp,
                on_leave=self._schedule_hide
            )

        self.content.pack(
            side="left"
        )

        # -------------------------
        # REACTION BUTTON
        # -------------------------

        self.reaction_button = tk.Button(
            self.message_line,
            text="♡",
            font=REACTION_BUTTON_FONT,
            bg=CHAT_BACKGROUND,
            fg=MUTED_TEXT,
            activebackground=CHAT_BACKGROUND,
            activeforeground=BUTTON,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self._toggle_reaction_picker
        )

        self.reaction_button.pack(
            side="left",
            padx=(
                5,
                0
            )
        )

        # -------------------------
        # TIMESTAMP
        # -------------------------

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

        # -------------------------
        # REACTIONS
        # -------------------------

        self._load_reactions()

    # =========================
    # REACTIONS
    # =========================

    def _load_reactions(self):

        message_id = self.message.get(
            "id"
        )

        if not message_id:

            return

        try:

            reactions = get_reactions(
                message_id
            )

            self._display_reactions(
                reactions
            )

        except Exception as error:

            print()
            print("REACTION LOAD ERROR:")
            print(error)
            print()

    def _display_reactions(
        self,
        reactions
    ):

        if self.reaction_display:

            self.reaction_display.destroy()

            self.reaction_display = None

        if not reactions:

            return

        self.reaction_display = ReactionDisplay(
            self.content_frame,
            reactions,
            self._reaction_clicked
        )

        self.reaction_display.pack(
            anchor=(
                "e"
                if self.is_me
                else "w"
            ),
            padx=4,
            pady=(2, 0)
        )

    def _toggle_reaction_picker(self):

        if self.reaction_picker:

            self.reaction_picker.destroy()

            self.reaction_picker = None

            return

        self.reaction_picker = ReactionPicker(
            self.content_frame,
            self._reaction_selected
        )

        self.reaction_picker.pack(
            anchor=(
                "e"
                if self.is_me
                else "w"
            ),
            padx=4,
            pady=(2, 0)
        )

    def _reaction_selected(
        self,
        reaction
    ):

        message_id = self.message.get(
            "id"
        )

        if not message_id:

            return

        try:

            add_reaction(
                message_id,
                self.username,
                reaction
            )

            if self.reaction_picker:

                self.reaction_picker.destroy()

                self.reaction_picker = None

            self._load_reactions()

        except Exception as error:

            print()
            print("REACTION ERROR:")
            print(error)
            print()

    def _reaction_clicked(
        self,
        reaction
    ):

        self._reaction_selected(
            reaction
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

            hour = int(parts[0])
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

        content_width = (
            self.content.winfo_reqwidth()
        )

        content_height = (
            self.content.winfo_reqheight()
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
            content_height // 2
        )

        if not self.is_me:

            self.timestamp.place(
                x=(
                    content_width
                    + TIMESTAMP_GAP
                ),
                y=center_y,
                anchor="w"
            )

        else:

            self.timestamp.place(
                x=(
                    row_width
                    - content_width
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

    def message_count(self):

        return len(
            self.messages
        )

    def last_message(self):

        if not self.messages:

            return None

        return self.messages[-1]