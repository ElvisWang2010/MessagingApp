import tkinter as tk

from config import (
    CHAT_BACKGROUND,
    TEXT,
    MUTED_TEXT,
    BUTTON,
    WINDOW_WIDTH
)


# =========================
# BUBBLE SETTINGS
# =========================

BUBBLE_PADDING_X = 14
BUBBLE_PADDING_Y = 9

BUBBLE_MAX_WIDTH = 330

CORNER_RADIUS = 16

MY_BUBBLE = BUTTON
OTHER_BUBBLE = "#FFE0E8"

MY_TEXT = "white"
OTHER_TEXT = TEXT


# =========================
# DRAWING
# =========================

def draw_rounded_rectangle(
    canvas,
    x1,
    y1,
    x2,
    y2,
    radius,
    fill
):
    """
    Draw a rounded rectangle on a Tkinter Canvas.

    Tkinter does not provide a native rounded rectangle,
    so the shape is built from rectangles and arcs.
    """

    canvas.create_rectangle(
        x1 + radius,
        y1,
        x2 - radius,
        y2,
        fill=fill,
        outline=fill
    )

    canvas.create_rectangle(
        x1,
        y1 + radius,
        x2,
        y2 - radius,
        fill=fill,
        outline=fill
    )

    canvas.create_arc(
        x1,
        y1,
        x1 + radius * 2,
        y1 + radius * 2,
        start=90,
        extent=90,
        fill=fill,
        outline=fill
    )

    canvas.create_arc(
        x2 - radius * 2,
        y1,
        x2,
        y1 + radius * 2,
        start=0,
        extent=90,
        fill=fill,
        outline=fill
    )

    canvas.create_arc(
        x1,
        y2 - radius * 2,
        x1 + radius * 2,
        y2,
        start=180,
        extent=90,
        fill=fill,
        outline=fill
    )

    canvas.create_arc(
        x2 - radius * 2,
        y2 - radius * 2,
        x2,
        y2,
        start=270,
        extent=90,
        fill=fill,
        outline=fill
    )


# =========================
# MESSAGE BUBBLE
# =========================

class MessageBubble(tk.Frame):

    def __init__(
        self,
        parent,
        content,
        is_me,
        on_enter=None,
        on_leave=None
    ):

        self.content = content
        self.is_me = is_me

        self.background = (
            MY_BUBBLE
            if is_me
            else OTHER_BUBBLE
        )

        self.text_color = (
            MY_TEXT
            if is_me
            else OTHER_TEXT
        )

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND
        )

        self.canvas = None

        self.on_enter_callback = on_enter
        self.on_leave_callback = on_leave

        self._create_bubble()

    # =========================
    # CREATE
    # =========================

    def _create_bubble(self):

        font = (
            "Arial",
            11
        )

        temporary = tk.Label(
            self,
            text=self.content,
            font=font,
            wraplength=BUBBLE_MAX_WIDTH,
            justify="left"
        )

        temporary.update_idletasks()

        text_width = temporary.winfo_reqwidth()
        text_height = temporary.winfo_reqheight()

        temporary.destroy()

        width = min(
            text_width + BUBBLE_PADDING_X * 2,
            BUBBLE_MAX_WIDTH + BUBBLE_PADDING_X * 2
        )

        if text_width + BUBBLE_PADDING_X * 2 > width:
            width = BUBBLE_MAX_WIDTH + BUBBLE_PADDING_X * 2

        height = (
            text_height
            + BUBBLE_PADDING_Y * 2
        )

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg=CHAT_BACKGROUND,
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack()

        draw_rounded_rectangle(
            self.canvas,
            1,
            1,
            width - 1,
            height - 1,
            CORNER_RADIUS,
            self.background
        )

        self.canvas.create_text(
            width / 2,
            height / 2,
            text=self.content,
            fill=self.text_color,
            font=font,
            width=BUBBLE_MAX_WIDTH,
            justify="left"
        )

        self._bind_hover()

    # =========================
    # HOVER
    # =========================

    def _bind_hover(self):

        self.bind(
            "<Enter>",
            self._handle_enter
        )

        self.bind(
            "<Leave>",
            self._handle_leave
        )

        self.canvas.bind(
            "<Enter>",
            self._handle_enter
        )

        self.canvas.bind(
            "<Leave>",
            self._handle_leave
        )

    def _handle_enter(self, event=None):

        if self.on_enter_callback:
            self.on_enter_callback()

    def _handle_leave(self, event=None):

        if self.on_leave_callback:
            self.on_leave_callback()

    # =========================
    # SIZE
    # =========================

    def get_width(self):

        return self.winfo_reqwidth()

    def get_height(self):

        return self.winfo_reqheight()