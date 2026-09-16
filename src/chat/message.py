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


# ============================================================
# SETTINGS
# ============================================================

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

TIMESTAMP_HIDE_DELAY = 250
TIMESTAMP_GAP = 8

MENU_HIDE_DELAY = 300
MENU_GAP = 6


# ============================================================
# MESSAGE ROW
# ============================================================

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

        # -------------------------
        # Timers
        # -------------------------

        self.hide_job = None
        self.menu_hide_job = None
        self.timestamp_after_id = None

        # -------------------------
        # Widgets
        # -------------------------

        self.content = None
        self.timestamp = None
        self.menu_button = None

        self.reaction_picker = None
        self.reaction_display = None

        self.context_menu = None

        # -------------------------
        # Hover state
        # -------------------------

        self.hovering_content = False
        self.hovering_menu = False
        self.hovering_timestamp = False

        self._create_row()

    # ========================================================
    # CREATE ROW
    # ========================================================

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

        # ====================================================
        # MESSAGE CONTENT
        # ====================================================

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
                on_enter=self._hover_enter,
                on_leave=self._hover_leave
            )

        else:

            self.content = MessageBubble(
                self.message_line,
                self.message.get(
                    "content",
                    ""
                ),
                self.is_me,
                on_enter=self._hover_enter,
                on_leave=self._hover_leave
            )

        # ====================================================
        # THREE DOT BUTTON
        # ====================================================

        self.menu_button = tk.Button(
            self.message_line,
            text="•••",
            font=MENU_FONT,
            bg=CHAT_BACKGROUND,
            fg=MUTED_TEXT,
            activebackground=CHAT_BACKGROUND,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            padx=3,
            pady=0,
            command=self._open_menu
        )

        self.menu_button.bind(
            "<Enter>",
            self._menu_enter
        )

        self.menu_button.bind(
            "<Leave>",
            self._menu_leave
        )

        # ====================================================
        # MESSAGE POSITION
        # ====================================================

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

        # Hide until hovering

        self.menu_button.pack_forget()

        # ====================================================
        # TIMESTAMP
        # ====================================================

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

        # ====================================================
        # REACTIONS
        # ====================================================

        self._load_reactions()

    # ========================================================
    # HOVER
    # ========================================================

    def _hover_enter(
        self,
        event=None
    ):

        self.hovering_content = True

        self._cancel_hide()
        self._cancel_menu_hide()

        self._show_controls()
        self._show_timestamp()

    def _hover_leave(
        self,
        event=None
    ):

        self.hovering_content = False

        self._schedule_hide_controls()
        self._schedule_hide()

    # ========================================================
    # SHOW CONTROLS
    # ========================================================

    def _show_controls(self):

        self._cancel_menu_hide()

        if self.menu_button is None:
            return

        if self.menu_button.winfo_ismapped():
            return

        if self.is_me:

            self.menu_button.pack(
                side="left",
                before=self.content,
                padx=(
                    0,
                    MENU_GAP
                )
            )

        else:

            self.menu_button.pack(
                side="left",
                after=self.content,
                padx=(
                    MENU_GAP,
                    0
                )
            )

        self.menu_button.lift()

    # ========================================================
    # HIDE CONTROLS
    # ========================================================

    def _schedule_hide_controls(self):

        self._cancel_menu_hide()

        self.menu_hide_job = self.after(
            MENU_HIDE_DELAY,
            self._hide_controls
        )

    def _hide_controls(self):

        if (
            self.hovering_content
            or self.hovering_menu
        ):
            return

        if self.context_menu is not None:

            try:
                self.context_menu.unpost()
            except tk.TclError:
                pass

            self.context_menu = None

        if self.menu_button is not None:
            self.menu_button.pack_forget()

        self.menu_hide_job = None

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

    # ========================================================
    # MENU HOVER
    # ========================================================

    def _menu_enter(
        self,
        event=None
    ):

        self.hovering_menu = True

        self._cancel_menu_hide()
        self._cancel_hide()

    def _menu_leave(
        self,
        event=None
    ):

        self.hovering_menu = False

        self._schedule_hide_controls()
        self._schedule_hide()

    # ========================================================
    # MESSAGE MENU
    # ========================================================

    def _open_menu(self):

        self._cancel_menu_hide()

        if self.context_menu is not None:

            try:
                self.context_menu.unpost()
            except tk.TclError:
                pass

            self.context_menu = None

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

        menu.add_command(
            label="React",
            command=self._open_reaction_picker
        )

        if self.is_me:

            menu.add_separator()

            menu.add_command(
                label="Delete",
                command=self._delete
            )

        self.context_menu = menu

        try:

            x = (
                self.menu_button.winfo_rootx()
                + self.menu_button.winfo_width()
                + 2
            )

            y = (
                self.menu_button.winfo_rooty()
            )

            menu.post(
                x,
                y
            )

        except tk.TclError:

            self.context_menu = None

    # ========================================================
    # DELETE
    # ========================================================

    def _delete(self):

        if self.context_menu is not None:

            try:
                self.context_menu.unpost()
            except tk.TclError:
                pass

            self.context_menu = None

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
            print("==============================")
            print("MESSAGE DELETE ERROR")
            print("==============================")
            print(error)
            print("==============================")
            print()

    # ========================================================
    # REACTIONS
    # ========================================================

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
            print("==============================")
            print("REACTION LOAD ERROR")
            print("==============================")
            print(error)
            print("==============================")
            print()

    def refresh_reactions(self):

        if not self.winfo_exists():
            return

        self._load_reactions()

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

    # ========================================================
    # REACTION PICKER
    # ========================================================

    def _open_reaction_picker(self):

        if self.context_menu is not None:

            try:
                self.context_menu.unpost()
            except tk.TclError:
                pass

            self.context_menu = None

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
            print("==============================")
            print("REACTION ERROR")
            print("==============================")
            print(error)
            print("==============================")
            print()

    def _reaction_clicked(
        self,
        reaction
    ):

        self._reaction_selected(
            reaction
        )

    # ========================================================
    # TIMESTAMP
    # ========================================================

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

            parts = time_part.split(
                ":"
            )

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

            return (
                f"{hour}:{minute} "
                f"{suffix}"
            )

        except (
            ValueError,
            IndexError
        ):

            return ""

    # ========================================================
    # SHOW TIMESTAMP
    # ========================================================

    def _show_timestamp(self):

        self._cancel_hide()

        if not self.winfo_exists():
            return

        self.update_idletasks()

        content_width = (
            self.content.winfo_reqwidth()
        )

        content_height = (
            self.content.winfo_reqheight()
        )

        timestamp_width = (
            self.timestamp.winfo_reqwidth()
        )

        row_width = (
            self.winfo_width()
        )

        if row_width <= 1:

            self.timestamp_after_id = self.after(
                10,
                self._show_timestamp
            )

            return

        center_y = (
            content_height // 2
        )

        if self.is_me:

            x = (
                row_width
                - content_width
                - TIMESTAMP_GAP
                - timestamp_width
            )

            self.timestamp.place(
                x=x,
                y=center_y,
                anchor="w"
            )

        else:

            x = (
                content_width
                + TIMESTAMP_GAP
            )

            self.timestamp.place(
                x=x,
                y=center_y,
                anchor="w"
            )

        self.timestamp.lift()

        self.timestamp_after_id = None

    # ========================================================
    # HIDE TIMESTAMP
    # ========================================================

    def _schedule_hide(self):

        self._cancel_hide()

        self.hide_job = self.after(
            TIMESTAMP_HIDE_DELAY,
            self._hide_timestamp
        )

    def _hide_timestamp(self):

        if (
            self.hovering_content
            or self.hovering_timestamp
        ):
            return

        if self.timestamp:

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

        if self.timestamp_after_id is not None:

            try:

                self.after_cancel(
                    self.timestamp_after_id
                )

            except tk.TclError:
                pass

            self.timestamp_after_id = None

    # ========================================================
    # TIMESTAMP HOVER
    # ========================================================

    def _timestamp_enter(
        self,
        event=None
    ):

        self.hovering_timestamp = True

        self._cancel_hide()

    def _timestamp_leave(
        self,
        event=None
    ):

        self.hovering_timestamp = False

        self._schedule_hide()

    # ========================================================
    # DESTROY
    # ========================================================

    def destroy(self):

        self._cancel_hide()
        self._cancel_menu_hide()

        if self.context_menu is not None:

            try:
                self.context_menu.unpost()
            except tk.TclError:
                pass

            self.context_menu = None

        if self.reaction_picker:

            try:
                self.reaction_picker.destroy()
            except Exception:
                pass

            self.reaction_picker = None

        super().destroy()


# ============================================================
# MESSAGE GROUP
# ============================================================

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

    # ========================================================
    # GROUP HEADER
    # ========================================================

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

    # ========================================================
    # ADD MESSAGE
    # ========================================================

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

    # ========================================================
    # REMOVE MESSAGE
    # ========================================================

    def remove_message(
        self,
        row
    ):

        if row in self.messages:

            self.messages.remove(
                row
            )

        row.destroy()

    # ========================================================
    # MESSAGE COUNT
    # ========================================================

    def message_count(self):

        return len(
            self.messages
        )

    # ========================================================
    # LAST MESSAGE
    # ========================================================

    def last_message(self):

        if not self.messages:
            return None

        return self.messages[-1]