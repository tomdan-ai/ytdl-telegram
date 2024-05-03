import logging
import math
import os
import requests
from pytube import YouTube
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the upload service URL
UPLOAD_SERVICE_URL = 'https://t.me/uploadbot'  # Replace with the actual URL of your upload service

# Define a function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    logger.info(f"Received /start command from user {update.effective_user.username}")
    update.message.reply_text('Hi! Send me a YouTube video link, and I will download it for you.')

# Define a function to split and upload a video in parts
def split_and_upload_video(video_file, update, context):
    try:
        # Assuming a maximum upload size of 50MB (adjust as needed)
        max_upload_size = 50 * 1024 * 1024

        file_size = os.path.getsize(video_file)
        num_parts = math.ceil(file_size / max_upload_size)

        for part_idx in range(num_parts):
            start = part_idx * max_upload_size
            end = min(start + max_upload_size, file_size)
            with open(video_file, 'rb') as f:
                f.seek(start)
                part_data = f.read(end - start)

            files = {'file': part_data}
            response = requests.post(UPLOAD_SERVICE_URL, files=files)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            file_id = response.json().get('file_id')

            if file_id:
                # Send the file part to the user
                context.bot.send_document(chat_id=update.effective_chat.id, document=file_id)
                logger.info(f"Sent video part {part_idx + 1}/{num_parts} to user {update.effective_user.username}")
            else:
                logger.error("Received an invalid response from the upload service.")
                update.message.reply_text("Sorry, there was an error uploading the video.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error uploading video to the service: {e}")
        update.message.reply_text("Sorry, there was an error uploading the video.")

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
            video_file = video.download()
            logger.info(f"Download complete: {yt.title}")

            # Split and upload the video in parts
            split_and_upload_video(video_file, update, context)

            os.remove(video_file)
            logger.info(f"Removed downloaded file: {video_file}")
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
