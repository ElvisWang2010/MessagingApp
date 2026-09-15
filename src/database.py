from supabase import create_client

from config import SUPABASE_URL, SUPABASE_KEY


# =========================
# SUPABASE CONNECTION
# =========================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================
# USERS
# =========================

def find_user(username):

    response = (
        supabase
        .table("users")
        .select("username, password")
        .eq("username", username)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]


# =========================
# MESSAGES
# =========================

def get_messages():

    response = (
        supabase
        .table("messages")
        .select("*")
        .order("created_at")
        .execute()
    )

    return response.data


def send_message(sender, content):

    response = (
        supabase
        .table("messages")
        .insert({
            "sender": sender,
            "content": content
        })
        .execute()
    )

    return response.data