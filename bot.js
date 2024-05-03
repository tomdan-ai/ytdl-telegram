// require('dotenv').config();
// const TelegramBot = require('node-telegram-bot-api');
// const ytdl = require('ytdl-core');
// const fs = require('fs');

// // Telegram bot token
// const token = process.env.TELEGRAM_BOT_TOKEN;

// // Create a bot instance
// const bot = new TelegramBot(token, { polling: true });

// // Listen for messages
// bot.on('message', async (msg) => {
//     const chatId = msg.chat.id;
//     const text = msg.text;

//     if (text.includes('youtube.com') || text.includes('youtu.be')) {
//         try {
//             // Extract YouTube video ID from the URL
//             const videoId = ytdl.getURLVideoID(text);
            
//             // Get video info
//             const info = await ytdl.getInfo(videoId);
            
//             // Get the highest quality video format
//             const format = ytdl.chooseFormat(info.formats, { quality: 'highest' });

//             // Send a message indicating that the video is being downloaded
//             bot.sendMessage(chatId, 'Downloading video...');

//             // Download the video
//             const stream = ytdl.downloadFromInfo(info, { quality: format.itag });
            
//             // Generate a random file name
//             const fileName = `${Date.now()}.mp4`;
            
//             // Create a writable stream to save the video
//             const fileStream = fs.createWriteStream(fileName);

//             // Pipe the video stream to the file
//             stream.pipe(fileStream);

//             // When the download is complete
//             fileStream.on('finish', () => {
//                 // Send the video file to the user
//                 bot.sendVideo(chatId, fileName);
//             });

//             // If there's an error during download
//             fileStream.on('error', (err) => {
//                 // Notify the user
//                 bot.sendMessage(chatId, 'Error downloading the video.');
//                 console.error(err);
//             });
//         } catch (err) {
//             // If there's an error, notify the user
//             bot.sendMessage(chatId, 'Error downloading the video.');
//             console.error(err);
//         }
//     } else {
//         // If the message doesn't contain a YouTube link, ignore it
//         bot.sendMessage(chatId, 'Please provide a valid YouTube link.');
//     }
// });

require('dotenv').config();
const axios = require('axios');
const ytdl = require('ytdl-core');
const TelegramBot = require('node-telegram-bot-api');
const { SocksProxyAgent } = require('socks-proxy-agent');

// Telegram bot token
const token = process.env.TELEGRAM_BOT_TOKEN;

// Proxy details
const proxyHost = '192.168.178.200';
const proxyPort = 1080;

// Create a SOCKS5 proxy agent
const proxyUrl = `socks5://${proxyHost}:${proxyPort}`;
const proxyAgent = new SocksProxyAgent(proxyUrl);

// Create a bot instance
const bot = new TelegramBot(token, {
    polling: true,
    request: {
        agent: proxyAgent
    }
});

// Function to send message to Telegram
async function sendMessage(chatId, text) {
    try {
        await axios.post(`https://api.telegram.org/bot${token}/sendMessage`, {
            chat_id: chatId,
            text: text
        });
    } catch (err) {
        console.error('Error sending message:', err.response.data);
    }
}

// Function to send video to Telegram
async function sendVideo(chatId, stream) {
    try {
        await axios.post(`https://api.telegram.org/bot${token}/sendVideo`, {
            chat_id: chatId,
            video: stream
        });
    } catch (err) {
        console.error('Error sending video:', err.response.data);
    }
}

// Listen for messages
bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const text = msg.text;

    if (text.includes('youtube.com') || text.includes('youtu.be')) {
        try {
            // Extract YouTube video ID from the URL
            const videoId = ytdl.getURLVideoID(text);

            // Get video info
            const info = await ytdl.getInfo(videoId);

            // Get the highest quality video format
            const format = ytdl.chooseFormat(info.formats, { quality: 'highest' });

            // Send a message indicating that the video is being downloaded
            await sendMessage(chatId, 'Sending video...');

            // Get the video stream
            const stream = ytdl.downloadFromInfo(info, { quality: format.itag });

            // Send the video stream to the user
            await sendVideo(chatId, stream);
        } catch (err) {
            // If there's an error, notify the user
            await sendMessage(chatId, 'Error downloading the video.');
            console.error(err);
        }
    } else {
        // If the message doesn't contain a YouTube link, ignore it
        await sendMessage(chatId, 'Please provide a valid YouTube link.');
    }
});



