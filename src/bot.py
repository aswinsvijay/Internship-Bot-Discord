import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from sqlfunctions import *
from googlefunctions import *

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USER_ID = os.getenv('BOT_USER_ID')

allowed_prefixes = (f'<@!{BOT_USER_ID}>' , f'<@{BOT_USER_ID}>')
prefix = allowed_prefixes[0]+' '
bot = commands.Bot(prefix)

extensions = ['commands_cog']
if __name__=='__main__':
    for extension in extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready.')
    global owner
    owner = (await bot.application_info()).owner

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if message.content.startswith(allowed_prefixes):
        for allowed_prefix in allowed_prefixes:
            message.content = message.content.replace(allowed_prefix,prefix+' ')
        message.content = message.content.split()
        message.content = ' '.join(message.content)
        await bot.process_commands(message)
        return

    if message.author.name == 'Zapier' or message.author == owner:
        if message.channel.id == sql_get_channel(message.guild.id):
            form = await google_create_form(message.content.split('\n')[0])
            if len(form)==2:
                await message.add_reaction('✅')

bot.run(BOT_TOKEN)
