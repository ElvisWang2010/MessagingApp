import tkinter as tk

from config import (
    CHAT_BACKGROUND,
    TEXT,
    BUTTON,
    MY_BUBBLE,
    OTHER_BUBBLE
)


# =========================
# BUBBLE SETTINGS
# =========================

BUBBLE_PADDING_X = 15
BUBBLE_PADDING_Y = 9

BUBBLE_MAX_WIDTH = 310

CORNER_RADIUS = 18

MY_TEXT = "#FFFFFF"
OTHER_TEXT = TEXT


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
    fill
):

    # Center
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

    # Top-left
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

    # Top-right
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

    # Bottom-left
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

    # Bottom-right
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

        # Kept for compatibility.
        # Hover is controlled by MessageRow.
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

        # =========================
        # MEASURE TEXT
        # =========================

        temporary = tk.Label(
            self,
            text=self.content,
            font=font,
            wraplength=BUBBLE_MAX_WIDTH,
            justify="left"
        )

        temporary.update_idletasks()

        text_width = (
            temporary.winfo_reqwidth()
        )

        text_height = (
            temporary.winfo_reqheight()
        )

        temporary.destroy()

        # =========================
        # SIZE
        # =========================

        width = min(
            text_width
            + BUBBLE_PADDING_X * 2,

            BUBBLE_MAX_WIDTH
            + BUBBLE_PADDING_X * 2
        )

        height = (
            text_height
            + BUBBLE_PADDING_Y * 2
        )

        # =========================
        # CANVAS
        # =========================

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            bg=CHAT_BACKGROUND,
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack()

        # =========================
        # BUBBLE
        # =========================

        draw_rounded_rectangle(
            self.canvas,
            1,
            1,
            width - 1,
            height - 1,
            CORNER_RADIUS,
            self.background
        )

        # =========================
        # TEXT
        # =========================

        self.canvas.create_text(
            width / 2,
            height / 2,
            text=self.content,
            fill=self.text_color,
            font=font,
            width=BUBBLE_MAX_WIDTH,
            justify="left"
        )

    # =========================
    # SIZE
    # =========================

    def get_width(self):

        return self.winfo_reqwidth()

    def get_height(self):

        return self.winfo_reqheight()