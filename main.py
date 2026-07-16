import discord
import os
import asyncio
from discord.ext import commands
from flask import Flask
from threading import Thread

# Flask 7/24 aktiflik
app = Flask('')
@app.route('/')
def home(): return "Bot aktif!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Flask'ı ayrı bir thread'de başlat
Thread(target=run_flask).start()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    # cogs klasöründeki tüm .py dosyalarını otomatik yükle
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"Yüklendi: {filename}")
            except Exception as e:
                print(f"Hata: {e}")

async def main():
    async with bot:
        await load_extensions()
        # Token değişkenini Railway Variables'dan alıyoruz
        token = os.environ.get('DISCORD_BOT_TOKEN')
        if token:
            await bot.start(token)
        else:
            print("HATA: DISCORD_BOT_TOKEN bulunamadı!")

if __name__ == '__main__':
    asyncio.run(main())