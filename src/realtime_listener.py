import asyncio
import threading

from supabase import acreate_client

from config import (
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================
# LISTENER
# =========================

async def listen_for_messages(
    callback
):

    supabase = await acreate_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    channel = supabase.channel(
        "chat-realtime"
    )

    # =========================
    # MESSAGES
    # =========================

    def handle_message(
        payload
    ):

        print()
        print("REALTIME MESSAGE EVENT")
        print(payload)
        print("=================================")
        print()

        data = payload.get(
            "data",
            {}
        )

        record = data.get(
            "record"
        )

        if record:

            callback(
                "message",
                record
            )

    channel.on_postgres_changes(
        event="INSERT",
        schema="public",
        table="messages",
        callback=handle_message
    )

    # =========================
    # REACTIONS
    # =========================

    def handle_reaction(
        payload
    ):

        print()
        print("REALTIME REACTION EVENT")
        print(payload)
        print("=================================")
        print()

        data = payload.get(
            "data",
            {}
        )

        record = data.get(
            "record"
        )

        old_record = data.get(
            "old_record"
        )

        callback(
            "reaction",
            {
                "record": record,
                "old_record": old_record,
                "event": data.get(
                    "type"
                )
            }
        )

    channel.on_postgres_changes(
        event="*",
        schema="public",
        table="reactions",
        callback=handle_reaction
    )

    # =========================
    # CONNECT
    # =========================

    await channel.subscribe()

    print(
        "Realtime listener connected."
    )

    # =========================
    # KEEP ALIVE
    # =========================

    while True:

        await asyncio.sleep(
            1
        )


# =========================
# THREAD
# =========================

def start_realtime_listener(
    callback
):

    def run():

        asyncio.run(
            listen_for_messages(
                callback
            )
        )

    thread = threading.Thread(
        target=run,
        daemon=True
    )

    thread.start()  