import tkinter as tk

from config import (
    CHAT_BACKGROUND,
    TEXT,
    BUTTON,
    BUTTON_HOVER
)


# =========================
# REACTIONS
# =========================

REACTIONS = [
    "❤️",
    "😂",
    "👍",
    "😭",
    "🥰",
    "😮"
]


EMOJI_FONT = (
    "Segoe UI Emoji",
    13
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
            bg="white",
            bd=1,
            relief="solid"
        )

        self.on_reaction = on_reaction

        self._create_buttons()

    def _create_buttons(self):

        for reaction in REACTIONS:

            button = tk.Button(
                self,
                text=reaction,
                font=EMOJI_FONT,
                bg="white",
                fg=TEXT,
                activebackground="#FFE5EC",
                activeforeground=TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=3,
                pady=2,
                command=lambda emoji=reaction:
                    self._select_reaction(
                        emoji
                    )
            )

            button.pack(
                side="left"
            )

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

    def _create_display(self):

        for reaction, count in (
            self.reactions.items()
        ):

            if count <= 0:
                continue

            button = tk.Button(
                self,
                text=(
                    f"{reaction} {count}"
                ),
                font=(
                    "Segoe UI Emoji",
                    9
                ),
                bg="#FFE0E8",
                fg=TEXT,
                activebackground="#FFD0DC",
                relief="flat",
                bd=0,
                cursor="hand2",
                padx=6,
                pady=1,
                command=lambda emoji=reaction:
                    self._clicked(
                        emoji
                    )
            )

            button.pack(
                side="left",
                padx=2
            )

    def _clicked(
        self,
        reaction
    ):

        if self.on_reaction_click:

            self.on_reaction_click(
                reaction
            )


# =========================
# REACTION BUTTON
# =========================

class ReactionButton(tk.Button):

    def __init__(
        self,
        parent,
        command
    ):

        super().__init__(
            parent,
            text="♡",
            font=(
                "Arial",
                11
            ),
            bg=CHAT_BACKGROUND,
            fg=BUTTON,
            activebackground="#FFE5EC",
            activeforeground=BUTTON_HOVER,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=4,
            pady=2,
            command=command
        )