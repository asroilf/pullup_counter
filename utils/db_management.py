from models.models import *
import logging
import os, sys
from datetime import datetime
import pickle
import videohash

logging.basicConfig(level=logging.INFO, filename="bot_logs.log", format="%(asctime)s - %(levelname)s - %(message)s")

log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stdout) 
console_handler.setLevel(logging.INFO) 
console_formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s') 
console_handler.setFormatter(console_formatter)

log.addHandler(console_handler)

async def check_newuser(username, first_name):
    user, created = User.get_or_create(username=username, defaults={'name':first_name})
    if created:
        log.info("User not found in the database so it is created!")
    else:
        log.info("User is found in the database!")
    return user


async def update_daily_performance(username, rips):
    date = datetime.now().date()

    user = User.get(username=username)
    log.info('User retrieved success')
    performance, created = DailyPerformance.get_or_create(user=user, date=date, defaults={'reps':rips})
    if created:
        log.info(f"User {username} not found for {date}. Creating a new row for the user")
    else:

        log.info(f"User {username} has been retrieved from database")
        user_reps = performance.reps+rips
        performance.reps = user_reps
    
        performance.save()
        log.info(f"User {username} data is updated to {user_reps} for {date}.")
    return performance.reps


async def is_uploaded(user, filename):
    video = videohash.VideoHash(path=f"./telegram/{filename}")
    log.info("Hashed success!")
    resent=False
    try:
        hashes = VideoHash.select().where(VideoHash.user==user)
        for i in hashes:
            unpickle = pickle.loads(i.video_hash)
            if  video.is_similar(unpickle):
                resent = True
                
        if not resent:
            pickled = pickle.dumps(video)
            VideoHash.create(user=user, video_hash=pickled)
            log.info("New Video hash added to the database")
    except Exception as e:
        log.error(e)
    return resent


