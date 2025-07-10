import os, sys, threading, time
import schedule
from telebot.async_telebot import AsyncTeleBot, types
from datetime import datetime, timedelta
from dotenv import load_dotenv
import asyncio, aiofiles
from utils.pullup_counter import count_reps
from utils.db_management import check_newuser, update_daily_performance, log, is_uploaded
from utils.reports import daily_report, user_report, complete_report
from models.models import *
load_dotenv()

token = os.getenv("PULLUPS_BOT_TOKEN")
log.info(f"Bot is up and running!")
bot = AsyncTeleBot(token)

@bot.message_handler(command=['start', 'hello'])
async def send_hello(message):
    await bot.reply_to(message, "Hello, welcome to Pull-ups counter bot!")
    await bot.send_message("To use this bot just upload the video of your pull-ups and it will count the number of reps in the video.")

@bot.message_handler(content_types = ['video'])
async def receive_video(message):
    from_user = message.from_user
    user = await check_newuser(from_user.username, from_user.first_name)
    try:
        file_info = await  bot.get_file(message.video.file_id)
        download_video = await bot.download_file(file_info.file_path)

        filename = f"{from_user.username}_.mp4"
        log.info(f"User {from_user.username} has sent a video")
        async with aiofiles.open(f"./telegram/{filename}", 'wb') as file:
            await file.write(download_video)
            log.info(f"The video has been saved to telegram/{filename}")
        resent = await is_uploaded(user, filename)

        if resent:
            await bot.reply_to(message, "You have sent the same video more than once!")
            log.info("User sent the same video twice")
        else:
            await bot.reply_to(message, f"Your video has been received!")
            total_reps = await count_reps(filename)

            log.info(f"MediaPipe has returned {total_reps}")
            total_today = await update_daily_performance(from_user.username, total_reps)
            if total_today<20:
                await bot.reply_to(message, f"Good job, @{from_user.username}! You did {total_reps} pull-ups in the video and {total_today} overall for today. It is not 20 though)). Keep pulling, you’ve got this!")
            else:
                await bot.reply_to(message, f"Awesome work, @{from_user.username}! 💪 You did {total_today} in total today and hit your daily target of 20 pull-ups. Keep up the great progress!")

            log.info(f"Message is sent to the user")
    except Exception as e:
        log.error(str(e))
        er = "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: file is too big"
        if er == str(e):
            await bot.reply_to(message, "The video shouldn't be more than 20MB and your video exceeds the limit!")


async def periodic_report():
    report = complete_report()
    try:
        message = CompleteReport.select().first()
        await bot.delete_message(chat_id='-1002500779625_659', message_id=message.message_id)
        message.delete_instance()

        sent = await bot.send_message(chat_id='-1002500779625_659', text=report, parse_mode='HTML', message_thread_id=659)
        CompleteReport.create(message_id=sent.message_id, message=report)
    except Exception as e:
        log.error(e)

        sent = await bot.send_message(chat_id='-1002500779625_659', text=report, parse_mode='HTML', message_thread_id=659)
        CompleteReport.create(message_id=sent.message_id, message=report)
        
    log.info("Daily report sent!")

event_loop = None


def async_wrapper():
    if event_loop and event_loop.is_running():
        event_loop.call_soon_threadsafe(asyncio.create_task, periodic_report())


schedule.every().day.at("16:56").do(async_wrapper)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


async def main():
    global event_loop
    event_loop = asyncio.get_running_loop()
    threading.Thread(target=run_schedule, daemon=True).start()
    await bot.infinity_polling()

if __name__=='__main__':
    asyncio.run(main())
