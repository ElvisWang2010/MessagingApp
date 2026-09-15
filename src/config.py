import os

from dotenv import load_dotenv


# =========================
# ENVIRONMENT
# =========================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_URL or SUPABASE_KEY is missing from .env"
    )


# =========================
# APP
# =========================

APP_TITLE = "Elvis & Nysa"

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