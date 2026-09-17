import tkinter as tk

from tkinter import messagebox

from database import (
    get_messages,
    send_message,
    send_image_message
)

from realtime_listener import (
    start_realtime_listener
)

from config import (
    BACKGROUND,
    HEADER,
    CHAT_BACKGROUND,
    INPUT_BACKGROUND,
    TEXT,
    MUTED_TEXT,
    BUTTON,
    BUTTON_HOVER,
    BORDER,
    SURFACE,
    MESSAGE_PADDING_X,
    MESSAGE_GROUP_SPACING
)

from .message import MessageGroup
from .image import upload_selected_image


# =========================
# SETTINGS
# =========================

HEADER_HEIGHT = 64

INPUT_HEIGHT = 72

SCROLL_SPEED = 3


# =========================
# ROUNDED RECTANGLE
# =========================

def draw_rounded_rectangle(
    canvas,
    x1,
    y1,
    x2,
    y2,
    radius,
    fill,
    outline=None,
    width=1
):

    if outline is None:
        outline = fill

    canvas.create_rectangle(
        x1 + radius,
        y1,
        x2 - radius,
        y2,
        fill=fill,
        outline=outline,
        width=width
    )

    canvas.create_rectangle(
        x1,
        y1 + radius,
        x2,
        y2 - radius,
        fill=fill,
        outline=outline,
        width=width
    )

    canvas.create_arc(
        x1,
        y1,
        x1 + radius * 2,
        y1 + radius * 2,
        start=90,
        extent=90,
        fill=fill,
        outline=outline,
        width=width
    )

    canvas.create_arc(
        x2 - radius * 2,
        y1,
        x2,
        y1 + radius * 2,
        start=0,
        extent=90,
        fill=fill,
        outline=outline,
        width=width
    )

    canvas.create_arc(
        x1,
        y2 - radius * 2,
        x1 + radius * 2,
        y2,
        start=180,
        extent=90,
        fill=fill,
        outline=outline,
        width=width
    )

    canvas.create_arc(
        x2 - radius * 2,
        y2 - radius * 2,
        x2,
        y2,
        start=270,
        extent=90,
        fill=fill,
        outline=outline,
        width=width
    )


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

        # All displayed messages
        self.message_rows = {}

        # Message -> group
        self.message_groups = {}

        self._create_header()

        self._create_chat_area()

        self._create_input_area()

        self._load_existing_messages()

        start_realtime_listener(
            self._receive_realtime_event
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


        # =========================
        # LEFT SIDE
        # =========================

        self.header_left = tk.Frame(
            self.header,
            bg=HEADER
        )

        self.header_left.pack(
            side="left",
            fill="y",
            padx=20
        )


        self.title_label = tk.Label(
            self.header_left,
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
            side="top",
            anchor="w",
            pady=(
                9,
                0
            )
        )


        self.status_label = tk.Label(
            self.header_left,
            text="♡ connected",
            font=(
                "Arial",
                9
            ),
            bg=HEADER,
            fg=MUTED_TEXT
        )

        self.status_label.pack(
            side="top",
            anchor="w",
            pady=(
                -1,
                0
            )
        )


        # =========================
        # RIGHT SIDE
        # =========================

        self.header_heart = tk.Label(
            self.header,
            text="♡",
            font=(
                "Arial",
                22
            ),
            bg=HEADER,
            fg=BUTTON
        )

        self.header_heart.pack(
            side="right",
            padx=20
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


        # =========================
        # CANVAS
        # =========================

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


        # =========================
        # SCROLLBAR
        # =========================

        self.scrollbar = tk.Scrollbar(
            self.chat_container,
            orient="vertical",
            command=self.chat_canvas.yview,
            relief="flat",
            bd=0,
            highlightthickness=0,
            troughcolor=CHAT_BACKGROUND,
            activebackground="#E8D3DA"
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )


        self.chat_canvas.configure(
            yscrollcommand=self.scrollbar.set
        )


        # =========================
        # MESSAGES
        # =========================

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


    def _leave_chat_area(
        self,
        event=None
    ):

        self.chat_container.unbind_all(
            "<MouseWheel>"
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


        # =========================
        # IMAGE BUTTON
        # =========================

        self.image_button = tk.Button(
            self.input_container,
            text="＋",
            font=(
                "Arial",
                18
            ),
            bg=BACKGROUND,
            fg=BUTTON,
            activebackground=BACKGROUND,
            activeforeground=BUTTON_HOVER,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            command=self._send_image
        )

        self.image_button.pack(
            side="left",
            padx=(
                12,
                4
            ),
            pady=12
        )


        # =========================
        # INPUT SHELL
        # =========================

        self.input_shell = tk.Frame(
            self.input_container,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightcolor=BORDER,
            highlightthickness=1,
            bd=0
        )

        self.input_shell.pack(
            side="left",
            fill="x",
            expand=True,
            pady=11
        )


        # =========================
        # ENTRY
        # =========================

        self.message_entry = tk.Entry(
            self.input_shell,
            font=(
                "Arial",
                11
            ),
            bg=SURFACE,
            fg=TEXT,
            insertbackground=BUTTON,
            relief="flat",
            bd=0,
            highlightthickness=0
        )

        self.message_entry.pack(
            fill="both",
            expand=True,
            padx=13,
            pady=8
        )


        # =========================
        # SEND BUTTON
        # =========================

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
            highlightthickness=0,
            cursor="hand2",
            command=self._send_current_message
        )

        self.send_button.pack(
            side="right",
            padx=(
                8,
                14
            ),
            pady=11,
            ipadx=10,
            ipady=5
        )


        # =========================
        # HOVER
        # =========================

        self.send_button.bind(
            "<Enter>",
            lambda event: self.send_button.config(
                bg=BUTTON_HOVER
            )
        )

        self.send_button.bind(
            "<Leave>",
            lambda event: self.send_button.config(
                bg=BUTTON
            )
        )


        self.image_button.bind(
            "<Enter>",
            lambda event: self.image_button.config(
                fg=BUTTON_HOVER
            )
        )

        self.image_button.bind(
            "<Leave>",
            lambda event: self.image_button.config(
                fg=BUTTON
            )
        )


        # =========================
        # ENTER
        # =========================

        self.message_entry.bind(
            "<Return>",
            self._enter_pressed
        )

        self.message_entry.focus()


    # =========================
    # LOAD HISTORY
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

        message_id = message.get(
            "id"
        )


        if message_id is not None:

            if message_id in self.message_rows:

                return self.message_rows[
                    message_id
                ]


        sender = message.get(
            "sender",
            ""
        )


        is_me = (
            sender == self.username
        )


        # =========================
        # GROUP
        # =========================

        if (
            self.current_group is None
            or sender != self.last_sender
        ):

            self.current_group = MessageGroup(
                self.messages_frame,
                sender,
                is_me,
                self.username
            )

            self.current_group.pack(
                fill="x",
                padx=MESSAGE_PADDING_X,
                pady=(
                    MESSAGE_GROUP_SPACING,
                    0
                )
            )

            self.last_sender = sender


        # =========================
        # MESSAGE
        # =========================

        row = self.current_group.add_message(
            message,
            username=self.username,
            on_delete=self._delete_message
        )


        if message_id is not None:

            self.message_rows[
                message_id
            ] = row

            self.message_groups[
                message_id
            ] = self.current_group


        if scroll:

            self._scroll_to_bottom()


        return row


    # =========================
    # DELETE MESSAGE
    # =========================

    def _delete_message(
        self,
        message_id
    ):

        row = self.message_rows.get(
            message_id
        )

        group = self.message_groups.get(
            message_id
        )


        if row is None:

            return


        if group is not None:

            group.remove_message(
                row
            )

        else:

            row.destroy()


        self.message_rows.pop(
            message_id,
            None
        )

        self.message_groups.pop(
            message_id,
            None
        )


        # Remove empty group

        if (
            group is not None
            and group.message_count() == 0
        ):

            group.destroy()

            if self.current_group is group:

                self.current_group = None

                self.last_sender = None


        self.update_idletasks()

        self._update_scroll_region()


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

            inserted = send_message(
                self.username,
                content
            )


            # Display immediately

            if inserted:

                for message in inserted:

                    self._add_message(
                        message,
                        scroll=True
                    )


            self.message_entry.delete(
                0,
                tk.END
            )


        except Exception as error:

            print()
            print("MESSAGE SEND ERROR:")
            print(error)
            print()


            messagebox.showerror(
                "Send Failed",
                str(error)
            )


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

            image_url = upload_selected_image()


            if not image_url:

                return


            inserted = send_image_message(
                self.username,
                image_url
            )


            if inserted:

                for message in inserted:

                    self._add_message(
                        message,
                        scroll=True
                    )


        except Exception as error:

            print()
            print("==============================")
            print("IMAGE MESSAGE ERROR")
            print("==============================")
            print(error)
            print("==============================")
            print()


            messagebox.showerror(
                "Image Send Failed",
                str(error)
            )


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

    def _receive_realtime_event(
        self,
        event_type,
        data
    ):

        self.after(
            0,
            lambda: self._handle_realtime_event(
                event_type,
                data
            )
        )


    def _handle_realtime_event(
        self,
        event_type,
        data
    ):

        if event_type == "message":

            action = data.get(
                "action"
            )

            record = data.get(
                "record"
            )


            if action == "INSERT":

                if record:

                    self._add_message(
                        record,
                        scroll=True
                    )


            elif action == "DELETE":

                if record:

                    message_id = record.get(
                        "id"
                    )


                    if message_id:

                        self._delete_message(
                            message_id
                        )


        elif event_type == "reaction":

            record = data.get(
                "record"
            )

            old_record = data.get(
                "old_record"
            )

            action = data.get(
                "action"
            )


            message_id = None


            if record:

                message_id = record.get(
                    "message_id"
                )


            if (
                message_id is None
                and old_record
            ):

                message_id = old_record.get(
                    "message_id"
                )


            if message_id is None:

                return


            row = self.message_rows.get(
                message_id
            )


            if row:

                row.refresh_reactions()


    # =========================
    # SCROLL
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
# PUBLIC CREATOR
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