from models.User import *
from models.VideoHash import VideoHash
from models.DailyPerformance import DailyPerformance
from models.CompleteReport import CompleteReport
from datetime import datetime
import sys, logging
import pickle, aiofiles
import videohash

logging.basicConfig(level=logging.INFO, filename="bot_logs.log", format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)
log.addHandler(console_handler)

class Database:

    @staticmethod
    def create_tables():
        if db.is_closed():
            db.connect()
        db.create_tables([User, VideoHash, DailyPerformance, CompleteReport])
        db.close()

    @staticmethod
    async def check_newuser(username, first_name):
        user, created = User.get_or_create(username=username, defaults={'name':first_name})
        if created:
            log.info("User not found in the database so it is created!")
        else:
            log.info("User is found in the database!")
        return user

    @staticmethod
    async def update_daily_performance(username, rips):

        date = datetime.now().date()
        user = User.get(username=username)
        log.info('User retrieved success')
        performance, created = DailyPerformance.get_or_create(user=user, date=date, defaults={'reps':rips})
        if created:
            log.info(f"User {username} not found for {date}. Creating a new record for the user")
        else:
            log.info(f"User {username} has been retrieved from database")
            user_reps = performance.reps+rips
            performance.reps = user_reps
            performance.save()
            log.info(f"User {username} data is updated to {user_reps} for {date}.")
        return performance.reps
