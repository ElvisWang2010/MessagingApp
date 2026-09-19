import os
import sys

from dotenv import load_dotenv


# =========================
# ENVIRONMENT
# =========================

def get_env_path():
    """
    Find the .env file both when running normally
    and when running as a PyInstaller application.
    """

    if getattr(sys, "frozen", False):
        # Running as a packaged PyInstaller application
        base_path = sys._MEIPASS
        return os.path.join(
            base_path,
            "src",
            ".env"
        )

    # Running normally from the source code
    return os.path.join(
        os.path.dirname(__file__),
        ".env"
    )


env_path = get_env_path()

load_dotenv(env_path)


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL:
    raise ValueError(
        "SUPABASE_URL is missing from src/.env"
    )


if not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_KEY is missing from src/.env"
    )


# =========================
# APP
# =========================

APP_TITLE = "Petal"

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 650

MIN_WIDTH = 400
MIN_HEIGHT = 500


# =========================
# COLORS
# =========================

BACKGROUND = "#FFF7FA"
HEADER = "#FFB6C9"
CHAT_BACKGROUND = "#FFFDFE"
INPUT_BACKGROUND = "#FFFFFF"

TEXT = "#3A3034"
MUTED_TEXT = "#8A7B80"

BUTTON = "#FF8FAB"
BUTTON_HOVER = "#FF7599"

ERROR = "#D65A70"