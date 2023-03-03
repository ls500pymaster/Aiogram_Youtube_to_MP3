import datetime
import os

from aiogram import Bot
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from moviepy.editor import AudioFileClip
from pytube import YouTube

import config

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_answer(message: types.Message):
	await message.answer(
		'<b>👋 Hello, I am Youtube mp3 downloader.</b> \n <b>▶️ Send me link on youtube video.</b>',
		parse_mode='HTML')


@dp.message_handler(commands=["help"])
async def cmd_answer(message: types.Message):
	await message.answer(
		"⁉🆘 <b> Do you need support?</b> \n✉️ <b>Contact me</b> <a href='https://t.me/Alexexalex'>@Alexexalex/a><b>.</b>",
		disable_web_page_preview=True, parse_mode="HTML")


@dp.message_handler()
async def cmd_answer(message: types.Message):
	if message.text.startswith('https://youtube.be/') or message.text.startswith(
			'https://www.youtube.com/') or message.text.startswith('https://youtu.be/'):
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
	else:
		await message.answer(f"❗️<b>Wrong url.</b>", parse_mode='HTML')


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
		                                                       f"👤 <b>{author}</b> \n\n"
		                                                       f"🗂 <b>Size —</b> <code>{file_size_mb}Mb</code> \n"
		                                                       f"ℹ️ <b>Downloaded with @i_want_mp3_bot</b>",
		               parse_mode='HTML')

	# cleanup
	if os.path.exists(mp4_path):
		os.remove(mp4_path)
	if os.path.exists(mp3_path):
		os.remove(mp3_path)


@dp.callback_query_handler(text="download")
async def button_download(call: types.CallbackQuery):
	url = call.message.html_text
	yt = YouTube(url)
	title = yt.title
	author = yt.author
	resolution = yt.streams.get_highest_resolution().resolution
	stream = yt.streams.filter(progressive=True, file_extension="mp4")
	mp4_path = stream.get_highest_resolution().download(f'{call.message.chat.id}', f'{call.message.chat.id}_{yt.title}')
	await send_mp3(bot, call.message.chat.id, mp4_path, yt)

if __name__ == '__main__':
	executor.start_polling(dp)