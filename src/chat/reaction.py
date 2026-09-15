import tkinter as tk

from config import (
    CHAT_BACKGROUND,
    TEXT,
    MUTED_TEXT,
    BUTTON,
    BUTTON_HOVER
)


# =========================
# REACTION SETTINGS
# =========================

REACTIONS = [
    "❤️",
    "😂",
    "👍",
    "😭",
    "🥰",
    "😮"
]

REACTION_FONT = (
    "Arial",
    13
)

REACTION_BUTTON_FONT = (
    "Arial",
    12
)


# =========================
# REACTION PICKER
# =========================

class ReactionPicker(tk.Frame):

    def __init__(
        self,
        parent,
        on_reaction
    ):

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND,
            bd=0,
            highlightthickness=0
        )

        self.on_reaction = on_reaction

        self._create_buttons()

    # =========================
    # CREATE
    # =========================

    def _create_buttons(self):

        for reaction in REACTIONS:

            button = tk.Button(
                self,
                text=reaction,
                font=REACTION_BUTTON_FONT,
                bg=CHAT_BACKGROUND,
                fg=TEXT,
                activebackground=BUTTON_HOVER,
                activeforeground=TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda emoji=reaction:
                    self._select_reaction(emoji)
            )

            button.pack(
                side="left",
                padx=2,
                pady=2
            )

    # =========================
    # SELECT
    # =========================

    def _select_reaction(
        self,
        reaction
    ):

        if self.on_reaction:

            self.on_reaction(
                reaction
            )


# =========================
# REACTION DISPLAY
# =========================

class ReactionDisplay(tk.Frame):

    def __init__(
        self,
        parent,
        reactions,
        on_reaction_click=None
    ):

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND
        )

        self.reactions = reactions
        self.on_reaction_click = (
            on_reaction_click
        )

        self._create_display()

    # =========================
    # CREATE
    # =========================

    def _create_display(self):

        for reaction, count in self.reactions.items():

            text = (
                f"{reaction} {count}"
            )

            button = tk.Button(
                self,
                text=text,
                font=(
                    "Arial",
                    9
                ),
                bg="#FFE0E8",
                fg=TEXT,
                activebackground="#FFD0DC",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda emoji=reaction:
                    self._clicked(emoji)
            )

            button.pack(
                side="left",
                padx=2,
                pady=(2, 0)
            )

    # =========================
    # CLICK
    # =========================

    def _clicked(
        self,
        reaction
    ):

        if self.on_reaction_click:

            self.on_reaction_click(
                reaction
            )