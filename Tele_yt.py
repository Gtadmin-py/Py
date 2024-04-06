import os
import requests
import telebot
from pytube import YouTube, Playlist

# Initialize the Telegram bot
bot = telebot.TeleBot("6667741068:AAHCnUPRXcUbU6rkpzAZylUUm8FDlXyXGiw")

# Handler for /yt_down command
@bot.message_handler(commands=['yt_down'])
def handle_yt_down(message):
    try:
        # Get the YouTube link from the message
        url = message.text.split(' ')[1]
        yt = YouTube(url)
        
        # Get available streams for the video
        streams = yt.streams
        
        # Create a keyboard with download options
        keyboard = telebot.types.InlineKeyboardMarkup()
        for i, stream in enumerate(streams):
            keyboard.add(telebot.types.InlineKeyboardButton(text=stream.resolution, callback_data=f'download_{i}'))
        
        bot.send_message(message.chat.id, "Choose the quality:", reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Handler for /yt_down_multi command
@bot.message_handler(commands=['yt_down_multi'])
def handle_yt_down_multi(message):
    bot.reply_to(message, "Downloading playlists is not supported yet.")

# Handler for /yt_info command
@bot.message_handler(commands=['yt_info'])
def handle_yt_info(message):
    try:
        # Get the YouTube link from the message
        url = message.text.split(' ')[1]
        yt = YouTube(url)
        
        # Get video information
        title = yt.title
        views = yt.views
        author = yt.author
        
        info_text = f"Title: {title}\nViews: {views}\nAuthor: {author}"
        bot.reply_to(message, info_text)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

# Handler for callback queries
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        url = call.message.text.split(' ')[1]
        yt = YouTube(url)
        stream = yt.streams[int(call.data.split('_')[1])]
        
        # Download the video
        filename = f"{yt.title}.{stream.subtype}"
        stream.download(filename=filename)
        
        # Send the video as a document
        bot.send_document(call.message.chat.id, open(filename, 'rb'))
        
        # Delete the downloaded video file
        os.remove(filename)
        
        # Delete the original message with the options
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error: {e}")

# Start the bot
bot.polling()