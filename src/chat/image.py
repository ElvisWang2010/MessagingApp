import tkinter as tk

from tkinter import (
    filedialog,
    messagebox
)

from io import BytesIO
from urllib.request import urlopen

from PIL import (
    Image,
    ImageTk
)

from config import (
    CHAT_BACKGROUND,
    TEXT
)

from database import (
    upload_image
)


# ============================================================
# SETTINGS
# ============================================================

MAX_IMAGE_WIDTH = 280
MAX_IMAGE_HEIGHT = 240


IMAGE_FORMATS = [
    (
        "Image files",
        "*.png *.jpg *.jpeg *.gif *.webp"
    ),
    (
        "PNG files",
        "*.png"
    ),
    (
        "JPEG files",
        "*.jpg *.jpeg"
    ),
    (
        "GIF files",
        "*.gif"
    ),
    (
        "WebP files",
        "*.webp"
    ),
    (
        "All files",
        "*.*"
    )
]


# ============================================================
# SELECT IMAGE
# ============================================================

def select_image():

    path = filedialog.askopenfilename(
        title="Choose an image",
        filetypes=IMAGE_FORMATS
    )

    if not path:
        return None

    return path


# ============================================================
# UPLOAD IMAGE
# ============================================================

def upload_selected_image():

    path = select_image()

    if not path:
        return None

    try:

        return upload_image(
            path
        )

    except Exception as error:

        print()
        print("==============================")
        print("IMAGE UPLOAD ERROR")
        print("==============================")
        print(error)
        print("==============================")
        print()

        messagebox.showerror(
            "Image Upload Failed",
            str(error)
        )

        return None


# ============================================================
# CHAT IMAGE
# ============================================================

class ChatImage(tk.Frame):

    def __init__(
        self,
        parent,
        image_path=None,
        image_url=None,
        on_enter=None,
        on_leave=None
    ):

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND,
            bd=0,
            highlightthickness=0
        )

        self.image_path = image_path
        self.image_url = image_url

        self.on_enter_callback = on_enter
        self.on_leave_callback = on_leave

        self.image = None
        self.photo = None
        self.label = None

        self._load_image()

    # ========================================================
    # LOAD IMAGE
    # ========================================================

    def _load_image(self):

        if self.image_path:

            self._load_local_image()

        elif self.image_url:

            self._load_remote_image()

    # ========================================================
    # LOCAL IMAGE
    # ========================================================

    def _load_local_image(self):

        try:

            self.image = Image.open(
                self.image_path
            )

            self._display_image()

        except Exception as error:

            print()
            print("==============================")
            print("LOCAL IMAGE ERROR")
            print("==============================")
            print(error)
            print("==============================")
            print()

            self._show_error()

    # ========================================================
    # REMOTE IMAGE
    # ========================================================

    def _load_remote_image(self):

        try:

            with urlopen(
                self.image_url,
                timeout=10
            ) as response:

                image_data = response.read()

            self.image = Image.open(
                BytesIO(image_data)
            )

            self._display_image()

        except Exception as error:

            print()
            print("==============================")
            print("REMOTE IMAGE ERROR")
            print("==============================")
            print(error)
            print("==============================")
            print()

            self._show_error()

    # ========================================================
    # DISPLAY IMAGE
    # ========================================================

    def _display_image(self):

        # Make a copy so the original PIL image
        # isn't modified by thumbnail().

        display_image = self.image.copy()

        display_image.thumbnail(
            (
                MAX_IMAGE_WIDTH,
                MAX_IMAGE_HEIGHT
            ),
            Image.Resampling.LANCZOS
        )

        self.photo = ImageTk.PhotoImage(
            display_image
        )

        self.label = tk.Label(
            self,
            image=self.photo,
            bg=CHAT_BACKGROUND,
            bd=0,
            highlightthickness=0
        )

        self.label.pack(
            padx=0,
            pady=0
        )

        self._bind_hover()

    # ========================================================
    # HOVER
    # ========================================================

    def _bind_hover(self):

        if self.label is None:
            return

        # IMPORTANT:
        #
        # Only the actual image gets hover events.
        # Do not bind them to both the Frame and Label.
        #
        # This prevents rapid Enter/Leave events when
        # moving quickly between images.

        self.label.bind(
            "<Enter>",
            self._handle_enter
        )

        self.label.bind(
            "<Leave>",
            self._handle_leave
        )

    def _handle_enter(
        self,
        event=None
    ):

        if self.on_enter_callback:

            self.on_enter_callback()

    def _handle_leave(
        self,
        event=None
    ):

        if self.on_leave_callback:

            self.on_leave_callback()

    # ========================================================
    # ERROR DISPLAY
    # ========================================================

    def _show_error(self):

        self.label = tk.Label(
            self,
            text="Unable to load image",
            font=(
                "Arial",
                10
            ),
            bg=CHAT_BACKGROUND,
            fg=TEXT,
            bd=0,
            highlightthickness=0
        )

        self.label.pack(
            padx=10,
            pady=10
        )

        self._bind_hover()