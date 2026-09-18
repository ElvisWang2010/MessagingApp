import tkinter as tk


class PetalLauncher:

    SIZE = 48
    MARGIN = 28

    BACKGROUND = "#FF8FAB"
    HOVER_BACKGROUND = "#FF789C"

    TEXT = "#FFFFFF"
    TRANSPARENT = "#000000"

    def __init__(self, root, on_open):

        self.root = root
        self.on_open = on_open

        self.window = tk.Toplevel(root)

        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)

        self.window.configure(bg=self.TRANSPARENT)

        try:
            self.window.attributes(
                "-transparentcolor",
                self.TRANSPARENT
            )
        except tk.TclError:
            pass

        self.canvas = tk.Canvas(
            self.window,
            width=self.SIZE,
            height=self.SIZE,
            bg=self.TRANSPARENT,
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack()

        self._draw_button()
        self._position()

        # Clicking
        self.canvas.bind("<Button-1>", self._clicked)

        # Hover
        self.canvas.bind("<Enter>", self._hover_enter)
        self.canvas.bind("<Leave>", self._hover_leave)

        # Right click
        self.canvas.bind("<Button-3>", self._show_menu)

        # Dragging
        self.canvas.bind("<ButtonPress-1>", self._drag_start)
        self.canvas.bind("<B1-Motion>", self._drag_motion)

        self.drag_start_x = 0
        self.drag_start_y = 0
        self.window_start_x = 0
        self.window_start_y = 0

    def _position(self):

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = screen_width - self.SIZE - self.MARGIN
        y = screen_height - self.SIZE - self.MARGIN

        self.window.geometry(
            f"{self.SIZE}x{self.SIZE}+{x}+{y}"
        )

    def _draw_button(self, background=None):

        if background is None:
            background = self.BACKGROUND

        self.canvas.delete("all")

        center = self.SIZE / 2

        # Main circle
        self.canvas.create_oval(
            4,
            4,
            self.SIZE - 4,
            self.SIZE - 4,
            fill=background,
            outline=""
        )

        # Flower
        flower_center_x = center
        flower_center_y = center - 2

        petal_radius = 5
        distance = 5

        petals = (
            (0, -distance),
            (distance, 0),
            (0, distance),
            (-distance, 0)
        )

        for dx, dy in petals:

            self.canvas.create_oval(
                flower_center_x + dx - petal_radius,
                flower_center_y + dy - petal_radius,
                flower_center_x + dx + petal_radius,
                flower_center_y + dy + petal_radius,
                fill=self.TEXT,
                outline=""
            )

        # Flower center
        self.canvas.create_oval(
            flower_center_x - 4,
            flower_center_y - 4,
            flower_center_x + 4,
            flower_center_y + 4,
            fill=background,
            outline=""
        )
    
    # ---------------------------------------------------------
    # Hover
    # ---------------------------------------------------------

    def _hover_enter(self, event=None):

        self._draw_button(
            self.HOVER_BACKGROUND
        )

    def _hover_leave(self, event=None):

        self._draw_button(
            self.BACKGROUND
        )

    # ---------------------------------------------------------
    # Clicking
    # ---------------------------------------------------------

    def _clicked(self, event=None):

        self.on_open()

    # ---------------------------------------------------------
    # Dragging
    # ---------------------------------------------------------

    def _drag_start(self, event):

        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root

        self.window_start_x = self.window.winfo_x()
        self.window_start_y = self.window.winfo_y()

    def _drag_motion(self, event):

        dx = event.x_root - self.drag_start_x
        dy = event.y_root - self.drag_start_y

        new_x = self.window_start_x + dx
        new_y = self.window_start_y + dy

        # Keep the launcher inside the screen.
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        new_x = max(
            0,
            min(
                new_x,
                screen_width - self.SIZE
            )
        )

        new_y = max(
            0,
            min(
                new_y,
                screen_height - self.SIZE
            )
        )

        self.window.geometry(
            f"{self.SIZE}x{self.SIZE}+{new_x}+{new_y}"
        )

    # ---------------------------------------------------------
    # Right-click menu
    # ---------------------------------------------------------

    def _show_menu(self, event):

        menu = tk.Menu(
            self.window,
            tearoff=False,
            bg="#FFF7FA",
            fg="#3A3034",
            activebackground="#FFB6C9",
            activeforeground="#3A3034",
            relief="flat",
            bd=0
        )

        menu.add_command(
            label="Open Petal",
            command=self._clicked
        )

        menu.add_separator()

        menu.add_command(
            label="Exit Petal",
            command=self._exit
        )

        try:

            menu.tk_popup(
                event.x_root,
                event.y_root
            )

        finally:

            menu.grab_release()

    # ---------------------------------------------------------
    # Exit
    # ---------------------------------------------------------

    def _exit(self):

        self.root.destroy()

    # ---------------------------------------------------------
    # Destroy
    # ---------------------------------------------------------

    def destroy(self):

        if self.window.winfo_exists():
            self.window.destroy()