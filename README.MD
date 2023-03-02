## YouTube MP3 Downloader Bot

![Tg bot](https://github.com/ls500pymaster/ls500pymaster/blob/main/assets/tg_bot.jpg?raw=true "Tg bot")


This is a Telegram bot that can convert YouTube videos to MP3 audio files and send them to you as audio messages.

### Getting Started

To use this bot, simply start a chat with it on Telegram (@i_want_mp3_bot) and send a YouTube video link. The bot will respond with details about the video and a "Download" button. Press the button to receive the audio message.

### Prerequisites 

To run this bot locally, you will need:

- Python 3.7 or higher
- pip package manager
- ffmpeg library

You can install ffmpeg on Ubuntu or Debian using the following command:

    pip install ffmpeg

### Installing
Clone this repository to your local machine.
Install the required Python packages using the following command:

    pip install -r requirements.txt
    
Create a config.py file in the root directory and add the following line:

    BOT_TOKEN = 'your_bot_token'
    
Replace your_bot_token with your Telegram Bot API token.

### Running the bot
To start the bot, run the following command in the root directory:
    python bot.py
    

### Built With
- aiogram - A Python framework for Telegram Bot API.
- moviepy - A Python module for video editing.
- pytube - A Python library for downloading YouTube videos.

### Author
[ls500pymaster](https://github.com/ls500pymaster "ls500pymaster")