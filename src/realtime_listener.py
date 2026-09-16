import asyncio
import threading

from supabase import acreate_client

from config import (
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==========================================================
# REALTIME LISTENER
# ==========================================================

async def listen_for_changes(
    message_callback,
    reaction_callback
):

    supabase = await acreate_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    channel = supabase.channel(
        "messaging-app-realtime"
    )

    # ======================================================
    # MESSAGE INSERTS
    # ======================================================

    def handle_message(payload):

        print()
        print("==============================")
        print("REALTIME MESSAGE EVENT")
        print("==============================")
        print(payload)
        print("==============================")
        print()

        data = payload.get(
            "data",
            {}
        )

        record = data.get(
            "record"
        )

        if record:

            message_callback(
                record
            )

    channel.on_postgres_changes(
        event="INSERT",
        schema="public",
        table="messages",
        callback=handle_message
    )

    # ======================================================
    # REACTION CHANGES
    # ======================================================

    def handle_reaction(payload):

        print()
        print("==============================")
        print("REALTIME REACTION EVENT")
        print("==============================")
        print(payload)
        print("==============================")
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

        reaction_callback(
            record,
            old_record,
            data.get("type")
        )

    # INSERT
    channel.on_postgres_changes(
        event="INSERT",
        schema="public",
        table="reactions",
        callback=handle_reaction
    )

    # DELETE
    channel.on_postgres_changes(
        event="DELETE",
        schema="public",
        table="reactions",
        callback=handle_reaction
    )

    # ======================================================
    # SUBSCRIBE
    # ======================================================

    await channel.subscribe()

    print(
        "Realtime listener connected."
    )

    # ======================================================
    # KEEP ALIVE
    # ======================================================

    while True:

        await asyncio.sleep(
            1
        )


# ==========================================================
# START LISTENER
# ==========================================================

def start_realtime_listener(
    message_callback,
    reaction_callback
):

    def run():

        try:

            asyncio.run(
                listen_for_changes(
                    message_callback,
                    reaction_callback
                )
            )

        except Exception as error:

            print()
            print("==============================")
            print("REALTIME LISTENER ERROR")
            print("==============================")
            print(error)
            print("==============================")
            print()

    thread = threading.Thread(
        target=run,
        daemon=True
    )

    thread.start()