from models import User, Video, DailyPerformance, Report
from datetime import datetime
from .logger import LOG
from .db import DB

class Database:

    @staticmethod
    def create_tables():
        if DB.is_closed():
            DB.connect()
        DB.create_tables([User, Video, DailyPerformance, Report])
        DB.close()

    @staticmethod
    async def check_newuser(username, first_name):
        user, created = User.get_or_create(username=username, defaults={'name':first_name})
        if created:
            LOG.info("User not found in the database so it is created!")
        else:
            LOG.info("User is found in the database!")
        return user

    @staticmethod
    async def update_daily_performance(username, rips):

        date = datetime.now().date()
        user = User.get(username=username)
        LOG.info('User retrieved success')
        performance, created = DailyPerformance.get_or_create(user=user, date=date, defaults={'reps':rips})
        if created:
            LOG.info(f"User {username} not found for {date}. Creating a new record for the user")
        else:
            LOG.info(f"User {username} has been retrieved from database")
            user_reps = performance.reps+rips
            performance.reps = user_reps
            performance.save()
            LOG.info(f"User {username} data is updated to {user_reps} for {date}.")
        return performance.reps

