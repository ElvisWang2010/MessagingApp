import os
import uuid
import tkinter as tk

from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk

from config import (
    CHAT_BACKGROUND,
    TEXT,
    BUTTON,
    BUTTON_HOVER,
    SUPABASE_URL
)

from database import upload_image


# =========================
# IMAGE SETTINGS
# =========================

MAX_IMAGE_WIDTH = 280
MAX_IMAGE_HEIGHT = 240

IMAGE_FORMATS = [
    ("Image files", "*.png *.jpg *.jpeg *.gif *.webp"),
    ("PNG files", "*.png"),
    ("JPEG files", "*.jpg *.jpeg"),
    ("All files", "*.*")
]


# =========================
# IMAGE SELECTOR
# =========================

def select_image():

    path = filedialog.askopenfilename(
        title="Choose an image",
        filetypes=IMAGE_FORMATS
    )

    if not path:

        return None

    return path


# =========================
# IMAGE UPLOAD
# =========================

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
        print("IMAGE UPLOAD ERROR:")
        print(error)
        print()

        messagebox.showerror(
            "Image Upload Failed",
            "Could not upload the image."
        )

        return None


# =========================
# IMAGE DISPLAY
# =========================

class ChatImage(tk.Frame):

    def __init__(
        self,
        parent,
        image_path=None,
        image_url=None
    ):

        super().__init__(
            parent,
            bg=CHAT_BACKGROUND
        )

        self.image_path = image_path
        self.image_url = image_url

        self.image = None
        self.photo = None

        self._load_image()

    # =========================
    # LOAD
    # =========================

    def _load_image(self):

        if self.image_path:

            self._load_local_image()

        elif self.image_url:

            self._load_remote_image()

    # =========================
    # LOCAL IMAGE
    # =========================

    def _load_local_image(self):

        try:

            self.image = Image.open(
                self.image_path
            )

            self._display_image()

        except Exception as error:

            print()
            print("LOCAL IMAGE ERROR:")
            print(error)
            print()

    # =========================
    # REMOTE IMAGE
    # =========================

    def _load_remote_image(self):

        # Remote image loading will be
        # implemented after the basic
        # image sending system is working.

        label = tk.Label(
            self,
            text="Image",
            font=(
                "Arial",
                10
            ),
            bg=CHAT_BACKGROUND,
            fg=TEXT
        )

        label.pack()

    # =========================
    # DISPLAY
    # =========================

    def _display_image(self):

        image = self.image.copy()

        image.thumbnail(
            (
                MAX_IMAGE_WIDTH,
                MAX_IMAGE_HEIGHT
            ),
            Image.Resampling.LANCZOS
        )

        self.photo = ImageTk.PhotoImage(
            image
        )

        label = tk.Label(
            self,
            image=self.photo,
            bg=CHAT_BACKGROUND,
            bd=0
        )

        label.pack()