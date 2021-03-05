import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USER_ID = os.getenv('BOT_USER_ID')

prefixes = [f'<@!{BOT_USER_ID}> ' , f'<@{BOT_USER_ID}> ']
prefix = prefixes[0]
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

    if message.content.startswith(prefixes[0]) or message.content.startswith(prefixes[1]):
        message.content = message.content[len(prefixes[0]):] if message.content.startswith(prefixes[0]) else message.content[len(prefixes[1]):]
        message.content = message.content.split()
        message.content = ' '.join(message.content)
        message.content = prefix+message.content
        await bot.process_commands(message)
        return

bot.run(BOT_TOKEN)
