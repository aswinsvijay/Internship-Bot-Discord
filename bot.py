import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USER_ID = os.getenv('BOT_USER_ID')

prefix = f'<@!{BOT_USER_ID}> '
bot = commands.Bot(prefix)
extensions = ['commands_cog']
if __name__=='__main__':
    for extension in extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

bot.run(BOT_TOKEN)
