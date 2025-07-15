from models import VideoHash, User, DailyPerformance
import pickle, aiofiles
import videohash
from .utils import LOG

class VideoFile:

    @staticmethod
    async def save(from_user, download_video):
        filename = f"{from_user.username}_.mp4"
        LOG.info(f"User {from_user.username} has sent a video")
        async with aiofiles.open(f"./telegram/videos/{filename}", 'wb') as file:
            await file.write(download_video)
            LOG.info(f"The video has been saved to telegram/videos/{filename}")
        return filename

    @staticmethod
    async def is_uploaded(user, filename):
        video = videohash.VideoHash(path=f"./telegram/videos/{filename}")
        LOG.info("Hashed success!")
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
                LOG.info("New Video hash added to the database")
        except Exception as e:
            LOG.error(e)
        return resent



