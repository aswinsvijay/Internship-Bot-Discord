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
        await set_student_guild(ctx.author.id, ctx.guild.id)

    @commands.command()
    async def apply(self, ctx):
        """
        To get internships from enrolled guild in DM
        """
        internships = await get_internships(ctx.author.id)
        embed = discord.Embed(title='Available internships')
        async for i in internships:
            embed.add_field(name=i[0], value=i[1], inline=False)
        await ctx.author.send(embed=embed)

def setup(bot):
    bot.add_cog(StudentCog(bot))
