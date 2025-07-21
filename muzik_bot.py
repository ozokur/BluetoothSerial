import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
SPOTIFY_CLIENT_ID = '212199e14d6348529b5de438b3d7ff0f'
SPOTIFY_CLIENT_SECRET = 'bf4640ccac0f43b298908d902aa2c4b7'

# Telegram Bot Token
TELEGRAM_TOKEN = '8109405872:AAG4UdybauYBwgzb0ioJ_bvNe9-loIxK0cA'

# Set up Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Merhaba! Bana bir şarkı ismi yaz, Spotify linkini bulayım.')

async def find_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        song_name = track['name']
        artist = track['artists'][0]['name']
        url = track['external_urls']['spotify']
        reply = f"🎵 {song_name} - {artist}\n{url}"
    else:
        reply = 'Üzgünüm, bu şarkıyı Spotify’da bulamadım.'
    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_song))
    app.run_polling()