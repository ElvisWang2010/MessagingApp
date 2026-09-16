import tkinter as tk

from config import (
    CHAT_BACKGROUND,
    TEXT,
    BUTTON
)


class MessageMenu(tk.Frame):

    def __init__(
        self,
        parent,
        can_delete,
        on_react,
        on_delete
    ):

        super().__init__(
            parent,
            bg="#FFFFFF",
            bd=0,
            highlightthickness=1,
            highlightbackground="#E8DDE1"
        )

        self.on_react = on_react
        self.on_delete = on_delete

        self._create(
            can_delete
        )

    def _create(
        self,
        can_delete
    ):

        react_button = tk.Button(
            self,
            text="React",
            font=(
                "Arial",
                10
            ),
            bg="#FFFFFF",
            fg=TEXT,
            activebackground="#FFF1F5",
            activeforeground=BUTTON,
            relief="flat",
            bd=0,
            anchor="w",
            cursor="hand2",
            command=self._react
        )

        react_button.pack(
            fill="x",
            padx=4,
            pady=2
        )

        if can_delete:

            delete_button = tk.Button(
                self,
                text="Delete",
                font=(
                    "Arial",
                    10
                ),
                bg="#FFFFFF",
                fg="#C75A70",
                activebackground="#FFF1F5",
                activeforeground="#B13F57",
                relief="flat",
                bd=0,
                anchor="w",
                cursor="hand2",
                command=self._delete
            )

            delete_button.pack(
                fill="x",
                padx=4,
                pady=2
            )

    def _react(self):

        if self.on_react:

            self.on_react()

    def _delete(self):

        if self.on_delete:

            self.on_delete()