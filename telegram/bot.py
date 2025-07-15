import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from service import PullupCounter
from service import Database, VideoFile
from service import Report 
from models import CompleteReport
from service import LOG

token = os.getenv("PULLUPS_BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")      # For groupchats
thread_id = os.getenv("THREAD_ID")  # For groups with topics enabled
LOG.info(f"Bot is up and running!")
Database.create_tables()
BOT = AsyncTeleBot(token)

@BOT.message_handler(commands=['start', 'hello'])
async def send_hello(message):
    await BOT.reply_to(message, "Hello, welcome to Pull-ups counter bot!")
    await BOT.send_message("To use this bot just upload the video of your pull-ups and it will count the number of reps in the video.")
    await BOT.send_message("Rules of using this bot is simple! Send a video of doing pull ups and it will give number of pull-ups in the video back to you. The bot will not recognize any message other than a video file.")

@BOT.message_handler(content_types = ['video'])
async def receive_video(message):
    from_user = message.from_user
    user = await Database.check_newuser(from_user.username, from_user.first_name)

    try:
        file_info = await BOT.get_file(message.video.file_id)
        download_video = await BOT.download_file(file_info.file_path)

        filename=await VideoFile.save(from_user, download_video)
        resent = False #await VideoFile.is_uploaded(user, filename)

        if resent:
            await BOT.reply_to(message, "You have sent the same video more than once!")
            LOG.info("User sent the same video twice")
        else:
            await BOT.reply_to(message, f"Your video has been received!")
            total_reps = PullupCounter.count_reps(filename)

            LOG.info(f"MediaPipe has returned {total_reps}")
            total_today = await Database.update_daily_performance(from_user.username, total_reps)
            if total_today<20:
                await BOT.reply_to(message, f"Good job, @{from_user.username}! You did {total_reps} pull-ups in the video and {total_today} overall for today. It is not 20 though)). Keep pulling, you’ve got this!")
            else:
                await BOT.reply_to(message, f"Awesome work, @{from_user.username}! 💪 You did {total_today} in total today and hit your daily target of 20 pull-ups. Keep up the great progress!")

            LOG.info(f"Message is sent to the user")
    except Exception as e:
        LOG.error(str(e))
        er = "A request to the Telegram API was unsuccessful. Error code: 400. Description: Bad Request: file is too big"
        if er == str(e):
            await BOT.reply_to(message, "The video shouldn't be more than 20MB and your video exceeds the limit!")


async def send_periodic_report():
    LOG.info("reached the periodic report function")
    try:
        report = await Report.get_complete_report()
        message = CompleteReport.select().first()
        await BOT.delete_message(chat_id=chat_id, message_id=message.message_id)
        message.delete_instance()

        sent = await BOT.send_message(chat_id=chat_id, text=report, parse_mode='HTML', message_thread_id=thread_id)
        CompleteReport.create(message_id=sent.message_id, message=report)
    except Exception as e:
        LOG.error(e)

        sent = await BOT.send_message(chat_id=chat_id, text=report, parse_mode='HTML', message_thread_id=thread_id)
        CompleteReport.create(message_id=sent.message_id, message=report)
        
    LOG.info("Daily report sent!")

