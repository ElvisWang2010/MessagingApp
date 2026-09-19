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

    print()
    print("==============================")
    print("STARTING REALTIME LISTENER")
    print("==============================")

    try:

        # -------------------------
        # CREATE ASYNC CLIENT
        # -------------------------

        supabase = await acreate_client(
            SUPABASE_URL,
            SUPABASE_KEY
        )

        print("Supabase async client created.")

        # -------------------------
        # CREATE CHANNEL
        # -------------------------

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
            print("==============================")
            print("REALTIME MESSAGE EVENT")
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
        # REACTION EVENTS
        # =========================

        def handle_reaction(
            payload
        ):

            print()
            print("==============================")
            print("REALTIME REACTION EVENT")
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
        # SUBSCRIBE
        # =========================

        print("Subscribing to Supabase Realtime...")

        response = await channel.subscribe()

        print()
        print("Realtime subscription response:")
        print(response)
        print()

        print("==============================")
        print("REALTIME LISTENER CONNECTED")
        print("==============================")
        print()

        # =========================
        # KEEP REALTIME RUNNING
        # =========================

        await supabase.realtime.listen()

    except Exception as error:

        print()
        print("==============================")
        print("REALTIME LISTENER ERROR")
        print("==============================")
        print(error)
        print("==============================")
        print()

        raise


# =========================
# THREAD
# =========================

def start_realtime_listener(
    callback
):

    def run():

        try:

            asyncio.run(
                listen_for_messages(
                    callback
                )
            )

        except Exception as error:

            print()
            print("==============================")
            print("REALTIME THREAD ERROR")
            print("==============================")
            print(error)
            print("==============================")
            print()

    thread = threading.Thread(
        target=run,
        daemon=True
    )

    thread.start()
