from models import VideoHash
from models import User, db
from models.User import db
from models import DailyPerformance
from models import CompleteReport
import sys, logging
from datetime import datetime
import pickle, aiofiles
import videohash

logging.basicConfig(level=logging.INFO, filename="bot_logs.log", format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)
log.addHandler(console_handler)

class VideoFile:

    @staticmethod
    async def save(from_user, download_video):
        filename = f"{from_user.username}_.mp4"
        log.info(f"User {from_user.username} has sent a video")
        async with aiofiles.open(f"./telegram/videos/{filename}", 'wb') as file:
            await file.write(download_video)
            log.info(f"The video has been saved to telegram/videos/{filename}")
        return filename

    @staticmethod
    async def is_uploaded(user, filename):
        video = videohash.VideoHash(path=f"./telegram/videos/{filename}")
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



