import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from sqlfunctions import *
from googlefunctions import *
import datetime

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')          # Bot access token

# Setting up the bot
bot = commands.Bot(
    commands.when_mentioned,
    strip_after_prefix = True,
    help_command = commands.DefaultHelpCommand(
        no_category = 'Others'
    )
)

@bot.event
async def on_ready():
    await database_connect()
    global owner
    owner = (await bot.application_info()).owner
    await owner.send(f'{bot.user.name} is ready.')

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    # If message starts with bot's command prefix, process commands and return
    if message.content.startswith(tuple(bot.command_prefix(bot, message))):
        await bot.process_commands(message)
        return

    # If message sender is Zapier or bot owner(for testing), consider it as internship
    if message.author.name == 'Zapier' or message.author == owner:
        if message.channel.id == await get_internship_channel(message.guild.id):
            message.content = message.content.split('\n')
            title = message.content[0]
            email = message.content[1]
            date = message.content[2]
            date = datetime.datetime.strptime(date, '%m/%d/%Y').date()

            form = await google_create_form(title, email)
            if len(form)==2:
                await add_internship(
                    message.id, message.guild.id,
                    title, email, date,
                    form[0], form[1]
                )
                await message.add_reaction('✅')

# Cogs for the bot
extensions = ['cogs.moderator_cog', 'cogs.student_cog']
for extension in extensions:
    bot.load_extension(extension)

bot.run(BOT_TOKEN)
