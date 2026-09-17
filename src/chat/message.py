import tkinter as tk

from .bubble import MessageBubble
from .image import ChatImage
from .reaction import ReactionPicker, ReactionDisplay

from database import (
    get_reactions,
    add_reaction,
    delete_message
)

from config import (
    CHAT_BACKGROUND,
    TEXT,
    MUTED_TEXT
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

MENU_FONT = (
    "Arial",
    11,
    "bold"
)

TIMESTAMP_HIDE_DELAY = 120
TIMESTAMP_GAP = 8

MENU_HIDE_DELAY = 250
MENU_GAP = 6


# =========================
# MESSAGE ROW
# =========================

class MessageRow(tk.Frame):

    def __init__(
        self,
        parent,
        message,
        is_me,
        username,
        on_delete=None
    ):

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND
        )

        self.message = message
        self.is_me = is_me
        self.username = username
        self.on_delete = on_delete

        self.hide_job = None
        self.menu_hide_job = None

        self.reaction_picker = None
        self.reaction_display = None

        self._context_menu = None

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

        # =========================
        # MESSAGE CONTENT
        # =========================

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
                )
            )

        else:

            self.content = MessageBubble(
                self.message_line,
                self.message.get(
                    "content",
                    ""
                ),
                self.is_me
            )

        # =========================
        # THREE DOT BUTTON
        # =========================

        # IMPORTANT:
        #
        # The button is ALWAYS packed.
        #
        # We never pack_forget() it.
        #
        # This means the message geometry never
        # changes when the mouse moves over it.
        #
        # It is simply made invisible by using the
        # same foreground color as the background.

        self.menu_button = tk.Button(
            self.message_line,
            text="•••",
            font=MENU_FONT,
            bg=CHAT_BACKGROUND,
            fg=CHAT_BACKGROUND,
            activebackground=CHAT_BACKGROUND,
            activeforeground=CHAT_BACKGROUND,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            padx=2,
            pady=0,
            command=self._open_menu
        )

        # =========================
        # MESSAGE ORDER
        # =========================

        if self.is_me:

            self.menu_button.pack(
                side="left",
                padx=(
                    0,
                    MENU_GAP
                )
            )

            self.content.pack(
                side="left"
            )

        else:

            self.content.pack(
                side="left"
            )

            self.menu_button.pack(
                side="left",
                padx=(
                    MENU_GAP,
                    0
                )
            )

        # =========================
        # TIMESTAMP
        # =========================

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
        # REACTIONS
        # =========================

        self._load_reactions()

        # =========================
        # HOVER
        # =========================

        self._bind_hover_events()

    # =========================
    # HOVER EVENTS
    # =========================

    def _bind_hover_events(self):

        # Only the message area controls hover.
        #
        # Do NOT bind hover separately to:
        #   - MessageBubble
        #   - Canvas
        #   - Image
        #   - MessageRow
        #   - content_frame
        #
        # Those nested bindings were causing rapid
        # enter/leave events.

        self.message_line.bind(
            "<Enter>",
            self._hover_enter
        )

        self.message_line.bind(
            "<Leave>",
            self._hover_leave
        )

        # The button is also explicitly bound so
        # moving onto it keeps the controls visible.

        self.menu_button.bind(
            "<Enter>",
            self._hover_enter
        )

        self.menu_button.bind(
            "<Leave>",
            self._hover_leave
        )

    def _hover_enter(
        self,
        event=None
    ):

        self._cancel_hide()
        self._cancel_menu_hide()

        self._show_controls()

    def _hover_leave(
        self,
        event=None
    ):

        self._schedule_hide_controls()

    # =========================
    # SHOW CONTROLS
    # =========================

    def _show_controls(self):

        self._cancel_menu_hide()
        self._cancel_hide()

        # The button is already part of the layout.
        # We only change its visibility.

        self.menu_button.config(
            fg=MUTED_TEXT,
            activeforeground=TEXT
        )

        self.menu_button.lift()

    # =========================
    # HIDE CONTROLS
    # =========================

    def _schedule_hide_controls(self):

        self._cancel_menu_hide()

        self.menu_hide_job = self.after(
            MENU_HIDE_DELAY,
            self._hide_controls
        )

    def _hide_controls(self):

        self._cancel_menu_hide()

        # DO NOT remove the button from the layout.
        #
        # Removing it would cause the message to move.

        self.menu_button.config(
            fg=CHAT_BACKGROUND,
            activeforeground=CHAT_BACKGROUND
        )

        # Close the native context menu if one exists.

        if self._context_menu is not None:

            try:
                self._context_menu.unpost()
            except tk.TclError:
                pass

            self._context_menu = None

    def _cancel_menu_hide(self):

        if self.menu_hide_job is None:
            return

        try:

            self.after_cancel(
                self.menu_hide_job
            )

        except tk.TclError:
            pass

        self.menu_hide_job = None

    # =========================
    # MESSAGE MENU
    # =========================

    def _open_menu(self):

        self._cancel_menu_hide()

        if self._context_menu is not None:

            try:

                self._context_menu.unpost()

            except tk.TclError:
                pass

            self._context_menu = None

            return

        menu = tk.Menu(
            self,
            tearoff=False,
            bg="#FFFFFF",
            fg="#222222",
            activebackground="#FFF0F4",
            activeforeground="#222222",
            relief="solid",
            bd=1,
            font=(
                "Arial",
                10
            )
        )

        # =========================
        # REACT
        # =========================

        menu.add_command(
            label="React",
            command=self._open_reaction_picker
        )

        # =========================
        # DELETE
        # =========================

        if self.is_me:

            menu.add_separator()

            menu.add_command(
                label="Delete",
                command=self._delete
            )

        self._context_menu = menu

        try:

            x = self.menu_button.winfo_rootx()

            y = (
                self.menu_button.winfo_rooty()
                + self.menu_button.winfo_height()
                + 3
            )

            menu.post(
                x,
                y
            )

        except tk.TclError:

            self._context_menu = None

    # =========================
    # DELETE
    # =========================

    def _delete(self):

        if self._context_menu is not None:

            try:

                self._context_menu.unpost()

            except tk.TclError:
                pass

            self._context_menu = None

        message_id = self.message.get(
            "id"
        )

        if not message_id:
            return

        try:

            delete_message(
                message_id
            )

            if self.on_delete:

                self.on_delete(
                    message_id
                )

        except Exception as error:

            print()
            print(
                "MESSAGE DELETE ERROR:"
            )
            print(error)
            print()

    # =========================
    # LOAD REACTIONS
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
            print(
                "REACTION LOAD ERROR:"
            )
            print(error)
            print()

    # =========================
    # REFRESH REACTIONS
    # =========================

    def refresh_reactions(self):

        if not self.winfo_exists():
            return

        self._load_reactions()

    # =========================
    # DISPLAY REACTIONS
    # =========================

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
            padx=2,
            pady=(
                1,
                0
            )
        )

    # =========================
    # REACTION PICKER
    # =========================

    def _open_reaction_picker(self):

        # Close native menu first.

        if self._context_menu is not None:

            try:

                self._context_menu.unpost()

            except tk.TclError:
                pass

            self._context_menu = None

        # Toggle picker.

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
            padx=2,
            pady=(
                2,
                1
            )
        )

    # =========================
    # REACTION SELECTED
    # =========================

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
            print(
                "REACTION ERROR:"
            )
            print(error)
            print()

    # =========================
    # REACTION CLICKED
    # =========================

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
    # DESTROY
    # =========================

    def destroy(self):

        self._cancel_hide()
        self._cancel_menu_hide()

        if self._context_menu is not None:

            try:

                self._context_menu.unpost()

            except tk.TclError:
                pass

            self._context_menu = None

        if self.reaction_picker:

            try:

                self.reaction_picker.destroy()

            except Exception:
                pass

            self.reaction_picker = None

        if self.reaction_display:

            try:

                self.reaction_display.destroy()

            except Exception:
                pass

            self.reaction_display = None

        super().destroy()


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
    # CREATE GROUP
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
            padx=6,
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
        username=None,
        on_delete=None
    ):

        if username is None:

            username = self.username

        row = MessageRow(
            self,
            message,
            self.is_me,
            username,
            on_delete=on_delete
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
    # REMOVE MESSAGE
    # =========================

    def remove_message(
        self,
        row
    ):

        if row in self.messages:

            self.messages.remove(
                row
            )

        row.destroy()

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