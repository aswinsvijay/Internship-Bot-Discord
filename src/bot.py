import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from sqlfunctions import *
from googlefunctions import *
import datetime

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')          # Bot access token
BOT_USER_ID = os.getenv('BOT_USER_ID')      # Bot user ID

# Prefixes that can be used for commands
allowed_prefixes = (f'<@!{BOT_USER_ID}>', f'<@{BOT_USER_ID}>')

# Setting up the bot
prefix = allowed_prefixes[0]+' '
bot = commands.Bot(
    prefix,
    help_command = commands.DefaultHelpCommand(
        no_category = 'Others'
    )
)

# Cogs for the bot
extensions = ['moderator_cog', 'student_cog']
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

    # Parse message and process command if message starts with an allowed prefix
    if message.content.startswith(allowed_prefixes):
        for allowed_prefix in allowed_prefixes:
            message.content = message.content.replace(allowed_prefix, prefix+' ')

        message.content = message.content.split()
        message.content = ' '.join(message.content)

        await bot.process_commands(message)
        return

    # If message sender is Zapier or bot owner(for testing), consider it as internship
    if message.author.name == 'Zapier' or message.author == owner:
        if message.channel.id == get_internship_channel(message.guild.id):
            message.content = message.content.split('\n')
            title = message.content[0]
            email = message.content[1]
            date = message.content[2]
            date = datetime.datetime.strptime(date, '%m/%d/%Y').date()

            form = await google_create_form(title, email)
            if len(form)==2:
                add_internship(
                    message.id, message.guild.id,
                    title, email, date,
                    form[0], form[1]
                )
                await message.add_reaction('✅')

bot.run(BOT_TOKEN)
