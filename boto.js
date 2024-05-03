const TelegramBot = require('node-telegram-bot-api');
const ytdl = require('ytdl-core');

// Replace YOUR_BOT_TOKEN with your actual Telegram bot token
const token = 'BOT_TOKEN';
const bot = new TelegramBot(token, { polling: true });

// Define a function to handle the /download command
bot.onText(/\/download (.+)/, async (msg, match) => {
  const chatId = msg.chat.id;
  const videoUrl = match[1];

  try {
    // Use ytdl-core to get the video metadata
    const info = await ytdl.getInfo(videoUrl);
    const videoTitle = info.videoDetails.title;
    const videoFormat = ytdl.chooseFormat(info.formats, { quality: 'highest' });
    console.log(videoFormat)

    // Send a message to the user indicating that the download has started
    await bot.sendMessage(chatId, `Downloading "${videoTitle}"...`);

    // Download the video and send it to the user's DM
    const stream = ytdl.downloadFromInfo(info, { format: videoFormat });
    stream.on('error', (err) => {
      console.error('Error downloading video:', err);
      bot.sendMessage(chatId, 'An error occurred while downloading the video.');
    });
    bot.sendVideo(chatId, stream, {}, { caption: videoTitle });

  } catch (err) {
    console.error('Error:', err);
    bot.sendMessage(chatId, 'An error occurred while processing the video.');
  }
});

console.log('Bot started...');
