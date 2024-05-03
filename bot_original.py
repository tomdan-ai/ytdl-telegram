import logging
import os
from pytube import YouTube
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    logger.info(f"Received /start command from user {update.effective_user.username}")
    update.message.reply_text('Hi! Send me a YouTube video link, and I will download it for you.')

# Define a function to handle YouTube video links
def download_video(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text
    logger.info(f"Received video link: {video_url} from user {update.effective_user.username}")

    try:
        yt = YouTube(video_url)
        logger.info(f"Fetching video information for {yt.title}")
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

        if video:
            logger.info(f"Downloading video: {yt.title}")
            video.download()
            logger.info(f"Download complete: {yt.title}")

            with open(video.default_filename, 'rb') as video_file:
                context.bot.send_video(chat_id=update.effective_chat.id, video=video_file)
                logger.info(f"Sent video {yt.title} to user {update.effective_user.username}")

            os.remove(video.default_filename)
            logger.info(f"Removed downloaded file: {video.default_filename}")
        else:
            logger.error("Could not find a video stream to download.")
            update.message.reply_text("Sorry, I couldn't find a video stream to download.")

    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        update.message.reply_text("Sorry, there was an error downloading the video.")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it the bot's token.
    updater = Updater("BOT_TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))

    # Add handler for video links
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    # Start the bot
    logger.info("Starting the YouTube Video Downloader Bot...")
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
