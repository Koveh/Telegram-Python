import asyncio
import sqlite3
from telegram import Bot
from create_image import create_image
import schedule
import time
import pytz
from datetime import datetime

bot_token = 'Telegram_token'
channel_id = '@Name_of_telegram_channel'
bot = Bot(token=bot_token)

async def send_message():
    # Connect to the SQLite database
    conn = sqlite3.connect('financial_terms.db')
    cursor = conn.cursor()

    # Define a SQL query to fetch the title and description
    query = "SELECT title, description FROM terms WHERE used = 0 LIMIT 1"

    # Execute the query
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()

    # Check if result is not empty
    if result:
        title, description = result
        print("Title:", title)
        print("Description:", description)

        create_image(title=title, description=description)
        
        with open(title + ".png", 'rb') as image_file:
            await bot.send_photo(chat_id=channel_id, photo=image_file, caption=f"*{title}*", parse_mode='Markdown')

        # Construct the message
        #message_text = f"*{title}*\n{description}"
        # Send a message to the channel
        #await bot.send_message(chat_id=channel_id, text=message_text, parse_mode='Markdown')

        # Mark the term as used in the database (if needed)
        cursor.execute("UPDATE terms SET used = 1 WHERE title = ?", (title,))
        conn.commit()
    else:
        print("No unused terms found in the database.")

    # Close the connection
    conn.close()

# Run the async function
#asyncio.run(send_message())

def job():
    # Convert current time to Central European Time (CET)
    cet = pytz.timezone('CET')
    now_cet = datetime.now(cet)
    print("Running the job at", now_cet)
    asyncio.run(send_message())

def run_daily_job():
    # Schedule the job to run daily at 11:00 AM CET
    schedule.every().day.at("11:00").do(job)

    # Keep running the script
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler
run_daily_job()