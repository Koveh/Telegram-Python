import json
import asyncio
import datetime
import time
import random
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler


api_id = ''
api_hash = ''

app = Client("my_account", api_id=api_id, api_hash=api_hash)


# Function to load friends from JSON file
def load_friends():
    try:
        with open("friends.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to save friends to JSON file
def save_friends(friends):
    with open("friends.json", "w") as file:
        json.dump(friends, file)

friends = load_friends()

async def add_friend(client, message):
    try:
        name, username, lang_or_text, date = message.text.split()[1:]
        friends.append([name, username, lang_or_text, date])
        save_friends(friends)
        await message.reply(f"Added {name} ({username}) to the list with the following message and date: {lang_or_text}, {date}")
        await print_friends_list()
    except ValueError:
        await message.reply("Invalid format. Please use the following format: /add name username lang_or_text date")

async def remove_friend(client, message):
    try:
        username = message.text.split()[1]
        for friend in friends:
            if friend[1] == username:
                friends.remove(friend)
                save_friends(friends)
                await message.reply(f"Removed {friend[0]} ({username}) from the list.")
                break
        else:
            await message.reply(f"Username {username} not found in the list.")
    except ValueError:
        await message.reply("Invalid format. Please use the following format: /remove username")

friends = load_friends()

async def send_birthday_message(friend):
    name, chat_id, lang, bday = friend
    message = ""

    if lang == "ru":
        message = f"{name}, с днем рождения!!!"
    elif lang == "en":
        message = f"{name}, happy birthday!!! Wish you the best!!!"
    else:
        message = lang

    try:
        await app.send_message(chat_id, message)
        print(f"Message sent to {name} ({chat_id}): {message}")
    except FloodWait as e:
        print(f"Flood wait for {e.x} seconds")
        time.sleep(e.x)
        await send_birthday_message(friend)

async def print_friends_list():
    me = await app.get_me()
    message = "Friends and their birthdays:\n\n/add name @username text date.\n/add Максим @maximk ru 05.09\n ru is - Максим, с днем рождения!, en - Maxim, happy birthday! \n\n"
    for friend in friends:
        message += f"{friend[0]} ({friend[1]}): {friend[3]}\n"
    await app.send_message(me.id, message)

async def check_birthdays():
    current_date = datetime.datetime.now().strftime("%d.%m")
    for friend in friends:
        if friend[3] == current_date:
            random_time = random.randint(9 * 3600, 11 * 3600)  # Random time in seconds between 9 AM and 11 AM
            await asyncio.sleep(random_time)
            await send_birthday_message(friend)

async def list_friends(client, message):
    await print_friends_list()

async def main():
    async with app:
        app.add_handler(MessageHandler(add_friend, filters.command(["add"]) & filters.me))
        app.add_handler(MessageHandler(remove_friend, filters.command(["remove"]) & filters.me))
        app.add_handler(MessageHandler(list_friends, filters.command(["list"]) & filters.me))
        await print_friends_list()

        while True:
            await check_birthdays()
            await asyncio.sleep(60 * 60 * 24)  # Check birthdays every 24 hours
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
