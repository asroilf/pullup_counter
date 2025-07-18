import threading, time
import schedule, asyncio
from telegram import BOT, send_periodic_report
from service import LOG

event_loop = None

def async_wrapper():
    if event_loop and event_loop.is_running():
        event_loop.call_soon_threadsafe(asyncio.create_task, send_periodic_report())


schedule.every().day.at("23:30").do(async_wrapper)

def run_schedule():
    LOG.info("run_schedule thread started")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(e)


async def main():
    global event_loop
    event_loop = asyncio.get_running_loop()
    threading.Thread(target=run_schedule, daemon=True).start()
    await BOT.infinity_polling()

if __name__=='__main__':
    asyncio.run(main())

