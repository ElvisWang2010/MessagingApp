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
    # MESSAGE EVENTS
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

        old_record = data.get(
            "old_record"
        )

        event_type = data.get(
            "type"
        )

        # -------------------------
        # INSERT
        # -------------------------

        if (
            event_type
            and str(event_type).upper()
            == "INSERT"
        ):

            if record:

                callback(
                    "message",
                    {
                        "action": "INSERT",
                        "record": record
                    }
                )

        # -------------------------
        # DELETE
        # -------------------------

        elif (
            event_type
            and str(event_type).upper()
            == "DELETE"
        ):

            callback(
                "message",
                {
                    "action": "DELETE",
                    "record": old_record or record
                }
            )

    channel.on_postgres_changes(
        event="*",
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

        event_type = data.get(
            "type"
        )

        callback(
            "reaction",
            {
                "record": record,
                "old_record": old_record,
                "action": str(
                    event_type
                ).upper()
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