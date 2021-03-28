import discord
from discord.ext import commands
from sqlfunctions import *

class StudentCog(commands.Cog, name='Students'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def enrol(self, ctx):
        """
        To enrol yourself to this guild
        """
        sql_add_student(ctx.author.id, ctx.guild.id)

def setup(bot):
    bot.add_cog(StudentCog(bot))
