import os
import uuid

from supabase import create_client

from config import (
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================
# SUPABASE
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
        .select(
            "username, password"
        )
        .eq(
            "username",
            username
        )
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


def send_message(
    sender,
    content
):

    response = (
        supabase
        .table("messages")
        .insert({
            "sender": sender,
            "content": content,
            "message_type": "text"
        })
        .execute()
    )

    return response.data


def delete_message(
    message_id
):

    response = (
        supabase
        .table("messages")
        .delete()
        .eq(
            "id",
            message_id
        )
        .execute()
    )

    return response.data


# =========================
# IMAGE MESSAGES
# =========================

def send_image_message(
    sender,
    image_url
):

    response = (
        supabase
        .table("messages")
        .insert({
            "sender": sender,
            "content": "",
            "message_type": "image",
            "image_url": image_url
        })
        .execute()
    )

    return response.data


# =========================
# IMAGE UPLOAD
# =========================

def upload_image(
    file_path
):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    filename = (
        f"{uuid.uuid4()}"
        f"{extension}"
    )

    content_type = (
        _get_content_type(
            extension
        )
    )

    print()
    print("==============================")
    print("IMAGE UPLOAD")
    print("==============================")
    print("File:", file_path)
    print("Bucket:", "chat-images")
    print("Filename:", filename)
    print("Content type:", content_type)

    with open(
        file_path,
        "rb"
    ) as file:

        response = (
            supabase
            .storage
            .from_("chat-images")
            .upload(
                path=filename,
                file=file,
                file_options={
                    "content-type": content_type,
                    "upsert": "false"
                }
            )
        )

    print("Upload response:")
    print(response)

    image_url = (
        supabase
        .storage
        .from_("chat-images")
        .get_public_url(
            filename
        )
    )

    print("Public URL:")
    print(image_url)

    print("==============================")
    print()

    return image_url


def _get_content_type(
    extension
):

    types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }

    return types.get(
        extension,
        "application/octet-stream"
    )


# =========================
# REACTIONS
# =========================

def get_reactions(
    message_id
):

    response = (
        supabase
        .table("reactions")
        .select(
            "reaction, username"
        )
        .eq(
            "message_id",
            message_id
        )
        .execute()
    )

    reactions = {}

    for item in response.data:

        reaction = item["reaction"]

        if reaction not in reactions:

            reactions[reaction] = 0

        reactions[reaction] += 1

    return reactions


def add_reaction(
    message_id,
    username,
    reaction
):

    existing = (
        supabase
        .table("reactions")
        .select("id")
        .eq(
            "message_id",
            message_id
        )
        .eq(
            "username",
            username
        )
        .eq(
            "reaction",
            reaction
        )
        .execute()
    )

    # -------------------------
    # TOGGLE OFF
    # -------------------------

    if existing.data:

        reaction_id = (
            existing.data[0]["id"]
        )

        (
            supabase
            .table("reactions")
            .delete()
            .eq(
                "id",
                reaction_id
            )
            .execute()
        )

        return False

    # -------------------------
    # TOGGLE ON
    # -------------------------

    (
        supabase
        .table("reactions")
        .insert({
            "message_id": message_id,
            "username": username,
            "reaction": reaction
        })
        .execute()
    )

    return True