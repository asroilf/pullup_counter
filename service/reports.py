from models.models import *
from datetime import datetime
from .utils import log

class Report:

    @staticmethod
    async def _get_today(date):
        user = {}
        users = User.select()
        todays_pullups = DailyPerformance.select().where(DailyPerformance.date==date)

        for i in users:
            user[i.username]=0
            for j in todays_pullups:
                if i == j.user:
                    user[i.username]+=j.reps
            if user[i.username] == 0:
                try:
                    DailyPerformance.create(user=i, reps=0, date=date)
                except Exception as e:
                    log.error(e)
        return user

    @staticmethod
    async def _get_user_report(user):
        user = User.get_or_none(User.username==user)
        u = DailyPerformance.select().where(DailyPerformance.user==user).order_by(DailyPerformance.date)
        result=""
        day=1
        skipped=0
        for i in u:
            if i.reps != 0:
                result += f"Day {day} ({i.date}): {i.reps}\n"
            else:
                result += f"Day {day} ({i.date}): Skipped\n"
                skipped+=1
            day+=1

        return [day-1, skipped, result]

    @staticmethod
    async def get_complete_report():
        current_datetime = datetime.now() 
        time = str(current_datetime.time())
        date = str(current_datetime.date())

        users = await Report._get_today(date)
        complete_report = DailyPerformance.select(
                DailyPerformance.user, 
                fn.SUM(DailyPerformance.reps)
                ).group_by(
                        DailyPerformance.user
                        ).order_by(
                                DailyPerformance.reps.desc())

        format = f"<b> Report </b>\n<b>Date:</b> {date}\n\n"
        format+="Top Ninjas:\n------------------------------------------------\n"
        places=1
        for i in complete_report:
            if places==1:
                format += f" 🥇#{i.user.username}\n"
            elif places==2:
                format += f" 🥈#{i.user.username}\n"
            elif places==3:
                format += f" 🥉#{i.user.username}\n"
            else:
                format += f"  #{i.user.username}\n"
            places+=1
            days, skipped, daily = await Report._get_user_report(i.user.username)
            for j in daily:
                format+=j
            format+=f"\n <b>Summary</b> : Workout days: {days-skipped} | Skipped days: {skipped} | Total reps: { i.reps }\n"
            format+="-----------------------------------------\n"
        log.info("Complete Report for users created!")
        return format
