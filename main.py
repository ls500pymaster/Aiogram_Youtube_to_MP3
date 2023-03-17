import datetime
import os
import re

from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import BoundFilter
from aiogram.utils import executor
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip
from pytube import YouTube
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("/start"))
keyboard.add(KeyboardButton("/help"))


load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def cmd_answer(message: types.Message):
	await message.answer(
		'<b>👋 Hello, I am Youtube mp3 downloader.</b> \n <b>▶️ Send me link on youtube video.</b>',
		parse_mode='HTML')


@dp.message_handler(commands=["menu"])
async def cmd_answer(message: types.Message):
	chat_id = message.chat.id
	text = "Hello! Choose actions:"
	await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)


@dp.message_handler(commands=["help"])
async def cmd_answer(message: types.Message):
	await message.answer(
		"⁉🆘 <b> Do you need support?</b> \n✉️ <b>Contact me</b> <a href='https://t.me/Alexexalex'>@Alexexalex/a><b>.</b>",
		disable_web_page_preview=True, parse_mode="HTML")


class YoutubeLinkFilter(BoundFilter):
	check_link = "is_youtube_link"

	def __init__(self, is_youtube_link):
		self.is_youtube_link = is_youtube_link

	async def check(self, message: types.Message):
		if self.is_youtube_link:
			return re.search(r'(?:youtube\.com\/|youtu.be\/)(?:watch\?v=)?([^\s]+)', message.text) is not None
		return True


@dp.message_handler(YoutubeLinkFilter(is_youtube_link=True))
async def cmd_answer(message: types.Message):
	url = message.text
	yt = YouTube(url)
	title = yt.title
	author = yt.author
	channel = yt.channel_url
	resolution = yt.streams.get_highest_resolution().resolution
	file_size = yt.streams.get_highest_resolution().filesize
	length = yt.length
	date_published = yt.publish_date.strftime("%Y-%m-%d")
	views = yt.views
	picture = yt.thumbnail_url

	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton(text="Download", callback_data="download"))
	await message.answer_photo(f'{picture}', caption=f"▶️ <b>{title}</b> <a href='{url}'>→</a> \n"
		                                                f"👤 <b>{author}</b> <a href='{channel}'>→</a> \n"
		                                                f"⚙️ <b>Resolution —</b> <code>{resolution}</code> \n"
		                                                f"🗂 <b>Size —</b> <code>{round(file_size * 0.000001, 2)}MB</code> \n"
		                                                f"⌚ <b>Duration —</b> <code>{str(datetime.timedelta(seconds=length))}</code> \n"
		                                                f"🗓 <b>Date published —</b> <code>{date_published}</code> \n"
		                                                f"👁 <b>Views —</b> <code>{views:,}</code> \n",
		                                            parse_mode='HTML', reply_markup=keyboard)



async def send_mp3(bot, chat_id, mp4_path, yt):
	# convert mp4 to mp3
	mp3_path = os.path.splitext(mp4_path)[0] + '.mp3'
	AudioFileClip(mp4_path).write_audiofile(mp3_path)
	title = yt.title
	author = yt.author
	file_size = os.path.getsize(mp3_path)
	file_size_mb = round(file_size / (1024 * 1024), 2)
	# send as audio message
	with open(mp3_path, 'rb') as audio:
		await bot.send_audio(chat_id, audio, caption=f"📹 <b>{title}</b> \n"
		                                                       f"👤 <b>{author}</b> \n"
		                                                       f"🗂 <b>Size —</b> <code>{file_size_mb}Mb</code>\n"
		                                                       f"ℹ️ <b>Downloaded with @i_want_mp3_bot</b>",
		                                                        parse_mode='HTML')
	if os.path.exists(mp4_path):
		os.remove(mp4_path)
	if os.path.exists(mp3_path):
		os.remove(mp3_path)


@dp.callback_query_handler(text="download")
async def button_download(call: types.CallbackQuery):
	url = call.message.html_text
	yt = YouTube(url)
	title = yt.title
	clean_title = re.sub(r'[^\w\s\[\]]', " ", title)
	author = yt.author
	resolution = yt.streams.get_highest_resolution().resolution
	stream = yt.streams.filter(progressive=True, file_extension="mp4")
	mp4_path = stream.get_lowest_resolution().download(f'{call.message.chat.id}', f'{clean_title}')
	print(mp4_path)
	print(yt)
	await send_mp3(bot, call.message.chat.id, mp4_path, yt)

if __name__ == '__main__':
	executor.start_polling(dp)