import asyncio
import threading

from supabase import acreate_client

from config import SUPABASE_URL, SUPABASE_KEY


async def listen_for_messages(callback):

    supabase = await acreate_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    channel = supabase.channel(
        "messages-realtime"
    )

    def handle_message(payload):

        print()
        print("REALTIME EVENT RECEIVED")
        print(payload)
        print("=================================")
        print()

        data = payload.get("data", {})
        record = data.get("record")

        if record:
            callback(record)

    channel.on_postgres_changes(
        event="INSERT",
        schema="public",
        table="messages",
        callback=handle_message
    )

    await channel.subscribe()

    print("Realtime listener connected.")

    while True:
        await asyncio.sleep(1)


def start_realtime_listener(callback):

    def run():

        asyncio.run(
            listen_for_messages(callback)
        )

    thread = threading.Thread(
        target=run,
        daemon=True
    )

    thread.start()