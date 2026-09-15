import tkinter as tk

from config import (
    CHAT_BACKGROUND,
    TEXT,
    BUTTON
)


REACTIONS = [
    "❤️",
    "😂",
    "😭",
    "😮",
    "😡",
    "👍"
]


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
                font=(
                    "Arial",
                    13
                ),
                bg="white",
                fg=TEXT,
                activebackground="#FFF0F4",
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda r=reaction:
                    self._select_reaction(r)
            )

            button.pack(
                side="left",
                padx=3,
                pady=3
            )

    def _select_reaction(self, reaction):

        self.on_reaction(
            reaction
        )


class ReactionDisplay(tk.Frame):

    def __init__(
        self,
        parent,
        reactions
    ):

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND
        )

        self.reactions = reactions

        self._create_display()

    def _create_display(self):

        for reaction, count in self.reactions.items():

            if count <= 0:
                continue

            text = (
                f"{reaction} {count}"
            )

            label = tk.Label(
                self,
                text=text,
                font=(
                    "Arial",
                    9
                ),
                bg="#FFF0F4",
                fg=TEXT,
                padx=7,
                pady=2,
                relief="flat"
            )

            label.pack(
                side="left",
                padx=2
            )


class ReactionButton(tk.Button):

    def __init__(
        self,
        parent,
        command
    ):

        super().__init__(
            parent,
            text="＋",
            font=(
                "Arial",
                11,
                "bold"
            ),
            bg="white",
            fg=BUTTON,
            activebackground="#FFF0F4",
            activeforeground=BUTTON,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=command
        )