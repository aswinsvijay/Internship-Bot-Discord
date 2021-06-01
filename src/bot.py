import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from utils import sql, google
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

@tasks.loop(minutes=15)
async def delete_internships_loop():
    global lastdate
    today = datetime.datetime.now().date()

    if today != lastdate:
        internships = await sql.delete_internships(today)
        forms_list = [i[2] for i in internships]
        await google.close_forms(forms_list)
        internships_dict = dict()
        for i in internships:
            internships_dict.setdefault(i[0], []).append(i[1])

        for channel_id in internships_dict.keys():
            channel = bot.get_channel(channel_id)
            for message_id in internships_dict[channel_id]:
                message = await channel.fetch_message(message_id)
                await message.delete()
        lastdate = today

@bot.event
async def on_ready():
    await sql.database_connect()

    # lastdate is the last day when internships were purged from channels
    # lastdate is set as the day before, to ensure internships are purged when bot comes online
    global lastdate
    lastdate = datetime.datetime.now().date() - datetime.timedelta(days=1)
    delete_internships_loop.start()

    owner = (await bot.application_info()).owner
    bot.owner_id = owner.id
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
    if message.author.name == 'Zapier' or message.author.id == bot.owner_id:
        if message.channel.id == await sql.get_internship_channel(message.guild.id):
            message.content = message.content.split('\n')
            title = message.content[0]
            email = message.content[1]
            date = message.content[2]
            date = datetime.datetime.strptime(date, '%m/%d/%Y').date()

            form = await google.create_form(title, email)
            if len(form)==2:
                await sql.add_internship(
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
