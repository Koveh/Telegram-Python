import time
import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait

api_id = ''
api_hash = ''

app = Client("my_account", api_id=api_id, api_hash=api_hash)

async def main():
    async with app:
        try:
            await app.send_message("@k_maxim_d", "hello!")
            print("Message sent!")
        except FloodWait as e:
            print(f"Flood wait for {e.x} seconds")
            time.sleep(e.x)
            await main()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())