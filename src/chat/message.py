import tkinter as tk

from .bubble import MessageBubble

from .reaction import (
    ReactionPicker,
    ReactionDisplay,
    ReactionButton
)

from .image import ChatImage

from database import (
    get_reactions,
    add_reaction
)

from config import (
    CHAT_BACKGROUND,
    TEXT,
    MUTED_TEXT
)


# =========================
# SETTINGS
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
        self.image = None
        self.timestamp = None

        self.reaction_button = None
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

        message_type = self.message.get(
            "message_type",
            "text"
        )

        # -------------------------
        # IMAGE
        # -------------------------

        if (
            message_type == "image"
            and self.message.get(
                "image_url"
            )
        ):

            self.image = ChatImage(
                self.content_frame,
                image_url=self.message.get(
                    "image_url"
                ),
                on_enter=self._show_controls,
                on_leave=self._schedule_hide
            )

            self.image.pack(
                side=(
                    "right"
                    if self.is_me
                    else "left"
                )
            )

        # -------------------------
        # TEXT
        # -------------------------

        else:

            self.bubble = MessageBubble(
                self.content_frame,
                self.message.get(
                    "content",
                    ""
                ),
                self.is_me,
                on_enter=self._show_controls,
                on_leave=self._schedule_hide
            )

            self.bubble.pack(
                side=(
                    "right"
                    if self.is_me
                    else "left"
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
            self._cancel_hide
        )

        self.timestamp.bind(
            "<Leave>",
            lambda event:
                self._schedule_hide()
        )

        # -------------------------
        # REACTION BUTTON
        # -------------------------

        self.reaction_button = (
            ReactionButton(
                self,
                self._show_reaction_picker
            )
        )

        self.reaction_button.place_forget()

        self.reaction_button.bind(
            "<Enter>",
            self._cancel_hide
        )

        self.reaction_button.bind(
            "<Leave>",
            lambda event:
                self._schedule_hide()
        )

        # -------------------------
        # EXISTING REACTIONS
        # -------------------------

        self._load_reactions()

    # =========================
    # MESSAGE DIMENSIONS
    # =========================

    def _message_dimensions(self):

        if self.bubble:

            return (
                self.bubble.winfo_reqwidth(),
                self.bubble.winfo_reqheight()
            )

        if self.image:

            return (
                self.image.winfo_reqwidth(),
                self.image.winfo_reqheight()
            )

        return 0, 0

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

            return (
                f"{hour}:{minute} {suffix}"
            )

        except (
            ValueError,
            IndexError
        ):

            return ""

    def _show_timestamp(self):

        self._cancel_hide()

        self.update_idletasks()

        message_width, message_height = (
            self._message_dimensions()
        )

        timestamp_width = (
            self.timestamp.winfo_reqwidth()
        )

        row_width = self.winfo_width()

        if row_width <= 1:

            self.after(
                1,
                self._show_timestamp
            )

            return

        center_y = (
            message_height // 2
        )

        if not self.is_me:

            self.timestamp.place(
                x=(
                    message_width
                    + TIMESTAMP_GAP
                ),
                y=center_y,
                anchor="w"
            )

        else:

            self.timestamp.place(
                x=(
                    row_width
                    - message_width
                    - TIMESTAMP_GAP
                    - timestamp_width
                ),
                y=center_y,
                anchor="w"
            )

        self.timestamp.lift()

    # =========================
    # SHOW CONTROLS
    # =========================

    def _show_controls(self):

        self._cancel_hide()

        self._show_timestamp()

        self.update_idletasks()

        message_width, message_height = (
            self._message_dimensions()
        )

        row_width = self.winfo_width()

        if row_width <= 1:

            self.after(
                1,
                self._show_controls
            )

            return

        button_width = (
            self.reaction_button.winfo_reqwidth()
        )

        # Put the reaction button ABOVE
        # the message instead of beside it.
        y = -(
            self.reaction_button.winfo_reqheight()
            + 2
        )

        if self.is_me:

            x = (
                row_width
                - message_width
            )

        else:

            x = 0

        self.reaction_button.place(
            x=x,
            y=y,
            anchor="sw"
        )

        self.reaction_button.lift()

    # =========================
    # HIDE
    # =========================

    def _schedule_hide(self):

        self._cancel_hide()

        self.hide_job = self.after(
            TIMESTAMP_HIDE_DELAY,
            self._hide_controls
        )

    def _hide_controls(self):

        self.timestamp.place_forget()

        self.reaction_button.place_forget()

        if self.reaction_picker:

            self.reaction_picker.place_forget()

        self.hide_job = None

    def _cancel_hide(
        self,
        event=None
    ):

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
    # REACTION PICKER
    # =========================

    def _show_reaction_picker(self):

        self._cancel_hide()

        if self.reaction_picker:

            self.reaction_picker.destroy()

        self.reaction_picker = ReactionPicker(
            self,
            self._reaction_selected
        )

        self.update_idletasks()

        picker_width = (
            self.reaction_picker.winfo_reqwidth()
        )

        message_width, message_height = (
            self._message_dimensions()
        )

        row_width = self.winfo_width()

        picker_height = (
            self.reaction_picker.winfo_reqheight()
        )

        if self.is_me:

            x = max(
                0,
                row_width
                - message_width
                - picker_width
            )

        else:

            x = 0

        y = (
            -picker_height
            - self.reaction_button.winfo_reqheight()
            - 5
        )

        self.reaction_picker.place(
            x=x,
            y=y,
            anchor="sw"
        )

        self.reaction_picker.lift()

        self.reaction_picker.bind(
            "<Enter>",
            self._cancel_hide
        )

        self.reaction_picker.bind(
            "<Leave>",
            lambda event:
                self._schedule_hide()
        )

    # =========================
    # REACTION SELECTED
    # =========================

    def _reaction_selected(
        self,
        reaction
    ):

        try:

            add_reaction(
                self.message["id"],
                self.username,
                reaction
            )

            self._load_reactions()

        except Exception as error:

            print()
            print("==============================")
            print("REACTION ERROR")
            print("==============================")
            print(error)
            print("==============================")

        if self.reaction_picker:

            self.reaction_picker.destroy()

            self.reaction_picker = None

        self._show_controls()

    # =========================
    # LOAD REACTIONS
    # =========================

    def _load_reactions(self):

        try:

            reactions = get_reactions(
                self.message["id"]
            )

        except Exception as error:

            print()
            print("REACTION LOAD ERROR:")
            print(error)
            print()

            return

        if self.reaction_display:

            self.reaction_display.destroy()

            self.reaction_display = None

        if not reactions:

            return

        self.reaction_display = (
            ReactionDisplay(
                self,
                reactions,
                on_reaction_click=(
                    self._reaction_selected
                )
            )
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
            pady=(0, 2)
        )

    def add_message(
        self,
        message
    ):

        row = MessageRow(
            self,
            message,
            self.is_me,
            self.username
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