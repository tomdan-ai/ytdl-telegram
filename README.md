
# YouTube Video Downloader Bot

This Telegram bot allows users to download YouTube videos by simply sending the video link. The bot will fetch the video and send it back to the user.

### How to Create Your Telegram Bot Token

- Open Telegram and search for the "BotFather" user.
- Start a chat with BotFather and use the command /newbot to create a new bot.
- Follow the instructions to set a name and username for your bot.
- Once your bot is created, BotFather will provide you with a token. Save this token as you'll need it to run the bot.

### Setting Up and Using the Bot Locally

- Clone or download the repository containing the bot code.
- Make sure you have Python installed on your system.
- Install the required Python packages using pip install -r requirements.txt.
- Set up environment variables:
  - Create a .env file in the project directory.
  -Inside the .env file, add BOT_TOKEN=your_bot_token, replacing your_bot_token with the token provided by BotFather.
- Run the bot using python bot.py.
- Start a chat with your bot in Telegram and send a YouTube video link.
- The bot will download the video and send it back to you.
Note:

#### The bot works for videos whose highest qualities are lower than 50MB due to Telegram's file size limitation.
#### Make sure your system has an active internet connection for the bot to download and upload videos.
