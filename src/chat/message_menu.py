import tkinter as tk


class MessageMenu:
    def __init__(self, parent, can_delete, on_react, on_delete):
        self.parent = parent
        self.can_delete = can_delete
        self.on_react = on_react
        self.on_delete = on_delete
        self.menu = None

        self._create_menu()

    def _create_menu(self):
        self.menu = tk.Menu(
            self.parent,
            tearoff=False,
            bg="#FFFFFF",
            fg="#222222",
            activebackground="#FFF0F4",
            activeforeground="#222222",
            relief="solid",
            bd=1,
            font=("Arial", 10)
        )

        self.menu.add_command(
            label="React",
            command=self._react
        )

        if self.can_delete:
            self.menu.add_separator()

            self.menu.add_command(
                label="Delete",
                command=self._delete
            )

    def show(self):
        try:
            x = (
                self.parent.winfo_rootx()
                + self.parent.winfo_width()
                + 4
            )

            y = self.parent.winfo_rooty()

            self.menu.tk_popup(x, y)

        except tk.TclError:
            self.close()

    def _react(self):
        self.close()

        if self.on_react:
            self.on_react()

    def _delete(self):
        self.close()

        if self.on_delete:
            self.on_delete()

    def close(self):
        if self.menu:
            try:
                self.menu.grab_release()
            except tk.TclError:
                pass

            try:
                self.menu.destroy()
            except tk.TclError:
                pass

            self.menu = None